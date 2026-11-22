# Floating Wine frame corners on both native bases

Final native Debian 13 and Ubuntu 26.04 packages render rounded ordinary and
owned Wine frames, and keep maximized/fullscreen windows square. This checkpoint
changes DE and Builder only. No push, distro/ISO, Forge, user VM or Acer change.

| Native artifact | Version | SHA256 |
| --- | --- | --- |
| Debian labwc | 0.8.3-1+karyo11 | 277f7e959cb5f8c963e8fd42a1b992fe52d83e497a213ba2c9b509e409dfd23f |
| Ubuntu labwc | 0.9.3-1+karyo8 | 3f7e509eba311a825903fcd127be3f7a37eb5eba3870276c0ac5fc79a90d25b8 |
| Debian wlroots | 0.18.2-3+karyo4 | a8710a26da667c56804e3bf3d9f2d15ca0ccce2f1d03e3e872806a9d00f350c8 |

Ubuntu retains the already accepted native 0.19.2-1+karyo3 library. Wine4 and the
Win32 runtime/resource package from DE e70b630 are unchanged; this stage modifies
its independent QA, not its installed runtime payload.

## Result and common policy

Floating .exe SSD frames have six-logical-pixel outer corners at both ends,
including curved lower borders and matching inner content masks. A titlebar
ancestor mask includes buttons, so cut caption pixels cannot still activate the
close button. Shadows and native resize extents are separate. Windows rounded
image variants retain their glyphs but use the scene mask rather than Linux
image-modifier dimensions. Native Linux styling stays configurable.

Opaque managed owned DIALOG/UTILITY windows with client-painted captions use a
four-pixel mask. Normal custom CSD, ARGB surfaces, menus/tooltips and unmanaged
popups keep their own shape. Class/type/parent changes and property deletion
recompute or remove the mask; resize, reload, minimize/restore and scene lifetime
retain correct state. No application name or private Wine-prefix setting is used.

Debian 0.18 ignored deleted parent/type properties, retaining stale data. Its XWM
now follows the already native 0.19.2 parser behavior, including empty type arrays.
The matching compositor requires the exact new Debian library version. Ubuntu
already has those semantics and receives no new library build here. Compared
with the accepted Debian library3, all 114 public header hashes, all 770 exports
and the SONAME are identical. There is no new ABI change in this step.

## Completed final checks

- Native labwc source builds pass upstream tests: Debian 2/2 and Ubuntu 3/3.
  Checksummed sources/recipes/patches match final Git contents. The Debian
  wlroots build invokes tests but reports No tests defined; own runtime checks
  establish its property-removal behavior instead of claiming upstream coverage.
- Public package driver --scenario rounded-frames executes 23 actual X11 phases
  per base, with private Wayland pointer and pixel reads. It covers all four
  corners, input through owned cutouts and normal client input, safe caption
  corner clicks, resize, max/fullscreen and reversal, minimize/restore, reload,
  removed/restored parent/type/class, normal CSD, ARGB and override popups.
- The same producer observes the previous square packages in distinct baseline
  mode. Both controls pass; their baseline.json is not positive acceptance.
- The default caption scenario passes separately on final packages: actual red
  close hover, visible glyphs, edge maximize/restore/minimize/close and narrow
  sizes. This gate caught and prevented a missing Ubuntu rounded-image variant.
- All ten ownership models and mixed-theme/class/reload checks pass on each base;
  normal and startup-lock protocols pass separately, six final jobs total.
  Their actual runtime images contain Debian library4 and Ubuntu library3.
- Twelve real Wine palette runs pass: PE32/64, two unmapped-owner repetitions
  and one mapped 1x1-owner repetition per base. Each checks all four corners of
  the real main frame and four actual WS_EX_TOOLWINDOW palettes after restore,
  plus focus, foreign overlap and grouped minimize/restore. Tools have actual
  depth 24 surfaces. The masked tool vertices reveal the parent client's gray;
  the main outer vertices reveal the black desktop.
- Every final real palette frame preserves four 11x11 red/white child close
  glyphs with exact 108 red and 13 white pixels. These are independent of the
  compositor hover resource.
- Eight actual PE32/64 menu runs pass, mouse and keyboard on both bases:
  repeated navigation and native POPUP_MENU/no-input semantics are preserved.
- Builder 50 unit tests pass, with two native-only skips on Windows.

Runtime images install verified native artifacts and exact SVG hashes before
unprivileged GUI checks. Displays, buses and homes are private, network is none,
root/source are read-only, capabilities are dropped and no-new-privileges set.
Representative main/tool/mask PNGs were inspected. This is scale 1 headless/Pixman
coverage; physical GPU and fractional DPI remain separate acceptance gates.

## Reproduction and evidence

DE compositor recipes now require scene-mask headers. Build the native wlroots
recipe first and install its matching runtime/dev pair in a disposable native
SDK, requiring apt-get check. Pass that prepared local image to source-package;
Builder captures its immutable identity. A stock compositor SDK does not declare
the new scene API. No private temporary image ID is a product input.

Use tests/acceptance/check-caption-buttons.py with --source, --runtime-acceptance,
--compositor-package, --wlroots-package, --win32-package and --output. Select
--scenario rounded-frames; --baseline is a separate previous-square observation.
The driver freezes both the scenario and shared harness. Default scenario still
checks caption controls. check-win32-palettes.py --rounded-frames adds real Wine
corner assertions; --owner mapped/unmapped selects the framework owner case.

Ignored Builder out/migration final receipts:

- rounded-frames-packaged-<base>-v3: final 23-phase mask/input checks.
- rounded-frames-buttons-<base>-v2: preserved caption controls/actions.
- rounded-frames-before-<base>-v1: earlier-square controls.
- rounded-frames-native-regression-v2: final model/theme/protocol/lock matrix.
- rounded-frames-<mapped|unmapped>-final-<base>-v2: twelve actual Wine cases.
- rounded-frames-menus-v2, rounded-frames-child-glyphs-v1.json and
  rounded-frames-debian-abi-v1.json: actual menus, child rendering and full public
  header/export/SONAME comparison. The library payload is unchanged across the
  interim/final compositor retries, so that ABI comparison is not repeated.
- rounded-frames-native-evidence.json joins current source/recipe/artifact/actor
  and supporting receipt hashes. Native final compositor outputs remain DE
  out/compositor/<base>/rounded-frames-final-packages. The Debian library is in
  removed-hints-wlroots-packages; the existing Win32 resource package is reused.

Retained preliminary failures are meaningful: the first Debian runtime reached
parent deletion and proved stale ownership; the newer native XWM behavior fixes
it. Initial compilation adapted differing native enum/include/SSD buffer APIs.
The first final button check found Ubuntu requests a rounded image-state variant,
which the former square-only theme did not populate; both variants now exist
without borrowing native Linux geometry. Final pairs were rebuilt and their full
runtime matrices rerun. Earlier intermediate receipts are not substituted for
final image tests.

Registered application icons, further real third-party applications, legacy
prefix import/upgrade, Darling, remaining VMware host channels, VPN lifecycle
and a joined current-HEAD installed desktop remain in the full goal. This
checkpoint does not claim those requirements complete.
