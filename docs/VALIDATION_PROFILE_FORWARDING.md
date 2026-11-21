# Installed physical profile forwarding

Accepted native runtime source: 088d33339f616357f49eba38c43179ca612217d2.
This is the physical IPv4 forwarding library gate, not the complete profile runtime.

## Exact native inputs

### Debian

- Output: out/migration/profile-forwarding-confirmed-debian/karyo-profile-accounts-20261121T143553Z-b0af19a4.
- Source archive SHA256: 757eec6d01e9ff97c69321ff7f4c303d403ce9969006ff8861d7fc509bf862c3.
- DEB SHA256: 73e650d73b238927ba3d95e08d494064ee59636cda1dc25ba2ae3a49709e9aba.
- Final native probe SHA256: 4c76d39d576b1cd35f2733eb078ead968ee303b7f04e6560e3e347267d986c52.

### Ubuntu

- Output: out/migration/profile-forwarding-confirmed-ubuntu/karyo-profile-accounts-20261121T143552Z-53f71c43.
- Source archive SHA256: 757eec6d01e9ff97c69321ff7f4c303d403ce9969006ff8861d7fc509bf862c3.
- DEB SHA256: d1b16914cbe2524e27b32aad43e4c42471e56d04e59488e2f9b32d0b46c125a2.
- Final native probe SHA256: 4c76d39d576b1cd35f2733eb078ead968ee303b7f04e6560e3e347267d986c52.

## Native code and regression coverage

The complete profile suite passes 178 cases on native Debian and Ubuntu, both
as root (three role-specific skips) and ordinary UID 65534 (42 skips). Physical
selection reads native main-table routes, link identity/carrier, connected IPv4
addresses and kernel sysfs device presence. It ignores lower-metric virtual VPN
routes, rejects ambiguous/down/expired/multipath candidates and reserves the
private /16. No NetworkManager-only discovery assumption is used: both QA VMs
actually use systemd-networkd and ens160.

The root library requires the profile configuration lock and an existing pinned
network lease with no consumers before mutation. An unused per-UID table contains
physical/private connected routes, a physical default and unreachable fallback.
Private source priorities 1–16 precede private return priorities 17–32. Numeric
iproute2 identities avoid table aliases masking collisions. Source/destination
selectors cover kernel reverse-source lookups as well as ordinary forwarding.
Foreign earlier policies, references to the private table, changed snapshots and
unacknowledged mutations are refused/retained rather than adopted or flushed.

An exclusive fresh nft inet table has a UUID comment and captured handle/full
contents. It admits only the expected private source/physical path, rejects
invalid private-source returns and applies narrow masquerade. No foreign chain
is modified, no host default is replaced, and the production library does not
toggle global forwarding or rp_filter. Native stdin is bounded to 4096 bytes.
Teardown removes only captured rules, the exact nft handle and recorded routes.

## Installed packet acceptance

Exact independent packages install no-remove without changing account/PAM/default
manager bytes; dpkg verification/audit stays clean and forged SSH callers remain
refused. Debian's missing nftables dependency is installed only in its disposable
VM; its service remains disabled. Ubuntu already has nftables. Neither package
activates a profile network service.

The opt-in fixed-hostname probe explicitly enables forwarding temporarily, then
creates an owned synthetic Home policy: physical LAN route, unreachable default
and unreachable physical-DNS /32 in a separate table/rule. Home route lookup and
its direct DNS connection fail. This is a synthetic policy, not an authenticated
ExternalProvider/NetBird deployment. Two profile namespaces exist concurrently, with
tables 40002/40003 and priorities 1/17 and 2/18. Actual route lookups choose the
physical interface on exit and each private veth for return traffic.

Each profile receives a validated DNS A response from the physical gateway and
establishes a real external TCP connection to numeric 1.1.1.1:443, checking its
private source address. No external DNS is needed for that TCP connection. Only
its captured physical default is removed; a new external route lookup must fail
through the unreachable fallback, then exact restoration and verification pass.

Three fresh cycles per native guest all pass: twelve private DNS/TCP exchanges
total, with every confirming DNS exchange reporting attempts=1. The DNS fixture
allows at most three one-second UDP attempts and validates transaction ID, reply
flag, response code and answer count. It does not treat a persistent timeout as
success. The TCP probe verifies a real bidirectional connection, not TLS trust or
application payload. A separate baseline HTTPS attempt observed a self-signed
interception chain; no private CA is imported or bundled to bypass that check.

