# Installed schema4 forwarding journal and private DNS GUI lifetime

This gate owns physical forwarding across controller restart and joins it to the
observed GUI/DNS lifecycle. This historical layer gate precedes the later explicit setup/public startup
acceptance in VALIDATION_PROFILE_PUBLIC_RUNTIME.md. The whole migration remains
unfinished. No push, owner-machine,
Forge or donor changes are performed.

## Exact runtime inputs

Installed DE source: b3e832e845064887815cc2963bb0e2af10e59a22.
Source archive SHA256:
f19a49bc6068ebf84cc7ef85213bce6672ac9e3a6881845e76680a853bcfa1f1.

- debian accounts: out/migration/profile-forwarding-journal-debian-accounts/karyo-profile-accounts-20261121T203447Z-3071fe66; 84412 bytes; SHA256 48a378695448b1dc3170e699bcf9619231fb9c0cb7cf05fa931219a4c3f7ac57.
- debian host: out/migration/profile-forwarding-journal-debian-host/karyo-profile-host-20261121T203501Z-bc506a85; 35224 bytes; SHA256 0e68ef43f878a38fa09048e2221d376b5abead4f98a1ab4cb361f0ce91db21d7.
- ubuntu accounts: out/migration/profile-forwarding-journal-ubuntu-accounts/karyo-profile-accounts-20261121T203722Z-0faba47a; 85690 bytes; SHA256 22dddc9b7d55e52b5d1f2f9ca7c413540ccc09ed199779d434788c4422c5fd5c.
- ubuntu host: out/migration/profile-forwarding-journal-ubuntu-host/karyo-profile-host-20261121T203737Z-0e04ff1f; 35652 bytes; SHA256 c8e6d827df0337ea47f8c62fb5ddcff900d313273635f6faad32a5db278da807.

Final public DE probes, executed as those exact root-owned bytes in both guests:

- profiles/tests/installed-journal-forwarding.py SHA256
  9286a75d32da0d7682b4a7ae21ca335c394bc9e73ee76c658ff79e1d6f428a2c.
- profiles/tests/installed-supervision-forwarding.py SHA256
  ddd138581c1ef1ef0b2e0728597c470c2deb909297110e76fc62d959c4f19026.

No Python source overlay is used. Earlier unblocked tests remain separately in
profile-{forwarding-journal,supervision-forwarding}-unblocked-native.log.

## Typed ownership and removal ACKs

Schema4 adds an optional forwarding record before DNS; old schemas1-3 remain
readable. A fixed physical underlay, priority pair, ordered route/rule snapshots
and comparison-only nft JSON with the original UUID comment/table handle are
validated. Deletion argv is reconstructed from the fixed spec/physical route plan,
never loaded from a recorded command. DNS and forwarding must share a physical
seed, and DNS cannot coexist with forwarding mutation intent.

Close records remove intent before native changes. Each acknowledged reverse-
order rule, nft table and route deletion checkpoints its remaining proof. A new
observer verifies the current native state; interrupted removal may reconcile
exactly the next fixed step before continuing. Changed selectors, non-suffix loss,
foreign/replaced nft handles, unknown creation and inconsistent dependency order
retain ownership/resources. No unknown object is adopted or flushed by name.

Living session observers verify an acknowledged forwarding lease when present.
Teardown is GUI/manager, DNS, forwarding, namespace. Offline DNS recovery also
closes its captured forwarding before namespace recovery; lower layers refuse a
higher owner. This production layer does not toggle global forwarding/sysctls.

All 357 profile tests pass on Debian13 and Ubuntu26.04 as root (skip3) and ordinary
UID65534 (skip99). New cases include real private schema4 files/reopen/interlock,
no-recreation reattachment with consumers, all seven interrupted ACK steps,
selector/route/firewall/dependency rejection and lifecycle order. Builder recipes
are unchanged; four pinned native DEB builds validate packaging. C++ is unchanged.

## Ten forwarding crash/packet cases per installed base

The fixed probe explicitly enables IPv4 forwarding only for its lifetime. It
captures a fresh synthetic Home table59000/rule100 with a physical LAN route,
unreachable external default and unreachable physical DNS /32. Home route lookup
and its direct DNS request must fail before private-profile acceptance begins.
This is a test policy, not a personal authenticated ExternalProvider/NetBird tunnel.

