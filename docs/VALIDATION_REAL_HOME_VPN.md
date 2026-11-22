# Real Home WireGuard alongside public Work NetBird

This gate replaces the earlier synthetic blocking-Home policy with an actual
Home kernel WireGuard tunnel, private DNS and packet service. It then launches
real Work NetBird through the installed public runtime on both Debian13 and
Ubuntu26.04. Full migration remains active; the particular external ExternalProvider
client is not accepted by substituting a WireGuard fixture for its integration.

## Inputs and production boundary

Production packages are unchanged: accounts/session-entry from effc7cb and
host/runtime/NetBird client from d140e14, with their previously recorded hashes.
This step only adds native QA and documentation. Source suites are not claimed
to have been rerun for a QA-only change. The real inert NetBird0.82.1 provider
is installed and purged using the earlier hash-checked native vendor stage.

Own disposable NetBird0.82.1 realm, temporary setup-key enrollment and two real
Work peers are used; no private user account, token, VPN profile or endpoint is
used. PKCE was accepted earlier and is not repeated in this gate. Temporary lab
observation credentials are transferred only through private stdin/root0600
files and are deleted after the captured test. No credential is committed or
printed in the exported log. The external HTTPS probe validates IPv4 internally
and only exports a boolean, not the machine's WAN address.

WireGuard tools were added only to the QA guests, not DE dependencies:
Debian1.0.20210914-3 and Ubuntu1.0.20250521-1ubuntu1. Ubuntu's installed AppArmor
wg profile stays enabled and unchanged. Root0600 keys reside under the allowed
absent-before /etc/wireguard/karyo-qa-home directory, not an AppArmor exception.

Exact QA source SHA256:

| DE actor | SHA256 |
| --- | --- |
| profiles/tests/installed-home-wireguard.py | 35ea14a710a112107eab852684b001ad88088de3b3abde69ee039194f5605de1 |
| profiles/tests/installed-public-netbird.py | 73f6381d2f7138eda99b1d70dfe2978b06b35bb71c7f51ca59218310000a7713 |
| profiles/tests/installed-netbird-peers.py | 0349066f637b1698801534bc51fac56630ba57d80f16ebd7250f53fe6f742ea9 |

## Actual Home tunnel

The fixed-host root controller creates unique absent-before WireGuard links and
a private peer namespace behind a captured veth pair. Native kernel keys and
handshakes carry traffic between10.240.254.1 and10.240.254.2. The peer owns only
its QA service address198.18.0.77 and answers the home-tunnel.karyo.test zone.
Its ordinary qaadmin server has only CAP_NET_BIND_SERVICE for DNS, in the
captured peer namespace; it is not a globally privileged application daemon.

A real Home IPv4 default policy routes through kq-home-wg. Explicit physical QA
LAN and WireGuard transport exceptions preserve control/management access.
The host's physical default route remains intact, as with a policy-routing VPN.
The interface advertises DNS routing domain~. through actual systemd-resolved.
An ordinary Home process resolves the QA name and exchanges a4096-byte TCP
payload, validates its digest and the source10.240.254.1 seen by the peer. A real
kernel handshake and nonzero received/sent WireGuard counters are required.

This service endpoint is on the other side of the encrypted tunnel. It is not
a synthetic ip-rule blackhole or a mocked resolver. The QA peer deliberately
does not act as a general Internet exit; Home Internet egress is not claimed.

## Simultaneous Work evidence

With Home already carrying its own DNS/TCP, each installed public helper cold
starts Work, enrolls real NetBird and verifies daemonStatus Connected. Both
Work sessions start ordinary peer services and exchange65536-byte TCP payloads
and UDP payloads by both the remote NetBird address and managed private FQDN.
All four digest/peer checks pass on each base. Actual packets trigger NetBird's
on-demand connection; an unused Idle channel is not treated as an offline device.

