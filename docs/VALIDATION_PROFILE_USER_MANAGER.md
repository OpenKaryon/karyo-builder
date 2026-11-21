# Installed offline user-manager scope

Accepted runtime source: db70d67b279d6c86d03a411a4e2f73d7719e05b7.
Published final fixed-host probe: Karyo DE 2ceb297ca97e6a35d850dde5da45ea9bfee8ca1f.
This accepts the native PAM/user-manager scope, not a complete graphical starter.

## Exact inputs

### Debian

- Output: out/migration/profile-manager-final-debian/karyo-profile-accounts-20261121T161903Z-f42e87d6.
- Source archive SHA256: 90c55e6eddcd39d0927fc38d20e8f4fa4e26a254958da1d92e79ba704b9e6b9f.
- DEB SHA256: a2a28ce044e5d2269ac1f5447d07e6b0252ee72986173e7c9bec8ccc85f647b7.

### Ubuntu

- Output: out/migration/profile-manager-final-ubuntu/karyo-profile-accounts-20261121T161905Z-56b75a2e.
- Source archive SHA256: 90c55e6eddcd39d0927fc38d20e8f4fa4e26a254958da1d92e79ba704b9e6b9f.
- DEB SHA256: 7a47bee74b2a5d1f61be5a3bd3f7117581e0640636c4bb01952720897aaa62ee.

- Final probe SHA256 on both bases: 9d914744bc6840129d0226470506b7e9d3030d57654a0dc271a3964bddc544a5.
- Final logs: out/BASE-vm-qa/results/profile-manager-bounding-native.log.
- Root helper: /usr/local/libexec/karyo-qa-user-manager.

## Native model and product behavior

A new profile requires no login of any kind, UID process, user runtime, linger
entry or existing private manager policy. The root controller owns a fresh
per-UID runtime drop-in by directory/file inode and complete bytes. The drop-in
sets private network/resolver scope, retaining the host system bus.

Complete logind owner inventory includes remote/TTY/closing and manager records.
A running scope captures exactly the expected new PAM login and the associated
systemd-user manager, with invocation, pidfd, executable/start time, UID,
init.scope and private network. Its actual resolver directory mount must match
the private runtime directory inode. Unknown or changed identities are refused.

PAM moves the native session process into session-ID.scope, while user@UID's
main process runs in its init.scope. The native experiment proves this on both
bases. Original service cgroup membership alone cannot own all graphical clients;
the pending graphical controller must capture logind leader/scope as well.

The library never sends stop to user@UID. After the owned PAM session ends,
it waits for normal logind lifetime and all UID logins/processes to finish.
Concurrent or restarted logins retain the graph. It removes only unchanged
owned drop-in data and rechecks after daemon-reload; global configuration,
foreign units and their files are not replaced.

## Capability regression found and fixed

Source 0231947 passes basic native scope/PAM checks, but the extended ordinary
manager job retains CAP_WAKE_ALARM in its inheritable set. Its permitted,
effective and ambient sets are zero and password sudo already succeeds.
The raw PAM session process has CAP_WAKE_ALARM in all four sets. The findings
are distinct; do not claim that the manager job kept ambient privilege.

Source 17f8b39 wraps the verified default manager ExecStart in setpriv, clearing
only inheritable/ambient capabilities. It neither empties the bounding set nor
enables NoNewPrivileges. Typed systemd D-Bus command identity must match the
supported native default; custom commands fail before drop-in creation.
db70d67 uses passive LoadUnit for idle templates before command inspection.
The first GetUnit lookup failed before private manager policy was created;
the fixture still restored its account and network graph.

## Acceptance on both native bases

The complete profile suite passes 226 cases as root (three role skips) and
UID 65534 (63 skips) on Debian 13 and Ubuntu 26.04. Native package build tests,
independent no-remove installation, account/PAM/default manager checks and
forged SSH-caller refusal all pass.

The final fixed-host fixture creates an absent-before known QA child using the
public library fixture, reserves VT9 and opens a custom temporary PAM session.
Its auth stack denies authentication; only the root QA starter opens the
account/session stack after proving the fresh account and free console.
The session stays inactive: the existing main GUI remains active on VT8.

The installed UserManagerScope prepares policy before PAM starts the manager.
A real application activated by that user manager proves:

- The same private network namespace as the captured session and manager.
- Resolver directory device/inode equals the private resolver runtime.
- Successful normal password sudo to root and host logind bus access.
- Zero inheritable/permitted/effective/ambient capability sets.
- NoNewPrivs=0 and capability bounding set equal to the unchanged main manager.

The QA child temporarily receives a generated random password held only in
memory and transmitted through stdin. Neither password nor shadow hash is logged,
put in command arguments, saved in a project artifact or committed. Its captured
original hash is restored before account cleanup; the main account's credentials
are never changed. The rejected proposal to embed a fixed QA credential was not
executed. No credential approval bypass is used.

The captured PAM scope is terminated and the manager releases through normal
logind lifetime (10.566 seconds Debian, 10.532 Ubuntu). The fixture sends no
user-manager stop. The known account/home/metadata, temporary PAM file and scope
drop-in disappear. Original account/common PAM bytes, full link/route/rule/nft/
namespace/resolver/forwarding snapshots and main shell PID are restored.
Native child runtime is absent; dpkg verification/audit is clean.

## Preserved evidence and boundaries

- native-session-exploration.log: first successful PAM/cgroup model experiment.
- profile-manager-native.log: initial installed scope pass, before capability assertion.
- profile-manager-confirmed-native.log: extended capability assertion fails; cleanup succeeds.
- Debian profile-manager-caps-diagnostic.log: exact residual inheritable bit and successful sudo.
- profile-manager-caps-native.log: idle GetUnit preflight failure; cleanup succeeds.
- profile-manager-final-native.log: corrected native capability boundary passes.
- profile-manager-accepted-native.log: final public probe cleanup simplification passes.
- profile-manager-bounding-native.log: final explicit unchanged bounding-set acceptance.

This fixture deliberately uses sleep as its PAM session process. It does not
claim a running graphical child, protected initial compositor entry, owned
graphical logout/teardown, persistent resource recovery or host dispatcher.
The direct PAM GUI entry still needs its own capability reset before launching
normal clients. Physical reconciliation, complete network runtime/dependencies,
actual NetBird lifecycle, family clipboard and other migration inventory remain.

The native model follows upstream
[systemd execution/PAM documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html).
Implementation and opt-in QA code are own GPL-3.0-or-later; no prototype unchecked
PAMName/TTYVHangup/session-name deletion workflow is copied.
