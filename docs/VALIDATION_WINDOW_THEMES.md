# Native per-view Windows theme foundation

Debian 13 and Ubuntu 26.04 separately build and run the new labwc frame-theme
foundation. The recipes keep native upstream source/packaging/tests and the
already accepted matching wlroots3 API. No Wine library or wlroots source changed
for this step. All changes belong to DE and Builder; nothing was pushed, installed
on a user machine or incorporated into an ISO.

| Base | labwc package | SHA256 |
| --- | --- | --- |
| Debian | 0.8.3-1+karyo8 | 291574ab67e38e8d3c08aaed8e62bfc4aa1c69255df05992d98a92129c8784eb |
| Ubuntu | 0.9.3-1+karyo6 | 0bde2186d677d11ca2f3a049c169c02f95509ca95a7dd3ef2e6e779501b67308 |

## Behavior and native adaptation

A generic .exe class on XWayland selects an independent Windows caption theme;
other clients retain the configured Linux theme. No application name or personal
rule is used. The caption is 23 logical pixels, with separate font, button
geometry and light active/inactive colors. A mapped class change selects the new
theme and rebuilds decorations; changing it back restores the native appearance.
Reload recreates both themes safely with mapped clients.

Ubuntu's own background pattern and SSD button/array APIs are used explicitly.
Native image-modifier callbacks depend on global Linux geometry, so the Windows
square hover uses an independent modifier and does not consume native rounded
variants. This preserves native Linux callback behavior and avoids silently
mixing dimensions between themes. Lower corners are a subsequent step.

## Completed checks

- Checksummed native source-package builds: upstream Meson tests 2/2 on Debian
  and 3/3 on Ubuntu. Exact original recipes and every patch digest were verified.
- An ordinary UID1001 headless/Pixman runtime renders two actual X11 clients.
  Linux has custom brown colors and 41x35 button settings; Wine retains its own
  light caption and exactly 23 rendered rows. Active/inactive RGB, late .EXE
  class changes, reversal and reload are checked from real PNG pixels.
- The same final producer against the previous labwc7/5 packages fails precisely
  the Wine inactive-color requirement on both bases. This is an expected negative
  control, not a passing old implementation or a modeled compositor.
- All ten native X11 ownership/layout cases pass on each base after theme checks,
  including four late palettes, foreign windows and grouped hide/restore.
- Normal and startup-lock protocol acceptance passes separately on both bases.
- Real Wine4 PE32 and PE64 palette applications pass two iterations per bitness
  on each base: eight real runs total. Tests include initially unmapped owners,
  late palette creation, focus return, foreign overlap and group hide/restore.
  Actual package installation rejects compositor-only upgrade over the stock
  library, then accepts the exact matching native wlroots3 pair.
- Representative mixed-theme PNGs were inspected. Artifact names/sizes/hashes,
  recipes, producer snapshot and final acceptance receipts are joined and checked.

The native grouping model is explicitly distinct from the real Wine runs. Runtime
containers use a private display, ordinary UID, no capabilities/network, read-only
root/source and private tmpfs homes. No desktop socket from the host is exposed.

## Reproduction and retained evidence

Use the native compositor source-package procedure in DE integrations/compositor,
with the previously accepted native runtime/dev wlroots3 pair installed in the
matching build SDK. tests/owned-windows.py runs in an isolated native image with
Xwayland, grim, python3-xlib/Pillow and the paired library; pass --package and
--output as documented there. Normal/startup-lock use native-acceptance.py.

For real Wine, tests/acceptance/check-win32-palettes.py accepts --source,
--runtime-acceptance, --compositor-package, --wlroots-package and --output. Use
--owner unmapped --verify-library-dependency with the accepted Wine4 runtime and
native package manifests. It verifies/install-checks the native pair and owns
its private containers. Default repeats=2 and bitnesses=32,64 were used here.

Ignored receipts under Builder out/migration:

- windows-theme-native-regression-v2: both ordinary and startup protocol cases,
  original default Linux theme models and PNGs.
- windows-theme-custom-regression-v3: final producer with explicitly different
  Linux colors/button dimensions and all ten grouping cases per base.
- windows-theme-before-v1: expected old-package failure on both bases.
- windows-theme-palettes-<base>-v1: real Wine runs, images and native install proof.
- windows-theme-native-evidence.json: joined exact recipe/artifact/producer/frame
  and acceptance receipt hashes. Source outputs remain in DE
  out/compositor/<base>/windows-theme-packages.

The first Ubuntu build exposed native title_bg.color replacing title_bg_color;
the second caught a missing direct ssd.h include in the XWayland module. Both
were fixed in the native adaptation and successful source rebuilt once. The first
new QA asked for _NET_FRAME_EXTENTS, which labwc does not publish for these
clients; it now measures actual frame pixels instead. All failed preparation
logs remain. No engine was rebuilt for subsequent QA-only changes.

This closes the per-view foundation only. Final caption button assets/widths,
registered application icon matching, lower/owned client rounding and input,
maximized/fullscreen transitions, real third-party applications and the rest of
the full migration goal remain open. This headless test does not establish
physical GPU, fractional scaling or complete installed current-HEAD acceptance.
