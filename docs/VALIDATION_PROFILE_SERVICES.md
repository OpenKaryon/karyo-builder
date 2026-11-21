# Owned private resolver service acceptance

Accepted product source: b08ce4daa22f036bc294c8f1a0cb952041b4b38e.
Published final installed probe: Karyo DE 3912203.
This is a DNS controller gate, not complete session supervision.

## Exact inputs

### Debian

- Output: out/migration/profile-services-debian/karyo-profile-accounts-20261121T154413Z-2f797c54.
- Source archive SHA256: 15225cef027a0056ec8d36e007ae36ffb6ee644957c952c1ade723b1e8b044f7.
- DEB SHA256: ff9a35f004dfb84dbf52ab60f1e53af813e1133e2bc0241afe7ec1c3486f6eb6.

### Ubuntu

- Output: out/migration/profile-services-ubuntu/karyo-profile-accounts-20261121T154415Z-193a65e2.
- Source archive SHA256: 15225cef027a0056ec8d36e007ae36ffb6ee644957c952c1ade723b1e8b044f7.
- DEB SHA256: 575435b063058fb3fbf541eac076eec653989b9136b842f4f6f743a2e84dca06.

- Final probe SHA256 on both bases: 19627d64bf981e82ac091560f4d7d069c9be69a6337832617eec6b71283a5ee3.
- Final evidence: out/BASE-vm-qa/results/profile-services-accepted-native.log.

## Product boundary

The internal controller starts only its fixed native private DNS bus/resolver
programs in fresh UUID-named transient units. The profile configuration lock and
root host user/network/mount namespaces are required. A private profile's sudo
process cannot accidentally perform host setup through this interface.

Each acknowledged unit captures systemd InvocationID, a pidfd, process start
time, executable device/inode, all UIDs, cgroup and expected network namespace.
The fixed program path is checked through root-owned nonwritable directories.
Creation refuses loaded units; launch timeout or failed ownership capture
retains resources instead of adopting an object by a later matching name.

Stop checks the captured invocation/process and never uses kill-by-name,
reset-failed or replacement of an existing unit. ResolverServices also refuses
to stop either daemon while another process remains in the private namespace.
Only service-specific sandboxing is applied; generic client sudo stays intact.
The resolver bus owner is proved before per-link DNS bootstrap.

This code is an internal trusted root library, not a new user-controlled command
endpoint. The plan accepts only its DNS service roles/properties. It enables no
service on installation and provides no persistent lease adoption/restart policy.

## Native checks

Final profile regressions pass 208 cases on both Debian 13 and Ubuntu 26.04,
as root (three role skips) and UID 65534 (52 skips). They include failed launch
acknowledgement, replaced unit identity, PID start mismatch, missing unit with
still-live process, lock/host namespace refusal, argument/property restrictions
and live namespace consumer shutdown refusal.

Clean independent packages install without changing accounts, PAM, the default
display manager or authentication policy. The full installed DNS replacement
probe now uses production ResolverServices instead of a QA service wrapper.

Both native bases pass:

- Private bus/resolver creation, readiness, proven resolve1 PID and seeding.
- A duplicate lease refuses an already running unit; its close is harmless.
- A stale InvocationID refuses stop and the real daemon stays available.
- A live client prevents resolver shutdown; both daemons remain verified.
- A genuinely elevated root client in private namespaces is rejected by the
  host controller, while its ordinary sudo-to-root check still succeeds.
- The same client retains libc DNS, host logind bus and private read-only queries
  through global stub atomic replacement, canonical symlink retarget and private
  per-link DNS/alias replacement. Unprivileged DNS mutation remains denied.
- Cleanup stops only captured services after clients, then removes owned network
  resources. Original host file identities, network snapshots, accounts/PAM and
  graphical shell PIDs remain unchanged; dpkg verification/audit is clean.

Final Debian client/resolver PIDs are 49291/49250; final Ubuntu client/resolver PIDs are
116687/116648. PID numbers are diagnostic, not authority.
The controller uses native invocation/process identity rather than these literals.

## Diagnostics and limits

The first production-controller installed run passes both bases
(profile-services-native.log). An extended QA-only edit initially contains an
invalid literal newline and is rejected before execution
(profile-services-extended-native.log). A later nested scope snippet has an
escaping error and fails its public-phase assertion; owned cleanup succeeds
(profile-services-confirmed-native.log). All embedded snippets are then compiled
before transfer. The corrected extended pass is profile-services-final-native.log;
the accepted log additionally asserts real/effective root before testing scope.
No product workaround is derived from these fixture syntax errors.

Current graphical sessions stay on VT8 with their original shell PIDs. Real
NetBird process/socket/authentication, user-manager mounts, stopped-profile VT
launch/owned teardown, persistent supervision/recovery, forwarding activation and
physical-change reconciliation remain separate required work. See
VALIDATION_PROFILE_DNS.md for resolver discovery/backend limitations.
