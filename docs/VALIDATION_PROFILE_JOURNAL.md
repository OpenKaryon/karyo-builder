# Installed profile ownership journal and network recovery

This gate adds persistent ownership across controller requests/crashes for the
first network resource layer. It does not declare the full profile graph,
public stopped-profile startup or overall migration complete. No push is made.

## Inputs

Runtime source: DE a80770316776d7f14878adb2235d18a7528a0d33.
Source archive SHA256:
435fe1adcb5a45ae2213480ea86baca84d74ce27af4c666cc348b260bf5b9b24.

The optional host recipe now declares iproute2, procps and util-linux for the
concrete network creation/recovery layer. Installation still enables no service,
changes no accounts/common PAM and replaces no display manager.

- debian accounts: out/migration/profile-journal-debian-accounts/karyo-profile-accounts-20261121T181115Z-ccf6d246; 69256 bytes; SHA256 ef65b839ec7cedf193014a90a075dc1c7d7a3d5feb05fd2d5140e38c592afa21.
- debian host: out/migration/profile-journal-debian-host/karyo-profile-host-20261121T181127Z-4a39bb67; 31660 bytes; SHA256 aa32dcc1020f9a775cfe8d1d4a579a1358e586b88a2f9b9d1f06c9af598e61a9.
- ubuntu accounts: out/migration/profile-journal-ubuntu-accounts/karyo-profile-accounts-20261121T181114Z-790f0ec7; 70330 bytes; SHA256 2765c7bc8816fd8ec5a893c8f29ba96125c979bc02c57948b52eecbaf1199eae.
- ubuntu host: out/migration/profile-journal-ubuntu-host/karyo-profile-host-20261121T181125Z-0f6c792e; 32024 bytes; SHA256 f9d4ade9736f7772be769b4eae54dc56bce653177da93be4198d7cfa7dfc0ccc.

The public installed DE probe profiles/tests/installed-journal.py has SHA256:
672bafe5cf8c6e0a25a300e6bfade1fe29dc1f75cad590cde026d87edc4f4b17.
Both disposable QA guests execute these exact root-owned bytes against installed
packages, with no Python source overlay. The fixed-host probe contains no
credentials and accepts only its internal controller branch argument.

## Ownership contract

RuntimeJournal owns a lifetime flock separate from the per-operation ConfigStore
lock. Its /run/karyo/profile-host directory is root-owned 0700, and its state and
controller lock are root-owned 0600. The bounded strict JSON schema pins the boot
and lock inode, typed account/source identity, random network token, namespace
device/inode, veth indices and MACs. Unknown fields/schemas, duplicate identities,
unsafe file types/permissions/links, changed content/inodes, unknown directory
objects and a competing controller are rejected without overwriting state.
Snapshots are copies. Journal close releases descriptors, never resources.

JournalNetwork checks an eligible offline family child and persists creation
intent before the native namespace mutation. A captured complete receipt replaces
that intent only after native verification. Removal intent precedes cleanup and
the record is removed only after acknowledged teardown. Multiple leases of the
current controller may coexist; old unreconciled entries prevent new allocation.
Password hashes and external credentials never enter the journal.

Host startup reconciles this network-only schema before serving requests. It
checks the unchanged offline account, pins the recorded namespace and verifies
veth indices, aliases and MACs, plus absence of consumers. It can finish an
interrupted removal after pair deletion or confirm a completed namespace removal.
Missing/replaced resources without a removal intent, changed proofs, live UID or
namespace consumers and unacknowledged creation retain state/resources. No
processes are killed and no replacement resource is adopted by name.

## Source and real-kernel acceptance

All 285 profile cases pass on Debian 13 and Ubuntu 26.04 as root (skip3) and
ordinary UID65534 (skip82). Nineteen new cases cover real root file descriptors,
permissions, atomic publication and interprocess controller exclusion, then
receipt/recovery/retention scenarios with the existing native-command fixture.
Previously public metadata still defaults to 0644; private atomic writes opt in
to 0600. Existing profile/source tests remain green.

Installed tests use the known two-session QA fixture to prepare an otherwise
absent UID1002 child. A fresh Popen child controller opens the real journal and
creates a real namespace/veth pair. The parent verifies its bounded receipt and
PID, confirms exclusion of a second controller, and SIGKILLs only that captured
child. Its kernel descriptors disappear as on a crash; named resources remain.
Both installed bases pass these cases:

- Active captured network: a new controller pins and closes the exact old network.
- Pair already removed under a recorded removal intent: recovery deletes only
  the still-pinned known empty namespace.
- Namespace already removed: recovery proves absence and clears only the receipt.
- Actual host startup: a root socket connection activates the installed host
  service, which recovers the nonempty journal before serving requests. The test
  observes an empty private journal while the service holds its lifetime lock.
- Unacknowledged creation: the fixed branch writes intent but performs no native
  mutation. Recovery refuses it and preserves exactly the original state bytes.
  The QA clears only that known synthetic no-mutation record; no production
  forget/adopt endpoint is introduced.

Host recovery service InvocationID/MainPID and fresh socket inode are captured;
only those owned units are stopped afterwards. The same installed host/private
network/mount transport probe also passes after the journal update.

Final logs under out/BASE-vm-qa/results:

- profile-journal-install.log
- profile-journal-native.log
- profile-host-native.log (post-journal transport regression)

Debian profile-journal-direct-native.log retains the earlier accepted direct
recovery cases before the service-startup case was added. Earlier host transport
evidence is preserved as profile-host-before-journal-native.log.

For every completed native case, links/routes/rules/nft/netns, resolver target/hash,
forwarding and the original active GUI match the initial state. Fixture cleanup
restores original account and common PAM bytes. Host units are inactive/disabled,
no socket remains, the private journal remains empty with its stable lock inode,
and dpkg verification/audit are clean. Main GUI shell PIDs36901/97122 remain
active/unlocked on VT8. Owner VM, Acer, donor and Forge are untouched.

## Remaining full runtime work

The current journal schema owns network receipts only. Resolver files/services,
user-manager, graphical service/logind scope, forwarding and VPN need typed
checkpoint/recovery in their dependency order before a complete profile can be
started through the host. Do not layer unjournaled resource creation onto this
schema or infer full GUI/VPN recovery from the network gate.

Public helpers still use existing-session switching and report DesktopStopped for
stopped targets. Long-lived full-graph supervision, physical network/DNS change
reconciliation, dependency/forwarding setup, source return after child logout,
primary Home restart and NetBird callback/socket integration remain required.
Profile catalogs, family clipboard and remaining platform/VMware integration
also remain open. Journal data in /run concerns the current boot's resource
ownership; durable account/configuration data remains in the existing /etc layer.


Later schema-2 private DNS ownership has its own accepted installed gate in
VALIDATION_PROFILE_DNS_JOURNAL.md. It extends the network-only schema without
claiming complete live graphical/VPN recovery.
