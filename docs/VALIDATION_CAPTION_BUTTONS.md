# Native Windows caption controls

The Debian 13 and Ubuntu 26.04 native compositor packages now use independent
Windows SVG controls and consistent per-button geometry. DE sourcee70b630 is
packaged through the regular Win32 component; no distro, Forge, user VM, Acer or
upstream repository changed. This is local acceptance, without push or ISO build.

| Artifact | Version | SHA256 |
| --- | --- | --- |
| Debian labwc | 0.8.3-1+karyo9 | b0d4fba3d1dd410c321139466149a8b429f71e42e6d26c01824e25296da30848 |
| Ubuntu labwc | 0.9.3-1+karyo7 | 1ce8feec834545d4cd3d1f93804dbf00e304844743e91a8f41681f9464fe8b53 |
| Debian karyo-win32 | 0.1.0-1 | 6b58e7903c7321a59c9708dd8f550534127f0510a59e7a1fa22656d09e6bc27c |
| Ubuntu karyo-win32 | 0.1.0-1 | 629682d1cdd60b0a88f2c2c401eb6383087d34e4981f21bd64ff0b22f6c47a4a |

## Result

Controls measure 46 logical pixels; the app-icon button measures 24. Initial and
resized layout, title offsets, hidden-button fitting, rendered image dimensions
and actual input rectangles use the same widths. Narrow windows preserve the
native hide priority. Native Linux configurable dimensions remain unchanged.

Five original GPL-3 SVGs install into share/themes/Karyo-Windows/labwc through
the regular win32-runtime component. They include thin control glyphs, overlapping
restore squares and a filled red/white close hover. The derivative compositor
patches retain upstream GPL-2.0-only separately. No Windows binary artwork or
per-program compatibility configuration is included.

## Verified scope

- Both native source builds pass upstream Meson tests: Debian2/2 and Ubuntu3/3.
  Original recipes, every patch digest and final Git content agree with inputs.
- Both regular karyo-win32 package builds capture DE e70b630, pass CTest and
  install the expected resources. The public driver checks native metadata,
  artifact sizes/SHA256 and every installed SVG against the frozen source.
- A real X11 client and persistent private Wayland pointer verify hover ink,
  clicks at the new left edges of maximize/restore/minimize, activation after
  iconify, WM_DELETE_WINDOW delivery and widths162/161/116/104/440. The white
  diagonal stroke is antialiased over red; only its central ink is measured,
  away from the software cursor. The blue caption background cannot pass as ink.
- The same frozen actor has a distinct --baseline mode: old native labwc8/6,
  even with the new resource package, must lack the new red close hitbox. Both
  controls pass; they are not substituted for positive interaction acceptance.
- Mixed native/Wine theme pixels, late class reversal and reload pass, followed
  by all ten X11 ownership layouts per base. Normal/startup-lock protocols pass
  separately: six jobs total across both bases.
- Eight real Wine4 palette runs pass: PE32/64, two iterations per base, unmapped
  owners, late tools, focus return, foreign overlap and group hide/restore.
- Each final palette frame still contains four actual red/white Wine child
  close buttons with the previously accepted exact11x11/108red/13white pixels.
  This is checked independently of the compositor hover glyph.
- Eight real menu runs pass: PE32/64 x mouse/keyboard x both bases. Repeated
  menu navigation and POPUP_MENU/no-input protocol are retained.
- Builder unit tests:50 pass,2 native-only skips on Windows. The first host
  invocation lacked PYTHONPATH; the corrected src import path passes.

All runtime displays, buses and homes are disposable. Runtime containers use
ordinary UID1001, network=none, read-only root/source, dropped capabilities and
no-new-privileges. Package installation runs only in disposable image builds.
Representative maximize/restore, close-hover and narrow PNGs were inspected.
This is scale1 headless/Pixman coverage, not physical GPU or fractional DPI proof.

## Native SDK correction

Earlier palette QA updated runtime wlroots while an existing distribution dev
package retained its exact dependency on the stock library. Runtime installation
worked, but apt-get check exposed that SDK inconsistency. The shared installer
now captures a matching optional dev artifact, installs it only if headers are
already present, then requires apt-get check. It does not add an SDK to runtime
systems. Both installed-SDK and absent-SDK branches pass on both native bases;
headerless controls remain headerless after reinstallation. Production library
source and its already accepted API are unchanged.

## Public reproduction

Build the compositor using DE integrations/compositor recipes, then build
examples/win32.json using the matching native SDK. Run
 tests/acceptance/check-caption-buttons.py with --source, --runtime-acceptance,
--compositor-package, --wlroots-package, --win32-package and --output. The runtime
receipt must identify an already accepted native Wine QA image. --baseline is a
separate previous-compositor observation; its result is baseline.json.

The driver freezes the actor, validates/copies native artifacts, uses the shared
native install verifier and compares installed SVG hashes before unprivileged
GUI testing. Its captured image can feed check-win32-palettes.py. The latter
now preserves an existing SDK coherently and rejects broken dependency state.

Ignored Builder out/migration receipts:

- caption-buttons-packaged-<base>-v1: final public driver/package interactions.
- caption-buttons-before-<base>-v1: old-package baseline controls.
- caption-buttons-native-regression-v1: all model/theme/protocol cases.
- caption-buttons-palettes-<base>-v1: real PE32/64 palette matrix.
- caption-buttons-menus-v1: eight actual mouse/key menu cases.
- caption-buttons-child-glyphs-v1.json and caption-buttons-devless-v2.json:
  independent real child rendering and SDK-absence checks.
- caption-buttons-native-evidence.json: joined recipes, source revision, hashes,
  images and final acceptance receipts. Native source outputs are DE
  out/compositor/<base>/caption-buttons-packages; regular component outputs are
  caption-buttons-win32-<base>-v1.

Preliminary caption-buttons-stage-v1 caught the SDK mismatch. Stage-v2 passed
installation but its pixel oracle assumed exact neutral-white diagonal pixels
and ignored the software cursor; stage-v3 accounts for actual antialiasing/cursor
while still requiring the red fill and white central glyph. Initial diagnostic
script/string-generation errors happened before their checks ran; logs remain.
Only QA changed for these retries, without repeated compositor/library builds.

Top/bottom and owned-client corner masks, registered application icons, further
real applications, legacy import/upgrade, Darling, VMware channels, VPN lifecycle
and a joined current-HEAD desktop remain in the full goal. Caption controls do
not close those separate migration gates.
