# Ordinary DNS and HTTPS with selected Work exits and live Home VPNs

The follow-up native gate now also passes ordinary Work DNS and TLS HTTPS while
each reciprocal exit route is selected. This closes that explicit limit in the
earlier [public exit packet gate](VALIDATION_HOME_VPN_EXIT.md); the earlier packet
evidence and its actor hashes remain a historical record of its narrower scope.

At DE `ce3f44c67bd8f3a35e767832e24dbfe2364a51d3`, the fixed QA controller executes a fresh ordinary Work Python
process through its captured user manager. Before deleting the exit route, this
process resolves the external service, performs a certificate-verified HTTPS
request without environment proxies and validates its public IPv4 response.
The address is retained only in probe memory; the exported result is boolean.
The same process verifies that Home's private DNS-only name cannot be resolved.

Both Ubuntu Work via Debian Work and Debian Work via Ubuntu Work pass. Both
Home tunnels simultaneously pass private DNS, digest-checked encrypted TCP and
real kernel handshakes during each selected route. The same connected provider/
session graph is reused. The earlier route, remote hostname, masqueraded source,
TCP/UDP nonce and encrypted-counter checks also run in this fresh realm.

## Inputs and exact restoration

Both guests retain the accounts package from DE27fc54a and the already recorded
host/runtime/provider inputs. This is an additional installed component gate,
not joined current-HEAD session deployment. Debian runs6.12.117+deb13-amd64 and
Ubuntu7.0.0-43-generic. The newly executed actors have these exact hashes:

| Actor | SHA256 |
| --- | --- |
| installed-public-netbird.py | `8e790ba70905cb3bb2a2003d44eb4294e4b638813bc5faf4b952cbf35c80c713` |
| installed-public-exit-control.py | `a63a996e2a16a9dca08ffcd0f1fdef3bbb39ccfec57bd8ca4662439ec36ea4f7` |
| installed-home-wireguard.py | `82fcb81917031ef7b5bc7e9c1066da0647bf0d990d712d154cd99923721b865d` |
| installed-netbird-peers.py | `0349066f637b1698801534bc51fac56630ba57d80f16ebd7250f53fe6f742ea9` |
| installed-netbird-lab-server.py | `f24df611d413e1caf1d3cd6cef2c37ae86e9d538392c84a1e02b921a8082d97f` |

The result and all log hashes are indexed by
`out/migration/home-vpn-exit-dns-evidence.json`; fresh realm, probes and postchecks
are under `out/migration/vpn-home-exit-v3`. Both postchecks prove empty runtime
journals, absent Work namespaces and temporary resources, original Home shell/
session/VT, unchanged account/PAM/display manager, clean package verification
and restored root network/resolver/forwarding snapshots. This includes Debian
after the independent Darling debugger installation; no account or Home change
is hidden by that installation. The exact temporary server, provider, exit route,
endpoint, Home tunnel and admission credentials are removed.

These fresh in-Work DNS/TLS checks execute while the exit is selected; they do
not export or compare the host's public address, and are not a separate physical
DNS packet privacy trace. External ExternalProvider broker/firewall interoperability,
physical DHCP/DNS/networkd and NetBird GUI/tray still need their own acceptance.
