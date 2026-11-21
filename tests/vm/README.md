# Disposable Debian and Ubuntu VM checks

These fixtures are for a new disposable Debian 13 VM, never a working machine.
They do not operate VMware on the host or contain login credentials. The recorded
run and remaining limits are in ../../docs/VALIDATION_DEBIAN_VM.md.

Start from the official Debian generic amd64 cloud image; verify its published
checksum before converting a sparse overlay to the hypervisor disk format.
Create a cloud-init seed with an SSH admin and a separate password-protected
sudo user for graphical checks. Supply freshly generated fixture credentials
locally, not through Git. Give the guest 4 GiB RAM and two vCPUs.

Run bootstrap.sh as root only in that disposable guest. It installs Xfce,
LightDM and the UI test clients, saves baseline files and restarts LightDM.
Log into Xfce through the greeter before installing Karyo runtime DEBs. Save the
PID of xfce4-session and hashes of the host identity, DM and Xfce session entry.
Install the bundle with apt-get --no-install-recommends and verify those values.
Log out, select Karyo in the greeter and perform an actual password login.

Do not use a host desktop controller. Use the VM console or isolated guest
input. vmrun captureScreen and SSH work without taking the host's focus. If
VNC is needed, require authentication and bind it to 127.0.0.1 only. Keep the
VM image/seed/key/profile under an ignored output directory.

## Applications, tray, authorization and portals

Build the Qt-only tray client in a native build environment:

```sh
cmake -S tests/vm -B /tmp/karyo-qa-tray
cmake --build /tmp/karyo-qa-tray
```

Run qa-tray-fixture in the graphical session. It starts hidden with a green
status-notifier icon. Check left-click activation and right-click menu actions;
~/qa-results/tray.log records actual callback invocations. Quit via its menu.
For polkit, create a disposable root-owned script and a .desktop entry using
pkexec --disable-internal-agent to invoke it. Launch through Start, authenticate,
and verify its root-only output and polkitd's agent log. Launching from SSH is
not equivalent to launching from the active graphical logind session.

Run the file portal client in that same session (python3-gi is required):

```sh
python3 tests/vm/portal-file.py --output /tmp/karyo-file-result.json
```

Select a known sample file. Assert Response=0 and the exact URI in the JSON.
The process remains on D-Bus until the response, unlike a one-shot gdbus caller.

Serve screencast.html from a local HTTP server inside the guest. In guest
Chromium, click Share this desktop, select Entire Screen and confirm Share.
The page records real stream settings, dimensions and sampled pixel diversity in
window.qaResult and a PNG in window.qaFrame. Inspect the preview/frame and stop
the tracks after the test. Do not enable fake display media: checking only the
portal interface version does not establish working screen sharing.

## Lock, sleep and package lifecycle

Use loginctl lock-session on the graphical session. Check LockedHint and the
managed lock process after a wrong password and after the correct password.
For systemctl suspend, retain an isolated hardware wake path. Confirm kernel
suspend entry/exit, a locked session after wake, and unchanged application PIDs.
A headless lock test or a host VM checkpoint alone is not this acceptance test.

make-upgrade-fixtures.py repacks a complete set of runtime DEBs with a higher
fixture version, matching exact Karyo dependencies and a changed shipped lock
PAM comment. It leaves executable payloads unchanged and writes a hash manifest:

```sh
python3 tests/acceptance/make-upgrade-fixtures.py /tmp/runtime-debs /tmp/upgrades
```

This is test data, not release packaging. If substituting a real rebuilt package,
record its actual source/hash separately and update the local fixture manifest.
Modify the installed lock PAM file, then install the fixture set with
-o Dpkg::Options::=--force-confold. Verify the local file, .dpkg-dist and live
application PIDs. Return to Xfce before removing the Karyo packages; verify its
PID survives, the Karyo session/portal selection disappears, and another real
LightDM login still reaches Xfce. Purge the lock to verify only owned conffiles
are removed. Retain logs/screenshots locally and shut down only this test VM.

## Native ScreenCast and PipeWire check

When a browser is unavailable, portal-screencast.py exercises the real
ScreenCast request lifecycle, waits for the normal monitor chooser and passes
the OpenPipeWireRemote file descriptor into GStreamer's pipewiresrc. It decodes
one actual PNG frame and records dimensions/pixel diversity; it uses no fake
source and does not bypass user selection.

Install python3-gi, gir1.2-gdkpixbuf-2.0, gstreamer1.0-tools,
gstreamer1.0-pipewire and gstreamer1.0-plugins-good in the disposable guest.
The session bundle needs slurp for the wlr output chooser. Run inside Karyo:

```sh
python3 tests/vm/portal-screencast.py --output ~/qa-results/cast
```

Click the monitor and change something on screen while capture starts (for
example, run a terminal counter). Debian's older wlr backend may wait for
damage before producing its first frame. Inspect pipewire-frame.png and retain screen-cast.json plus
gstreamer.log. Repeat with Escape at the chooser: the command must fail and
leave no PNG or PASS JSON from an earlier attempt. The D-Bus session remains
alive until capture finishes and is then closed, including error paths.

Protocol references: [ScreenCast](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.ScreenCast.html)
and [Gio Unix FD calls](https://docs.gtk.org/gio/method.DBusConnection.call_with_unix_fd_list_sync.html).
