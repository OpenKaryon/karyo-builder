# Distribution inputs for isolated desktop networking

The opt-in `examples/profile-runtime.json` recipe declares the unchanged
distribution NetworkManager, its graphical connection editor and OpenVPN plugin,
and WireGuard tools. They are runtime inputs, not bundled client forks. The
account-only recipe remains usable without pulling these network applications.
Standard distribution dependency installation retains its ordinary package
lifecycle; the Karyo runtime itself still requires explicit enablement.

The private worker uses root-owned per-desktop configuration/state, a captured
network namespace and resolver, and a private service bus. Debian uses its stock
keyfile backend; Ubuntu also runs its stock Netplan generator on private inputs
and outputs. The host retains physical Wi-Fi/Ethernet management.

The current DE source provides stock CLI/editor launch adapters. New worker
receipts publish a read-only context hint, and captured user-manager/child
environments select it. The ordinary default system bus preserves caller UID/PID;
temporary desktop UID rules exclude the host network-control services. This
does not replace normal administrator authorization.

Source-native QA on Debian 13 and Ubuntu 26.04 verifies real simultaneous
WireGuard and, separately, OpenVPN tunnels across three preallocated contexts,
private DNS/TCP/UDP, reconnect, worker retirement/recreation, later context
creation and host baseline restoration. A separate real graphical fixture uses
the normal user manager and stock CLI to create/list/delete a temporary private
connection. The editor's launcher help runs; GUI-editor actions remain untested.

These component gates are not current installed-package or complete mixed-VPN
Home/Work acceptance. Automatic production main/child service allocation, the
main graphical launch environment, physical network UI mediation, NetBird and
mixed-provider coexistence, IPv6/carrier changes and joined installed-session
validation remain required before that claim. No distro/ISO recipe is changed.
