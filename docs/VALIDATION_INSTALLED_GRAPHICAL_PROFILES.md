# Installed controlled graphical profiles

Accepted runtime source: f2edff367c64b949575f0e792ea0bdc452890aa2.
Published fixed-host probe: Karyo DE b0bf3e1df0ff01c2401b06c2ac88cb2f1d6b3ca0.
Probe SHA256: 656a575f8940b09638b56f072f8db48cf239fb5f458b5b384058b946b1a86f9f.

This accepts controlled graphical startup/explicit owned teardown, not a public
stopped-profile operation or persistent runtime service.

## Exact independent native inputs

### Debian

- accounts output: out/migration/profile-graphical-fixed-debian-accounts/karyo-profile-accounts-20261121T171100Z-0d10ac2a.
- accounts DEB SHA256: de31f4356f627be7a5f13e4f5b92fe27807f6b3a258797309848d9c57e0149f2.
- entry output: out/migration/profile-graphical-fixed-debian-entry/karyo-profile-session-20261121T171108Z-a42795ce.
- entry DEB SHA256: 21cbd89a92f54a59e55bcb3353081a67905d5b851f2e71d3a011dfa42225aa9c.
- Source archive SHA256: 8fd41637324061b80d5055fc3405cc67ef6dab5ff5a1098bdc29f9cfed90626b.

### Ubuntu

- accounts output: out/migration/profile-graphical-fixed-ubuntu-accounts/karyo-profile-accounts-20261121T171101Z-777bb740.
- accounts DEB SHA256: 23cb754ee8bab6bc44282700e18a49cdb4531ba5e2d5a660cf2f58443ce55173.
- entry output: out/migration/profile-graphical-fixed-ubuntu-entry/karyo-profile-session-20261121T171109Z-aa276672.
- entry DEB SHA256: 6627702b309ebcc324ecbf60c6fa37673b6c7f4248d269a056235139099c2143.
- Source archive SHA256: 8fd41637324061b80d5055fc3405cc67ef6dab5ff5a1098bdc29f9cfed90626b.

The optional karyo-profile-session package stages only its fixed entry programs,
PAM stack and documentation. It enables no service and changes no common PAM
stack or display manager. Accounts libraries stay in their own package.
Both native package sets install no-remove and preserve original account/PAM/
default manager identities and package verification.

## Ownership and activation boundary

The root library consumes a captured offline user manager and held free-console
lease. Its fresh transient unit opens native account/session PAM management
under karyo-desktop; the PAM auth stack denies authentication. The already
authorized host controller owns entry authorization. The common wrapper clears
PAM inheritable/ambient capabilities without reducing the bounding set or
enabling NoNewPrivileges.

A native waiter resolves its own process's logind identity, confirms the UID and
waits up to sixty seconds for explicit activation. It cannot activate its own VT
or source a user environment before that point. The ordinary protected
karyo-session entry starts only afterward.

The graphical lease captures unit InvocationID and pidfd, then logind
leader/name/UID/service and independent session.scope invocation/cgroup. Process
start, namespace and manager/resolver scope are verified separately from the
original system.slice unit. Enter checks the active caller/family and locks a
protected source before activating the new profile. Teardown targets only the
captured login scope and original service; it never kills by process name.

## Native acceptance on both bases

Debian 13 and Ubuntu 26.04 pass 242 profile cases as root (three role skips)
and UID 65534 (63 skips), plus separate /usr and /etc payload staging. Existing
C++ code is unchanged during this gate; its full unrelated suite is not repeated.

The exact installed packages pass all three modes with the published root probe:

| Mode | Debian | Ubuntu |
| --- | --- | --- |
| No password | pass | pass |
| Home password | pass | pass |
| Separate password | pass | pass |

Each case creates an absent-before captured QA child and native PAM login on
reserved inactive VT9. No child compositor or shell exists before explicit
entry, and the original source stays active on VT8. After entry, the actual
compositor, shell and optional Files service run in the private profile context.

