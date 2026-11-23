# Common Cocoa compatibility work after the installed45 milestone

The independent Debian and Ubuntu installed45 receipts remain the accepted
runtime baseline. Both pass the original Cocoa and Qt clients, the actual
reviewed text raster, bounded original event/run-loop waits, ordinary upstream
TextEditor editing/save/quit, and preservation of the original53-byte Mac
fixture across a normal restart of its own persistent server. The original
Debian stock-utility run still contains a cold-prefix uname exit136. Warm and
one fresh-prefix rechecks pass, but its cause is unresolved and the first
failure must remain visible.

DE commits 7033fe7, c2c2b8b and b774608 add three common changes:

* Patch0046 keeps shared System catalog colors resident across temporary
  autorelease pools during platform-plugin initialization. Custom catalogs and
  explicit fallback-color construction retain their existing behavior.
* Patch0047 stores independent optional window tabbing and titlebar preferences.
  It does not implement tab groups or transparent compositor decorations.
* Patch0048 supplies nil-default NSMenuItem.view storage with retained
  assignment, independent copied ownership and final release. Embedded custom
  view rendering, event delivery and keyed archiving remain separate work.

These changes contain no application-name tests or per-application settings.
Their ordinary temporary prototypes pass on both installed45 bases, including
QApplication construction with the unchanged UGENE Qt5.15.10 frameworks, window
property independence/reset, and menu-view assignment/copy/final-release
ownership. Prototype success is not installed shared-library acceptance.

The complete48-patch input at DE
b7746080c5e370642a568d0ce6968490548f3a2f passes source preparation on both pinned
SDKs. Git and zero-fuzz quilt application/reversal restore all86 original
files; the 44 Swift preparation patches remain unchanged. The recorded source
closure contains 161 modules and 292917 archive members. Shared policy/security
unit suites are not executed. Full native builds and installed48 application
checks are queued separately, Ubuntu first and then Debian, with one full
engine build at a time. No successful installed48 result is claimed here.

## The official macOS UGENE application remains unaccepted

The unchanged official Intel UGENE53.1 DMG has SHA256
460a194a25e351d477891de812bab820231655778d7572e6b9fe343946c79ef6.
The original ugeneui executable and bundled frameworks/plugins are preserved.
No UGENE profile, diagnostic environment option or temporary helper is added
to the product launcher. The original installed48 attempt uses the ordinary
launcher and is separate from the following temporary diagnosis on45.

Common system-color and optional window/menu prototypes advance the original
application to startup-plugin loading, but it still exits without an accepted
window. Repeating that diagnostic with stdout/stderr directed to an ordinary
file exposes a lazy binding failure for CGColorSpaceCopyPropertyList in the
original libqcocoa.dylib. The complete regular-file output is 35834 bytes,
SHA256 ea4066a5cb88ce14523cc55dd42f3367abfb36e97934e1559e649d2a58af2cfd.
Its previous pipe-captured tail ended in the middle of a task-registration
message, before this diagnostic was visible.

The [Apple API](https://developer.apple.com/documentation/coregraphics/cgcolorspace/copypropertylist())
returns an optional property-list representation. The
[original Qt IOSurface caller](https://github.com/qt/qtbase/blob/5.15/src/plugins/platforms/cocoa/qiosurfacegraphicsbuffer.mm)
uses that representation as surface color-space metadata. This is a general
graphics API gap, not an application-specific project-loading error.

A temporary helper exposing the missing function and returning no
representation does not establish a fix: the subsequent original application
attempt still exits 1, and its retained log does not confirm that function was
actually called. That combined helper must not be promoted into the product
runtime or counted as color-space serialization, IOSurface rendering or full
UGENE compatibility. A later actual framework export requires its own review
and installed checks, as recorded in the [bioinformatics report](VALIDATION_MACOS_BIOINFORMATICS.md).
The additional `Unsupported assertion type` text comes from the pinned iokitd
power-assertion implementation returning KERN_INVALID_ARGUMENT; that text
alone is not proof of the application's fatal cause.

The diagnostic helper SHA256 is
6975e951e976d2dc9a0b145bba19951ee95c7297e9ea57add4535ec012159f69.
The second complete regular-file output is 35968 bytes, SHA256
b2e82230e00ba18f64eae14af1f6eab23c4da4e37f23d08131c895d445a57f68.
Both attempts are diagnostic failures retained in out/migration/ugene-macos,
not GUI passes. The next gate is the original application on the actual
installed48 libraries, followed by diagnosis of its observed graphics path.

Only completed, provenance-identified QA prefixes were shut down before these
checks to free VM memory. No prefix files were deleted, and the persistent
data fixture was excluded. User VMs, hardware sessions, Forge, distribution
sources and ISO outputs were not modified. All product commits remain local.
