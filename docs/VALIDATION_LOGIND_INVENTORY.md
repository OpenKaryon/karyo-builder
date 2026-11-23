# Complete logind inventory during unrelated login churn

The installed profile package at DE revision `27fc54a4e4270fe17adaf78dd14b0d6e34dffefd`
passes an actual disappearing-login regression on Debian 13 and Ubuntu 26.04.
This fixes a race found while preparing the simultaneous Home VPN / Work
exit-node gate; that larger network gate is not accepted by this result.

A real short SSH/PAM login is first observed in the actual `loginctl` inventory.
The QA command wrapper then waits until logind can no longer read that login
before returning the original list to the installed module. No synthetic session,
cgroup, environment-based authority or fabricated loginctl output is substituted.

Before updating either guest, graphical-session, greeter and occupied-console
enumeration fail with SessionError; the previously protected owner inventory
already retries successfully. After the one-package update, all four operations
discard the incomplete result and succeed after reading a fresh complete list.
The original Home remains present, with its console reserved. The shared deadline
includes the list request and permits at most three attempts; permanent service
errors, malformed metadata and timeouts never establish an offline desktop.

All 477 profile source tests pass in both Debian and Ubuntu images as an ordinary
user (115 root-only skips), and as root (3 ordinary-user-only skips). Early harness
attempts lacked an init child PID or writable executable fixture directories;
their errors are preserved separately and are not classified as product failures.

The installed accounts module has SHA256
`4575e8ba1b9f7e0f686828a95734fffefe1f2009fb5edb0dcadbebc6f256f3f4`.
Both packages are built by Builder from that exact committed revision:

| Native base | Package SHA256 |
| --- | --- |
| Debian | `39ace665493c354f7763256be5a0f877f15935283391312f241342b59d183a9b` |
| Ubuntu | `a2b3eacc4f8b0fe00097131256dcfcb3e767d4517f7198920fc51ae686d0d8bd` |

The package version remains the development `0.1.0-1`. Installation preserves
account/group/shadow and common PAM hashes, the selected display manager and both
original graphical Home sessions. Package verification and dpkg audit are clean.
The failed preceding network fixture was removed through captured identities;
both native postchecks prove no private Work namespace, temporary provider,
forwarding rule, fixture endpoint or changed host-network policy remains.

Local receipts, package manifests, negative/positive native observations and log
hashes are indexed by `out/migration/logind-inventory-evidence.json`. The native
test drivers and detailed logs live under `out/migration/logind-churn`; source-test
logs are in the chat output directory. This is a component regression gate, not
joined-current-HEAD session acceptance, full VPN acceptance or migration completion.
