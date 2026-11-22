# Installed optional Windows launcher acceptance

The standalone ordinary-user launcher is source e8c9506, with native Qt dialog
identity/home correction e782fb0. It adapts donor26bad17 without fixed desktop
slots, per-RomArtist settings, a Wine fork or imported private prefixes. The
optional Builder recipe examples/win32.json packages only this component and
uses the selected native Wine/PyQt6 dependencies. It is not an ISO rebuild.

## Native artifacts and execution

Both final packages use exact DE e782fb0ebb5c515a16fc402d70e5e6fec17c9a32.
The independently built labwc+karyo3 packages retain their previous revision.

| Base | Native Wine | karyo-win32 DEB SHA256 |
| --- | --- | --- |
| Debian13 | 10.0~repack-6 | c3efcf73da55c92210f7dd04c7f4942057922369274d67579b4d24c076d2a02f |
| Ubuntu26.04 | 10.0~repack-12ubuntu1 | ace1561d4699c769044018ed3f62d4f66035dae47e08875967c472a871667416 |

Both native package manifests report successful CTest/dpkg-deb validation.
The complete DE build passed72/72 CTest groups on both bases after the launcher
and desktop-catalog changes. The final Qt correction separately passed all16
policy cases and real source/installed Qt dialogs on both bases. The full C++
suite was not repeated for this Python-only GUI correction.

The reproducible host actor tests/acceptance/check-win32-runtime.py installs
hash-verified DEBs, compiles our own PE64 and MSI, and checks package integrity.
Product packages create no QA users. Only disposable images add UID1001/1002;
all actual GUI/engine calls run as ordinary users, with capabilities dropped,
NoNewPrivileges, read-only root/source, fresh tmpfs homes, private D-Bus and no
network. No current desktop, display, personal prefix or host bus is forwarded.

On each base the installed acceptance passes:

- Real native Qt file picker cancellation and error dialog, installed desktop
  identity, non-null fallback icon and no Windows storage creation.
- Real UID1002 selection with forged HOME/legacy slot ignored, no prefix writes,
  native GIO Karyo MIME default and explicit user MIME override precedence.
- Real Wine64 PE window and GDI pixels under private labwc/Xwayland, with the
  recorded Unicode executable WM_CLASS and literal non-shell arguments.
- UTF-8/Unicode Windows file I/O, removed Linux Qt environment, unchanged private
  D-Bus address and native kernel UID/capability/NoNewPrivileges report.
- PE icon extraction, stable identifier-only desktop Exec, registered relaunch,
  reused prefix and retained real exit42 in CLI plus private launch metadata.
- Real per-user MSI installation, installed payload hash and automatic inherited
  prefix when launching its EXE. Independent application profiles stay distinct.
- Private0600 logs/records and unchanged installed karyo-win32/labwc package files.

The kernel report is read through Wine's Z: mapping to /proc/self/status and
identifies wineserver64 on Debian/wineserver on Ubuntu. It is explicitly a
native Wine process report, not an assertion that this is the PE client's PID.
Second-account acceptance checks identity selection/MIME, not a simultaneous
second Wine session. Recorded frames were visually inspected on both bases.

## Retained corrections and evidence

Initial e8c9506 runtime engine runs passed on both bases. Real Qt inspection
then reproduced the missing desktopFileName; e782fb0 fixes it and also avoids
trusting HOME for the picker's initial directory. The same Qt assertions and
real engine suite pass against the new installed package on both bases.

The first QA PE compile failed because -municode already defines UNICODE;
ifndef guards correct the fixture while preserving compiler -Werror. The
failed image logs and initial successful engine evidence are retained. Native
D-Bus wrappers print nonfatal unknown-child notices for Wine descendants; all
acceptance drivers and actual engine invocations finish successfully.

Local out/migration/win32-runtime-evidence.json joins final package, actor,
compositor/image and individual evidence hashes. Native package manifests are
under win32-{base}-package-v2; win32-{base}-acceptance-v2 contains installed Qt,
account and engine receipts, logs and frames. Initial package/runtime and failed
image logs remain under their original paths. No binary or Wine prefix is
committed. The driver leaves its uniquely named synthetic QA images available
for inspection; they contain no initialized Wine prefix or credential.

## Open product gates

This closes ordinary-user64-bit EXE/MSI launch, registration, native MIME and
frontend acceptance in the tested containers. It does not close32-bit engine
preparation, explicit legacy prefix import, an installed existing-user VM
upgrade, actual application popup-menu/focus loops, Windows-like caption and
child-window rounding/buttons, full taskbar association or Wine engine patches.
Darling, VMware enabled host payload/DnD/HGFS and remaining VPN lifecycle work
retain separate gates. See VALIDATION_WIN32_OWNED_WINDOWS.md for prior modeled
palette/minimize compositor evidence; that is not relabeled as an actual Wine
owned-palette test. Full migration remains active and no push/fetch was used.
