# Native Wine default close buttons

The generic LGPL patch in DE commit `e0a2ed5` renders a white cross on a solid red
square for enabled default child/tool/owned caption buttons. It saves/restores
the complete GDI DC state, sets copy-pen drawing and preserves native disabled
controls and small-button fallback. There is no application-name rule, private
prefix, registry tweak or proprietary asset. Compositor-provided main frames
and application-painted custom captions are separate boundaries.

## Native source outputs

| Source target | Version | libwine DEB SHA256 |
| --- | --- | --- |
| Debian amd64 | 10.0~repack-6+karyo2 | `8ad4464ca322a901e43c4e48cb7931a5fcaedaf2df4e058190a77d3f80ec7bc3` |
| Debian i386 | 10.0~repack-6+karyo2 | `ac2cde1978a644f78f1f3e39767d28aaa054693dcc2d75fb50ecd37efe9e5dad` |
| Ubuntu native WoW64 | 10.0~repack-12ubuntu1+karyo2 | `8759ef1825cdf9c49d34ee634781552c371cbc2614d0d59be8362ef8b2f70cfb` |

All three ordered source recipes retain the existing popup-menu patch, the same
Debian32/64 source and changelog epoch, native control/packaging and original
Wine LGPL-2.1-or-later notices. The caption patch SHA256 is
`863af83b9d0ffa5488ea328b70e0af673d0ef684fc668ef9bed7492956b303e0`.
Captured original recipes match the final files exactly. All three source builds
complete successfully; native Wine packaging still disables upstream tests, so
compilation is not presented as passing Wine's upstream unit suite.

The actual Debian coinstallation again verifies all 88 shared libwine files
identical, with 786 amd64-only and 845 i386-only paths. Both architectures install
in one verified transaction. The compositor/library pair is unchanged from the
[unmapped-owner checkpoint](VALIDATION_WIN32_UNMAPPED_OWNERS.md): native Debian
labwc 0.8.3-1+karyo5 with wlroots 0.18.2-3+karyo2; native Ubuntu labwc 0.9.3-1+karyo4
with wlroots 0.19.2-1+karyo2. Its real dependency refusal/paired recovery gate passes
again before palette acceptance.

## Real runtime, pixels and displayed frames

Each base passes all eight installed runtime/menu stages: Qt, separate account,
PE64 engine, keyboard/mouse menus, PE32 engine and keyboard/mouse PE32 menus.
Each then passes four real fully unmapped-owner palette runs, PE32/PE64 twice,
including late palettes, foreign-frame return, group hide/restore, focus and
clean close. These are eight palette runs in total across both native bases.

The same frozen caption C/actor runs PE32 and PE64 on each old and new engine.
The final baseline is v4; positive caption acceptance is v3. Both native bases
pass every case, with the following GDI observations in each positive bitness:

| Default control | Red pixels | White cross pixels | Square size |
| --- | --- | --- | --- |
| WS_CHILD caption close | 240 | 16 | 16x16 |
| Tool caption close | 108 | 13 | 11x11 |
| Disabled tool close | 0 | unchanged native path | no new red face |
| Ordinary unowned close | 0 | unchanged native path | no new red face |

The actor requires readable pixels, a square with at least 75 percent red fill
and white pixels inside. A red outline cannot pass. Before the patch, all four
controls report no new red face. This GDI check is supplemented by actual saved
Wayland compositor frames, so backing-store pixels alone are insufficient.

The host driver checks the accepted palette producer/actor SHA256 against the
exact own fixture source. For each restored-0.png it locates connected red
components and counts the white pixels within their bounding boxes. All eight
baseline frames contain no red button; all eight new frames contain exactly
four 11x11 components with 108 red and 13 white pixels each. Representative Debian
and Ubuntu frames were also visually inspected. The same frame assertions now
run inside the public caption QA driver before its real C fixture runs.

Final C source SHA256:
`c5a282cf7d70780768e3684973f82d372a9481ef75ff52c0af857cf6c19fd0af`.
Unchanged final actor SHA256:
`d1ebabec6169f7efdeb3487a59e4791cbfe207c6867857b76412733d339c074c`.
Own source, actors, Docker inputs, native images and per-case logs are retained.
The image preparation uses root only for native package installation/compilers;
Wine runs as UID 1001 with no capabilities/new privileges, no network, private
home/runtime/bus and a read-only system root. No host display or user data is used.

The original runtime/menu launcher package remains source `e782fb0`. A subsequent
combined check installs the corrected source `236dd5a` launcher over each new engine:
Debian runs PE32 twice in an existing native win32 prefix, Ubuntu runs PE32 twice
in an existing win64 WoW64 prefix, preserving the architecture/data marker.
Both pass. All five installed launcher Python files also match current checkout
runtime bytes exactly. This does not relabel every component as a joined current-
HEAD DE installation; [prefix acceptance](VALIDATION_WIN32_EXISTING_PREFIX.md)
keeps its original before/after evidence separate.

## Reproduction and retained evidence

The host caption QA script additionally requires Pillow for frame inspection;
this is a QA dependency, not a dependency of the standard-library Builder CLI.
After preparing an accepted native palette matrix, run from the Builder tree:

    python tests/acceptance/check-win32-captions.py --source ../karyo-de --runtime-acceptance out/migration/wine-close-palettes-debian-v2 --output out/new-caption-debian

Use --baseline with the accepted Wine+karyo1 palette matrix. Output must be new.
Native Wine source outputs are DE out/wine/<target>/close-packages. Builder local
wine-close-runtime-<base>-v2, wine-close-palettes-<base>-v2,
wine-close-captions-<base>-v3 and wine-caption-baseline-<base>-v4 retain exact
artifacts. wine2-existing-prefix-<base>-v1 records the new-engine/new-launcher
combination. wine-close-native-evidence.json joins them; wine-close-native-builds
and wine-caption-rendered-evidence JSON files retain source and frame details.

An initial ignored orchestration script selected labwc-dbgsym with an overbroad
glob. Dpkg rejected image preparation before any Wine execution. The corrected
helper chooses manifest.binaries.labwc and the complete v2 runtime/palette gates
pass. That failed v1 output is preserved; neither successful source build was
restarted. Earlier caption actor cleanup assumed /usr/bin/wineserver on Ubuntu;
the corrected actor closes its own compositor/container and final v4/v3 passes.

## Remaining boundaries

Pressed/hover rendering, alternate DPI/themes, custom captions, real MDI child
layouts, bottom/child rounding, caption metrics/icons, resize trails, real
third-party applications, legacy-prefix import/conversion and installed-user
upgrade still have separate gates. The displayed-frame test covers the captured
native default-DPI software-rendered fixture, not arbitrary physical GPU behavior.
Darling, remaining VMware host channels/resize and VPN lifecycle remain in the
full migration plan. No push/fetch, Forge work, user/QA VM deployment, Acer change
or ISO rebuild was performed. This milestone does not complete the whole goal.
