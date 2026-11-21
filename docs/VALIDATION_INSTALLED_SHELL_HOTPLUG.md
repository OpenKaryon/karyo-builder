# Installed shell output recovery

Exact shell runtime source: bb46dfc3a3ab88b7f11223eafe8b70df77b60f9c.
The final native DEBs are installed without source wrappers or binary overlays.
Lock remains from 283cce4; session-entry from 156d1aa; native labwc is +karyo2.
Profile accounts now use bf831b0 and include the public karyo-desktops CLI.

## Exact native inputs

### Debian

- Output: out/migration/shell-hotplug-final-debian/karyo-shell-20261121T120937Z-3ccece96.
- Source archive SHA256: 5bcc729ac260b1f76db49c50ff2fe5be2ace31a9220f5037dbefcf2a3cd67753.
- DEB SHA256: afb7b5c1b9326e08d40f0b416247b1a64446401b45deb7c586617083c385313d.

### Ubuntu

- Output: out/migration/shell-hotplug-final-ubuntu/karyo-shell-20261121T120936Z-2ea63d5d.
- Source archive SHA256: 5bcc729ac260b1f76db49c50ff2fe5be2ace31a9220f5037dbefcf2a3cd67753.
- DEB SHA256: 483db32464d7de3834b95dc0cfcd2ad8a9f9606803505d754bf437bd4e6edf7e.

## Installed acceptance

Both clean builds run all 68 CTests successfully. The installer verifies exact
source revision, artifact SHA and absent source overlays. No-remove installation
preserves passwd/shadow/group, every common PAM file and the default manager;
dpkg verification/audit are clean. The known QA startup driver hash is checked
before adding only the disposable user protection metadata.

Real LightDM login reaches an observed mandatory initial password form before
the shell or Files start. Correct PAM starts the packaged /usr/bin/karyo-shell.
A Terminal is opened from the real panel, DND is set through the native session
bus and Start is opened. The fixed QA driver switches to an unoccupied console,
waits for inactive/LockedHint confirmation, and restores the original VT. Its
READY result is followed by actual visual inspection and PAM authentication.

On both guests the returned password form is visible and interactive. Correct
PAM restores a visible panel and Start opens again. Shell/Terminal PIDs remain
unchanged: Debian 32074/32191, Ubuntu 87639/87882. Shared notification DND still
returns true after the panel has been recreated, and is reset to false. These
are final package checks, not source-overlay checks. The earlier two-roundtrip
source gate separately exercised the same behavior on both native Qt versions.

Metadata cleanup verifies original account/PAM bytes, removes only the known
temporary policy/state and checks package integrity/audit again. The GUI sessions
are retained for subsequent two-profile work. No test profile child exists yet.
Root-only PAM recovery and the fixed startup driver are deliberately retained.

The reproduced Ubuntu invisible-taskbar regression is closed for the tested
single virtual-display VT lifecycle. No physical multi-monitor or GPU coverage
is implied, and desktop icon content was not separately asserted in the GUI.
Distinct-session switching, owned stopped-session startup/VT allocation, network
namespaces/DNS/VPN isolation and family clipboard remain required. Shell menu
wiring still uses the legacy command and must be connected to the new public API.

Evidence under out/{debian,ubuntu}-vm-qa/results: shell-hotplug-final-install.log,
shell-hotplug-final-native.log, shell-hotplug-final-cleanup.log, and final
initial/return/menu PNGs. Exact input receipts/SHA are in shell-hotplug-final-input.
Nothing is pushed; Forge, the private donor and owner machines are unchanged.
