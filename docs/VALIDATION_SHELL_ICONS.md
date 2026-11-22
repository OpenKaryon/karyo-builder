# Actual Karyo taskbar icons and grouping

The actual Karyo shell now passes the joined Windows icon acceptance on Debian13
and Ubuntu26.04: one real resource tile for a two-window group, and matching
caption/taskbar icons for public PE32/64 launches. This is a QA/Builder checkpoint;
installed DE runtime code does not change relative to the accepted icon stage.
No push, distro/ISO, Forge, donor, user VM or Acer change was made.

## Exact shell artifacts

Both regular packages archive DE revision
9d7b77081c5598a4ef21a2fcff2ba80e887915b1, the HEAD selected at build time. The
following DE commit only changes QA/documentation. Native SDKs and all regular
package source revisions are captured, without fabricated latest-HEAD provenance.

| Native package | SHA256 | Bytes |
| --- | --- | --- |
| Debian | bfc2c4cb457af331e7d6feac5d26b36a044e1dff3deb0dc5d350e640af5ffdd9 | 559752 |
| Ubuntu | f2dbfa3174011be5f92a4551d0b6a8de1c67b313f10af5c394d5367a69b9e779 | 639310 |

Both builds complete all 72 CTest cases with zero failures. The existing native
compositor12Deb/9Ub, library4Deb/3Ub, Wine4 and accepted regular Win32 runtime
packages remain unchanged. Their recipe and artifact details are recorded in
VALIDATION_DESKTOP_ICONS.md.

## Joined acceptance

The public check-caption-buttons.py driver accepts --scenario shell-icons with
--shell-package <captured-regular-package-result>. It validates the shell artifact
and native distribution, installs coherent dependencies, verifies payload hashes
and captures all actor inputs. Regular package rows now explicitly include their
source Git revision and archive hash in addition to manifest/artifact hashes.

The installed shell starts before the user applications directory or any app
entry exists. No mocked taskbar widget replaces it. The test observes actual
wlr/ext identities and screenshots of the bottom layer-shell panel:

- Eleven phases pass on each native base, covering new registration, cache/icon
  replacement, missing/restored applications directory, native/late EXE classes,
  ordinary entries and a two-window group.
- The group has exactly one 28x28 resource tile: 784 exact resource pixels in a
  single bounded region, rather than duplicate buttons or a monogram fallback.
- Actual PE64 and PE32 launch through /usr/bin/karyo-win32 and Wine in that same
  desktop. Each has 784 taskbar resource pixels, the correct caption icon and
  both expected foreign IDs. The GDI client center must be RGB25/105/175 before
  its final screenshot is accepted. An early mapped caption alone is insufficient.
- The shared actor's non-panel mode independently passes all ten phases on both
  bases after the refactor, including those first-frame GDI assertions.
- Builder runs 50 unit cases successfully, including two native-only host skips.
- Representative two-window and actual PE screenshots were visually inspected.

Runtime preparation adds native Qt Wayland, LayerShellQt, PolkitQt, SVG plugins
and XDG utilities with captured versions. The first preparation correctly failed
package installation because the last two declared dependencies were missing;
that failed v1 is preserved. Final v2 installs all dependencies, passes apt-get
check and preserves the exact pre-existing Wine/libwine/compositor/Win32 versions
and payload checks. Nothing is force-configured or installed on the host.

Actors use UID1001, a private headless Wayland/XWayland display, private home and
session bus, network none, read-only root/source, dropped capabilities and
no-new-privileges. The icon actor does not claim virtual-pointer usage.

## Reproduction and evidence

Build examples/shell.json with Builder package and the native full SDK, then
prepare a disposable Wine/compositor runtime satisfying the shell DEB's native
APT dependencies. Invoke the existing artifact driver with the extra inputs:

    python tests/acceptance/check-caption-buttons.py --source ../karyo-de \
      --runtime-acceptance <captured-prepared-runtime> \
      --compositor-package <native-compositor-result> \
      --wlroots-package <native-library-result> \
      --win32-package <regular-win32-result> --scenario shell-icons \
      --shell-package <regular-shell-result> --output <new-output-directory>

Ignored out/migration records:

- desktop-icons-shell-<base>-v1: regular packages, manifests, archives, 72-test logs.
- shell-icons-runtime-preparation-v2/<base>: final dependency preparation;
  parent receipts retain the first preparation and its package-version snapshots.
- shell-icons-joined-<base>-v2: eleven-phase final receipts, shell logs and PNGs.
- shell-icons-shared-<base>-v2: final ten-phase non-panel regression receipts.
- shell-icons-joined-evidence.json: four validated receipts, package hashes,
  explicit source revisions, runtime preparations and actual installed images.
- shell-icons-builder-tests.log: final host CLI unit suite.

## Remaining boundaries

The container has no logind login session. Expected Polkit registration warnings
do not prove authentication-agent coverage; installed-session tests cover that
separately. This scenario establishes actual taskbar resource rendering/grouping,
not all interactions in a fully installed current-HEAD desktop. Physical GPU and
fractional scaling, real third-party Windows programs, legacy prefix import and
upgrade, Darling runtime, remaining enabled VMware host channels/DnD/HGFS/resize/
multioutput, VPN lifecycle and final installed DE integration remain in the
active goal. Work continues only in DE and Builder.
