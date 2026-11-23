# Installed Darling applications on both native bases

Both complete43-patch engines now run the original clean Mach-O loader, Cocoa
bundle and Qt5.15.19 bundle on their native Debian13 and Ubuntu26.04 kernels.
Actual whole-desktop frames have been exported, hash-checked and viewed. The
Cocoa and Qt UTF-8 window titles are correct, both application reports pass,
and the original Qt application saves its real widget PNG. These checks use
installed shared libraries without the executable prototype overrides.

| Native base | Runtime package SHA256 | Bytes |
| --- | --- | --- |
| Debian13 |9edb564d5eabfb50534245af17575228c5b22ee50b7a4c1252f60d959bd5a628|87746440|
| Ubuntu26.04 |2db5e47d3633f3c0b5517e9e70698fa10aa4c7f3e880b237a5579c4682aaf366|92674430|

Both machines preserve protected account/PAM/display-manager configuration and
installed package versions during the runtime reinstall. The development
version alone does not identify the patch set: actual provenance and all native
package artifacts are checked. All four upstream utilities pass exact stdout:
uname, UTF-8 echo, defaults write and defaults read. The launcher stream fix
keeps diagnostics on stderr and in the launch log.

The unchanged upstream Cocotron TextEditor opens its ASCII document through
standard NSOpen on both systems. Both actual document frames were viewed.
Separate ordinary X11 input runs select and replace the text, save exactly45bytes
and exit the native application with code0. The saved-file SHA256 on both is
05786532df55212187f436d1163809d540c98cd0ad30ea1881bfbcbd831bca74.
The quit helper reports1; Debian's retained stderr identifies BadWindow from
X_SendEvent, consistent with the target closing during final key delivery.
The application exit and saved data are checked independently. These are
synthetic ordinary-session events, not physical-keyboard or all-menu coverage.

The ordinary native actor is now committed in DEa097825 after both actual
frame reviews. Its unchanged SHA256 is
febc88686dac09babb3d8f863f43f94b44935d813c87f52e80a536effe26fa33.
It leaves full compatibility and external visual review separate from its
captured-frame metadata. No shared policy or security suites run in this work.

Two common follow-ups remain for the next engine. DE1a87889 bounds the Mach
receive by the existing run-loop deadline; the source-only44 checks and real
50ms Mach-receive helper pass on both kernels. DE66da772 preserves the current
CoreText text origin. An executable-only function prototype on both installed43
systems renders a clear Qt label and button and exits normally. Both PNGs are
byte-identical, SHA256
d90cf2c330b6cb14b737a913f15a4e4430fe7607b7c79394ba77041b4d3347d6,
and both actual frames and rasters have been viewed. This is proposed-function
evidence, not acceptance of installed shared-library fixes.

The combined45 stack passes application and reversal with Git and zero-fuzz
quilt on both SDKs, restores84 pristine files and records no unit-suite run.
Its immutable source bundle records DE66da7724bf2bbf9415c8654ba9e6646650e780a0.
The later actor-only commit does not change that runtime patch input.
The twelve waiting44 controllers were intentionally stopped before any full44
build, with exact process-identity receipts. The combined45 Ubuntu engine is
building, then Debian45 follows; original apps, utilities, unchanged editor,
keyboard/save and original uninstrumented deadline diagnostics are queued.

Installed45 acceptance is pending. Qt glyph quality in the installed43 engine,
windowed event deadlines, transformed/repeated drawing, broader macOS APIs,
multioutput and joined DE lifecycle remain explicit limits. This is a real
application milestone, not arbitrary macOS application compatibility or a
completed distribution. Full joined receipts and reviewed artifact hashes are
in out/migration/darling-native43-both-and-combined45-evidence.json.
