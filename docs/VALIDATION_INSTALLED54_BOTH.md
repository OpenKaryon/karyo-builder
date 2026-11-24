# Installed54 on Debian and Ubuntu: CPU surfaces and remaining GUI failures

Both full54 engines built and were explicitly installed in the separate native
Debian13 and Ubuntu26.04 QA guests. All four artifacts per base were rechecked by
size and SHA256. The11-stage ordinary pipelines are terminal on both bases:
the first10 jobs return0 and the public-surface job returns1. This is partial
component evidence; the whole migration and UGENE GUI remain unaccepted.

The immutable54 bundle records DE6ecdfaaad6335fe0e613459fa04e702e51b6e37e.
The current ordinary observer hash is
6df6d669164ac8281e2589b0600fd36fa81b3a0585b84520f82c32e78e3908ed.
Native kernels are6.12.117+deb13-amd64 and7.0.0-43-generic respectively.
No security tests or shared unit suites ran for this slice.

## Native artifacts

### debian

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
|karyo-darling-runtime-dbgsym_0.1.20260906+git60ba801-1+karyo1.debian13_amd64.deb|3716428|`630447b7996ea6e33c870c0cef00c15a3c3ec05066acdbf14a37ad0932e72c7d`|
|karyo-darling-runtime_0.1.20260906+git60ba801-1+karyo1.debian13_amd64.deb|87814740|`811628fdc3d5a5e78dff39ae20bd5a742ee35d02d05096ad15b50015da71dc1f`|
|karyo-darling_0.1.20260906+git60ba801-1+karyo1.debian13_amd64.buildinfo|16195|`f9aa7165f40cbb7879a61fa6f7236a1575efc0185a891030301ec5990ad06805`|
|karyo-darling_0.1.20260906+git60ba801-1+karyo1.debian13_amd64.changes|1882|`4c4364203134f608221f4c85763736d1866a7b97ae2b4b5a2b1e208293812bd0`|

### ubuntu

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
|karyo-darling-runtime-dbgsym_0.1.20260906+git60ba801-1+karyo1.ubuntu2604_amd64.ddeb|3698398|`06a2d2184541bb571de7e62c608361543e6d0e41f7dae67694902c2497b0dfd7`|
|karyo-darling-runtime_0.1.20260906+git60ba801-1+karyo1.ubuntu2604_amd64.deb|92707742|`0022923b0d34fc20746a8ad91e2b6150048c54c99f4892f7740f6cf429910368`|
|karyo-darling_0.1.20260906+git60ba801-1+karyo1.ubuntu2604_amd64.buildinfo|17969|`92201c1d330fdbe4c02f1287b21fbd1b8de170f2a929c22b4fd62bef04c90653`|
|karyo-darling_0.1.20260906+git60ba801-1+karyo1.ubuntu2604_amd64.changes|1927|`22c8f272d8d1b49f175ec547cacaae913d805a1dfe880c7ba1b8bdb5cf1e9332`|

## What actually passed

Loader argument/file I/O cases, Cocoa and static Qt controls, packaged utility
cases, event/deadline handling and shared window/menu/dynamic-Qt scenarios pass.
Eight actual compositor frames, four per base, were exported, rehashed and
viewed: Cocoa and Qt UTF-8 captions/labels/buttons, original TextEditor opening
its fixture, and normal keyboard editing. The exact45-byte edited document has
SHA25605786532df55212187f436d1163809d540c98cd0ad30ea1881bfbcbd831bca74.
The independent Qt widget raster remains
d90cf2c330b6cb14b737a913f15a4e4430fe7607b7c79394ba77041b4d3347d6.

Existing application data and prefix identity survive their own normal server
restart. Original macOS MUSCLE5.3 aligns the three-sequence FASTA using upstream
default threads on both bases. Its unchanged GNU dependencies stay in its own
prefix. This is CLI bioinformatics evidence, not UGENE GUI compatibility.

