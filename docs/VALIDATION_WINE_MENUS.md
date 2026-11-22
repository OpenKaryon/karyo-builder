# Generic standard-menu Wine engine migration

The reviewed prototype x11-popup-menu-type.patch at donor26bad17 is adapted
without application names, registry settings or imported prefixes. The system
PopupMenu class atom32768 is published as _NET_WM_WINDOW_TYPE_POPUP_MENU and
never requests input focus. Other window types keep their native behavior.
Wine-derived source retains LGPL-2.1-or-later; the independent launcher and own
QA actors remain GPL-3.0-or-later. Native copyright/control files are preserved.

## Native source and artifact identity

Both source builds apply the one reviewed patch with zero fuzz and retain all
native binaries, buildinfo/changes files, input/runner hashes and environment
inventories. Builder does not request nocheck, but Wine's own native packaging
configures --disable-tests. No upstream Wine unit-suite claim is made.

| Base | Native Wine package version | libwine amd64 SHA256 |
| --- | --- | --- |
| Debian13 | 10.0~repack-6+karyo1 | 4daf2ecdde0e3426c30872e1cc1da5feaaf64078e5ce3f1d003eee46dca33a5c |
| Ubuntu26.04 | 10.0~repack-12ubuntu1+karyo1 | 12c8cadd2ac9a078fe39e15ef63013845a6c274bc11a0c0575f91ddbb6547c80 |

Native source-package manifests remain in DE out/wine/{base}/menu-packages:
Debian karyo-source-package-20261122T075315Z-2e3a93ec, manifest SHA256
051a82dffb8bd577cae2d1c1199d2eaaf0e6c62c2996cb19d9eec4dc8f906181;
Ubuntu karyo-source-package-20261122T080035Z-a6ee4797, manifest SHA256
9a005f5d85a476dbdc1b4955cf4a92860e0e1ff8b9ab4c415a871de19dec8bad.
The own launcher package remains exact source e782fb0, not the later QA-only HEAD.
The compositor remains the previously accepted native labwc+karyo3 package.

## Actual baseline and installed acceptance

Baseline own PE64 menus on both systems are observed as DIALOG. Both keyboard
navigation and nine real pointer selections already work in this controlled
fixture. Ubuntu also passes the same baseline in PE32. This establishes incorrect
EWMH metadata, not reproduction of the older RomArtist hover/focus failure.

The positive installed-package driver freezes actor and fixture bytes before
execution, selects a verified native Wine runtime subset, checks every artifact
hash and installs it into a disposable image. Development/debug/tool packages
are retained as build evidence but excluded from the runtime image installation.
Every stage uses an ordinary account, fresh private HOME, private D-Bus and own
headless labwc/Xwayland, no network, read-only root and no capabilities. No
current desktop or personal prefix is forwarded. Windows code never runs as root.

Debian PE64 and Ubuntu PE64 plus PE32 all pass:

- Real GDI window/pixels and Unicode Windows file I/O and literal arguments.
- Removed Linux Qt environment, private D-Bus preservation and native Wine
  process UID/capability/NoNewPrivileges report with its actual process name.
- Extracted PE icon and stable identifier-only menu registration, registered
  relaunch, reused prefix and real exit42 retained in CLI/private metadata.
- Real per-user MSI installation, exact payload hash and inherited EXE prefix.
- Keyboard and persistent Wayland pointer menu navigation with only POPUP_MENU,
  inputfalse observations. Keyboard records seven selections; mouse records nine.
- Installed native Qt picker/error handling, second-account selection and native
  MIME user override checks, plus unchanged karyo-win32/labwc package integrity.

The pointer fixture keeps one private virtual device alive for the whole sequence.
It never connects to the user's compositor. The protocol XML is unmodified MIT
upstream source with pinned revision/hash and retained copyright. Actual positive
Ubuntu PE32 menu frames were visually inspected; typed and mouse receipts retain
exact bitness. Runtime container teardown removes its own temporary prefixes.

## Source preparation and retained corrections

Initial Ubuntu build-dep fails because current generator data exceeds Wine10's
native dependency bounds. Its source/QA image selects only unicode-data15.1.0-1,
unicode-idna16.0.0-1 and unicode-cldr-core46-0.1 from the signed official Ubuntu
snapshot20250417T000000Z. Every other package from that snapshot has negative
APT priority; native ABI libraries remain resolute. No control dependency is
relaxed and no runtime/host APT source is modified. The official snapshot service
is documented at https://snapshot.ubuntu.com/.

Earlier baseline fixture failures are retained: DockerFROM treated sha256:ID as
a repository, then transient wlrctl devices produced no observed menu. Neither
is accepted as a Wine failure. The corrected actor uses a verified local image
tag and persistent own input, requires actual observed DIALOG baseline windows,
and preserves source bytes before image construction. Valid v4 and later native
receipts replace those weak observations; no assertion is weakened for a pass.

Local wine-debian-patched-acceptance-v1 and wine-ubuntu-patched-acceptance-v1
contain the final package/actor/build input hashes, per-stage logs, receipts and
frames. wine-menu-baseline-evidence.json and the original baseline directories
remain separate. No binary, prefix or personal credential is committed.

## Remaining integration boundaries

Debian's matching native Wine32 source build is separate and still needs version,
common-file and coinstallation checks plus real PE32 acceptance. Ubuntu's native
WoW64 already provides tested32-bit Windows support without i386 system packages.
Do not transfer that result to Debian's legacy Wine64 stack.

Existing-user deployment, actual Wine hidden-owner palettes/minimize, Windows-like
caption/child rounding and close-button styling, complete taskbar association,
legacy prefix import and Darling remain separate gates. The modeled compositor
palette checks keep their previous identity; these menu/engine tests are not
silently relabeled as those application cases. Full migration remains active.
The owner VM, ordinary QA desktop sessions, Acer, Forge and donor were untouched;
no push/fetch or ISO rebuild was performed.


The later matching Debian Wine32 build, shared-file comparison and actual
PE32/PE64 coinstallation gate are now accepted separately; see
VALIDATION_WINE_COINSTALLATION.md. The earlier single-architecture and Ubuntu
receipts above retain their exact historical scope.
