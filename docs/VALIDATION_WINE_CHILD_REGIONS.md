# Native Wine child and MDI regions

The common LGPL engine patch gives ordinary captioned Win32 children small
DPI-scaled corners, using the same default shape for rendering and input. It
also corrects stale minimized-icon pixels during MDI restore. This checkpoint
covers WS_CHILD regions; compositor-provided main/owned-popup frames, their
metrics/icons and bottom rounding remain separate. There are no RomArtist rules,
per-application registry settings, imported prefixes or proprietary resources.

## Native builds and runtime pair

| Native target | Wine version | libwine DEB SHA256 |
| --- | --- | --- |
| Debian amd64 | 10.0~repack-6+karyo4 | `45cfa65993cdfe588bac480f5be71b8b7a63379e044f4a3e017400a93db806f0` |
| Debian i386 | 10.0~repack-6+karyo4 | `1dce82dc51eebcb050f5928951a98035e3e2efc43e5d1cbe0c57ce0b995cc0ab` |
| Ubuntu native WoW64 | 10.0~repack-12ubuntu1+karyo4 | `9095ff3aa0edea66b3887ed7e99903f15d0088b730ad8efdcffd41b3bb47b56d` |

The three original recipes match the captured build inputs byte for byte.
Debian32/64 retain the same source, patch order and changelog epoch. Native
coinstallation proves all 88 shared libwine paths identical, with 786 amd64-only
and 845 i386-only paths. Runtime files are selected from verified manifests;
debug/development packages are not indiscriminately installed into QA runtimes.
Native packaging preserves the upstream Wine test configuration, which disables
its upstream suite. Successful compilation is not an upstream unit-test pass.

Debian uses labwc 0.8.3-1+karyo6 and wlroots 0.18.2-3+karyo2; Ubuntu uses native
labwc 0.9.3-1+karyo4 and wlroots 0.19.2-1+karyo2. Each actual paired-install check
first rejects the new compositor alone with a stock library, then accepts the
matching exact dependency. The Debian absolute-input correction is described in
[its separate report](VALIDATION_ABSOLUTE_POINTER.md).

## Shape and restoration behavior

The default cache is separate from the application's explicit win_region and
is freed with the window. Native DPI and size determine its two-logical-pixel
corners. Custom SetWindowRgn rectangles and holes take priority. The explicit
GetWindowRgn API still reports ERROR for an implicit default shape, a simple
region for an explicit rectangle and a complex region for the application hole.
Straight edges and the client body remain visible and input-active.

Maximized, minimized, layered, tiny, non-captioned and popup windows retain the
native exception paths tested against the matching before image. All four
corners and edge midpoints use actual WindowFromPoint and captured output pixels;
the complex hole also checks center input/background. Ordinary and true MDI
children receive real pointer body/corner clicks through the private compositor.

The first rounded-child implementation passed those initial checks but visual
review found a separate damage defect: restoring a minimized MDI icon left its
old rectangular corners behind. At 192 DPI, retained frames on both native bases
show 48 stale pixels inside its old footprint; Wine2 leaves zero. The stronger
unchanged-fixture negative control fails the old Wine3 implementation on Debian.
It requires complete erasure of the old icon rectangle, not just a few corners.

The corrected engine captures the old visible region before changing shape-
affecting style/exstyle bits. It then exposes and redraws the difference before
the subsequent position request. The final Wine4 native packages leave zero
stale pixels in every tested bitness/DPI case. No whole-desktop periodic repaint,
application-name heuristic or preemptive prefix rewrite is used.

## Actual before and after matrix

Each base passes PE32 and PE64 at actual 96 and 192 DPI, both before and after.
The original fixture reports DPI through Win32; the actor refuses a mismatched
value. DPI settings are applied only to each fresh disposable QA prefix and are
not product-wide or per-application policy.

Every case completes these 15 real engine stages:

- Ordinary captioned child, repeated live growth and subsequent shrink.
- True MDI child, maximize, restore, minimize and restore from its icon.
- Explicit rectangle, complex region with a hole and explicit-region removal.
- Layered, non-captioned, tiny and owned-popup native exceptions.

