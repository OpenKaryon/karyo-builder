# Native scene masks for subsequent Windows frames

The renderer/input mechanism needed for rounded parent and owned windows now
passes on native Debian 13 and Ubuntu 26.04. This checkpoint adds a node-local
mask API and its matched compositor/library pair. Application frame themes,
caption metrics/icons and actual rounded-window integration remain next.

## Native package identities

| Base | Native wlroots | Compositor | Original exports retained |
| --- | --- | --- | --- |
| Debian 13 | 0.18.2-3+karyo3 | labwc 0.8.3-1+karyo7 | all 769, plus one new function |
| Ubuntu 26.04 | 0.19.2-1+karyo3 | labwc 0.9.3-1+karyo5 | all 823, plus one new function |

Debian runtime-library DEB SHA256:
`dd7d1855548ec46b8fb3e0e7b7c2833ba15352306cafac09da9374933c70962f`.
Debian compositor DEB SHA256:
`a473cbe52273b00fa193b6566a568efce551a83c8dedb3ddd9cd7d2aa1801e22`.
Ubuntu runtime-library DEB SHA256:
`ca6624e42aa72170813129466ac653fe606a6a751b528c6aff093c145ca3f1f6`.
Ubuntu compositor DEB SHA256:
`5ec2a285d2bd4116298f448eab3d881cc72782fa83ac23c2d6b8589ee6c00859`.

The copied original recipes match the final files byte for byte. Native source,
strict compilation and packaging are preserved. Labwc's native tests pass two
suites on Debian and three on Ubuntu. Both upstream wlroots releases report
`No tests defined`; the runtime checks below provide this feature's acceptance.
Neither native source package contains a .symbols policy file. Validation checks
the actual exported symbols and SONAME without inventing such packaging metadata.

## API, ownership and native ABI

The MIT patch adapts the reviewed prototype scene-clip-region.patch at 26bad17,
original SHA256
`fc18e9a3959178bd5a2b419ef2ea17d85fffce8ee1d207fb246d4bef06ece3a4`.
It uses the existing node addon lifecycle and copies a Pixman region in node-
local coordinates. Clearing the region removes the addon. Node and ancestor
masks restrict visible/opaque regions, hit testing and output damage. No public
structure field is added. The direct-scanout guards are adapted separately to
native 0.18's boolean and 0.19's refactored enum/destination-box paths. Unclipped
nodes retain their existing eligibility decisions.

Each QA executable is compiled with the original stock SDK headers before the
new native runtime/development packages are installed into a fresh image. Its
binary hash remains unchanged after installation. The new symbol is obtained
through dlsym; all previous dynamic exports and the native SONAME must match.
Only wlr_scene_node_set_clip_region may be added to the export set.

A separate program compiled against the new headers reports the same public
sizes and offsets as that old-header executable:

| Native type | Debian before/after | Ubuntu before/after |
| --- | --- | --- |
| wlr_scene_node | 112 bytes | 112 bytes |
| wlr_scene_tree | 128 bytes | 128 bytes |
| wlr_scene_rect | 136 bytes | 136 bytes |
| wlr_scene_buffer | 400 bytes | 440 bytes |

Parent, link, enabled, x/y, events, data and addon offsets also match within each
native ABI. The distinct 0.18 and 0.19 layouts are retained, with no cross-base
library transplant. Both installed native package sets pass dpkg verification
and apt-get check in their disposable SDK images.

## Real renderer, input and damage

The own C producer allocates an actual CPU buffer, native Pixman renderer,
allocator, headless output and nested scene nodes. It reads the resulting output
buffer and calls native wlr_scene_node_at for every corresponding logical point.
Each phase checks all 400x320 output pixels and input targets against the fixture's
explicit geometry. Real pointer transport with rounded application frames remains
a subsequent integration gate.

Each native base passes four cases: output scales 1/2, normal/90-degree transforms.
The positive matrix covers copied masks after caller mutation, all four corner
cutouts, a complex hole, nested parent/child clips, moving, reparenting and return,
empty/cleared masks, hide/restore while the mask remains active and subtree
destruction. The before-hide and restored frames must also be byte-identical. Independent addons
and source pixel buffers must be released. Six initial frames exercise buffer
reuse before damage-changing operations; the test does not force periodic full
repaints. Representative complex-hole frames from both bases were inspected.

