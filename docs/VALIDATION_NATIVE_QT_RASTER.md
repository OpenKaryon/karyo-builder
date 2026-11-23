# Native Qt raster output and the common43-patch follow-up

The explicit Qt diagnostic prototype now exits0 and produces a nonnull460x194
widget image plus a real saved PNG on both Debian and Ubuntu kernels. Its
reports confirm visible state, button signal, UTF-8 text state and raster output.
Both whole-desktop frames and the saved widget PNGs are exported and reviewed.
The PNG bytes match across both systems:
a043c436661c41667bf846c902634e4fe52841306c83a161ca8f87ad207b4325.

This is a diagnostic application with explicitly compiled proposed methods and
functions. It is not the unchanged sample running against the installed common
corrections. The installed engines are still35; complete43 builds and ordinary
unchanged application checks remain required. Visible glyph/spacing defects
are retained as an open observation. A passing raster report does not establish
complete visual quality, keyboard/menu interaction or a document edit/save flow.

## Corrections supported by actual observations

The first backing-size implementation forwarded a signed window-space vector.
On the flipped QNSView this produced widget DPR -1 and a null0x0 image. Patch0039
uses lengths of the local axes instead, retaining bounds scale and its inverse.
Ordinary/flipped views at1x/2x pass on both kernels. The attempted rotation setter
is unimplemented, so its duplicate cases are not evidence of rotation support.

Actual screen diagnostics show valid backend IDs but an empty device dictionary,
depth0 and no backing-scale selector. Patch0040 exposes NSScreenNumber and the
current8-bit RGB/1x backing metadata, including a consistent no-RandR ID. Ubuntu
also reports a1280x800 display and an inactive0x0 output as equally online.
Patch0041 filters online enumeration and membership by real geometry while
preserving backend IDs, primary order and the ordinary count-query contract.

With those corrections the original PNG operation reaches a missing
CGImageSourceCopyTypeIdentifiers symbol. Patch0042 exports a list of decoder
classes actually present and implements the existing destination capability
query for TIFF/PNG and conditionally JPEG. Arrays follow Copy ownership; stubbed
BMP/GIF/JPEG2000 encoder branches are not advertised. PNG prototype output is
accepted; broader codecs and installed symbol behavior remain separate gates.

Qt also calls the stubbed font-family enumeration API. Patch0043 uses the
existing real CoreText collection/descriptor backend without an AppKit dependency
or forced font. The prototypes enumerate200 Debian and198 Ubuntu families and
resolve Noto Sans. Their widget PNG remains identical, so this does not fix the
observed glyph quality. The family counts describe those actual QA environments.

## Complete builds and ordinary application checks

Source-only43 preparation passes on both SDKs:43 Git/quilt forward and reverse
patches, zero fuzz,83 pristine files restored,44 fixed Swift inputs and
unit_tests_executed:false. The bundle is recorded in
out/migration/darling-functional-graphics-inputs.json. Only the explicit pinned
NSScreen source/header and ImageIO source/header expand the allowed file list;
other changes remain inside existing framework directories.

Both35 engines finish successfully. Debian35 CLI/Cocoa reports and the real Cocoa
frame pass; its four stock utilities pass. Ubuntu35 Cocoa is likewise displayed
and defaults persistence passes, while uname/echo retain strict failures because
EGL diagnostics pollute stdout. Qt35 on both still lacks the new backing API.
The unchanged editor35 opens a blank document; the prior type-fallback prototype
displays actual file contents on both. No broader acceptance is inferred.

Eight waiting38 controllers were intentionally replaced before a full38 build
started, after discovering the flipped-axis error. No running engine was killed.
New complete43 engines run serially Ubuntu then Debian; matching ordinary
CLI/Cocoa/Qt, stock utility and unchanged editor NSOpen checks wait for each
build. No security suites, push, Forge/distro changes or user working VM actions
occur. Evidence:out/migration/darling-native-qt-functional43-evidence.json.
The broad DE/Builder migration and full installed graphical acceptance remain open.
