# Actual Cocoa display and stock preferences on Debian34

The complete34-patch engine builds and installs on the normal Debian QA guest.
The real Mac Cocoa application now produces its successful report: visible
window, button action and native event-loop iterations. Real CLI arguments,
UTF-8 file I/O and exit17 retain their existing passing behavior. The packaged
upstream uname, echo, defaults write and defaults read all pass; this accepts the
installed Foundation persistent-domain correction on Debian, beyond its earlier
standalone proposed-method checks.

## Actual displayed frame

The original observer searches for the expected window title and records no
frame. A separate ordinary Cocoa run captures the real Wayland desktop and X11
tree. The unique KaryoCocoaProbe client is mapped at460x246+410+266 but has no
WM_NAME. Visual inspection of the saved1280x800 frame confirms the actual Cocoa
window, readable Cyrillic label and button on Karyo. Its caption is blank. This
is genuine displayed output; it does not establish correct title publication.

Frame SHA256: e1653f57e08b4e76c63e5cf30b257d8fdb2985fb8709f736a4758345063df4c8.
Local artifact: C task output/cocoa34-display-diagnostic/frame-8.png, alongside
the X11 tree and original result. The untracked ordinary actor now permits an
unambiguously visible matching WM_CLASS when the name is absent, recording
title_missing and separating expected/observed title metadata. Its35 installer
recognizes the previous32/34 actor hashes. No arbitrary window is accepted and
visual review remains separate from the application's self-report.

## Shared Qt follow-up and remaining editor issue

The independent Qt run still fails with the actual setRestorable: selector
exception. DEfbeaaf1 adds general NSWindow isRestorable/setRestorable: methods.
The existing Mac SDK's NSWindowRestoration header defines titled windows as
restorable by default and untitled windows otherwise; explicit assignments are
stored separately. This implements that flag, not automatic window restoration.

Source-only35 preparation passes on both SDKs:44 Swift inputs,35 Git and zero-fuzz
quilt forward/reverse patches,76 pristine files restored, unit_tests_executed:false.
The source bundle is recorded in darling-restorable-inputs.json. Complete35 builds
run serially Ubuntu then Debian after the completed Debian34 engine. Real35
Cocoa/Qt/stock/editor checks remain pending; source success is not a native pass.

The unchanged upstream TextEditor no longer emits the prior longjmp failure on
Debian34, but no visible editor window is accepted. It remains alive until its
controlled25-second fixture close, including the repeat with WM_CLASS fallback.
Investigate bundle/nib/document startup with actual observations rather than
treating an alive process as a usable editor. Caption publication and slow Cocoa
completion are also open observations. Full graphical compatibility on both
bases remains incomplete. Only ordinary functional/source checks run, and all
commits remain local without a push.
