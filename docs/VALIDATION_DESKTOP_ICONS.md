# Registered Windows icons on Debian and Ubuntu

The standalone compositor now sees freshly registered PE icons and exposes the
matching desktop ID to both taskbar protocols. Changes are limited to DE and
Builder. No push, distro/ISO, Forge, donor, user VM or Acer changes were made.

| Artifact | Version | SHA256 |
| --- | --- | --- |
| Debian labwc | 0.8.3-1+karyo12 | c80047bc5d3b5f550df3122bf817ee08c5d615981b8404631fa95d7be1b3ac55 |
| Ubuntu labwc | 0.9.3-1+karyo9 | ebfccf0db95c09c730cefd5dc9fad09e3e3eb882dca77159da7f6ff27c1ae7da |

DE implementation: 9d7b77081c5598a4ef21a2fcff2ba80e887915b1. Both existing native wlroots libraries,
Wine4 and Win32 runtime/resource payloads remain unchanged. Compositor builds
use the captured matching native SDKs; they do not import Debian libraries into
Ubuntu or install build dependencies on Windows.

## Behavior

The launcher atomically creates a user desktop entry before starting Wine.
libsfdo used to cache entries at compositor startup, so the first launched
program could still receive the fallback caption icon. Windows icon and foreign
identity lookups now refresh changed application directories, including a
previously absent, removed or restored directory. Device, inode and nanosecond
mtime/ctime distinguish replacements. Transient stat/load errors retain the old
database and Ubuntu retains its selected locale. No global polling was added.

Only XWayland .exe identities matched to karyo-win32- desktop entries are
remapped in wlr-foreign-toplevel and ext-foreign-toplevel-list. Raw view classes
stay intact for Windows theme/ownership/grouping policy. Linux classes and
ordinary desktop identities retain native behavior. No program whitelist,
private prefix or program-specific configuration is involved.

## Completed checks

- Native source packages pass upstream suites: Debian 2/2 and Ubuntu 3/3.
  Recipes, ordered patch hashes, actual donor Git blobs and packaged artifacts
  were checked. Native library/Wine/runtime packages were reused unchanged.
- The public --scenario desktop-icons driver freezes the actor, shared harness,
  dual-protocol C observer and wlr XML; validates artifact hashes/distribution;
  installs coherent native runtime/dev pairs when needed; and checks dependencies.
- Ten phases pass on each native base. A real PE resource is extracted by the
  installed registration API, and caption pixels plus both real foreign protocols
  cover initial lookup miss, first registration, atomic icon-path replacement,
  applications-directory removal/restoration, native and late EXE class changes,
  and an ordinary desktop entry outside the public launcher namespace.
- Actual PE64 and PE32 programs then launch through /usr/bin/karyo-win32 and
  native Wine. Their registered ID reaches both protocols and their orange
  resource is visible in the native caption. Each launcher completes successfully.
- Previous compositor packages are exercised separately with --baseline on both
  bases. They retain executable-only foreign IDs. baseline.json is a negative
  control and does not replace positive acceptance.
- New packages also pass the actual caption pointer/glyph/narrow-window actions
  and all 23 rounded-frame pixel/input phases on each native base.
- Builder unit tests: 50 run successfully, including two native-only skips on Windows.

GUI execution uses UID1001, private homes/display/D-Bus, no network, read-only
root/source, dropped capabilities and no-new-privileges. The icon actor explicitly
reports private_pointer=false; caption/rounding actors really use the private
pointer. The baseline does not claim a Wine application run.

## Reproduction and evidence

Build current DE compositor recipes with source-package and the prepared native
SDKs described in DE integrations/compositor/README.md. Then invoke:

    python tests/acceptance/check-caption-buttons.py --source ../karyo-de \
      --runtime-acceptance <accepted-native-Wine-runtime-directory> \
      --compositor-package <native-compositor-result> \
      --wlroots-package <matching-native-library-result> \
      --win32-package <accepted-regular-win32-package-result> \
      --scenario desktop-icons --output <new-output-directory>

Ignored out/migration evidence:

- desktop-icons-<base>-v2: final positive ten-phase receipts and PNGs.
- desktop-icons-before-<base>-v2: previous-package controls.
- desktop-icons-rounded-frames-<base>-v1 and
  desktop-icons-caption-buttons-<base>-v1: regressions on new packages.
- desktop-icons-native-evidence.json: native artifacts, DE revision, receipt
  hashes and actual installed image identities.
- desktop-icons-builder-tests.log: host CLI suite.

## Remaining work

Both compositor lookup and the IDs supplied to taskbars are established here.
The actual Karyo shell rendering/grouping needs a separate joined check; these
protocol observations are not presented as that check. Third-party Windows
programs, physical GPU/fractional DPI, legacy-prefix import/conversion and upgrade,
Darling runtime, remaining enabled VMware host channels/DnD/HGFS/resize/multioutput,
VPN lifecycle and the final current-HEAD installed DE remain in the active goal.
