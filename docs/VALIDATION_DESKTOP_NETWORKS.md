# Per-desktop network preparation checkpoint

The new implementation target gives every managed desktop, including the main
account, its own network, DNS and network-service environment. Upstream VPN
executables remain unchanged; owned launch adapters are the primary path and a
cooperative provider API is optional. Karyo DE's `docs/NETWORK_ISOLATION.md`
defines the approved architecture and remaining installed acceptance matrix.

This checkpoint validates the first source-layer implementation, not a Builder
recipe/package update or a completed desktop/VPN feature.

## Inputs and execution

- DE runtime allocation change: `e0dbff9`.
- DE native fixture and precise acceptance limits: `b7a9300`.
- Debian GNU/Linux 13, native kernel `6.12.118+deb13-amd64`.
- Ubuntu 26.04.1 LTS, native kernel `7.0.0-44-generic`.
- Two independent full QA disk copies, each limited to one vCPU and 2 GiB RAM.
  The copies have separate MACs and DHCP leases. No user workstation VM is used.

Eight selected journal/preparation model cases pass on both native bases. They
run from temporary source overlays in the existing dedicated acceptance guests;
only temporary fixture files change, and their kernel implementation is mocked.

The separate `profiles/tests/native_main_network.py` runs on the new networking
copies with actual namespaces, private resolved/D-Bus instances and ordinary-user
clients. Its three temporary offline accounts represent main-network contexts,
not actual graphical Home/Work logins or a family-switch operation.

## Actual native observations

Each context resolves its own fixture name and exchanges TCP/UDP payloads with
an endpoint on its owned veth. A neighboring fixture name does not resolve in
that DNS view. Three namespace and resolver identities are distinct, and all
clients pass while the contexts coexist.

Stopping Home's captured endpoints/resolver/network leaves the other contexts
working. Recreating Home gives a fresh runtime token and working DNS/TCP/UDP;
neighbor namespace and resolver identities remain unchanged. Captured teardown
empties the journal and restores the original host links, routes, rules,
namespace inventory, forwarding value and resolver target/content.

Read-only postchecks on both networking copies find zero temporary fixture
accounts, zero fixture DNS/probe units and no remaining private namespaces.
No global forwarding, host resolver or installed login/PAM configuration is
changed by the fixture. Logs and preparation metadata remain local ignored QA
artifacts; no credentials or private client identifiers are included here.

## Remaining work

Main graphical entry must attach to the prepared context before application and
user-manager activation. Service/socket views, physical forwarding and IPv6
need their own implementation/observations. Then install the changed packages
and run real upstream WireGuard/OpenVPN/NetBird connections simultaneously,
including reconnect, exit routing, browser/GUI operation and profile retirement.

No actual VPN is started by this fixture. Source packet success does not imply
installed-package, graphical-session, upstream-client or arbitrary-VPN support.
