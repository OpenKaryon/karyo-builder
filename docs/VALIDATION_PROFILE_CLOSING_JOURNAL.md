# Installed offline graphical and manager closing reconciliation

This accepts interrupted teardown after the recorded native owners have already
exited. Active interrupted close, automatic logout/crash return and the complete
public profile runtime remain unfinished. No push or changes to owner machines,
Forge or the donor are performed.

## Exact runtime inputs

Installed DE source: 4a5846866d6d732739a6ffc719bde09930254bd6.
Source archive SHA256:
ad3890a5fd991ee6152d8b2934ad2cb6669628ff7b32255866892ba0cffbdfd5.

- debian accounts: out/migration/profile-closing-journal-debian-accounts/karyo-profile-accounts-20261121T195241Z-fe936114; 79204 bytes; SHA256 1c7b78ff6349799edc9b518c65924b0c029558f848caac8d0b3463e945f86995.
- debian host: out/migration/profile-closing-journal-debian-host/karyo-profile-host-20261121T195253Z-a7eb191c; 34168 bytes; SHA256 6ad24f814eb63062f02eb8555b2fd7716caaed47aa4518a57686b31118388516.
- ubuntu accounts: out/migration/profile-closing-journal-ubuntu-accounts/karyo-profile-accounts-20261121T195324Z-4bbb78c3; 80432 bytes; SHA256 866b6b9991a62d26d249519fd4d53bcc22063414d5ff537777ff7d35cb6cf6c2.
- ubuntu host: out/migration/profile-closing-journal-ubuntu-host/karyo-profile-host-20261121T195338Z-b4405906; 34572 bytes; SHA256 2cf75cc35815134ec624b950188dfca8f11f6923a10697082e2bc21f8b351684.

Public DE profiles/tests/installed-journal-closing.py has SHA256
b1b9943514d8cc5eb70af026c573baf693f6662fd9918b48e045402169e8d0d2.
Both guests execute those exact root-owned bytes against installed packages with
no Python source overlay. Existing live and preparation probes are unchanged.

## Completed owner and policy proof

The registry recognizes recorded login-close/manager-close transitions before
living-session restoration. Recovery requires an unchanged offline account, old
process start identities gone, both recorded logind IDs absent, a still-captured
network and DNS-only consumers. A remaining graphical service and logind scope
must be the same inactive/failed invocation with empty cgroups and no main PID.
If graphical close was already acknowledged, uncaptured remaining units prevent
cleanup. Dead process observation alone is insufficient.

A manager policy can be the exact captured full file/directory, the same empty
directory after unlink, or an already removed directory under manager-close
intent. The native policy must match the captured scoped configuration or its
original baseline. An empty directory is removed only with the captured inode;
unknown files, changed bytes/inodes, active/reused logins or foreign invocations
retain ownership and resources. Missing files are never recreated to verify them.
The normal manager close supports an already removed directory without inventing
an FD. It reloads systemd, checks the original inactive baseline and then records
session removal. Lower DNS/network recovery runs only after that acknowledgement.
This offline path never signals a process or stops user@UID.service.

## Native crash acceptance

All 327 profile tests pass on Debian 13 and Ubuntu 26.04 as root (skip3) and
ordinary UID65534 (skip97). New cases use real captured root-owned files for full,
unlinked, absent and reloaded policy states, and reject replaced directories,
foreign files/native policies, changed payloads, live processes, reused login IDs
and foreign graphical invocations/cgroups. Builder recipes are unchanged; four
pinned native DEB builds pass their packaging validation. C++ is unchanged.

The fixed-host probe prepares an absent synthetic child and starts its actual
private network/DNS, scoped manager and PAM graphical entry. The first case enters
a real compositor and returns to the validated original main login before known
teardown; other cases retain the native waiting PAM entry until teardown. It
waits for the captured manager to exit naturally, then its parent SIGKILLs only
the captured controller. All six cases pass on both kernels:

- GUI closed before the graphical-close journal acknowledgement.
- GUI acknowledged closed, with the full manager policy still present.
- Manager policy file unlinked, captured directory still empty and present.
- Captured policy directory already removed before daemon-reload.
- Native manager close/daemon-reload already acknowledged, before journal update.
- Actual installed host socket startup reconciles an unlinked-file transition.

The exact original account/common-PAM bytes, source login and network snapshot
return after every case. No GUI or user manager is restarted during recovery.
Results are profile-closing-journal-native.log under each QA results directory.
The socket-activated recovery host PIDs were 97906/175295 and are now stopped;
these diagnostics are not persisted identities for any later recovery attempt.

On the final 4a58468 runtime, both living editor/protected-lock scenarios pass
again: same manager/compositor/editor PIDs and synthetic unsaved cache, unchanged
source file, locked desktop with no shell/editor. Prepared three-case, DNS
six-case, network five-case and private NET/MNT transport acceptance also pass.
Their logs retain the usual profile-*-native.log names; previous bcff209-runtime
evidence is saved under before-closing prefixes.

Final closing-journal-postchecks.log confirms original main shells36901/97122,
logins595/765 active/unlocked on VT8, no temporary child/home/runtime/policy,
no named namespace/private DNS runtime/configuration, forwarding0, empty private
schema3 journal (directory0700/files0600), socket disabled/inactive and service
static/inactive. All three installed journal probe hashes, dpkg -V and dpkg
--audit are clean. No owner VM, Acer or physical hardware was touched.

## Next work

A recorded close with still-running native owners must be supervised through its
remaining natural lifetime. Automatic logout/crash return needs validated family
or greeter activation without stealing another active session. The complete public
runtime, primary Home host-network startup, forwarding/DHCP/DNS reconciliation,
actual NetBird/PKCE, profile catalogs, family clipboard and remaining Wine/macOS/
VMware integration are still pending. These offline recovery checks do not prove
Internet/VPN routing or physical GPU/Wi-Fi/camera/microphone support.


The later observed-lifetime gate in VALIDATION_PROFILE_SUPERVISION.md accepts normal logout/crash and Home return by the actual polling host, with no client traffic driving cleanup. These offline closing probes pass again on ac3beda. Already-dead startup replay and complete public runtime remain open.
