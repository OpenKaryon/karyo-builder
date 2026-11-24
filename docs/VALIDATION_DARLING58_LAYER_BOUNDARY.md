# Installed Ubuntu58 layer fixes and remaining backing ABI failure

The full58-patch Ubuntu26.04 native engine builds successfully and is installed
in the own older Darling QA guest. All four artifacts are independently checked
against their manifest size/SHA256. The source is immutable DE396312d, before
later documentation-only HEAD changes. Debian remains installed56: its next full
build deliberately waits for successful installed Ubuntu graphics checks.

## Accepted installed slices

The ordinary baseline passes. Actual Cocoa and static Qt UTF-8 text/buttons
are captured, exported, hashed and viewed. Public IOSurface matching, CPU buffer,
owner/reader/after-release lifecycle, root surface redraw/preservation and release
checks pass. Actual root center pixels are red[224,64,32] then cyan[32,176,192];
both frames are viewed.

The ordinary nested-layer client now displays its blue grandchild at unchanged
visible coordinates, displays the same blue surface after flattening, then
correctly overlays it with a later yellow sibling. All three exact center pixels
match blue[32,96,224], blue[32,96,224], yellow[224,192,32]. The program and its
owned cleanup pass, and all three actual frames are exported, hashed and viewed.
This accepts the tested2D painter-order fix, not arbitrary3D layer behavior.

The first tree export stopped on a QA whitelist typo: a series-number replacement
changed the digit alphabet0123456789 to0123458789. The ordinary client had already
finished successfully. Future controllers are corrected and the existing log/
frames are exported by a separate versioned exporter, without relaunching it.
The failed exporter log remains separate from the recovered pixel result.

## Actual remaining failure

The implicit backing-view client now sees one public setLayer call, one
makeBackingLayer call, three displayLayer calls and zero drawRect calls.
Direct/coalesced/repeated display-demand checks pass and the original IOSurface
remains its contents. Its actual two frames, however, remain light gray
[237,237,237] instead of the requested red/cyan. Both are viewed. Successful
callbacks are therefore not promoted to successful backing presentation.

A separate positive public-signature observation reproduces return-length0
for each inherited bounds, position and opacity getter on the actual backing
layer. These methods need CGRect, CGPoint and float return ABIs. The backing
subclass unconditionally supplied a void signature, while the renderer obtains
these values through NSInvocation. This motivates the common0059 superclass-
signature fix. Its source/compiler and future installed result remain distinct
from the observed58 runtime; no runtime library or application was replaced to
make this diagnostic pass.

The failed backing pixels stop the automatic gate. No Debian58 engine is built,
and neither base runs the queued58 editor/dynamic-Qt/original-UGENE retries.
The obsolete waiting Debian installer child is stopped only after its exact
PID/start relationship/arguments and absence of any Debian58 build/install are
verified; its parent and regression queue exit through their existing guards.
These orchestration exits are not additional Debian application failures.

## Evidence and limits

The local hashed index is
out/migration/native58-ubuntu-layer-boundary-evidence-v1.json. Nine actual frames
are viewed. The original UGENE56 resource-prepared black-window results remain
separate, not a58 application result. The joined Xfce/Karyo chooser guests are
also separate and still run Xfce after their accepted ordinary roundtrip.
No security/shared unit suite, policy weakening, user VM/Acer/Forge/distro change,
Git fetch or push is part of this slice. Full DE migration remains active.
