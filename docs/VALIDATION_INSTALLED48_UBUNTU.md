# Installed common Cocoa changes on Ubuntu

The complete48-patch native Ubuntu engine is built and installed. Original
loader, Cocoa, Qt and upstream TextEditor checks pass, as do the new ordinary
clients of the actual shared window/menu APIs and original UGENE Qt frameworks.
This accepts those common changes on Ubuntu. Debian48 remains under native
build/test, and the later49 export is not part of this installed package.

The 92687400-byte runtime package has SHA256
df5004b0019b577184b61ce74fa035eeb19c1766af4452e1f339a1274c7dac9a.
The source bundle records DE b7746080c5e370642a568d0ce6968490548f3a2f;
its build folder is karyo-source-package-20261123T164052Z-81e62b4e.
The ordinary actor SHA256 is
febc88686dac09babb3d8f863f43f94b44935d813c87f52e80a536effe26fa33.
The install receipt and subsequent application receipt are distinct records;
the install receipt's initial runtime_tested:false is not itself a test result.
The subsequent normal actor exits 0. Account/PAM/display-manager configuration
and existing package versions remain preserved by the installation check.

## Shared-library execution and reviewed frames

Cocoa and the original Qt5.15.19 client report visible windows, button signals
and UTF-8 titles. Their actual whole-desktop frames were exported, hash-checked
and viewed. The Qt widget raster is unchanged, SHA256
d90cf2c330b6cb14b737a913f15a4e4430fe7607b7c79394ba77041b4d3347d6.

| Actual reviewed frame | SHA256 |
| --- | --- |
| Cocoa |2c00c3f3448e517104d64f33b5c3d79be17fcf8324a57e98ebf68731738517dd|
| Qt widgets |212af6a3a2141cb3baa623fcef45dfde7c823657913afb51f2e17188bc63dd72|
| Original TextEditor document |4883942c6c8ae0db11da20c57266edc3eabbdd379775573c4718dd7eded4eddd|
| TextEditor after ordinary input/save |5ee7cd7c9ce2656c142c2cc2a4d341499c20f83b285a5cf6060fa46856f1d149|

The unchanged upstream editor opens its standard NSOpen document. Ordinary
X11 keyboard input saves exactly 45 bytes, then the application and Quit helper
exit0 with no forced cleanup. The saved file SHA256 remains
05786532df55212187f436d1163809d540c98cd0ad30ea1881bfbcbd831bca74.
The original-document 25-second observation uses controlled close; it is a
separate case from the successful ordinary save-and-quit run.

The original uninstrumented Cocoa 50ms waits take 0.051721, 0.051262 and 0.051713
seconds. The windowed CoreFoundation waits take 0.006918, 0.050699, 0.050857 and
0.050911 seconds. All requested bounds pass without function overrides or a
deadline guardian. All four packaged upstream utility cases pass exact stdout.

The original 53-byte Mac data fixture is read successfully after normal shutdown
of its own server 8834 and startup of distinct server 18267. Its prefix identity
remains 2049:803696. The original before record and earlier after records remain
intact; no fixture is rewritten to make the new read pass.

## Direct checks of the new common APIs

Two ordinary Mac clients call the actual installed NSWindow and NSMenuItem
implementations, without category replacements or associated-object prototypes.
The window client confirms automatic/opaque defaults, independent per-window
values and reset. The menu client confirms nil defaults, caller-release
retention, self-assignment, copied ownership, clearing and exact final release.
Both exit0; the root observer requires no cleanup.

Their executable SHA256 values are:

* window-properties: de2d6aa0cbdab2b6b80c41e625d2b926ed806e0f172bd9bed5fc9fd1ee4cb929
* menu-view-ownership: eb734a314d07a428bb5d111252726fdff0b433c172877ff20795879296c99d20

The original dynamic Qt client 97ebf854ed1499065f80f82e162855ad6dfe78c137a1316547aefc87779f1ff5
also runs with the unchanged UGENE Qt5.15.10 frameworks and Cocoa platform
plugin. It constructs QApplication and QLabel and exits 0 without the temporary
system-color factory cache. This confirms the installed common lifetime fix
for the previously failing initialization path. It does not show that client's
own window or establish arbitrary Qt rendering compatibility.

The first QA controller fails before any VM upload because Windows Path
normalizes a POSIX guest path. The corrected controller uses PurePosixPath on
the host and writes separate v2 receipts. Partial first frame exports also
remain retained: a numeric text substitution damaged a path-character list.
The corrected exports use separate directories. Neither harness failure is
relabelled as an application failure or a successful test.

## UGENE remains unaccepted

The unchanged original UGENE53.1 attempt on installed48 lasts until its
45-second observation deadline and needs controlled cleanup of that exact own
fixture. The X11 tree contains initial UGENE windows, but the exported actual
frame shows only the desktop. That frame's SHA256 is
b0de7b17eeec3f7296adc50b7c06e4ec2c7491270227b2a4983eb9ecf1fa03e6.
The custom watcher's captured:true therefore does not establish a viewable or
rendered application window. The application_compatibility_accepted and
full_gui_accepted fields remain false. Future observation must check Map State
and actual frames rather than the presence of a title in the X11 tree.

The known later CoreGraphics bind gap is addressed only in source49 and is
queued for its own full native builds. Native tab groups, transparent frames,
custom menu-view rendering/events/archiving, UGENE's actual document workflow
and broader joined-DE lifecycle remain open.

Receipts: out/migration/darling-kernel-ubuntu48-installed.json and
darling-kernel-ubuntu48-runtime-latest.json; upstream-texteditor/ubuntu48.json
and ubuntu48-keyboard-v1.json; runloop-installed48-v2-timing/ubuntu.log and
window/ubuntu.log; darling-data-upgrade/ubuntu-after48.json;
cocoa-installed48-functional-v2/ubuntu.json; ugene-macos/ubuntu48-v1.json.
All commits remain local. Shared policy/security suites are not executed.
