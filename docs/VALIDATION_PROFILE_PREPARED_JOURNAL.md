# Installed acknowledged profile preparation recovery

This extends the living GUI gate with offline preparation reconciliation. It does
not complete graphical closing/logout supervision or the overall migration. No
push, owner-machine changes, Forge changes or donor modifications are performed.

## Exact runtime inputs

Installed DE source: bcff209564eb98b292129260be174450f6946cbd.
Source archive SHA256:
3a2a5163bccf8f0c605e8785e674da3c08924c7e93b4eb7a7efcf94a35f716a3.

- debian accounts: out/migration/profile-prepared-journal-debian-accounts/karyo-profile-accounts-20261121T194020Z-e6386c2c; 77916 bytes; SHA256 2c7f48e26f8ca99e07010fc431f3f0b24796d7036d90b19d8cf86a5d398d7d4f.
- debian host: out/migration/profile-prepared-journal-debian-host/karyo-profile-host-20261121T194035Z-c797aa70; 33768 bytes; SHA256 afde7031332edede143f8b97aa1dbe60acbe590b8257e25c82a4a20b9399579a.
- ubuntu accounts: out/migration/profile-prepared-journal-ubuntu-accounts/karyo-profile-accounts-20261121T194111Z-b7dd72e2; 79062 bytes; SHA256 a2d08b98fb13852686ed258b2fad0e7bd1ec0eff6cd11dd9bc84a23b87eb5152.
- ubuntu host: out/migration/profile-prepared-journal-ubuntu-host/karyo-profile-host-20261121T194123Z-66fd5251; 34204 bytes; SHA256 2fe9bd3b961a960013efc06573733713b26bc7620f9806cdf820bb4c703edd15.

Final public DE profiles/tests/installed-journal-prepared.py has SHA256
5175a706e260294fee2dc9aab08b75074128ecc4b6a60400e75d81c9c3cf6d93.
Both guests execute those exact root-owned bytes with installed packages, without
Python source overlays. The earlier living GUI proof is documented separately in
VALIDATION_PROFILE_SESSION_JOURNAL.md; its original logs are retained as
before-prepared-profile-session-journal-native.log under each QA results folder.

## Narrow prepared transition

SessionRegistry first considers only a fully acknowledged offline prepared manager
receipt, with no graphical/live-manager receipt and pending null or login-start.
It verifies unchanged account metadata, no native UID/login owners, the captured
network and DNS-only consumer inventory, exact prepared policy inode/bytes and
inactive manager state. The token-derived graphical service must be absent.
No process is adopted, signaled or started from an unacknowledged GUI transition.

Manager-close intent is written before policy removal, and the session receipt is
removed only after native close acknowledges success. The existing offline path
then closes private resolver, bus, files and network. Failure releases observer
FDs only and retains remaining ownership intent/resources. Unacknowledged manager
creation, partial policy removal, living or interrupted graphical closing are
not misclassified as an ordinary prepared lease.

## Accepted evidence

All 314 profile tests pass on Debian 13 and Ubuntu 26.04 as root (skip3) and
ordinary UID65534 (skip89). Added cases exercise prepared/unstarted-login success,
unknown GUI unit retention, changed accounts/live owners, non-prepared transition
rejection and retained close intent after failed policy removal. Builder recipes
are unchanged; native pinned package builds validate their current output.

The fixed-host probe creates a proven new synthetic QA child, starts its owned
private network/DNS and prepares its exact scoped manager policy. It captures the
journal and child PID, verifies lifetime-lock exclusion, then SIGKILLs only that
child. All three cases pass on both kernels:

- Prepared receipt before any graphical startup intent.
- Published login-start intent with no graphical unit created.
- The same offline transition reconciled by the actual installed host's native
  socket activation before its request accept loop.

The known policy, DNS/bus/configuration and namespace are removed. No user manager
or GUI appears during recovery. Native logs are results/profile-prepared-journal-
native.log. Final root probe SHA matches on each guest. Original account/common-
PAM bytes, main login, network links/routes/rules/nft/netns/resolver and forwarding
snapshot are restored after each case.

The existing installed living-editor and initially locked desktop fixture is
rerun on these exact final packages. The same editor PID and synthetic unsaved
cache survive; original source bytes stay unchanged. The lock remains locked
with the same PID and no shell/editor. Legacy DNS six-case, network five-case and
private-network/mount transport gates also pass on both final runtimes. Their
current logs use profile-{session-journal,dns-journal,journal,host}-native.log;
previous-runtime logs were saved with before-prepared prefixes.

Final results/prepared-journal-postchecks.log confirms main shell36901/97122,
login595/765 active/unlocked on VT8, no temporary child account/home/runtime/policy,
no private DNS configuration/runtime or named namespace, forwarding0, empty private
schema3 journal with mode0700 directory/0600 files, disabled/inactive host socket,
static/inactive host service, exact installed QA bytes and clean dpkg -V/--audit.
No C++ code changed, so the earlier complete CTest suite remains applicable.

## Still required

Interrupted manager-policy unlink/removal, closing graphical receipts and natural
logout/crash recovery need explicit reconciliation. The full public runtime,
primary Home host-network restart, forwarding/DHCP/DNS reconciliation, actual
NetBird/PKCE integration, profile catalogs, family clipboard and remaining
Wine/macOS/VMware integration remain open. No Internet/VPN or physical-hardware
claim is inferred from this disposable-VM preparation gate.


The later offline close gate in VALIDATION_PROFILE_CLOSING_JOURNAL.md accepts partial policy unlink/removal and completed graphical receipts. The prepared, living-editor/lock and legacy probes pass again on its 4a58468 runtime. Active closing/logout supervision still remains open.