After every cycle, original links, route/rule/nft contents, named namespace list,
all existing IPv4 conf sysctls, global IPv4/IPv6 settings and resolver target/hash
match exactly. Accounts/PAM and original shell PIDs remain unchanged. Main GUI
sessions stay active on VT8 (Debian shell 36901/session 595; Ubuntu 97122/session
765); no test desktop accounts are created. Only lo/ens160 remain; forwarding
returns to zero and no namespace, PBR, synthetic policy or nft table remains.

## Failed attempts and diagnostic limits

The first native capture received numeric RTN_UNREACHABLE type 7 instead of its
symbolic name. Production retained that unrecognized acknowledged sentinel and
its namespace. The final library normalizes only that known equivalent value.
A fixed ignored recovery script verifies exact failed-fixture UUID/namespace
inode/type, peer indices/MAC/aliases, private address and absence of consumers,
foreign rules or nft state, then removes that exact sentinel and pair. Its first
attempt omitted the manual pair-created flag, refused the remaining peer and
removed no unknown device; the corrected fixed recovery completed. No generic
adoption or cleanup sweeper is added to production.

Earlier interface-only reverse FIB queries from loopback failed under the Home
policy. Source/destination selectors now cover those queries. An exploratory
Debian diagnostic temporarily changed two rp_filter values and restored them;
timing also affected reply delivery, so that experiment alone does not prove
the cause of every timeout. Final production code and confirming probes leave
rp_filter unchanged.

Earlier single-datagram DNS probes timed out. Packet capture recorded correct
private ARP and a NATed DNS request on ens160, with no response observed entering
the VM in that failed capture. Other captures observed full request/reply/NAT
exchange. Preserve these failed runs rather than attribute all losses to one
kernel setting. The final fixture reports bounded UDP attempts and adds a
separate TCP test; all confirming exchanges succeeded without retransmission.
No blind readiness sleep or global source-validation weakening is added.

Logs are under out/{debian,ubuntu}-vm-qa/results/profile-forwarding-*:
first-native (numeric type), known-recovery and recovery-first, final-native and
accepted-native (earlier singleton timeouts), retransmit-native (first UDP/TCP
PASS), confirmed-native (three fresh final cycles). Debian packet-diagnostic,
exact-diagnostic, rpf-diagnostic, packet-trace, cold-arp-trace, physical-arp-trace
and delay-diagnostic preserve separate observations. Runtime manifests and final
probe SHA are under profile-forwarding-confirmed-input and the corresponding
out/migration/profile-forwarding-confirmed-{base} artifact outputs. Root/user
suite copies are under out/migration/forwarding-evidence/{base}.

## Limits and next runtime work

Ordinary physical IPv4 Ethernet/Wi-Fi gateways are supported by discovery;
bridged/bonded, point-to-point, multipath and IPv6 underlays are explicitly
unsupported at this stage. Existing administrative firewall drops still apply;
Docker/firewall-manager cooperation needs a tested integration. Reserved subnet
and early-priority conflicts are refused, not guessed around.

The future supervisor must explicitly provide dependencies/forwarding, validate
and stop owned consumers, retain leases and reconcile physical changes. There
is no enabled daemon, automatic crash recovery, private resolver mount, scoped
user manager, real NetBird daemon/UI/callback test or stopped desktop starter.
Current namespace verification intentionally refuses extra devices at teardown;
a live VPN lifecycle must distinguish readiness checks from strict post-stop
cleanup. Full family clipboard, Win32/macOS/VMware runtime/agents and remaining
compositor work are still part of the active goal. Forge, donor and owner
machines are untouched. All Git commits stay local; no push or ISO change.

Primary interface references: [ip-rule](https://man7.org/linux/man-pages/man8/ip-rule.8.html),
[nftables exclusive tables/handles](https://netfilter.org/projects/nftables/manpage.html),
[Linux IP sysctls](https://docs.kernel.org/networking/ip-sysctl.html) and upstream
[Linux v6.12 fib_frontend.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/torvalds/linux/+/v6.12/net/ipv4/fib_frontend.c).
The kernel source is read only for interface behavior; no implementation is copied.