A proven new synthetic child owns a journaled namespace and forwarding. After
controller SIGKILL, reattachment keeps the same native identities and exchanges a
valid DNS A reply with the physical gateway plus a real bidirectional TCP connect
to numeric 1.1.1.1:443 from private source10.231.0.10. TCP proves connectivity,
not TLS certificate trust or an application payload. All ten cases pass:

- Normal acknowledged close.
- Living forwarding reattachment plus real DNS/TCP despite blocked Home policy.
- Seven actual SIGKILL boundaries after each native delete and before journal ACK.
- Actual installed host socket startup reconciliation.

Current results/profile-forwarding-journal-native.log records Home policy/DNS
blocked, both DNS answers and TCP success, every recovery step and final PASS.

## Joined private DNS/NSS and GUI lifetime under blocked Home

The second fixed probe uses the same synthetic Home block and combines namespace,
forwarding, private DNS/bus, scoped manager and PAM compositor. The installed host
reattaches the living graph. A root QA client enters that captured graphical
cgroup and network/mount context, contacts the host and executes ordinary
getaddrinfo through the mounted resolver plus external TCP. This is not a new
interactive polkit/PAM authorization or locked-user access claim.

All four cases pass on each base: normal logout through the scoped user manager,
verified compositor pidfd crash, background exit and initial-lock compositor
crash. Each case resolves two IPv4 answers, reports TCP source10.231.0.10, makes
one actual host return decision and finishes GUI/manager, DNS, NAT and namespace
cleanup. Background keeps the already active Home. No further client request
drives teardown. Results are profile-supervision-forwarding-native.log.

## Cold UDP failure and diagnostic limits

The first strengthened blocked-Home probe used three one-second UDP attempts and
failed in both guests after its clean case. It retained the exact acknowledged
NAT/network receipts and QA account, while restoring global forwarding and the
synthetic policy. Those failures remain in
profile-forwarding-journal-cold-3s-failed-native.log; they are not accepted passes.

Read-only FIB/owner checks and a controlled Debian diagnostic used the captured
receipt. A fresh blocked-policy namespace lost its first three UDP attempts, then
resolved on a subsequent attempt without any route change or FIB-probe operation.
Later explicit FIB lookups agreed in both directions. The recorded successful
retry was around five seconds after the initial query. This does not identify
whether ARP, the VMware DNS proxy, upstream DNS or another transient caused loss;
it does not prove a permanent routing/RPF defect or its fix.

Only the final QA query budget changed: at most six one-second attempts, fresh
UDP socket each time, transaction/reply/rcode/answer validation and failure on
persistent timeout. The production route/RPF/sysctl code was not changed to hide
the failure. Final blocked-policy probes pass with real correct responses
(attempts1 in the final logs). Failed receipts were recovered through production
journal recovery after exact fixed-token checks; no generic cleanup sweep was
introduced. Diagnostic logs are forwarding-home-policy-diagnostic.log and
forwarding-home-cold-diagnostic.log under Debian QA results.

## Compatibility, final state and remaining gates

On the final b3e832e runtime/schema4, old living-editor/lock, no-NAT supervision,
offline closing/preparation, DNS/network and private NET/MNT transport probes all
pass on both bases. Current profile-*-native.log files hold those results; earlier
ac3beda evidence is saved with before-forwarding-journal prefixes.

The final forwarding-journal-postchecks.log verifies original main shells36901/
97122 and logins595/765 active/unlocked on VT8, no temporary child/home/runtime/
policy, no private DNS or namespace/NAT/PBR remnants, forwarding0, empty private
schema4 journal (directory0700/files0600), socket disabled/inactive and service
static/inactive. All six public installed probe hashes, dpkg -V and --audit are
clean. Original account/common-PAM, resolver, routes/rules/nft and IPv4 conf
snapshots are restored. No personal VM, Acer or physical hardware was touched.

Still required: explicit optional host forwarding setup/dependencies and public
stopped-profile startup; physical DHCP/DNS reconciliation; already-dead/half-
closing startup replay, primary Home host-network restart and missing greeter
creation; actual NetBird/PKCE, catalogs, family clipboard and remaining Wine/macOS/
VMware integration. These tests do not claim a real authenticated VPN deployment
or universal physical GPU/Wi-Fi/camera/microphone support.