That is 60 stages per base, or 120 across the positive native matrix, plus the
matching before matrix. Region API results, every corner and edge, visible body,
actual pointer targets, vacated resize pixels and the complete vacated icon area
must pass. Default shapes do not accidentally become explicit application regions.
The source and actor identities match their corresponding native baseline.

Producer source SHA256:
`ebc1a0b09f818eb6c71d1685ddc8385a7296ff9116542e1c8b586b0ee1541393`.
Actor SHA256:
`ecdfc8635a47b727258487a688bc412588901bad20407ade74edf9224542a381`.
Native child-region patch SHA256:
`d7da3afe7a88f72f9ea79283eca750c34023b104bc4e526bba1da160b4b344cb`.

A server-only diagnostic first confirmed the correction with 15 stages and zero
stale pixels while native packages were still compiling. It is explicitly marked
as diagnostic-only. The final acceptance above instead uses complete installed
native DEBs on both bases. Representative Debian PE32/PE64 high-DPI packaged frames are also byte-identical
to the inspected diagnostic frame; their stored frame hashes are verified.

## Regression and launch boundary

Both final native engines also pass all eight runtime/menu checks, four fully
unmapped-owner palette cases, PE32/PE64 caption-button checks and existing-prefix
reuse. The menu checks use real keyboard and persistent-pointer navigation.
Palettes retain late creation, foreign-frame return, focus and group hide/restore.
Caption checks retain GDI pixels and four displayed red/white tool buttons per
frame; disabled and ordinary unowned controls keep their native paths.

The own launcher package still comes from source `236dd5a`. Its five installed
Python runtime files match the current checkout exactly. Debian runs PE32 twice
in an existing native win32 prefix, Ubuntu twice in an existing win64 WoW64
prefix, retaining its architecture and pre-existing application-data marker.
This does not assert pure-win32 prefixes on Ubuntu or legacy import/conversion.
It also does not relabel every DE component as a joined current-HEAD installation.

All application execution uses disposable ordinary accounts, private home,
runtime directory, D-Bus and labwc/Xwayland output, no network/capabilities/new
privileges and a read-only system root. Native package preparation is separate.
The fixture is own GPL-3.0-or-later C/Python QA; Wine derivatives retain LGPL-2.1-or-later and native copyright notices. Test programs are not installed as product
runtime payloads.

## Reproduction and retained evidence

From Builder, after preparing an accepted native runtime/palette image:

    python tests/acceptance/check-win32-child-region.py --source ../karyo-de --runtime-acceptance out/migration/wine4-palettes-debian-v1 --baseline-matrix out/migration/wine-child-region-baseline-debian-v5 --output out/new-child-debian

First use --baseline with a captured pre-rounding image to obtain a matching
native before matrix. Output paths must be new. The host driver freezes C/actor
inputs, compiles both actual PE machines with strict warnings and retains each
frame, native report and log. Fixture identity and native baseline-receipt hashes
are checked; accepted presence alone is insufficient.

Local Builder out/migration retains wine-child-region-baseline-<base>-v5,
wine4-runtime-/palettes-/child-region-/captions-/existing-prefix-<base>-v1,
wine-child-region-damage-negative-debian-v1 and the explicitly diagnostic-only
wine-child-region-server-diagnostic-debian-v1. Earlier failed and superseded
runs remain distinct. wine-child-region-native-evidence.json joins exact native
manifests, artifact hashes, source/actor identities and all final receipts.
Native DE outputs are out/wine/<target>/child-region-damage-packages.

Physical GPU/direct-scanout behavior, other themes and arbitrary applications
remain unproven here. Main/owned frame styling, real third-party apps, legacy
prefix import and existing-user deployment, Darling, remaining VMware host
channels/resize, VPN lifecycle and a joined current-HEAD desktop remain in the
full goal. Only DE and Builder changed; no push/fetch or ISO rebuild was run.
