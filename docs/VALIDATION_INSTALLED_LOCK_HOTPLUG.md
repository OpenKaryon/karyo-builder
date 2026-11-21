# Installed final lock output recovery

Exact lock runtime source: 283cce42a4a6823585152b3f3be1e73e05bce835.
Shell/session-entry remain from 156d1aa and native labwc is +karyo2.
Only the disposable QA VMs are used; no source overlay remains installed.

## Exact native inputs

### Debian

- Output: out/migration/lock-hotplug-final-debian/karyo-lock-20261121T112508Z-7240af13.
- Source archive SHA256: 9f8c1cbb528fc093105ac27b36e0e3b3c6bfee9ebe1cb75060eb93d3942e2568.
- DEB SHA256: 666ae85c4341787589804ea3e92c672038621173304b95b8f243888de7b6900c.
- Actual QA driver SHA256: 176641d98d1aebe8d324b7cfc316f7d8ce8085ba45256c50f2fd4f9cafd95cde.

### Ubuntu

- Output: out/migration/lock-hotplug-final-ubuntu/karyo-lock-20261121T112508Z-faff4dd7.
- Source archive SHA256: 9f8c1cbb528fc093105ac27b36e0e3b3c6bfee9ebe1cb75060eb93d3942e2568.
- DEB SHA256: 132f3d584c85f469df5ddda392a2f9867b0e5b734732950e3c1a2f2b619245f9.
- Actual QA driver SHA256: 176641d98d1aebe8d324b7cfc316f7d8ce8085ba45256c50f2fd4f9cafd95cde.

## Installed acceptance

Both clean native builds run all 68 CTests. Before no-remove lock reinstall,
input and DEB hashes are checked, no GUI session or overlay may remain, and the
old QA driver must match its previously recorded hash. Installation preserves
accounts, every common PAM file and the default manager. dpkg audits/verification
are clean. The enabled account/PAM helpers remain compatible and untouched.

Actual LightDM login first reaches the installed initial PAM lock, with one
flagged compositor, LockedHint yes and no shell/Files. Real password forms are
observed on both guests. Correct authentication starts the ordinary desktop.
The fixed-host QA roundtrip driver refuses an occupied console, activates the
empty console through Linux VT_ACTIVATE, waits for inactive lock confirmation
and restores the original graphical VT even on failure. Its READY result does
not substitute for visual inspection and actual authentication.

Both installed lockers retain actual password forms on return. Wrong passwords
show the PAM error and leave the lock intact; correct passwords restore the same
shell PID: Debian 29050, Ubuntu 80982. Ubuntu also repeats output replacement
during a pending failed PAM request and remains interactive afterward. This
closes the previously reproduced wallpaper-only lock/PAM failure for the tested
virtual-display VT lifecycle. No source wrapper/binary is used for this gate.

Metadata cleanup checks original account/PAM hashes and removes only the known
new policy and state. Package verification remains clean. GUI sessions are kept
temporarily for the distinct shell panel investigation described below; owner
systems and Forge are unchanged. Input stages and root-only PAM recovery remain.

## Related API and remaining shell defect

From actual terminal windows launched by the real shell, native pkexec accepts
desktop-list and current-desktop desktop-switch. Machine results contain only
the owning karyoqa family and changed=false at VT8. This complements actual SSH
context rejection from the earlier profile-controls checkpoint. Initial VNC
redirection typed a period instead of >; the corrected fixed QA script, executed
from the genuine GUI terminal, avoids that tool limitation. Script/JSON outputs
are removed after recording results. No root authorization failure is hidden.

Full-session inspection also exposes a separate Ubuntu shell surface defect:
the existing taskbar becomes invisible after output replacement. The shell PID
survives, its DBus ToggleStart opens a visible menu, and that menu launches real
applications, but the existing panel is absent. Debian retains its panel. This
is an open shell output-lifecycle regression, not a failed PAM unlock. It must
be fixed before claiming complete profile VT switching.

Evidence under out/{debian,ubuntu}-vm-qa/results: lock-hotplug-final-install.log,
lock-hotplug-final-native.log, lock-hotplug-final-cleanup.log, initial/return/
wrong captures prefixed lock-hotplug-final, profile-controls-positive.log and
profile-controls-terminal/status captures. Ubuntu menu-after-vt also shows its
missing panel. No physical multi-monitor or GPU matrix is implied. Actual
two-profile switching, owned stopped-session startup, network/DNS/VPN and family
clipboard remain required.
