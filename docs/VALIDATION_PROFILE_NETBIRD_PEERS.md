# Ordinary NetBird peer payload and private NSS resolution

Two captured profiles in disposable Debian13 and Ubuntu26.04 guests now exchange
real TCP and UDP application data over their NetBird overlay, both by address
and through ordinary libc name resolution. Their Home user managers do not
resolve those private peer names or inherit the provider endpoint. This extends
Connected-state acceptance with actual data-plane and private-NSS evidence.

## Provenance and fixture

Installed production packages remain the eight artifacts from DE
`25273daa8aac34426787a7c78be1cd2b55867ea9`, source archive SHA256
`b9731d0501e744c1d833ac44375b518c44939d16630650bf476e6e73975ed438`.
Individual package and external NetBird0.82.1 server/CLI hashes are documented in
VALIDATION_PROFILE_NETBIRD_CONNECTED.md; no product code/package changed here.

QA-only DE revision: `4a71ecc746546346735e8b307f40402eaff3e2d4`.
`karyo-de/profiles/tests/installed-netbird-peers.py` SHA256: `e855552206c193c05b778f679148a423f1a2b87f94a99c5364ab01d84a3bf6e5`.
The fixed-host probe holds the typed network/forwarding/private resolver/provider/
graphical/user-manager ownership graph while a host runner coordinates the two
peers through bounded JSON commands. It permits only the two disposable hostnames
and fixed root/ordinary QA identities. Root-only temporary admission is copied
to an inode-captured child-owned key file; no key value is passed in argv.

The same captured unprivileged combined-server helper creates an ephemeral realm
on the private VM address. No real user account, private endpoint or VPN profile
is imported. Extracted client binaries use verified public DEBs without vendor
postinst or global service setup. Server/private admission material is removed
through captured cleanup, and safe evidence contains no setup key or credential.

## Actual matrix

Each ordinary user1002 manager starts a TCP/UDP server bound only to its own
overlay address on43861. The root controller captures its native unit invocation,
PID and start time, verifies consumers while it lives, and stops only that same
server before graphical teardown. The server handles TCP segmentation with an
exact bounded read; payload replies include the digest of received bytes.

| Origin | Destination | TCP by IP/name | UDP by IP/name | Private name via NSS |
| --- | --- | --- | --- | --- |
| Debian Work | Ubuntu Work | 65536bytes each, digest matches | 1024bytes each, digest matches | Exact destination overlay IP |
| Ubuntu Work | Debian Work | 65536bytes each, digest matches | 1024bytes each, digest matches | Exact destination overlay IP |

No resolver override or extra environment is supplied to payload clients. Their
normal Python `socket.getaddrinfo` uses the profile's mounted resolver/NSS path.
The exact destination route is `wt0`; its RX and TX byte counters increase during
the exchange. Both root controllers verify the living provider and scoped user
consumers before each observation.

For each exchange an ordinary Home user1001 manager queries that same private
name: no address is returned (`EAI_NONAME`), provider endpoint is absent and the
network namespace differs from Work. This is DNS/environment separation evidence,
not a claim that every conceivable external route or VPN combination was tested.

## Evidence and cleanup

Safe coordinator report: `out/migration/netbird-peers-observations.json`, SHA256
`408ff53d7b2b478a55196ed49c334806b2e3e33e8880ad917ad776950f68a1d2`. It captures both ready packets, actual route/link-counter and ordinary
client/Home results, then both successful closed/host-restored packets. Exactly
one exchange in each direction was needed; all checks passed on the first run.

The controller returns the original Home, waits for natural manager exit, closes
provider/DNS/forwarding/network without `netbird down`, verifies host route/rule/
firewall/resolver snapshots and account/common-PAM hashes, and removes its known
previously absent state/peer/key fixtures and exact extracted CLI. Admission
cleanup additionally checks captured directory/key inodes and digest.

Both final postchecks returned0 after lab-server cleanup: original Home shell/
login active and unlocked, empty schema6 journal, forwarding0, host socket disabled
and inactive, host/runtime inactive, dpkg verification/audit clean. No child1002,
manager/provider policy/state, vendor CLI/GUI, namespace/veth/NAT, peer/admission/
recovery/lab fixture or temporary server binary remains. Public staged inputs
and fixed QA helpers may remain only in the disposable guests.

This is a QA-only extension. The prior425 root/ordinary profile discovery runs
remain the source-runtime evidence, and actual connected controller-loss recovery
has its separate accepted gate. Exit-node routing, Home tunnel interference,
real browser PKCE and final GUI/tray, inert vendor/catalog packaging and public
VPN startup are still required. Public configured VPN continues to refuse before
allocation; the full standalone DE migration remains active and nothing is pushed.