Public IOSurfaceRoot matching now passes both query paths. The ordinary17x9 BGRA
buffer client creates storage, verifies layout, locks it, writes/reads its pixels
and unlocks successfully on both bases. This validates the common0054 temporary
directory fix in installed engines. Dynamic Qt's layer client also finishes its
event loop; that exit alone does not accept its visual output.

## What still fails

The cooperating lifecycle reader passes, but its owner fails after reader exit.
Additional ordinary diagnostic clients reproduce on both bases: initial local
count2, reader completion, failed owner pixel lock, local count0 and a shared
in-use flag stilltrue. Source inspection finds object-port messages bypass the
caller-refresh callback already used by the master port. Common0055 reuses that
same callback on the main queue. Its two units compile with Clang19 and21, and
the entire55 stack applies/reverses using Git and quilt on both bases in
source-only mode. Installed55 lifecycle acceptance is still pending.

The original Ubuntu layer client's two frames are black. Debian's original
layer launch times out after60.62s with no frame under severe guest memory
pressure; this remains a separate failed observation. After normal shutdown of
27 proven idle own QA prefixes, available memory rises68848->1003924KiB. Existing
data/MUSCLE prefix identity and server remain unchanged; no files are deleted.

A corrected ordinary diagnostic follows Apple's layer-hosting order: assign a
custom layer before wantsLayer, manage its contents through Core Animation, and
do not ask the view to draw. It initially holds the IOSurface, but Darling's
subsequent NSView drawing replaces the contents. Both native bases show black
frames for both expected colors; program and pixel acceptance remainfalse.
One frame per base was viewed and each pair has identical hashes. This is a
reproducible general hosting issue; no application method overrides were used.
The original backed-view probe's apparent program success is not GUI acceptance.

Original, unchanged Intel UGENE53.1 still exits0 before a usable window appears:
- debian: 2.247177s, no captured application frame.
- ubuntu: 2.13693s, no captured application frame.

No alignment through UGENE, installer success or GUI compatibility is claimed.
Do not replace this failure with the successful MUSCLE result or a probe result.

## Debian53 recovery and review trail

Earlier Debian53 attempts failed at apt180s and outer SSH660s. VIX showed67 idle
Darling servers,468 mldr processes and about107MiB available memory. Normal
shutdown of28 proven completed QA prefixes restored about1.1GiB; protected data
and MUSCLE remained intact. The retry-v3 controller then executed all11 jobs:
first9 return0, dynamic-layer/public-surface return1. Its four actual ordinary
application frames were exported, rehashed and viewed. The earlier failures are
retained as infrastructure observations, not established UGENE defects.

The local evidence index is
`out/migration/darling-native54-both-evidence-v1.json`, SHA256
3361614e5322f3d06760eb064e67f612bee4d5ef06e25d1a1bcb4be2fb1ed4c3.
It includes exact manifests, all artifact hashes, both pipelines, public and
hosting records, UGENE outcomes and all eight reviewed frame hashes.
Diagnostics live in `out/migration/surface54-diagnostic-v1` and
`out/migration/surface54-hosting-v2`. The immutable55 input index is
`out/migration/darling-common-apis55-inputs.json`; source-only proof is
`out/migration/darling-current-inputs-accepted-v33/acceptance.json`.

The next55 run is deliberately limited to the ordinary main baseline and
targeted IOSurface/hosting cases. Full engine builds stay sequential. GPU import,
full Core Animation semantics, UGENE GUI and whole DE acceptance remain open.

Apple reference for the ordinary hosting contract:
[NSView.wantsLayer](https://developer.apple.com/documentation/appkit/nsview/wantslayer).
Per-process usage semantics:
[IOSurfaceGetUseCount](https://developer.apple.com/documentation/iosurface/iosurfacegetusecount(_:)).

Installed55 follow-up: [both native lifecycle results](VALIDATION_INSTALLED55_BOTH.md).
