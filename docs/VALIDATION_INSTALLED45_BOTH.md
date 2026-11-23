# Installed45 application checks on both native bases

Both complete45-patch Darling engines now run original loader, Cocoa and
Qt5.15.19 clients on their native Debian13 and Ubuntu26.04 kernels. Real
whole-desktop frames and widget rasters were exported, hash-checked and viewed.
UTF-8 titles and displayed label/button text are correct. This confirms the
shared text-origin fix for these clients; it does not establish arbitrary
macOS application compatibility or complete desktop lifecycle acceptance.

| Base | Runtime bytes | Runtime SHA256 |
| --- | --- | --- |
| Debian13 |87807000|d2e5e9d4204e36ad321867f412ec0cb5aad637ced4ddc9e042fd96be55ebaf89|
| Ubuntu26.04 |92688610|845967568932c91c90725d8a7fae581133153392fae265eaa2e1fd1f0fd6c638|

Both source bundles record DE66da7724bf2bbf9415c8654ba9e6646650e780a0.
The actor-only a097825 commit does not change runtime patch inputs. Native
package provenance, actual artifact hashes and package verification are checked;
the development version string alone cannot identify the patch stack. Existing
account/PAM/display-manager configuration and package versions remain preserved.

The real Qt widget PNG on both is byte-identical, SHA256
d90cf2c330b6cb14b737a913f15a4e4430fe7607b7c79394ba77041b4d3347d6.
These original clients use installed shared libraries, without executable
function prototypes. Transformed/repeated CoreText drawing remains a separate
graphics compatibility limit.

Original uninstrumented event-loop clients also pass on both systems. Debian's
three50ms Cocoa waits are0.051191,0.051433 and0.051170seconds; its windowed
CoreFoundation waits are0.006862,0.000769,0.051800 and0.052568seconds.
Ubuntu's corresponding values and retained controller failures are recorded in
[the earlier Ubuntu checkpoint](VALIDATION_INSTALLED45_UBUNTU.md).
The common deadline patch replaces approximately29–30-second baseline waits
with the requested bounds. No executable deadline guardian is used.

The unchanged upstream TextEditor opens its standard NSOpen document on both.
Displayed original-document and after-save frames were viewed. Ordinary X11
input saves exactly45bytes and exits the native application with code0;
both successful Quit helpers also return0. The saved-file SHA256 is
05786532df55212187f436d1163809d540c98cd0ad30ea1881bfbcbd831bca74.
Debian's first input attempt saved correctly but did not quit; its second uses
explicit EWMH window activation before normal global Quit. The failed first
attempt is retained. This is ordinary synthetic QA-session input, not physical
keyboard or all-menu coverage.

The original53-byte Mac persistent-data fixture also passes a read after
normal shutdown of its own old server and startup of a distinct new server on
both systems. Prefix directory identities remain unchanged. Old before/after
records are retained independently of the latest runtime version.

## Open reliability result

Ubuntu's four stock utility cases pass exact stdout. Debian's first45 run
passes echo and defaults write/read, but uname exits136 with Floating point
exception while creating a new prefix. A targeted recheck succeeds in that
same prefix and in one additional fresh prefix. The original failure is not
overwritten or relabeled as a pass. The bounded system-journal interval has no
matching trap/core entry, and the cause remains unresolved. Complete stock
utility reliability is therefore **not accepted** on Debian45.

## Next original application

UGENE53.1 has now been attempted on both systems, and neither original UI is
accepted. A separate client of its unchanged dynamic Qt5.15.10 frameworks
reproduces a system-color lifetime failure on both bases; a proposed common
factory cache fixes that client's initialization. See the exact diagnosis and
limits in [the system-color report](VALIDATION_SYSTEM_COLOR_LIFETIME.md).
The common46 patch passes independent source checks; installed-runtime and
additional optional-window/menu API checks remain open.

Receipts remain under out/migration: darling-kernel-base45-installed.json and
runtime-latest.json; upstream-texteditor/debian45.json,
debian45-keyboard-v2.json and ubuntu45-keyboard-v3.json;
runloop-installed45-v2-timing/base.log and window/base.log;
darling-data-upgrade/base-after45.json. The Debian utility failure and targeted
rechecks are in darling-stock-utilities/debian45-v1.json,
debian45-uname-recheck-v1.log and debian45-uname-system-log-v1.log.
No shared policy/security unit suites are executed for this milestone.
