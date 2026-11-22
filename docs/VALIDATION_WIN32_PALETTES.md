# Real Wine owned-palette acceptance

This closes the explicit mapped 1x1 framework-owner palette/minimize gate on
native Debian 13 and Ubuntu 26.04. It does not declare the full DE migration or
all Windows applications complete. Forge, donor repositories and user VMs were
not changed. Every commit remains local; no push, fetch or ISO rebuild was run.

## Captured native stacks

| Base | Compositor | Native wlroots | Wine runtime |
| --- | --- | --- | --- |
| Debian 13 | 0.8.3-1+karyo4 | 0.18.2-3+karyo1 | 10.0~repack-6+karyo1, matching amd64+i386 |
| Ubuntu 26.04 | 0.9.3-1+karyo3 | 0.19.2-1+karyo1 | 10.0~repack-12ubuntu1+karyo1, native WoW64 |

The own installed Win32 launcher still comes from source e782fb0. Later commits
add native recipes, compositor corrections, fixtures and evidence; they are not
misrepresented as a new joined installation of every current DE component.

Final Debian labwc DEB SHA256:
72a6eae48026d96c9890cefd45434f11f736fbaffdff833c10461f87a45819ca.
Final Debian libwlroots DEB SHA256:
e4c631b2240e273c81c1ae4f37b2a4dcb04c22a692c94446278723d0d6524b01.
Ubuntu retains labwc DEB SHA256:
97f6d56a2d244d56aca289c5c0caf004da1137def9ced352c5ca544e65fae041.
Final Ubuntu libwlroots DEB SHA256:
6c4bdeb58205765c82d93e5097c3c95b9680dc12062f76bae0f5f543b3dcd43f.

## Actual producer and observations

The original GPL-3.0-or-later Win32 fixture is compiled with both native MinGW
compilers, strict warnings and a real PE32/PE64 header check. It creates a main
frame, four distinct colored owned tool palettes (two delayed), one 1x1
no-activate owner and an ordinary independent frame. No RomArtist binary or
other proprietary program, personal prefix, authentication or registry rule is
used. Each case is a new ordinary-user home/prefix and private D-Bus,
labwc/Xwayland display, temporary runtime and software-rendered headless output.
The system root is read-only, with no network or capabilities.

The actor verifies actual matching positive PID/class and all real shared
WM_TRANSIENT_FOR owners. It waits for compositor-published X11 clients and actual
main-window paint, rather than mistaking an XSync acknowledgement for completion
of the compositor's event loop. Captured pixel colors establish that each late
palette stays above its main frame, an unrelated frame may obscure the group,
and returning the main frame restores every palette. Scene minimization hides
the group while every real X11 handle remains NormalState and the process stays
alive. Restoring retains owners and colors. Normal close uses WM_DELETE_WINDOW.

Root focus notifications must settle for a bounded quiet interval before and
after the scene operations. A separate real X11 process supplies the negative
focus probe. First a private Wayland virtual pointer clicks the visible Wine
client and the actor waits for actual Wine input focus. Only then does the
other process attempt an unsolicited XSetInputFocus; input must return to a
Wine frame/palette. This is a component regression check, not a claim that X11
is a security sandbox. A globally active client may reject a programmatic focus
offer, so an unacknowledged EWMH request is not used as the test's precondition.

## Native defects and completed corrections

Debian's previous group patch bypassed the raise cache unconditionally. The
native cache is restored and invalidated when a view maps, retaining late tools
without repeated focus-generating restacks. The final five-layout model passes.

Both wlroots releases could receive a Wayland buffer before the X11 serial
associated that surface. Their association installed a commit listener but did
not process an already-current buffer. Protocol traces show the ordering. The
fix invokes the existing role-owned commit handler after association/listener
setup. Null-buffer surfaces stay unmapped. No compositor code forces role maps.

Debian additionally acknowledges accepted same-positive-PID FocusIn transitions
without another WM_TAKE_FOCUS and ignores stale notifications. The foreign-PID
denial path remains. This follows the newer native XWM focus-state approach
without exported ABI or public struct changes. Ubuntu needed no new labwc restack
patch; the exploratory Ubuntu karyo4 packages remain ignored, unaccepted output.

Native source builds preserve distribution packaging, dependency checks and
Werror. Ubuntu-only compatibility handles an unrepresentable new libinput
switch without a false lid event and keeps a C23 strchr result const-correct.
wlroots derivatives retain its MIT notices; labwc patches retain GPL-2.0-only.
Upstream wlroots dh_auto_test reports no defined tests and is not claimed as a
unit-test pass. Separate comparisons confirm unchanged SONAME and all 769/823
native defined dynamic symbols on Debian/Ubuntu respectively.

## Reproduction and retained results

Use tests/acceptance/check-win32-palettes.py with --source, a successful
--runtime-acceptance directory, matching --compositor-package and
--wlroots-package native source-package outputs, and a new --output directory.
--bits 32 64 and --repeats 2 are the normal matrix; --owner mapped is explicit.
The driver captures immutable runtime images, verifies native metadata, SHA256
and OS release before installation, freezes actors/C input and uses one fresh
container per case. It preserves failed cases; --baseline writes baseline.json
rather than a positive acceptance receipt.

Local final evidence: wine-palettes-final-debian-v5 (both bitnesses),
wine-palettes-final-ubuntu-v6 (both bitnesses, twice), plus the earlier successful
four-case Debian v3 and eight-case Ubuntu v3 runtime matrix. Final actors include
the real-click precondition and cross-process probe, and their SHA256 matches
the committed actor. wlroots-native-regression-v1 additionally runs frozen X11
five-layout/late-tool models and normal/startup-lock protocol scenarios against
both installed native stacks. wlroots-native-abi-v1.json retains symbol/SONAME
comparisons. All original failed experiments remain at their original paths.
Builder's existing 50-test suite passes without skips in both native
karyo-source-tests SDKs. Windows runs 48 checks and skips two native-symlink
fixtures, which the Linux runs cover. Initial attempts in minimal build SDKs
lacked Git for four tests; those environment failures remain preserved and no
unit-test assertion was changed to obtain the native pass.

Initial fixture failures used an unsupported EWMH close request and a WM_HINTS
access typo. A proposed late-map labwc fix checked mapped rather than an existing
buffer and did not address the actual role race; it was not promoted. Later
focus-probe failures demonstrated why input-focus acknowledgement/real click is
required before attributing a failed test to focus-denial behavior.

## Remaining boundaries

At this checkpoint a truly unmapped owner was still exploratory. The subsequent
paired native metadata refresh now accepts that layout separately; see
[unmapped-owner validation](VALIDATION_WIN32_UNMAPPED_OWNERS.md) for current native
versions, stricter negative cases and exact artifacts. The historical packages
in this report remain the mapped-only checkpoint, not the new runtime pair.
Legacy prefix import, existing-user upgrade, real third-party application
acceptance, full taskbar association and Windows-like parent/child caption,
close-button and corner styling remain separate Wine migration gates. Darling,
remaining VMware host channels/resize and VPN lifecycle also remain open in the
full migration plan. No hardware/GPU, host clipboard/DnD or ordinary user session
was exercised by these container-only checks.
