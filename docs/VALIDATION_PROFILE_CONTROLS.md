# Profile list/switch entrypoint acceptance

Source: a9fd17f, fixed profile list/switch launchers and active-caller policies.
Only the disposable Debian 13 and Ubuntu 26.04 QA guests are changed.

## Native artifacts

### Debian

- Output: out/migration/profile-controls-debian/karyo-profile-accounts-20261121T113632Z-be4529f7.
- Source: a9fd17f5e04cc998b75a861d6a92df6f07ea973a.
- Source archive SHA256: ba3e1b8ee0e7b11c614d7ee6e5ffdbf80a80184f2ed2543fbfa9e4be3c0c5e70.
- DEB SHA256: 2baf54ac81f923885e71f00c1134ee7d3a94bafa92a37c86a1ca0e63f374d83e.

### Ubuntu

- Output: out/migration/profile-controls-ubuntu/karyo-profile-accounts-20261121T113634Z-b8e86cd7.
- Source: a9fd17f5e04cc998b75a861d6a92df6f07ea973a.
- Source archive SHA256: ba3e1b8ee0e7b11c614d7ee6e5ffdbf80a80184f2ed2543fbfa9e4be3c0c5e70.
- DEB SHA256: 35db7f89840c3e19d565908483e4c42712d6d274dacd669f7c26eb1a41e2e216.

## Verified boundary

Independent profiles CMake builds and stages the five isolated fixed-operation
launchers, package-owned Python modules and three fixed-path polkit actions.
No Qt build is needed. All 120 Python cases pass on both bases; ordinary UID
65534 passes with 42 root fixtures skipped, and root skips three ordinary cases.
Native CTest for this independent component is the profile-policy suite, not
the full graphical suite. Switch arguments cannot select an arbitrary owner,
session ID, executable or path. Failed caller authorization never constructs
a privileged switch backend; a stopped target has exit 3 without implicit start.

Exact input and DEB hashes are verified before no-remove reinstall. Account
databases, every common PAM file and the default display-manager link remain
byte-identical. The enabled optional password-sync package remains installed.
dpkg verification/audit are clean, and original LightDM remains active.

Actual pkaction on both guests recognizes desktop-list and desktop-switch,
with implicit any=no, inactive=no and active=yes, bound to their exact root
helper paths. From a real SSH cgroup, root invokes each helper with forged
PKEXEC_UID=1001, USER=karyoqa and XDG_SESSION_ID. Both reject that context with
exit 1 and the active-local-desktop error. Environment identity cannot replace
the native libsystemd session lookup.

Evidence: out/{debian,ubuntu}-vm-qa/profile-controls-input/record.json, SHA256SUMS
and results/profile-controls-install.log. Native build/test receipts live in
the outputs above; full source/ordinary logs are under out/migration/{base}.

This closes installed packaging, policy registration and negative SSH context
acceptance. Positive authorization from a genuine graphical process, actual
two-session lock-before-activate switching, stopped-session systemd/VT startup
and shell wiring are separate required gates. No newly created child account
or running child session is claimed by this checkpoint.

## Positive graphical caller checkpoint

The final lock QA later launched actual Terminal windows through the genuine
shell. Native pkexec accepted desktop-list and desktop-switch karyoqa: the list
contained only that owning family, and the current-session noop returned VT8
with changed=false on both native guests. This closes the genuine graphical
caller boundary for these operations; it does not exercise a different running
profile, its lock preparation or controlled startup. See the installed-lock
acceptance report and results/profile-controls-positive.log for evidence.
