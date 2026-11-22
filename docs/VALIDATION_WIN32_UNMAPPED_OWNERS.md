# Native Win32 unmapped-owner acceptance

This extends the earlier mapped-owner checkpoint. Both native Debian 13 and
Ubuntu 26.04 now pass the fully unmapped 1x1 framework-owner layout with real
PE32 and PE64, while preserving mapped-owner behavior and the existing client
ownership hints. No application-name rule, registry option, proprietary program,
personal prefix or user VM was used. The broader DE migration remains active.

## Actual defect and guarded behavior

The first observation showed a positive native owner PID, 1x1 dimensions and no
decorations, but no cached WM_CLASS or associated surface. A visible-sibling
fallback alone made the real Wine fixture pass; an added explicit-class negative
model then proved that this was insufficient. WM_CLASS could have been set
before the XWM subscribed to PropertyChange events, leaving the cached value
unread rather than genuinely absent. That failed model is retained.

The native wlroots karyo2 patch now refreshes bounded WM_CLASS and Motif hints
when a transient references an unassociated parent. It reuses the existing
parsers, performs two batched property reads at that reference point and does
not put X11 requests in the rendering/stacking loop. A real explicit owner class
is authoritative. Only a classless, tiny, undecorated, unassociated owner with
the same positive PID may borrow its visible sibling's executable class.
Unique-main-frame, fixed-palette and ambiguity guards remain in place.

Labwc's native runtime dependency requires exactly the corresponding wlroots
karyo2 package. This prevents unread stock-library metadata from being treated
as verified missing identity. The native library update and compositor must be
rebuilt/validated together. No public structure, function or SONAME changes are
introduced. Both library symbol comparisons match stock native exports exactly:
769 on Debian 0.18 and 823 on Ubuntu 0.19.

## Exact native packages

| Base | Runtime package | Version | DEB SHA256 |
| --- | --- | --- | --- |
| debian | labwc | 0.8.3-1+karyo5 | `3ca474fb052e7c2489161f4d7610fa6169208d15f78ef06b85d95eb046c41d15` |
| debian | libwlroots-0.18 | 0.18.2-3+karyo2 | `c2e5e84c1d9d28bbcdd10cc198e818774c206fe87a78c999d0157f44ef24b2ef` |
| ubuntu | labwc | 0.9.3-1+karyo4 | `1784611582d02c36192ce2254db1a42a9c38e4846022b0a93062dbb4fd38d790` |
| ubuntu | libwlroots-0.19 | 0.19.2-1+karyo2 | `fde7a2506bdb2cdb7b85b36bd741aa822c28123f0ef605ec24661c6399840712` |

The source outputs are DE out/compositor/<base>/unmapped-owner-paired-packages
for labwc and unmapped-parent-wlroots-packages for the library. Earlier unpaired
or diagnostic outputs are evidence, not the current runtime pair. All source
parts and downstream patches remain checksum-locked. Native compiler Werror,
source packaging and upstream license notices remain unchanged. The libraries
retain MIT; labwc derivatives follow GPL-2.0-only and original packaging notices.
Upstream wlroots still reports no defined tests; real acceptance is separate.

## Native packaging refusal and recovery

Builder's --verify-library-dependency mode starts with a captured earlier native
runtime, not an image which already contains the required library. Before the
positive paired installation, it verifies the compositor's exact Depends and
attempts to install it alone. Dpkg must reject configuration specifically for
the missing library version and leave the target unpacked. It then installs
both verified native DEBs and runs dpkg -V before testing applications.

Both actual negative checks returned status1 for the expected dependency:
Debian 0.18.2-3 to 0.18.2-3+karyo2, Ubuntu 0.19.2-1 to 0.19.2-1+karyo2. The paired
installation/configuration succeeds in the same disposable image. These are
real dpkg operations on the image filesystem, not a verifier which only compares
strings and never exercises the failure path. No system package on the host,
Acer or existing QA/user VM was upgraded by this test.

The native installer is now a separate source file copied into the Docker build
context, with its SHA256 captured in build_inputs. It is not Python code emitted
from a quoted string. It refuses non-native/non-root execution and validates
native OS release, package identity, actual architecture and hashes before any
installation. The host driver freezes all actors and fixture sources, captures
immutable image IDs and preserves failed preparation/runtime cases separately.

## Functional matrix

wine-unmapped-owner-debian-v2 and wine-unmapped-owner-ubuntu-v2 each pass PE32 and
PE64 twice: eight actual fully unmapped-owner runs in total. The corresponding
wine-mapped-owner-<base>-v1 directories each pass both bitnesses once: four mapped
regression runs. The unchanged original Win32 producer/actor verifies real
PID/class/owner hints, late tool palettes above the main frame, unrelated-frame
occlusion and return, group hide/restore without IconicState or process exit,
stable focus, real-click activation/foreign-process focus refusal and clean
WM_DELETE_WINDOW close. Every run has fresh ordinary-user home/prefix, private
bus/display, read-only system root, no capabilities and no network.

unmapped-owner-native-regression-v2 freezes the model/protocol sources and uses
the installed native library pair. Both bases pass all ten X11 layouts:
mapped Wine owner, fully unmapped owner, unmapped native class, mapped untyped
owner, explicit owner-class mismatch, foreign-process owner, native application,
visible owner, multiple frames and resizable custom frame. Only the first two
are grouped. Both positive layouts also exercise four late palettes, unrelated
occlusion and NormalState-preserving group minimize/restore. Four additional
normal/startup-lock protocol runs pass. unmapped-owner-native-abi-v1.json retains
the actual SONAME/export comparisons. All 50 existing Builder tests pass on each
native Linux base, including the symlink fixtures.

Final actor SHA256 is the unchanged
04db492e5f9c5fd2faf82f482281a29ce364b0630bb42f737355d5aefb7c6dcc.
Producer source SHA256 is
f887d6c891ae76082b2c31fe741bc4db38b67a06bc14c2bbca536f3e8dc01872.
Copied installer SHA256 is
e0af2982e2976f40f4818055a320bbf52bcbc05ca2c9a07bbefa159d42740c89.
Local receipts contain all source manifests, native package/image identities,
per-case frames/logs and the real rejected-dependency receipt. Earlier fallback-
only negative failures and the initial observation package remain preserved.

## Remaining work

This accepts two concrete framework-owner layouts, not arbitrary Windows UI
patterns. Windows-like parent/child captions, red close buttons and rounded
corners, complete taskbar binding, actual third-party applications, legacy-prefix
import and installed-user deployment remain distinct gates. Darling, remaining
VMware host channels/resize and VPN lifecycle stay in the full migration plan.
The own launcher package still comes from e782fb0; these later compositor/library
and QA changes are not mislabeled as a joined current-HEAD DE installation.
No push/fetch, ISO rebuild, Forge work or existing desktop changes were performed.
