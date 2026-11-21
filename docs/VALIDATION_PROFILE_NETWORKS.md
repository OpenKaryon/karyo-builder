# Installed owned profile network primitive

Accepted native runtime source: b56892acd35ff3ac089193aa3f0190262527f32b.
This gate is the namespace/veth kernel resource layer, not complete profile networking.

## Exact native inputs

### Debian

- Package output: out/migration/profile-networks-accepted-debian/karyo-profile-accounts-20261121T135513Z-6b5c5555.
- Source archive SHA256: 86409f218254765a360581e692cdbf946ad2b61e1cf35b00d259c17df3eab174.
- DEB SHA256: 739fe96ae9180fe08ff2999613914c8c693ecf103fd8605d000776a97f4d3f60.
- Native probe SHA256: a657574476a59c74991be484406c2f5410609535aa5435257fe0db6a9e9bc5fa.

### Ubuntu

- Package output: out/migration/profile-networks-accepted-ubuntu/karyo-profile-accounts-20261121T135516Z-db647fdb.
- Source archive SHA256: 86409f218254765a360581e692cdbf946ad2b61e1cf35b00d259c17df3eab174.
- DEB SHA256: 44536bc0c595498814e9175046907227a35bcb4439bc9e7699c87c9b52c29e2d.
- Native probe SHA256: a657574476a59c74991be484406c2f5410609535aa5435257fe0db6a9e9bc5fa.

## Accepted behavior

The native profile test suite passes 157 cases on both bases, as root (three
role-specific skips) and ordinary UID 65534 (42 skips). New cases cover a bounded
UID/private-/30 pool, literal ownership tokens, root/config-lock enforcement,
namespace/link/route collisions, pinned namespace replacement, peer index/type/
alias/master changes, unknown devices, live consumers, acknowledged rollback,
lost mutation acknowledgements and partially applied tags. Native command output
is bounded, uses a minimal environment and accepts no shell fragments. The kernel
gateway precondition regression failed before the final ordering fix.

Native account packages are built and installed independently, with exact source
and artifact hashes checked. Installation uses no-remove and retains existing
account/PAM/default-manager bytes; package audits stay clean and forged SSH
profile callers remain denied. No full C++ rebuild is needed for this library
change; the complete Python profile suite runs on both native bases.

The installed fixed-hostname QA probe holds two fresh namespaces for UID pool
slots 1002/1003 without creating accounts. Both have distinct native namespace
descriptors and independent peer indices; descriptors are close-on-exec. Native
ICMP reaches each private host endpoint and no IPv6 addresses exist inside.
A specifically owned sleep process blocks cleanup without being terminated;
a changed host alias likewise blocks deletion until the fixture restores only
its exact known interface. A duplicate UID/subnet is refused before mutation.
After normal closure the original links, routes, rules, namespace list, global
IPv4/IPv6 settings and resolver target/hash match their initial snapshots.

Post-acceptance checks leave only lo/ens160, no named namespaces, clean dpkg
verification/audit, and the same unlocked active VT8 sessions: Debian shell
36901/session 595; Ubuntu shell 97122/session 765. No owner VM or Acer is used.

## Failures retained in evidence

The first probe's snapshot tried to decode an empty `ip -j netns list` response
as JSON. Correct only the QA snapshot to compare the native namespace list as
text. That failure occurred before resource creation.

The next native run showed that acknowledged veth creation did not apply aliases
included in the creation request. Production refused the unknown ownership and
retained those incomplete resources. Recover only the exact known QA objects,
after separately verifying native namespace type/inode, captured link/peer
indices, MACs, down state, empty addresses, no consumers and original route/rule
inventories. No generic adoption or wildcard recovery is added to production.

After explicit post-creation tagging, the private gateway route failed because
the peer interface was still down. Production removed its fully captured pair
and namespace. Move route creation after link readiness; add a reproducing unit
regression and rerun the full native suite and installed probe. Both pass.

Evidence under out/{debian,ubuntu}-vm-qa/results:
profile-networks-first-native.log (empty snapshot), profile-networks-native.log
(alias retention), profile-networks-known-recovery.log (exact QA recovery),
profile-networks-final-install.log (gateway failure and owned rollback),
profile-networks-accepted-install.log (final PASS). Input manifests/checksums are
in each VM's profile-networks-accepted-input folder. Root/user test copies are
under out/migration/network-evidence/{debian,ubuntu}. The gateway failing-before
log remains out/migration/debian/network-before-link-order-fix.log.

## Remaining scope

The future root supervisor must validate the account and absence of unknown
consumers, keep leases alive, stop only its proven units, and revalidate under
the profile configuration lock before teardown. Namespace PID inventory is an
additional guard, not a replacement for proving and stopping all owned units.
There is no automatic crash recovery or sweeping of older names.

No NAT, global forwarding policy, physical underlay selection, DNS mount view,
user-manager isolation, NetBird daemon/UI/callback integration or stopped desktop
startup is claimed. A later runtime package must supply native dependencies and
consume this primitive; installing profile-accounts alone enables none of them.
The host network is deliberately unchanged. Forge, donor and owner systems are
untouched. All commits remain local and nothing is pushed.
