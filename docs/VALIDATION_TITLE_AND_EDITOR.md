# Native title encoding and upstream TextEditor observations

## General title correction

The same compiled Mac Foundation diagnostic runs normally on both QA guests:
Debian34 and Ubuntu32. UTF8String returns the complete `Karyo Cocoa — Привет`
title, while legacy cString returns an empty string. The default encoding reports
UTF-8 on both systems; replacing the call with a locale guess is insufficient.
The previously reviewed Debian Cocoa frame independently shows a blank caption.

DE b37a989 adds patch0036 in the common pinned X11Window backend. It publishes
_NET_WM_NAME with type UTF8_STRING and maintains the legacy WM_NAME through a
checked ICCCM conversion whose allocated storage is freed. There are no app
rules, injected titles or changes to the Cocoa sample. Source-only preparation
passes on both SDKs:36 Git/quilt forward-and-reverse patches, zero fuzz,76 pristine
files restored and44 fixed Swift files. Unit suites are not executed.

The36 source bundle is recorded in out/migration/darling-utf8-title-inputs.json.
The installed title correction is still pending complete builds and real window
property/display checks. Existing35 builds continue unchanged; source preparation
does not silently replace their inputs or constitute a graphical runtime pass.

## Actual unchanged upstream editor window

The pinned Cocotron TextEditor bundle does create a real visible native window
on Debian34. Its X11 name is `Untitled 1 - Text Editor`, class TextEditor twice,
geometry489x623+395+77. The saved whole-desktop1280x800 frame is visually reviewed:
caption, menu bar, white document area and scrollbar are present on Karyo.
Frame SHA256:ac5c80859f876cdba033b9bafeb58420a19a4d7fba7bef9589624fc4b04a679a.

This corrects the earlier inference that no editor window appeared. The observer
was looking for the provided document fixture name and deliberately accepts its
class fallback only for unnamed windows. It therefore missed the named untitled
window; do not broaden that observer into accepting arbitrary unrelated windows.

A separate instrumented diagnostic copy reports main-bundle/principal/nib data
and completes launch with one MyDocument and one window. That diagnostic changes
main.m and is not represented as the unchanged upstream application. The viewed
frame comes from the original unchanged bundle. All fixture closes target only
the captured own application process through its recorded PID/start identity.

Passing a plain document path still opens the empty untitled document, and a
standard NSOpen attempt also retains that title. Document delivery and actual
edit/save interaction remain open. An alive process, visible blank editor or
controlled launch timeout is not a complete document-workflow acceptance.

Evidence:out/migration/darling-title-and-editor-evidence.json; native logs in
out/migration/title-encoding-functional and out/migration/upstream-texteditor.
Host artifacts reside in the C task output/title-encoding-functional and
texteditor34-display-diagnostic-v2 directories. Only ordinary functional and
source-only checks run; security suites are not run. Commits remain local.