Each base completes 87 positive phases and 41 before phases. The before matrix
requires the new API to be absent and validates native unclipped rendering,
input, scaling/transform and scanout availability. It is not presented as an
old masked-rendering defect. Final producer SHA256:
`31869fb9f370e88ac4a5afe350e54e08c4e5cabda228f3f720228401417b3ce0`.

The scale 1/normal case additionally uses a full-output opaque green buffer above
a black background. The native output-sample event proves direct scanout is
selected before clipping, rejected for the masked buffer and restored after
clearing. Actual corner pixels must agree. This exercises the common native
scanout decision path on headless outputs; physical DRM hardware, fractional
scales, color management and arbitrary GPU drivers remain separate gates.

## Matched pair and existing behavior

The compositor requires the exact native wlroots karyo3 version. Each base first
rejects a compositor-only installation over its stock library and then accepts
the complete native pair. Four actual PE32/PE64 unmapped-owner Wine palette runs
and four mapped 1x1-owner runs pass on each base, including late tools, focus,
foreign-frame return and group hide/restore. The engine is the accepted Wine4
from the [child-region milestone](VALIDATION_WINE_CHILD_REGIONS.md).

Ten real X11 layout models per base retain explicit foreign classes/processes,
ordinary native clients, ambiguous documents and the supported owner layouts.
These models are separate from the actual Win32 program above. Ordinary and
startup-lock protocol tests also pass on both packaged compositor/library pairs.
No new compositor code applies masks to application frames at this checkpoint.

All runtime execution uses disposable ordinary users with no capabilities/new
privileges/network, private displays and a read-only system root. The ABI/render
probe opens no desktop socket and uses its own in-process Wayland display. Native
package installation and compilation occur in separate image-preparation steps.
Test code is own GPL-3.0-or-later; the native derivatives retain MIT/GPL notices.

## Reproduction and retained attempts

After building the native wlroots recipe, run from Builder:

    python tests/acceptance/check-scene-clip.py --source ../karyo-de --package-directory PATH_TO_NATIVE_WLROOTS_RESULT --sdk-image karyo-wlroots-source-builder:trixie --output out/new-scene-debian

Use the captured native SDK image from the source manifest; Ubuntu uses its own
ubuntu2604 SDK. The host driver validates package identities/size/hash, freezes
the producer, checks old/new headers and retains native logs plus actual PPM
frames. Each run owns bounded containers and cleans up its own names on exit.

Final Builder out/migration receipts are scene-clip-<base>-acceptance-v6,
scene-clip-palettes-<base>-v1, scene-clip-mapped-palettes-<base>-v1 and
scene-clip-native-regression-v1. scene-clip-native-evidence.json joins them with
native source manifests and exact final recipes. Source outputs are DE
out/compositor/<base>/scene-clip-wlroots-packages and scene-clip-paired-packages.

Initial v1 before cases exposed the fixture's assumption of unfiltered texture
edges at scale 2. Both stock native renderers use linear filtering there. The
synthetic texture now explicitly chooses nearest filtering, keeping every-pixel
criteria exact without changing desktop filtering. V2 then passed every before
case but image preparation misused a bare sha256 image ID as a Dockerfile FROM
name; the driver now uses its verified local capture tag. Failed logs remain.
V3 completed both matrices; V4 additionally validates aliased artifacts and owns
container cleanup. V5 added active-mask hide/restore coverage, which passed,
but failed the later fullscreen control because its expected corner flag was
not reset for the new buffer. V6 corrects that independent test-state transition
and passes every case. Native source packages were not rebuilt for QA-only changes.

Windows frame resources/metrics/icons and their real input behavior, remaining
Wine applications/import/deployment, Darling, VMware host channels, VPN lifecycle
and a joined current-HEAD desktop remain in the full goal. Only DE and Builder
changed. No push/fetch, ISO rebuild or user-system deployment was performed.
