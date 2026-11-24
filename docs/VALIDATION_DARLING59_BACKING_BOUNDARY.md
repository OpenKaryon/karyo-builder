# Installed Ubuntu59 backing-layer boundary

The complete Ubuntu engine from DE `2ce0031` builds and installs successfully.
All four artifact sizes and SHA256 values are independently checked. Ordinary
Cocoa/static Qt windows have reviewed actual text/buttons. Public IOSurface
matching/storage/lifetime and hosted-root red/cyan pixels pass. Nested painter
order shows blue grandchild, flattened blue and later yellow sibling. All nine
ordinary baseline/root/tree/backing frames are exported, hashed and viewed.

Implicit backing presentation remains a real failure: both frames are gray
`237,237,237`. The program nevertheless reports the correct inherited return
lengths `32/16/4`, one public setter, one makeBackingLayer call, three delegate
display calls and zero drawRect calls. Direct/coalesced/repeated display demand
also passes. Patch0059 fixes its observed signature contract; it does not alone
fix visible backing presentation. A successful callback report is insufficient.

## Initialization-order diagnosis

Separate ordinary clients preserve the backing-view scenario and inspect its
geometry. Public getters and KVC both report bounds/frame `340x180`, position
and anchor `0,0`, opacity1 and no active animations. A read-only Objective-C
object-ivar observer sees the same live view/layer context, its root equal to
the backing layer and texture1, but **no native subwindow**.

Moving only ordinary window realization before layer configuration yields a
native subwindow and actual red/cyan pixels, also exported, hashed and viewed.
That diagnostic retains the original zero-draw assertion, which now includes
one legitimate pre-layer draw; its whole program result remains a failure.
It is causal initialization-order evidence, not original UGENE acceptance.
The first private-KVC observer attempt also failed separately; its corrected
read-only object-ivar observer is recorded without overwriting the first run.

NSWindow's child-creation method sends directly to `_platformWindow` before its
lazy creation. General patch0060 uses the existing private lazy backend accessor.
The exact changed method expression compiles with Debian Clang19 and Ubuntu
Clang21. A full NSWindow translation-unit attempt lacks NSColorSpace.h in the
reduced saved closure, so that attempt is not accepted as a native unit compile.
Full-stack application/reversal and installed60 checks remain separate gates.
The unchanged before-order-front backing probe remains the runtime acceptance.

## Queue and evidence limits

The Ubuntu59 targeted gate ends with stage statuses `0,0,0,1`. It prevents the
next Debian full engine and further editor/dynamic-Qt/original-UGENE attempts.
The exact captured Debian waiting child is stopped before staging; its parent
and GUI guard finish normally through their existing failure paths. All six59
controllers are terminal. Debian59 is neither built nor installed.

Evidence is `out/migration/native59-ubuntu-backing-boundary-evidence-v1.json`,
SHA256 `f4f4f85cc62a1070ac0ce1222d7e0969645e95e0ef4692979000badc70638c75`.
Full native artifacts are in the own QA `darling-native-ubuntu/` folder
`karyo-source-package-20261124T021428Z-bc7469be`; their manifest records exact
source, images, patches, native package dependencies and output hashes.

Original unchanged UGENE53.1 still has no accepted GUI. Its earlier56 black
windows on both bases remain recorded separately. A source/compiler success or
realized-order diagnostic does not replace original-application acceptance.
Work remains local, without push, shared/security suites, Forge, distro, donor,
user VM or Acer changes. The whole DE/Builder migration remains active.
