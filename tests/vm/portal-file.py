#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Request a real session FileChooser; select a file manually to finish."""
import argparse
import json
from pathlib import Path
from gi.repository import Gio, GLib

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
loop = GLib.MainLoop()
result = None

def response(bus, sender, path, interface, name, parameters, userdata):
    global result
    code, data = parameters.unpack()
    result = {"response": code, "uris": data.get("uris", [])}
    loop.quit()

subscription = bus.signal_subscribe(
    "org.freedesktop.portal.Desktop", "org.freedesktop.portal.Request",
    "Response", None, None, Gio.DBusSignalFlags.NONE, response, None)
bus.call_sync(
    "org.freedesktop.portal.Desktop", "/org/freedesktop/portal/desktop",
    "org.freedesktop.portal.FileChooser", "OpenFile",
    GLib.Variant("(ssa{sv})", ("", "Karyo portal file acceptance", {
        "handle_token": GLib.Variant("s", "qa_file"),
        "modal": GLib.Variant("b", True)})),
    GLib.VariantType("(o)"), Gio.DBusCallFlags.NONE, 10000, None)
GLib.timeout_add_seconds(90, lambda: (loop.quit(), False)[1])
loop.run()
bus.signal_unsubscribe(subscription)
if result is None:
    raise SystemExit("Timed out waiting for the portal response")
args.output.write_text(json.dumps(result, indent=2) + "\n")
raise SystemExit(0 if result["response"] == 0 else 1)
