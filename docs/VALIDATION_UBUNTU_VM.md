# Ubuntu VM session and application acceptance

Observed on 2026-11-21 UTC in a new disposable VMware VM. The workstation VM,
Acer and Forge were not modified. The session lifecycle checks below passed. Later migrated components remain to
be checked; this document does not mark the full DE migration complete.

## Verified base and isolation

Official image: https://cloud-images.ubuntu.com/resolute/current/resolute-server-cloudimg-amd64.img

The downloaded 861563904-byte image matched the official SHA256SUMS entry:

```text
7b90593f5532b49b7e3fe3d2743f0d1f0d822e5b07cebcd8e00c0df8069ecab9
```

The guest identifies as Ubuntu 26.04.1 LTS (resolute), kernel 7.0.0-43-generic,
with native Qt 6.10.2. Configuration: UEFI, two vCPUs, 4096 MiB RAM, 24 GiB
sparse disk, NAT e1000e, SVGA with 3D disabled and pixman. Separate disposable
SSH-admin and password-protected GUI/sudo accounts were generated locally.
Keys, credentials, media and VM disks remain in ignored QA output.

A real LightDM password login reached Xfce before Karyo installation. Saved
hashes cover os-release, the default display manager and the Xfce desktop entry.
Xfce PID 9193 survived initial APT installation and all three hashes matched.
No private browser, VPN, account or workstation profile was imported.

## Observed graphical behavior

| Scenario | Result |
| --- | --- |
| Session selection | Actual LightDM picker selected Karyo; password login started active seat0 Desktop=karyo, Type=wayland. After package upgrade, another real login started the same desktop/type successfully. |
| Lock/PAM | Real session lock set LockedHint=yes; a wrong password retained the lock, and the correct fixture password removed it. |
| Suspend/resume | Karyo's delay inhibitor was present. Kernel s2idle entry/exit at 00:25:52/00:25:57 UTC; virtual Shift woke the guest. LockedHint remained yes and shell/Photos PIDs survived; correct password unlocked normally. |
| Authorization | A Start-launched pkexec fixture displayed Karyo's dialog and produced a root-only uid=0 result. polkitd recorded authorization through the active agent. |
| Status notifier | Native Qt fixture registered in the overflow. Real left click recorded activated-3; right click displayed its menu and Open recorded menu-open. |
| FileChooser | A persistent Gio caller received Response=0 and the exact local sample.txt URI after the actual GTK chooser selection. |
| ScreenCast/PipeWire | Native Gio CreateSession/SelectSources/Start/OpenPipeWireRemote used the normal slurp chooser. GStreamer decoded an actual 1280x800 PNG with 35 sampled colors. Frame was saved and visually inspected; session closed successfully. |
| Capture cancellation | Escape returned SelectSources Response=1, the caller failed, and its old PNG/PASS JSON were absent. No chooser bypass or fake frame was used. |
| Terminal | Native QTermWidget data dependency resolved on Ubuntu. An unprivileged PTY command wrote its expected result in the GUI user's home. |
| Photos | Installed viewer rendered a synthetic gradient. Ctrl+C advertised image/png and text/uri-list; clipboard PNG decoded to the original 320x240 dimensions. |
| Editor | Installed editor visibly rendered the exact public sample text. Recovery/encoding and real second-process routing are additionally tested natively on both bases. |
| PDF Reader | Installed reader rendered an independently generated PDF, including its thumbnail and text. |
| Player | Installed player recognized the generated PCM WAV and its 2-second duration. VM currently has no audio device, so audible playback is not accepted. Native QAudioBufferOutput tests separately receive actual decoded PCM buffers on both bases. |
| Package ownership | Fresh native shell/lock packages own their hidden desktop descriptors; dpkg-query -S confirms both. GIO resolves their executable/NoDisplay identity. |
| Upgrade/conffiles | Eleven acceptance-only packages upgraded to 0.1.0-2 while shell/editor/reader PIDs survived. Local PAM hash stayed identical and the changed default became .dpkg-dist. All three host-file hashes still matched. |
| Removal/purge | After returning through LightDM to Xfce, removal of the eleven Karyo packages left the Xfce PID alive and removed the Karyo session/portal choice. Local PAM survived removal. Explicit lock purge then removed its owned PAM file; all three host-file hashes still matched. A further LightDM password login reached Xfce successfully. |

## Defects and fixture corrections

Qt 6.10 portal registration requires installed desktop identity for shell and
lock. Hidden NoDisplay descriptors now belong to their runtime components.
The original f8d8e8c Ubuntu packages predated that fix; descriptors were first
checked manually, then verified as owned files after the native 9f1d1d7 rebuild.

The wlr portal had no installed output chooser and returned cancellation.
The session recipe now depends on slurp. The successful capture exercises that
real chooser. A matching Debian native capture also passed at 1280x800/29 sampled
colors; Debian's older wlr needed screen damage from an updating terminal before
producing the first frame. A static-screen attempt timed out and was retained
as a failed fixture attempt, not counted as successful capture.

The first Terminal fixture inherited the SSH admin's inaccessible working
directory. Correcting the QA launcher to the GUI user's home resolved the PTY
failure; the actual application launcher already uses a suitable directory.
The Ubuntu data package is qtermwidget6-data, not Debian's qtermwidget-data;
the public recipe declares the correct alternative names.

Chromium's Ubuntu Snap transport stalled without downloading data. Its change
was aborted, the real APT process was allowed to finish, and dpkg configuration
was recovered without deleting locks. Ubuntu screen capture here uses the native
Gio/GStreamer client, not an untested Chromium claim. Debian's separate report
retains an actual Chromium getDisplayMedia acceptance.

## Source and artifact record

Initial seven runtime/application packages came from DE f8d8e8c; corrected
Terminal from 9b649f8. Later shell, lock, session, editor, reader and player
were independently rebuilt by Builder from exact DE commit
9f1d1d7472e47e7619a9c6096eef1c43cbecda94.
The native Debian editor/reader/player package builds use that same source.
Each package directory retains manifest.json, environment packages, image ID,
recipe, source archive hash, build/CTest logs and artifact SHA256. The upgrade
fixture input record maps all eleven original native artifacts to their exact
source/hashes; make-upgrade-fixtures changes only metadata/PAM comment.

Local evidence is under ignored out/ubuntu-vm-qa/results (screenshots and copied
GUI/system logs); no test credentials or captured private data belong in Git.
Full current native tests pass on Debian 13 and Ubuntu 26.04. Later Monitor/Snip
source commits have separate regressions and are not claimed installed by this
older package set. Physical camera/audio, video decoding/overlay integration,
protected-PDF interaction and newer app package checks remain explicit gates.