Protected initial entry confirms compositor lock and absence of initial shell/
Files clients. Real VM-only VNC input supplies a wrong password; lock and absent
clients remain. Correct authentication starts the desktop. Home/Work roundtrips
preserve both graphical shell PIDs. Leaving a protected source confirms its lock;
re-entry displays a new password form and correct authentication resumes the
same child shell. The unprotected mode roundtrips without password input.

Both GUI compositor and shell have zero inheritable/permitted/effective/ambient
sets, NoNewPrivs=0 and a bounding set equal to the unchanged original main user
manager. The private namespace and resolver/user-manager identity are checked.
Normal password sudo for the user-manager path is accepted separately in
VALIDATION_PROFILE_USER_MANAGER.md; this fixture does not claim an extra terminal
sudo interaction.

Visual phases use bounded stdin acknowledgements before the controller advances.
The host driver captures only each disposable VM's VNC framebuffer; it never
focuses the VMware window or controls the host mouse/keyboard. Captured
locked/wrong/running/home/re-entry images have been inspected. Initial wrong
password and later re-entry are visible on both native bases.

Credentials are bounded stdin input, never source constants, argv, environment,
logs or new artifact files. Separate mode uses an in-memory random child password
and restores the captured original hash. Home mode reads the existing ignored
synthetic QA seed credential into driver memory and changes neither main nor
child credentials. The main account is never modified. No personal user tunnel,
browser profile, SSH credential or authorization token is imported.

All final cases restore account/common PAM bytes, host link/route/rule/nft/
namespace/resolver/forwarding snapshots and the original graphical shell PID.
The known QA child/home/metadata and private runtime disappear, and native
user-manager lifetime ends through logind. dpkg verification/audit stays clean.

## Evidence and corrections

Final per-base logs under out/BASE-vm-qa/results:

- profile-graphical-none-roundtrip.log
- profile-graphical-home-roundtrip.log
- profile-graphical-separate-roundtrip.log

Each ends with the clean phase and PASS restoration. Images have matching
profile-graphical-MODE-PHASE.png names. Separate first-source evidence remains
under graphical-dfbf917-evidence and graphical-f2edff3-first-evidence.

The initial root fixture incorrectly nested ConfigStore around ExistingSwitcher,
which already owns that lock. The fixture is corrected; product switching
semantics are unchanged. Raw first Debian failure remains preserved.

Initial Ubuntu graphical entry/roundtrip worked, but teardown listed a login
just before logind removed it. The following owner property query failed.
Source f2edff3 retries a complete fresh owner inventory within one deadline.
Only a fully successful inventory can establish absence; persistent failure is
still an error. Regression cases cover both outcomes.

The one retained Ubuntu QA graph (243ec87c0c134627bc0bf4890f59de56) was reconciled
separately after its graphical scope and manager had already ended. Recovery
checks fixed namespace device/inode, veth indices/MAC/aliases, private addresses,
configuration directory/file inodes and exact expected bytes/hashes, native DNS
unit invocation/PID identities and absence of UID logins/processes. It stops
only those known DNS units, then closes only their captured files and link/
namespace and removes the already captured QA account. Successful recovery is
recorded in profile-graphical-known-recovery.log. No generic adoption/recovery
endpoint is added to production code. Do not rerun that one-use fixed helper.

VMware captureScreen refused anonymous guest operations. VM-only VNC capture
replaces it; no credential workaround or host-focus interaction is used.
Early visual phases could race a following switch, so the accepted protocol
requires per-phase acknowledgement. Earlier captures are retained as diagnostic
evidence rather than relabeled final acceptance.

## Remaining full-feature work

The public helper still reports DesktopStopped for a stopped target. A persistent
host root controller must own leases across requests, validate the actual peer
caller before leaving a private helper context, provide journaled recovery and
automatic return after user-initiated logout. The fixture uses explicit owned
teardown and return; it does not claim that watcher/return feature.

The GUI fixture proves namespace/resolver scope, not complete Internet/VPN
forwarding. Physical forwarding has its independent accepted gate; runtime
dependency/sysctl activation and physical-change reconciliation still need
integration. Actual private NetBird daemon/state/socket/auth callback/browser,
profile catalog overlays, family clipboard, remaining Win32/macOS and VMware/
Wine integrations remain open. This does not change distribution recipes or Forge.