The QA controller uses the own realm's read-only management-online state to
identify the current counterpart, avoiding stale ephemeral peer records. It
checks that counterpart against the real CLI peer map. An ordinary incoming
TCP/UDP counter barrier proves reciprocal completion before either peer logs
out; a guessed grace delay is not used as proof.

On each base an ordinary Work process also resolves example.com, completes
external IPv4 HTTPS, and cannot resolve the Home-only QA zone. Meanwhile Home
still resolves its own zone and transfers through WireGuard. Existing Home/Work
switches retain the captured runtime/provider token. Connected Work logout
returns to the same captured Home, cleans the profile graph and leaves the
original Home VPN route/rule/nft/resolver snapshot intact. A further Home DNS/TCP
and kernel-counter probe passes after all Work resources have gone.

The selected Work peers here do not use a published NetBird exit-node default
route. The earlier exit-node packet gate remains independent; simultaneous Home
VPN plus a Work exit node is not established by ordinary external HTTPS alone.

## Failures retained and corrected in QA

- Initial Debian DNS used a .invalid name, which the native resolver rejected
  locally before transmission. The QA name now uses .test. This was not a DE
  resolver regression.
- Initial Ubuntu wg refused its key outside/etc/wireguard under AppArmor. Keys
  moved to its standard allowed location; no policy was disabled or weakened.
- The lab server's initial idle precondition rejected an already-created Home
  namespace. Known Home fixtures were first recovered, then the server was
  prepared before the real tunnel, in the correct dependency order.
- The first cleanup compared iproute2 dst and dstlen to a CIDR string. Native
  JSON normalization and complete rule validation now precede teardown.
  Exact known inode/alias/public-key and host snapshots guided successful recovery.
- The first joint Connected/DNS/HTTPS-only runs passed both bases. Strengthened
  reciprocal runs first raced offline peer records and early teardown; a later
  Connected-only filter waited forever on legitimate on-demand Idle peers.
  Their failures remain recorded and retained profiles were recovered through
  captured compositor/provider/runtime/account identities, not broad deletion.
- Final management-online selection, traffic-driven connection and explicit
  reciprocal barrier passed both bases. Prior failed handles were confirmed
  terminal before recovery or another run. Production routing and DNS were not
  weakened or changed to make these QA fixtures pass.

## Complete teardown and evidence

Final Work receipts and temporary provider package, admission keys and observation
credentials were removed. The Home fixture validates captured links, aliases,
namespace, server invocation and keys, then removes its DNS association, exact
policy rules, links, namespace and root-owned key directory. Original route,
rule, nftables, resolver and forwarding snapshots compare equal. Finally the
own realm/server/owner/key state is removed. Remaining QA tools are not shipped.

Final postchecks0 on both bases prove unchanged Home baselines from checkpoint251:
Debian shell288593/login1631/VT7; Ubuntu shell406670/login1808/VT7, active/unlocked.
Journal7 is empty, forwarding0, runtime/host services inactive, host socket
disabled/inactive, and no child/provider/private DNS/NET/veth/NAT/Home-WG resources
or credentials remain. Package verification and dpkg audit are clean.

Ignored evidence is indexed with hashes and actual result JSON in
out/migration/netbird-home-vpn-evidence.json. Main native logs reside in
out/{base}-vm-qa/results/netbird-real-home-vpn-native.log; Connected-only and both
peer-fixture failures are kept separately. home-wireguard-{prepare,probe,
after-netbird,cleanup}.log and netbird-home-vpn-final-postchecks.log record the
Home transport/lifetime/restoration checks. Lab preparation/cleanup logs live
under out/migration/home-vpn-netbird-lab-*. No new screenshots are claimed here.

## External provider boundary and remaining work

Remaining gates include provider-specific broker/firewall integration, live Home
VPN disconnect/reconnect while Work remains active, simultaneous Work exit nodes,
physical DHCP/DNS changes, onward NetBird GUI/tray, family clipboard and the
remaining Wine/macOS/VMware integrations. Full goal remains active. No push,
Forge change, personal VM or Acer operation occurred.
