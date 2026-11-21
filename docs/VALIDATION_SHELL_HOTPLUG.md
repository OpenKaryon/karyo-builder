# Shell output recovery: native source acceptance

Exact DE source: bb46dfc3a3ab88b7f11223eafe8b70df77b60f9c.

This checkpoint uses temporary, hash-recorded source overlays on disposable
Debian 13 / Qt 6.8 and Ubuntu 26.04 / Qt 6.10 VMware guests. It is separate
from clean native DEB installation acceptance, which is still running.
The packaged shell and default manager are not modified by the overlay.

## Inputs

### Debian

- Source binary SHA256: 44a6e743aed565df0b16c3ee8ca873d40e174be6e4ca5f6cd4c266f94be6fa5d.
- QA wrapper SHA256: ac6bbef45afb446bbcbb5edb1357ceb7bcc7bd8598ba124adac4e5dfe8a60cdc.
- Source hashes/record: out/debian-vm-qa/shell-hotplug-input/record.json.

### Ubuntu

- Source binary SHA256: 0c990158f3ccdb5e9f34464eb20bae67efee745aba02d8e1108552d8c003fa4b.
- QA wrapper SHA256: ac6bbef45afb446bbcbb5edb1357ceb7bcc7bd8598ba124adac4e5dfe8a60cdc.
- Source hashes/record: out/ubuntu-vm-qa/shell-hotplug-input/record.json.

## Observed runtime behavior

Both real LightDM sessions first reach their installed mandatory initial PAM
lock with no shell or Files. Correct authentication starts the new source
shell and an ordinary Terminal window. The fixed-host QA VT driver rejects
an occupied console, waits for inactive/LockedHint confirmation, then restores
the original graphical VT. Its READY response is not used as UI acceptance.

On both guests the actual password form is visible on return and correct PAM
restores a visible panel and the same Terminal. Start opens from the restored
panel. A second roundtrip retires an already open Start menu; the returned
panel remains usable. Shell and Terminal keep their PIDs through both cycles:
Debian 30268/30376, Ubuntu 83966/84221. DND, set on the shared notification
service before the second roundtrip, remains true afterward, as verified through
the native session bus. It is reset to false after the check. Quick settings
open through the returned network/sound control on both guests.

This corrects the reproduced Ubuntu panel disappearance without restarting
the shell or its services. The shell ignores Qt placeholder screens, recreates
output-bound views and gives desktop icons to the current real primary output.
No application-specific rule or hardware driver replacement is involved.

## Cleanup and limits

The cleanup driver verifies wrapper/binary hashes, rechecks identical PIDs,
checks original account/common-PAM bytes, removes only the known temporary
policy, terminates the QA user and removes the source overlay. Package checks
and dpkg audit remain clean; LightDM is active. Root-only earlier PAM recovery
snapshots and the fixed QA startup driver remain available for final package QA.

Evidence is under out/{debian,ubuntu}-vm-qa/results: shell-hotplug-before,
return, after, menu and quick PNGs; Ubuntu second-return; source-cleanup.log
and overlay-install.log. Native incremental build/test logs are under
out/migration/{debian,ubuntu}/shell-hotplug-{build,ctest}.log. Four targeted
regressions pass on both bases (session contract, tray, search, service policy).

This covers one virtual display and actual VT-driven output removal/recreation,
not physical multi-monitor/GPU coverage. No physical Wi-Fi, Bluetooth, camera or
audio claim follows from the VM quick-settings check. Controlled two-profile
session startup/switching, network/DNS/VPN isolation and family clipboard remain
separate migration gates. Nothing is pushed; Forge and owner machines are untouched.
