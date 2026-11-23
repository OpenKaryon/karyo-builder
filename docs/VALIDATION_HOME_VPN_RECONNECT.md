# Live Home VPN replacement with connected Work

The installed public Work runtime passes two complete Home tunnel disconnect/
reconnect cycles on each native QA guest. This extends the simultaneous-tunnel
packet gate in [VALIDATION_REAL_HOME_VPN.md](VALIDATION_REAL_HOME_VPN.md).
The full DE migration remains active.

## Executed boundary

The Home fixture removes its resolved DNS association, exact captured default
policy and actual WireGuard interface. Reconnect creates a new link identity
with the captured private key, peer, address and DNS policy. Reserved rules,
private root receipt, key metadata/public identity, links and peer server are
checked before mutation; partial phases retain captured resources for review.

Work starts cold through the installed public switcher and enrolls the pinned
inert NetBird0.82.1 provider into an own temporary realm. No user VPN account,
profile or endpoint is used. The same ordinary Work manager then runs fresh
Connected/DNS/HTTPS probes before and during each disconnection and after each
reconnect. Private network and resolver identities stay unchanged; the captured
session/provider graph and token are reused, rather than replacing Work.

| Phase | Home evidence | Work evidence |
| --- | --- | --- |
|Initially connected|Private DNS,4096-byte TCP digest, kernel handshake and encrypted counters|Connected, external DNS/IPv4 HTTPS, Home-only name hidden|
|Disconnected, twice|Actual link/default policy absent; external name lookup succeeds and private name fails|Same private namespace/resolver and graph; Connected/DNS/HTTPS succeed|
|Recreated, twice|New link identity; renewed kernel handshake/private DNS/encrypted TCP|Same provider/session, Connected/DNS/HTTPS succeed|
|After both cycles|Home tunnel still answers its own zone and payload|Reciprocal65536-byte TCP and UDP by NetBird IP and managed private FQDN; existing switches and connected logout|

External IPv4 is validated in probe memory and exported only as a boolean. The
Home lookup without a VPN link is a functional resolver check, not a separate
physical DNS packet trace. Neither this test nor ordinary Work HTTPS proves a
simultaneous Work exit-node default route. Browser PKCE was accepted separately
and is deliberately not relabeled as exercised here.

## Exact inputs and restoration

DE QA commit: 67dd969e7210f00a5097839cedef1960f6aab5ad. Both native guests use accounts/host/runtime/NetBird
client0.1.0-1 production packages already recorded by the earlier gate; production
routing source and packages are unchanged in this wave. Debian uses kernel
6.12.117+deb13-amd64 and Ubuntu7.0.0-43-generic. This is not a joined current-HEAD
installation claim. Source actors are:

| Actor | SHA256 |
| --- | --- |
| installed-home-wireguard.py | `82fcb81917031ef7b5bc7e9c1066da0647bf0d990d712d154cd99923721b865d` |
| installed-public-netbird.py | `08b8f109f374d33134fee19db27dbecf8b729b750dc82ea67a2c826dbce56694` |
| installed-netbird-peers.py | `0349066f637b1698801534bc51fac56630ba57d80f16ebd7250f53fe6f742ea9` |
| installed-netbird-lab-server.py | `f24df611d413e1caf1d3cd6cef2c37ae86e9d538392c84a1e02b921a8082d97f` |

Both public actors return0, complete both cycles, pass reciprocal private peer
traffic and log out. Their captured runtime activation, optional provider and
admission/observation credentials are removed. Home still exchanges encrypted
traffic after Work closes; its own final teardown restores the original route,
rule, nftables, resolver and forwarding snapshots exactly. The current captured
lab controller removes its server, directory, temporary owner/keys and binary.

Dedicated final postchecks on both bases prove original active/unlocked Home
shell/login, empty schema7 journal, forwarding0, disabled/inactive optional
runtime socket, inactive host/runtime services, no child/provider/vendor/private
network/DNS/NAT/Home-WG/laboratory resources and clean dpkg verification/audit.
Original account/common-PAM hashes also match. Fixed QA helpers and inert staged
inputs remain only in the disposable QA guests.

The joined hash index is out/migration/home-vpn-reconnect-evidence.json. Complete
native logs, installed versions and fresh postchecks are under
out/migration/vpn-home-reconnect-v1/. Each receipt binds the exact current actor
hash, commit, native result and log hashes; historical postchecks are not used
as substitutes for this gate's dedicated final logs.

## Retained preparation failures and limits

Initial preparation mistakenly reused an older ignored local setup script. It
omitted the server data directory and polled GET /api/setup, which is a POST-only
route in the pinned source. The proper readiness endpoint is GET /api/instance.
The stopped, captured fixture was repaired by identity, then the already-running
server was resumed without replacing it. Those failed logs remain. Current
tracked installed-netbird-lab-server.py already contains both corrections and
performed final status/cleanup; future runs should use that actor directly.
This was a QA setup issue, not a DE routing change.

The external ExternalProvider client/broker integration, simultaneous Work exit-node
routing, physical DHCP/DNS replacement, onward NetBird GUI/tray and remaining
VMware/macOS/final joined-head gates still require acceptance. No new screenshot
or user-machine evidence is claimed. No push, Forge/donor/distro modification,
working Karyo VM or Acer operation was performed.
