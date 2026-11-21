# Real exit-node forwarding between disposable profile guests

Debian13 and Ubuntu26.04 now pass actual TCP and UDP forwarding through each
other's captured NetBird profile as an exit node. A digest-checking endpoint
outside that profile observes the selected router host and its masqueraded
profile address. This is forwarding evidence beyond Connected status or traffic
terminating locally on the router's overlay interface.

## Exact inputs

Production remains the eight installed DE packages from
`25273daa8aac34426787a7c78be1cd2b55867ea9`, source archive SHA256
`b9731d0501e744c1d833ac44375b518c44939d16630650bf476e6e73975ed438`.
See VALIDATION_PROFILE_NETBIRD_CONNECTED.md for package and public external
NetBird0.82.1 input digests. No product code or package changed in this QA wave.

QA-only DE revision: `a46e3819ed8ce817c56ad0618e370b68797d40d0`.
- `profiles/tests/installed-netbird-peers.py` SHA256: `0349066f637b1698801534bc51fac56630ba57d80f16ebd7250f53fe6f742ea9`.
- `profiles/tests/installed-netbird-exit-endpoint.py` SHA256: `b6e4dc2f232588f1ab7cf6274b4e5f0310a3045734f4e77d004069d6b46fa4d7`.
- Safe coordinator evidence `out/migration/netbird-exit-observations.json` SHA256:
  `847b876276799eb26c24ccb4b9a7ee735e9b89a5f596b85a4f5fe969dbf1e8eb`.

The pinned upstream0.82.1 route OpenAPI/handler and CLI networks command were
inspected. The lab runner creates a temporary enabled `0.0.0.0/0` route with
`network_id=karyo-qa-exit`, an explicit router peer, All distribution/access groups,
masquerade enabled and automatic apply allowed. The ordinary client waits for
publication and uses `netbird networks select karyo-qa-exit`; it does not rely on
an unsupported `up --exit-node` flag. The route is withdrawn and its captured API
identity checked before each role reversal. The existing server helper controls
only its own ephemeral realm; PAT/admission material remains private and no real
user profile or management endpoint is imported.

## External endpoint ownership

An explicit fixed-host QA helper requires absent fixture, interface, native unit
and test-prefix routes before preparation. It creates `kq-exit-probe`, a dummy
interface with `198.18.0.11/32` from the reserved benchmarking range, in the main
host namespace of each disposable guest. A native transient server runs as
UID1000, with no capabilities, NNP, strict filesystem protection, private devices
and a private writable readiness directory. It binds only that address on43862.

The helper captures directory inode, namespace identity, interface kind/index/
unique alias/address and service invocation/PID/start/executable/cgroup. Cleanup
requires empty profile ownership and forwarding0, stops only that verified server,
deletes only the captured dummy interface and fixture, and compares original
host routes/rules/firewall/resolver state. It does not sweep existing interfaces.

Both guests intentionally have the same benchmark endpoint address. Replies carry
the endpoint's hostname as well as the digest and observed source. This catches
an accidental direct path to the client's own host: only the selected remote
router hostname is accepted. The address is not assigned to the router profile's
loopback, so packets must leave its overlay through the profile's routed side.

## Actual matrix

The ordinary user1002 manager first repeats the accepted bidirectional peer-IP/
private-NSS TCP/UDP matrix, with Home private-name/endpoint separation. Then:

| Client | Exit-node profile | Observed external endpoint | TCP/UDP source |
| --- | --- | --- | --- |
| Ubuntu Work | Debian Work | `karyo-de-acceptance` | Debian profile guest address `10.231.0.10` |
| Debian Work | Ubuntu Work | `karyo-de-ubuntu-acceptance` | Ubuntu profile guest address `10.231.0.10` |

In each role the client sends65536bytes by TCP and1024bytes by UDP. Both responses
match the payload digest, report the correct remote host and the expected
masqueraded source. The client's destination route is `wt0` in table7120 and its
RX/TX counters increase. Captured private rules include the provider's default
routing policy. Both roles passed on the first attempt, with no manual route or
firewall changes inside profile namespaces to make the provider forward.

The benchmark destination is on the router's main QA host, beyond its private
profile namespace. This proves routed/masqueraded egress over that boundary; it
does not claim a distinct public Internet exit address, arbitrary WAN paths,
IPv6 exit routing or all DNS behavior during a default-route change.

## Cleanup and remaining scope

Both temporary API default routes were removed through their captured identities.
Both peer controllers then returned Home and closed their captured graph/manager/
provider/DNS/forwarding/network without provider `down`. Host/account/PAM snapshots
were restored, extracted CLI/state/peer/admission fixtures removed. Endpoint
cleanup on each base restored its original main-host routing/firewall/resolver
snapshot and removed the dummy link, native unit and fixture. Finally captured
lab cleanup removed the server/data and temporary owner/PAT/setup key/binary.

The final postcheck on both guests returned0: original Home active/unlocked,
empty schema6 journal, forwarding0, host socket disabled/inactive, host/runtime
inactive, clean dpkg verification/audit, and no child1002/home, profile/provider
policy/state, vendor CLI/GUI, namespace/veth/NAT, endpoint/peer/admission/recovery/
lab fixture, dummy link or temporary endpoint/server unit remains. Fixed QA
helpers and public staged inputs may remain only in the disposable guests.
Logs: `out/<base>-vm-qa/results/netbird-exit-{endpoint-prepare,endpoint-cleanup,stderr}.log`
and Debian `netbird-exit-server-cleanup.log`.

These are QA-only changes, with native behavior exercised on both bases; the
prior425-case root/ordinary runtime regression remains the unchanged product's
source evidence. Home tunnel interference, real browser PKCE and GUI/tray,
inert vendor/catalog packaging and public VPN startup remain open. Public VPN
still refuses before allocation, and the full DE migration is active with no push.
