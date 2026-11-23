# Reusable ordinary Cocoa property clients

The Mac probe builder now accepts `--suite cocoa-properties` in addition to
the default application suite. This compiles DE's separate window preference
and menu-view ownership clients without invoking Qt or qmake. Existing
commands without the option continue to build the original loader, Cocoa
window and static Qt application. Both suites validate the expected Intel64
Mach-O executables and archive metadata before writing their build receipts.

```sh
python tests/acceptance/build-macos-probes.py --suite cocoa-properties \
    --de-source /path/to/karyo-de --image local-macos-cross-sdk --output out
```

The property sources, build script and instructions are in DE commit 3ac14b2,
under integrations/macos/tests/cocoa-properties. They contain no replacement
methods or copied runtime implementations. A tracked NSView subclass observes
destruction; the menu item itself is the actual installed NSMenuItem class.
These executables are not shipped in desktop packages or added to the default
three-application archive.

The immutable external SDK image is
sha256:4bfaf1eb25e15355258071ca76f0ba5d86779677746783598eb8077d680cc7b6.
The property build is macos-probes-20261123T174121Z-ed9e6ad7; the separate default
application regression build is macos-probes-20261123T174159Z-16b3df92.
Both complete normally. The build initially records the test sources as dirty
relative to DE 05c6f67; all recorded input byte hashes were verified to match
the source files subsequently committed in 3ac14b2.

| Property executable | SHA256 |
| --- | --- |
| karyo-macos-window-properties-probe |78e2cbe414ee8e6ce2aa229f98e9b827c277e9865176fccaa9e9692d1679e44c|
| karyo-macos-menu-view-probe |bd4cd35c31281071e3a7fc8a693b9bb217c2bc5c5de36d41c6656bcf7e89f70f|

Both property binaries execute through karyo-macos on the installed48 native
Debian and Ubuntu engines. Each JSON report has passed:true, both exit 0, and
the owning QA worker reports no timeout or forced cleanup. The window report
confirms automatic/opaque defaults, independent values and reset. The menu
report confirms default nil, caller-release retention, self-assignment,
copied ownership, clearing and exact final release.

The reports explicitly leave native tab groups, transparent compositor frames
and custom menu-view rendering unaccepted. No windows are shown by these
clients, so they are not GUI screenshot evidence. The actual UGENE interface
and layer-backed drawing remain separate checks.

Compile manifests remain immutable with runtime_tested:false. Actual execution
is proven separately by out/migration/public-cocoa-properties48/base.json,
including original source hashes, SDK identity, binary hashes, commands,
installed patch count and observed JSON reports. The default application
regression build is compilation/archive acceptance, not a fresh GUI claim.
Shared policy/security test suites are not executed.
