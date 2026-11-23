# Public Work exit routing with a simultaneous Home VPN

Both native QA guests pass cold public Work startup, ordinary exit-node selection
and reciprocal routed packet exchange alongside their real Home WireGuard VPNs.
This extends [Home reconnect acceptance](VALIDATION_HOME_VPN_RECONNECT.md), without
claiming the remaining external ExternalProvider, physical network or GUI boundaries.

The actor at DE `18914c1db946878e345e31e6b536a06919ce5376` starts Work through the installed public switcher.
Its private namespace, resolver, user manager, provider and graphical session
are captured in the existing runtime journal. Each provider enrolls into a fresh
own temporary NetBird0.82.1 realm. No user VPN profile, account or credential is used.

The root-only fixed-host QA controller opens a private local UNIX socket under
the existing root0700 admission directory. Bounded JSON requests require a root
SO_PEERCRED and permit only exit-payload or close operations. Before and after
each operation it verifies the same session/provider graph and Connected status.
The ordinary Work CLI receives and selects one published temporary default route;
an ordinary Work manager process sends nonce-bound TCP and UDP to the other VM.

| Origin | Selected exit | Actual evidence |
| --- | --- | --- |
| Ubuntu Work | Debian Work | Remote Debian hostname; selected guest's masqueraded source; wt0 route and increasing RX/TX |
| Debian Work | Ubuntu Work | Remote Ubuntu hostname; selected guest's masqueraded source; wt0 route and increasing RX/TX |

The endpoint has the same fixed test address on each native root host. Therefore
a local shortcut cannot pass the remote-host identity check. The route is deleted
by its captured API identity before reversing roles. While each default route is
selected, both Home fixtures independently pass their private DNS, digest-checked
encrypted TCP and actual kernel handshake checks. Both existing Home/Work switch
targets reuse their captured live graph; final connected logout returns Home.

## Exact inputs and restoration

The account package on both guests is built from DE
`27fc54a4e4270fe17adaf78dd14b0d6e34dffefd`, containing the generally applicable
[logind inventory race fix](VALIDATION_LOGIND_INVENTORY.md). Other installed
profile components retain their prior recorded package inputs; this is not a
joined current-HEAD deployment claim. Debian runs6.12.117+deb13-amd64 and Ubuntu
7.0.0-43-generic. Executed source actors are:

| Actor | SHA256 |
| --- | --- |
| installed-public-netbird.py | `9c1871eaac4c0888af3ffbe14d27ee5d6603ff73c75777e16724652e637144af` |
| installed-public-exit-control.py | `94aa66c1a87ae240bc483f3513241be2e3a007db1309d99284c4a17cade3a056` |
| installed-home-wireguard.py | `82fcb81917031ef7b5bc7e9c1066da0647bf0d990d712d154cd99923721b865d` |
| installed-netbird-peers.py | `0349066f637b1698801534bc51fac56630ba57d80f16ebd7250f53fe6f742ea9` |
| installed-netbird-lab-server.py | `f24df611d413e1caf1d3cd6cef2c37ae86e9d538392c84a1e02b921a8082d97f` |
| installed-netbird-exit-endpoint.py | `b6e4dc2f232588f1ab7cf6274b4e5f0310a3045734f4e77d004069d6b46fa4d7` |

Both postchecks verify empty runtime journals, removed Work namespaces and QA
accounts, disabled/inactive optional runtime, original Home shell/session/VT,
unchanged account/PAM/display-manager configuration, package verification and
dpkg audit. Captured teardown removes the provider, exact exit route, temporary
credentials, server realm, endpoint interfaces and Home tunnel. Original root
routes, rules, nft state, resolver and forwarding snapshots are restored.

The first attempt failed before exit selection: an unrelated SSH login vanished
between logind list/show, and the provider legitimately returned null peer details
before discovery. The former is fixed generally and tested with actual before/
after native logins; the latter is awaited by the QA actor while malformed types
still fail. Both first-attempt failures and their explicit identity-based cleanup
are retained under `out/migration/vpn-home-exit-v1`. The successful fresh realm,
packets and full restoration are under `vpn-home-exit-v2`; exact source and log
hashes are indexed by `out/migration/home-vpn-exit-evidence.json`.

## Remaining scope

This gate accepts packet routing and simultaneous Home tunnel independence.
Work external DNS/HTTPS while its exit route is selected remains a separate
scenario: earlier ordinary DNS/HTTPS acceptance ran before selecting this route.
External ExternalProvider broker/firewall interoperability, physical DHCP/DNS/networkd,
and onward NetBird GUI/tray acceptance also remain open. A kernel WireGuard QA
fixture does not substitute for the external ExternalProvider application.
