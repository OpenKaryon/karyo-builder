# Live physical-route metric acceptance

DE `d5bffcb` fixes a false reconciliation requirement for an already-owned
forwarding lease. A host route's metric ranks candidate physical paths; it does
not appear in the pinned private route plan. Live verification now compares the
selected interface, kernel index, address, prefix and gateway. Cold creation
still verifies the complete discovery snapshot. Native private routes, rules,
firewall identity and contents remain checked exactly.

## Before and after on both native bases

Use only the two disposable kernel guests, Debian13 and Ubuntu26.04. Start the
fixed laboratory NetBird server at its documented QA address and wait for API
readiness before preparing either Home WireGuard fixture. The first preparation
attempt timed out before the API existed, with no public Work started. Both
Home/endpoint fixtures and the captured server were removed with exact rollback;
its logs are retained in `physical-metric-before-v1`. The separate v2 attempt
prepared the server first and completed. This is not hidden as a passing run.

The public actor creates an ordinary Work through the installed profile entry
point, enrolls it in the separate temporary realm and verifies reciprocal
65536-byte TCP/UDP traffic by IP and FQDN. Its root-only control socket admits
only root peer credentials in a root0700 directory. The captured session,
namespace, forwarding objects and provider invocation are reused throughout.

`installed-public-metric-control.py` creates a root0600 write-ahead intent, then
adds exactly one additional static main-table default through the same real
ens33 gateway/source with a free lower metric. It never removes or rewrites the
OS-owned DHCP default, connection profile or resolver configuration. Both native
bases select metric99 instead of100 with the same physical identity.

An observer restores and verifies the captured forwarding receipt without
acquiring the active controller's journal lock or permitting journal writes.
It closes only its own pinned namespace descriptor. Unexpected errors are not
accepted as the old regression. On the previous accounts package, both bases
produce exactly the physical-network-changed reconciliation error. Every owned
route, rule and firewall object is retained, and exact rollback restores the
original physical route inventory.

Build and reinstall only `karyo-profile-accounts` from the production commit
using the native trixie and ubuntu2604 Builder recipes. Verify artifact and
installed-module hashes, preserved account/PAM/display-manager configuration,
LightDM still active and clean dpkg verification. Do not replace the DE session.

Run the same public gate again. Both forwarding leases now verify while metric99
is actually selected. A fresh ordinary Work process resolves an external name,
performs CA- and hostname-verified HTTPS without proxy inheritance and confirms
that the Home-only name cannot resolve. The same session/provider graph remains.

Both before and after gates also repeat both actual public Work exit-node roles:
nonce TCP/UDP packets reach the other guest, masqueraded source and remote host
match, wt0 is selected and its RX/TX counters advance. DNS and verified HTTPS
work while each exit is selected; both Home tunnels still pass private-DNS,
digest TCP and real WireGuard handshake checks. Running Home/Work switches and
public logout clean up the captured profile rather than recreate it.

## Rollback and evidence

The preferred-route observer verifies the exact extra native row and retained
original inventory before deleting only its own route. It checks the complete
original inventory and selected physical path afterward. An uncertain add, ACK,
identity or rollback retains the root intent for explicit review.

Both full native runs finish with no QA child, public profile, provider, namespace,
endpoint, Home WG or lab credentials. The host socket/service return to their
original disabled/inactive state, IPv4 forwarding returns to0, both original
Home shell/login identities and VT7 remain, and accounts/PAM/DM and dpkg audits
are unchanged. The corrected accounts package is the intended retained update.

`out/migration/physical-metric-evidence.json` indexes both observations, exact
source actors, production/QA revisions, native package manifests and log hashes.
The four source-test runs each pass all479 cases: ordinary115 expected skips,
root3 expected skips on each base. The original source also reproducibly fails
the added metric regression before the production fix. Local logs live under
`physical-metric-before-v2`, `physical-metric-after-v2` and
`physical-metric-packages`; they contain no personal VPN profiles.

## Deliberate boundary

This accepts a metric-only change of the same selected physical path. Real
interface/index/address/subnet/gateway replacement, DHCP renewal, physical link
disconnect and physical DNS-source updates still require their own lifecycle
implementation and tests. External ExternalProvider broker/firewall integration and
NetBird GUI/tray remain separate requirements. This does not complete the full
DE migration or imply acceptance of untested network transitions.
