#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Capture one real portal/PipeWire frame in a disposable graphical VM."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid
import gi
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gio, GLib, GdkPixbuf

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
# Never leave an earlier PASS report behind when this attempt is cancelled.
for name in ("screen-cast.json", "pipewire-frame.png", "gstreamer.log"):
    (args.output / name).unlink(missing_ok=True)
bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
service = "org.freedesktop.portal.Desktop"
path = "/org/freedesktop/portal/desktop"
interface = "org.freedesktop.portal.ScreenCast"

def request(method, signature, values, options):
    options = dict(options, handle_token=GLib.Variant("s", "qa_" + uuid.uuid4().hex))
    loop = GLib.MainLoop()
    response = None
    expected = None
    def receive(connection, sender, object_path, iface, signal, parameters, userdata):
        nonlocal response
        if object_path == expected:
            response = parameters.unpack()
            loop.quit()
    subscription = bus.signal_subscribe(service, "org.freedesktop.portal.Request", "Response",
        None, None, Gio.DBusSignalFlags.NONE, receive, None)
    try:
        result = bus.call_sync(service, path, interface, method,
            GLib.Variant(signature, (*values, options)), GLib.VariantType("(o)"),
            Gio.DBusCallFlags.NONE, 10000, None)
        expected = result.unpack()[0]
        timer = GLib.timeout_add_seconds(60, lambda: (loop.quit(), False)[1])
        loop.run()
        if response is not None:
            GLib.source_remove(timer)
        if response is None or response[0] != 0:
            raise RuntimeError(f"{method} did not succeed: {response}")
        return response[1]
    finally:
        bus.signal_unsubscribe(subscription)

session = None
remote = None
try:
    created = request("CreateSession", "(a{sv})", (),
        {"session_handle_token": GLib.Variant("s", "qa_" + uuid.uuid4().hex)})
    session = created["session_handle"]
    request("SelectSources", "(oa{sv})", (session,),
        {"types": GLib.Variant("u", 1), "multiple": GLib.Variant("b", False)})
    started = request("Start", "(osa{sv})", (session, ""), {})
    streams = started["streams"]
    if not streams:
        raise RuntimeError("No real capture stream returned")
    node, properties = streams[0]
    reply, descriptors = bus.call_with_unix_fd_list_sync(service, path, interface,
        "OpenPipeWireRemote", GLib.Variant("(oa{sv})", (session, {})),
        GLib.VariantType("(h)"), Gio.DBusCallFlags.NONE, 10000, None, None)
    remote = descriptors.get(reply.unpack()[0])
    frame = args.output / "pipewire-frame.png"
    with (args.output / "gstreamer.log").open("wb") as log:
        subprocess.run(["gst-launch-1.0", "-q", "pipewiresrc", f"fd={remote}",
            f"path={node}", "num-buffers=1", "!", "videoconvert", "!", "pngenc",
            "!", "filesink", f"location={frame}"], pass_fds=(remote,),
            stdout=log, stderr=subprocess.STDOUT, timeout=20, check=True)
    image = GdkPixbuf.Pixbuf.new_from_file(str(frame))
    width, height = image.get_width(), image.get_height()
    pixels, stride, channels = image.get_pixels(), image.get_rowstride(), image.get_n_channels()
    colors = {pixels[y*stride+x*channels:y*stride+x*channels+3]
              for y in range(0,height,23) for x in range(0,width,19)}
    if width <= 0 or height <= 0 or len(colors) < 16:
        raise RuntimeError("Captured frame is empty or blank")
    report = {"width":width,"height":height,"sampled_colors":len(colors),
              "portal_node":node,"source_type":properties.get("source_type"),
              "reported_size":properties.get("size")}
    (args.output / "screen-cast.json").write_text(json.dumps(report,indent=2)+"\n")
    print("PASS real portal/PipeWire capture:", json.dumps(report))
finally:
    failed = sys.exc_info()[0] is not None
    if remote is not None:
        os.close(remote)
    if session is not None:
        try:
            bus.call_sync(service, session, "org.freedesktop.portal.Session", "Close",
                None, None, Gio.DBusCallFlags.NONE, 10000, None)
        except GLib.Error:
            if not failed:
                raise
