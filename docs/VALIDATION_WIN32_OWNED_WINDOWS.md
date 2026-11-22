# Generic Win32 owned-window compositor migration

DE e7ccb5a adds native Debian/Ubuntu labwc patches for the remaining generic
hidden-owner palette and minimize behavior. It does not introduce RomArtist
rules or change any application's prefix. The donor is read-only revision
26bad17cef413d26c36c117f2f1123dca4edded7, specifically its
wine-owned-window-groups.patch and wine-owned-window-minimize.patch.

## Behavior and adaptation

Some legacy Win32 toolkits give one decorated main frame and several fixed-size
palettes the same tiny invisible owner. Ordinary sibling stacking can then raise
the main frame over all its palettes. The patch uses the unique decorated NORMAL
frame as the compositor's effective root only when the tiny owner is undecorated,
the PID is positive and matches, the case-insensitive .exe class matches, and
there is no second decorated document frame or resizable custom NORMAL frame.
The actual X11 WM_TRANSIENT_FOR ownership remains untouched.

The recognized scene group minimizes without sending IconicState to its actual
X11 windows. This preserves normal mapped handles that a legacy framework might
otherwise withdraw. The group remains behind unrelated applications; it is not
implemented as always-on-top. Debian0.8's raise cache is bypassed for recognized
roots so later palettes participate. Ubuntu0.9 has no equivalent cache, and its
patch uses the native wlroots0.19 window-type API. Native wlroots packages are
not replaced by this slice.

The derived labwc patches retain upstream GPL-2.0-only licensing. The independent
GPL-3.0-or-later QA tool adapts the prototype's regression, adds late palettes,
package integrity checks and conservative isolated lifecycle handling. Native
Python Xlib, Pillow, grim and Xwayland are external test dependencies. No private
binary, credential or saved Wine configuration is imported.

## Native builds and tests

Builder source-package captured the recipe, every ordered checksum-locked patch
and each native source archive before a network-disabled build. The successful
manifest's ordered patch hashes match the current recipes exactly. Normal native
packaging/hardening and upstream Meson tests are retained: Debian2/2, Ubuntu3/3.

| Base | Native package | labwc artifact SHA256 |
| --- | --- | --- |
| Debian13 | 0.8.3-1+karyo3 | 5494d2d079303d582919d30c29af388466a95b2cc951cab56454911d91a76293 |
| Ubuntu26.04 | 0.9.3-1+karyo3 | 97f6d56a2d244d56aca289c5c0caf004da1137def9ced352c5ca544e65fae041 |

The test executes the extracted native package under UID65534 with a private
HOME, config, headless compositor and Xwayland, isolated /tmp, no network,
read-only root/source, cap-drop=ALL and NoNewPrivileges. It never connects to a
running desktop. The exact source actor SHA256 is
685fce832e9f4acbd5fe17c632b092f0de5b8aafa29530158812d8d3bcc90876.

Both original karyo2 packages reproduce the missing Wine grouping. Both new
packages pass the same real XWayland model checks:

- Matching .EXE hidden-owner palettes stay above their main frame after focus
  switches and remain occluded by unrelated application windows.
- Four differently colored late-created palettes remain visible, preserve their
  actual owner hints and restore together after scene minimization. All retain
  X11 NormalState while minimized; captures prove the group is actually hidden.
- Native class, visible owner, multiple document frames and resizable custom
  frames retain the original fallback behavior.
- Separate existing native protocol clients still pass both normal and initial-
  lock modes: snapshots/stacking/minimize, layout safe absence, security-context
  filtering and fail-closed startup lock/crash recovery.

These are real compositor/client pixel and protocol checks, not mocked grouping
functions. They do not establish actual Wine application behavior or physical
input, nor a native VM package upgrade or current-desktop replacement.

## Retained failures and fixture corrections

The first Ubuntu source build failed because labwc0.9/wlroots0.19 replaced the
older window-type helper and enum. Its build output remains under the failed
source-stage directory. The corrected variant calls the native surface API and
its new checksum is captured by the successful build.

The stronger four-palette test then exposed a cross-case fixture race on Ubuntu:
XSync acknowledged Xwayland deletion but not the compositor WM loop, allowing
python-xlib to reuse IDs while old events were pending. The frame lacked the
expected newly created main window, and the negative native case failed. The
failed log/frame is retained. The final actor waits for those IDs to disappear
from compositor-published _NET_CLIENT_LIST before allowing reuse. Every expected
pixel/state/ownership assertion is retained; final before/after runs pass on
both bases. This is documented as a fixture correction, not a production fix.

## Evidence and remaining compatibility scope

Local out/migration/win32-owned-windows-evidence.json joins native manifests,
recipes/patches, image IDs, artifact hashes, checks and individual log/frame
hashes. out/migration/owned-windows-{debian,ubuntu} retains baseline-v3,
patched-v3, normal/startup-lock protocol results, the exact executed actor and
older failed observations. Native packages remain in DE's ignored
out/compositor/{base}/owned-packages; no binary is committed.

The ordinary QA VM sessions, owner VM, Acer, Forge and donor were not modified.
No remote push/fetch was used. Existing DE runtime tests were not rerun merely
for this external source-patch change; native build suites and actual new
compositor protocol gates cover it.

Still open: actual Win32 executable/prefix launch and native installed upgrade,
Wine/XWayland focus-loop and popup-menu behavior, Windows-like captions/rounding,
icons/desktop registration, Wine engine patches and experimental Darling. The
full DE migration remains active; this slice closes only the generic compositor
owned-window capability under the verified model above.


Later ordinary-user EXE/MSI/registration acceptance is documented separately in
VALIDATION_WIN32_RUNTIME.md; actual generic Wine menu metadata and native source
package checks are in VALIDATION_WINE_MENUS.md. Those later gates do not relabel
this older modeled palette/minimize evidence as actual Wine-owned-window proof.
