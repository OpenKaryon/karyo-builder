# System colors during initialization of the original dynamic Qt client

The official Intel macOS UGENE53.1 distribution remains unaccepted as an
application. Its unchanged Qt5.15.10 frameworks expose an AppKit lifetime bug
on both installed45 runtimes. The ordinary external application attempt on
Ubuntu exits without a window; the Debian attempt remains without a window
until its45-second observation deadline. Neither is counted as a GUI pass.

Temporarily disabling UGENE's own crash handler with its upstream diagnostic
option exposes an NSException about an O2Color receiver where an NSColor is
expected. This option was used only for diagnosis, never installed as a product
setting. Reading the original GUI/CLI entry points and Mac style factory found
no application implementation of the failing system-color conversion.

A minimal original client linked to the exact bundled QtCore/QtGui/QtWidgets
frameworks reproduces failure during QApplication construction on both bases.
Their SHA256 values are:

| Framework | SHA256 |
| --- | --- |
| QtCore |428d39fdd8cca929579cbcfce55732e941144423ca12b880938b17454175ec44|
| QtGui |177efc1c1bf6ddb74774485be1c5f5f7977c6902ad5cb849974f16b63e4ea904|
| QtWidgets |942803f5748b0b255aeb94c4de321daaea3a531c0378329f24bcf9f89f45cc28|

The runtime reports Qt5.15.10. Its original platform plugin is used as well.
No UGENE executable, framework, plugin or source code is modified.

A temporary method tracer in that separate client observes valid
NSColor_catalog/NSColor_CGColor pairs during system palette construction.
When widget-role palettes initialize later, controlTextColor's stored backing
pointer instead identifies a CFString. The captured stack passes through
qt_mac_toQColor, the Cocoa plugin and
QApplicationPrivate::initializeWidgetPalettesFromTheme. Storage has been reused
after the autoreleased system-color proxy was released. The different O2Color
and CFString exception receivers reflect the reused storage, not a valid
CoreGraphics-to-AppKit color conversion.

Two narrower ordinary clients pass: direct access/conversion of ten system
colors, and capture/conversion of three system colors initialized before main.
Neither proves survival across the plugin's temporary autorelease-pool cleanup.
A separate temporary uncaught-exception helper did not produce a useful stack;
its retained attempts are diagnostic failures, not acceptance evidence.

The proposed common fix keeps shared System catalog proxies in a synchronized
cache while preserving custom catalogs and explicit fallback-color creation.
An executable-only factory prototype allows the same actual dynamic Qt client
to construct QApplication and QLabel and exit0 on **both** native bases.
The prototype binary SHA256 is
1ac0670e6a03c5778d500a88a9092f6c25f762b7f3df74a163e38834a116b588.
This demonstrates the proposed lifetime mechanism; it is not installed46
acceptance, a visible Qt window test, or acceptance of the full UGENE UI.

DE patch0046 implements that common cache in the existing catalog source file.
Its SHA256 is278438fa2bdbb905c7700acace7955b07bdfbe16dcaa9972bd9a0bea75756229.
Source-only application and pristine reversal of all46 patches pass on both
SDKs, restoring84 original files without running the shared unit suites.
Installed shared-library acceptance still requires a complete native build.
The existing X11 system palette remains the source of colors; broader dynamic
appearance and color-management compatibility are not claimed by this fix.

With a temporary common cache, the unchanged UGENE progresses to its own
initialization and then encounters missing NSWindow tabbingMode and titlebar
preference methods. A further window/menu prototype records only an opaque
titlebar request and nil NSMenuItem.view assignments, and reaches startup plugin
loading. It still exits1 without a captured window, so this is diagnostic
progress rather than acceptance of the full application. The additional APIs
require their own general implementation and validation.

Ordinary diagnostics/prototype logs are retained in out/migration/ugene-macos:
ubuntu45-no-handler-v1.log, ubuntu45-qt-palette-trace-v1.log,
ubuntu45-system-color-cache-prototype-v1.log,
debian45-dynamic-qt-v1.log and debian45-system-color-cache-prototype-v1.log.
The verified original DMG/bundle receipts remain separate from these clients.
Shared policy/security suites are not executed in this work.

Primary client code consulted without copying Qt code into the runtime patch:
https://raw.githubusercontent.com/qt/qtbase/5.15/src/plugins/platforms/cocoa/qcocoatheme.mm
https://raw.githubusercontent.com/qt/qtbase/5.15/src/gui/painting/qcoregraphics.mm
