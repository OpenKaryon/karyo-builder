# Installed52 Ubuntu evidence and the remaining single-service query

The complete52 engine built successfully on native Ubuntu26.04 and was explicitly
reinstalled into the separate ordinary QA VM. Its source bundle records DE
`7d13ab5a287fea7e2b0e820c0103a0c14214a791`; the later ordinary-argument actor comes
from `7d577875eab4c337debbd54128c3fa158343a90b`. No user VM or Acer was changed.
The already queued Debian52 full build is still running; this report does not
extend Ubuntu's results to that base.

All four native artifacts were checked by size and SHA256 before installation.
The runtime is92705884 bytes, SHA256
`e0badbefed5979c09399a4f11c6138065dcba1cd0147ddc55cbaf7705893cf2a`.
The debug package is3697708 bytes, SHA256
`454b8cacfedb3ca6860afcb76fd699ae4cafc54f623973c99885f6ea26572cbc`.
The buildinfo and changes hashes are respectively
`e4ffd3da32ab41ce14281a2fe20574690e88a790bd34f1e2d15ef9dc2a7f08d5`
and `dd98f3ad77af6742c6b1b589c916aa18005f6a71f627898177189973fbf98fac`.
Account/PAM/display-manager and previously installed package versions remain
unchanged. Actual provenance distinguishes these development packages with the
same version string; a version comparison alone would not prove the upgrade.

## Ordinary application results

The actual loader, Cocoa and static Qt clients pass, including ordinary words,
UTF-8 and a spaced filename. No literal command-transport or policy-denial cases
run in this profile. Cocoa reports79 event iterations; Qt reports working text,
button signal and raster rendering. The two actual compositor frames were
exported, hash-checked and viewed, showing their labels and buttons:

| Frame | SHA256 |
| --- | --- |
| Cocoa |3ed858e7da48bcbeccce1caa0e7992b562cb1ece080252184273addeb26b30fc|
| Qt Widgets |2a0c1cbf444d28fd92ca4a6df621a7c64fc6ba7f2262ad4bb629ae15d30e09c4|
| TextEditor opened document |f3adc3fecf47007a77207f76d1cc2a127cb8e6e1fc38f9ff1010b5d57d1ec22e|
| TextEditor edited document |f156a14babbc6ad9dc0694286457c7a9eb0ae52a9167e4066a9148145e9cafb6|

The four stock utility operations pass. Original TextEditor opens the ordinary
document in a captured window. Its separate keyboard scenario saves the exact
45-byte edited text, exits through normal global Quit, and needs no cleanup.
Both editor frames were exported, hash-checked and viewed, showing the original
and edited text. The document-only bounded observation uses controlled termination and
must not be confused with the normal Quit result.

NSEvent waits are0.051216/0.051239/0.050730 seconds. The CF window loop returns4
for two early handled sources, then3 after0.050568/0.051361 seconds. A separate
aggregate must retain the distinction between source handling and a timeout.
The original53-byte Mac data file is read after its own prefix server changes
23927 to28194, preserving prefix identity. Original Mac MUSCLE5.3 again performs
real FASTA alignment with its default two threads after its own prefix restart,
25636 to29844. The shared ordinary Cocoa APIs and unchanged dynamic Qt framework
client also pass. None of these results establishes layer-backed UGENE drawing.

## Failed layer boundary, retained rather than accepted

The clean public buffer client now gets past layout, but exits1 at creation with
`Cannot obtain IOSurfaceRoot!`. It does not reach the cross-process lifecycle or
two-color layer client. The ordinary dynamic Qt layer client also exits1 without
a frame. These are actual ordinary application failures, without timeout or
leftover-process cleanup in the public-buffer worker.

Original UGENE remains alive until the45-second observation bound and creates
viewable X11 objects. The saved compositor frame
`44431b6bf5ee9fc26055ce2725e186d20783a29eb1bcccb417dc0162a039c42e`
was exported and viewed: it shows the desktop with no UGENE content. X11 viewable
metadata alone therefore does not prove a visible application window. Its worker
ends with controlled termination; the FASTA workflow and GUI remain unaccepted.

A new ordinary public client asks for the same IOSurfaceRoot service twice,
using enumeration and direct single lookup. On installed52 enumeration returns
the real expected class, while single lookup returns no object. Both calls use
their own consumed matching dictionary and release acquired ports. This narrows
the failure to the unsupported single-result binary RPC in iokitd, rather than
absence of the registered service.

Common0053 implements that RPC through the existing registry iterator and removes
the redundant dictionary release in the IOSurface initializer. Its three changed
units compile with Clang19 and21 against actual generated MIG headers. The initial
closure export ran before the ongoing build had generated a header; the corrected
export generated it with the exact upstream command in a separate temporary
directory. A subsequent archive-directory assertion was also retained and fixed.
The complete53 stack subsequently passes Git/quilt zero-fuzz apply/reverse on
both bases, restoring105 files, with `unit_tests_executed:false`. The first
source attempt retained an incomplete explicit file-kind list; the corrected
check adds only the exact reviewed ServiceRegistry.mm path. These source checks
do not prove a linked or installed53 runtime. DE commit268d372 contains the
common fix and the ordinary matching client; Builder now expects all four
public IOSurface-suite executables.

Current receipts are under `out/migration`: `darling-kernel-ubuntu52-*`,
`upstream-texteditor/ubuntu52*`, `runloop-installed52-v2-*`, `ugene-macos/ubuntu52-v2`,
`dynamic-qt-layer/ubuntu52-v1`, `public-iosurface52/ubuntu` and `iokit-single52/ubuntu`.
Source/client inputs and exported images retain separate hashes and dirty-state
records. Only ordinary functional and source checks ran. No shared/security suite,
push, Forge/distro/ISO/donor modification or host computer use is involved.
