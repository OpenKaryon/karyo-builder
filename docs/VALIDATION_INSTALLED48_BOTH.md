# Installed common Cocoa changes on both native bases

Both complete 48-patch engines now pass the original loader, Cocoa, Qt,
upstream TextEditor, packaged utilities and persistent-data checks. The actual
shared window/menu APIs and unchanged dynamic UGENE Qt frameworks also pass
their ordinary clients on both systems. Reviewed desktop frames confirm the
original Cocoa/Qt and TextEditor display paths. UGENE's own GUI and layer-backed
drawing remain unaccepted; the later49 engine is still under build/test.

| Native base | Runtime bytes | Runtime SHA256 |
| --- | --- | --- |
| Debian13 |87800760|8d2441fa8e8cf7787ed780f0bdb26e6a574e586388a167dffb767e1c4aa7b4b1|
| Ubuntu26.04 |92687400|df5004b0019b577184b61ce74fa035eeb19c1766af4452e1f339a1274c7dac9a|

Both immutable engine inputs record DE b7746080c5e370642a568d0ce6968490548f3a2f.
Later test-only DE 3ac14b2 does not alter their runtime patch inputs. Explicit
reinstallation and build provenance identify the actual engine because these
development packages share version strings across patch stacks. Existing
account/PAM/display-manager configuration and package versions remain preserved.

The common system-color cache is now exercised through the actual shared
libraries by the original dynamic Qt5.15.10 client on both systems, without
the temporary factory-cache helper. QApplication and QLabel construction
return normally. The real optional window preference and menu-view ownership
clients also return 0, with no root cleanup. Their supported boundaries remain
property state and lifetime, not tab groups, transparent decorations or custom
menu-view rendering. The new [reusable property suite](VALIDATION_COCOA_PROPERTY_PROBES.md)
provides committed sources and the additional structured native48 receipts.

## Actual documents, frames and deadlines

The original upstream TextEditor opens its standard NSOpen document on both
systems. Actual input replaces its text, saves 45 bytes and uses normal global
Quit. Both application and Quit helper return 0. The saved-file SHA256 remains
05786532df55212187f436d1163809d540c98cd0ad30ea1881bfbcbd831bca74.
Actual original-document and after-save frames were exported, hashed and viewed.

| Reviewed Debian48 frame | SHA256 |
| --- | --- |
| Cocoa |4d3f5982887253d033ab3d8c188c005d8ed01b50518a8efd2bf933046967ffc9|
| Qt widgets |fd9c75a1cb04c7f2477e0fbd06dd52cb140a00a8ef9b794395512242baf9d1b5|
| Original TextEditor document |8e4b6bcd53d96829862237b500676f794c7c6aa2a2bd32e523f884c6edf6d6d3|
| TextEditor after save |1e1fb65f7e4e0f50996fabb2ef706c19f42d79d5bfc533a318a2dd661c2cd4d2|

The corresponding Ubuntu frames are recorded in the
[earlier Ubuntu48 checkpoint](VALIDATION_INSTALLED48_UBUNTU.md). The original
Qt widget raster remains identical on both, SHA256
d90cf2c330b6cb14b737a913f15a4e4430fe7607b7c79394ba77041b4d3347d6.

Debian's three original 50ms Cocoa waits take 0.050964, 0.050935 and 0.051216 seconds.
Its windowed CoreFoundation waits take 0.007876, 0.050804, 0.051068 and 0.050783 seconds.
Ubuntu's corresponding bounds also pass. No executable deadline guardian or
function replacement is used. The original 53-byte fixture is read after normal
shutdown/start of its own server on both: Debian 19920 becomes 22942 with prefix
identity 2049:666516; Ubuntu 8834 becomes 18267 with identity 2049:803696.

All four packaged utility cases pass on each installed48 engine, including
fresh-prefix uname. This does not explain or relabel Debian45's retained first
uname exit136. Its unresolved cause remains a reliability limit rather than a
claimed fix in these unrelated Cocoa patches.

The original macOS MUSCLE calculation also passes after each installed48
upgrade and normal restart of its own prefix server, using the upstream default
two threads and unchanged official dependencies. Its output matches the earlier
45 runs exactly. See the [bioinformatics report](VALIDATION_MACOS_BIOINFORMATICS.md).

## Original UGENE and the graphics boundary

Debian48's original UGENE attempt exits 0 without a captured window. Ubuntu48
reaches its 45-second deadline; its title-only watcher reports captured:true,
but the actual reviewed frame contains only the desktop. Neither result
accepts the GUI or FASTA workflow. Initial X11 titles and an application exit
code are insufficient evidence of usable graphics.

A separate ordinary client requests a layer-backed visible QLabel using the
unchanged bundled Qt frameworks. On Ubuntu48 it exits 1 without a visible frame.
An instrumented variant confirms that QApplication and QLabel construction
succeed, then execution stops during show; no Objective-C or C++ exception is
caught. Its exact fatal cause is not yet established. A regular-file diagnostic
avoids pipe-tail ambiguity but still supplies no decisive error, so it is not
attributed to a guessed API. Both bases have the same unmodified client queued
after installed49 to measure the next graphics boundary.

Source inspection of incomplete backing-layer methods is diagnostic context,
not acceptance evidence or justification for silently ignoring drawing work.
The original UGENE CoreGraphics metadata bind gap has its own source49 patch;
whether that is sufficient for the layered client must be observed separately.

Receipts are out/migration/darling-kernel-base48-installed.json and runtime-latest;
upstream-texteditor/base48.json and base48-keyboard-v1.json;
runloop-installed48-v2-{timing,window}/base.log;
darling-data-upgrade/base-after48.json; cocoa-installed48-functional-v2/base.json;
public-cocoa-properties48/base.json; muscle-macos53/base-installed48-v5.json;
ugene-macos/base48-v1.json; dynamic-qt-layer/ubuntu48-v1.json and
dynamic-qt-layer-stage/ubuntu48-v1.json. All failures remain retained.
No shared policy/security suites or user VM/hardware changes are made.
