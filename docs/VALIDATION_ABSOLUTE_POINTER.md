# Absolute pointer re-entry on Debian

DE commit `fefa6aa` corrects the Debian labwc absolute-motion handler: it no
longer sends an additional relative-motion event for an absolute position.
The real relative-device handler is unchanged. This follows native labwc0.9.3
behavior, retaining the GPL-2.0-only upstream license and native public ABI.
There are no Wine application-name rules or user-prefix settings.

## Controlled before/after

The identical own Win32 C producer and private persistent-pointer actor run
against the same Wine+karyo2, launcher and native wlroots library. The only
runtime replacement is Debian labwc0.8.3-1+karyo5 to 0.8.3-1+karyo6.
The native labwc DEB SHA256 is
`a28273358b5883760b8ffe7f6ee339876bf86629eb7e0b060da3096c822eadf3`.
The source patch SHA256 is
`c3dcf9f6257b5d10eb2fc04f6e7aa0c88f0e590f05293fce1802010640c038aa`.
Native wlroots remains 0.18.2-3+karyo2 with its exact package dependency.

Before the fix, moving out of a Wine surface and back reports X11 position
(691,247), but pressing the pointer button jumps to (1279,719), outside the
client. The own target receives no button-down message. With the new compositor,
button press/release retain the requested position and the correct client
receives the input. Passive X11 traces retain coordinates, button masks, child,
focus and active-window IDs; the test does not move the pointer through XTest.

The pointer client remains alive throughout the session and acknowledges every
command. Removing the earlier non-client corner gesture from a diagnostic
control still reproduces the old failure. A cursor parked over a screenshot
sample and an earlier per-command pointer hotplug attempt were separate QA
problems; neither is presented as this native input defect's cause.

Frozen producer SHA256:
`ebc1a0b09f818eb6c71d1685ddc8385a7296ff9116542e1c8b586b0ee1541393`.
Frozen actor SHA256:
`94d57c0a7b002084fd8a310a44d0ec15ca0547fa54ab6bc25601937024f3285f`.
These bytes predate the subsequent stricter MDI damage assertion. The later
child-rounding change has separate before/after evidence and acceptance.

## Regressions

The corrected Debian stack passes PE32 and PE64 at actual 96 and 192 DPI.
Each case completes all 15 native child/MDI/style/explicit-region stages,
including real body and corner clicks for ordinary and MDI children. That
checkpoint uses Wine2, whose native default children remain rectangular.
It does not accept the later experimental rounded-child implementation.

Four actual Wine palette cases also pass: PE32/PE64 twice with a fully unmapped
framework owner, late palettes, foreign-frame return, stable focus and group
hide/restore. The same compositor subsequently passes that matrix with Wine3,
but Wine3 child rounding remains a distinct unfinished gate at this checkpoint.

The independently frozen native regression suite passes ten real X11 layouts,
including explicit owner-class mismatch, foreign-process owner, native and
ambiguous frames. Ordinary and startup-lock protocol runs also pass. These
are actual installed compositor processes, not source-text assertions.

Wine runs as disposable UID1001 with a fresh home/prefix, private D-Bus and
labwc/Xwayland display, no capabilities or new privileges, no network and a
read-only system root. No user VM, host display or existing prefix is involved.
Ubuntu26.04's native labwc0.9.3 handler already follows this input path: it is
unchanged and passes the same four bitness/DPI baseline cases separately.

## Local evidence and limits

Preserved Builder out/migration directories:

- wine-child-region-pointer-debian-probe-v1: negative old compositor.
- wine-child-region-pointer-debian-fixed-probe-v1: identical input fixtures pass.
- wine-child-region-pointer-no-first-border-debian-v1: diagnostic exclusion only.
- wine-child-region-baseline-debian-v4 and baseline-ubuntu-v4: full native matrix.
- wine2-absolute-pointer-palettes-debian-v1: corrected input with Wine2.
- wine3-absolute-pointer-palettes-debian-v1: additional palette regression.
- absolute-pointer-native-regression-v1: captured source hashes and native logs.
- absolute-pointer-evidence.json: joined receipt identities for this checkpoint.

Physical tablets, locked-pointer gameplay, hardware GPUs and VMware host input
are not established by headless virtual-pointer checks. Full DE migration,
child damage/rounding, existing-user deployment and remaining integrations stay
open. Only DE and Builder were changed; no push/fetch or ISO rebuild was run.
