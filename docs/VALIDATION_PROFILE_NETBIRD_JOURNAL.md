# Installed pre-login NetBird journal and controller recovery

Schema-5 provider ownership has native acceptance on Debian13 and Ubuntu26.04.
This completes the offline **pre-login** provider journal gate, not public VPN,
connected tunnel, graphical-owner recovery or the full migration. All commits
remain local. Forge, the private donor, owner VM and Acer were not modified.

## Exact production and package inputs

Installed DE revision: `f0bf1ad561ac2c7f6664c44896741d3746ea8d43`.
Source archive SHA256: `9427b735e1517eb075444aff362da7e7e8b1e60c9ebb889229a03aa80ec8773c`.
All eight package builds and both inactive installations returned zero. Native
QA was subsequently committed separately in `61e4e63`.

| Base | Component | Bytes | DE package SHA256 |
| --- | --- | ---: | --- |
| debian | accounts | 93072 | `3f8ab44698e180a4c355641e5b92dc155b0cee8afbb9c7e95d600604805064a5` |
| debian | host | 37432 | `f28a72c4ab46cdeeffb854010308d46428b97b1d47a8db1cf391be49f12af00e` |
| debian | runtime | 37392 | `a15468cfaa23166db85674d5480b5b5364a120deb4339bba99c7b3991fc0900f` |
| debian | client | 37196 | `c65a3d379efb57ff0d1a8c6f473e71ac46838ec03b52a352e62b8988c88e5c6e` |
| ubuntu | accounts | 94480 | `4d983a83d49010f81235958c2f67f5ce4d68513769e7bc199e9c5953d259fb5f` |
| ubuntu | host | 37898 | `9cf32406d0088041e465fff1fb728e8e0e3820984b10da9909f3c96fa5a494c1` |
| ubuntu | runtime | 37900 | `c9cbbb8a59e3ebcc4ee11758575372b0facbc5730d74010bcb27ab87c0a12b7e` |
| ubuntu | client | 37714 | `11974025d2f483502ff3d508d53c54193b16638f79bfbe7541cec83c4cbdcf79` |

Exact manifest paths remain in
`out/migration/profile-netbird-client-{debian,ubuntu}-inputs.json`. Individual
artifact folders and manifests preserve the revision even when a later gate
updates these input pointers. The native probe is
`karyo-de/profiles/tests/installed-journal-netbird.py`, SHA256
`823f8052d31e5c2d49bc606032946a61a09ecf3fb95c3cc176bcf7886b5433eb`.

External NetBird0.82.1 CLI is the same reviewed 15864072-byte archive, SHA256
`4adff2bbc1529942e914c181badfc17585c78f0532ccaf6c000f5c9300d9a632`,
obtained from the official HTTPS APT index. The exact binary was extracted into
the disposable guests without running the vendor global-service installer, and
removed only after matching its digest following successful cleanup. This is
not a signed-APT-chain validation claim. No credentials, setup keys or private
management URL were provisioned. No GUI or enrollment occurs in this gate.

## Journal contract

The root journal still reads schemas1–4 and upgrades to5 when provider ownership
is published. A provider record contains only fixed `netbird` kind, mutation
intent and native identity receipts. It carries no executable/path/command from
the client, opaque provider config, key or authentication URL.

State receipts capture root-owned state-directory and ownership-stamp device/
inode plus the user's captured home generation. Service receipts capture native
unit invocation, main PID/start time, executable, private network and runtime
identities, control socket and client metadata inode. All paths and unit names
are derived from the validated local account/token. Restore checks those native
objects and ownership, rather than adopting whatever currently has the same name.

Write-ahead intents precede state preparation, service start and stop. Missing
creation acknowledgement stays retained for administrator review. A recorded
stop may be completed after controller death only when the original process is
gone and no runtime objects remain; a changed service/account/receipt is retained.
Persistent opaque provider state is preserved by product cleanup.

Recovery runs only for an offline account without a captured graphical owner and
accepts only its verified private resolver and provider consumers. Unknown
consumers block cleanup. Provider shutdown precedes DNS, forwarding and pinned
namespace cleanup. The strict pre-login namespace inventory still refuses
connected/changed tunnel interfaces: this change does not add wt0 adoption or a
connected teardown policy. Public `VPN=netbird` startup remains refused before
allocation, without an ordinary-network fallback.

## Native crash matrix

Each disposable guest completed all four modes with the actual daemon settled
in `NeedsLogin`. Persistent state inode was reused across all runtime leases.

| Mode | Captured operation | Required result on both guests |
| --- | --- | --- |
| clean | Acknowledged normal provider lifecycle | Dependency-order cleanup and empty journal |
| active | SIGKILL the recorded controller while daemon stays alive | Reattach identical native service/state/socket/endpoint without a restart; status still NeedsLogin; clean close |
| service-stopped | Stop the owned daemon after writing intent; kill before clearing receipt | Recognize the completed stop without touching a replacement or restarting a daemon; clean lower layers |
| host-restart | SIGKILL controller with live provider; activate installed root host through its Unix socket | Startup reconciliation closes provider before DNS/forwarding/network and retains lifetime journal lock |

Only the captured controller PID is killed. The gate verifies the lifetime lock
while it is alive, exact receipts after its death, original active Home login,
unchanged host routes/rules/nft/resolver and restored account/common PAM bytes.
A normal systemd warning that the socket can retrigger the service is emitted
during explicit QA service stop; the captured socket is then also stopped and
its identity checked. It is not a failure or unbounded retry.

Logs: `out/{debian,ubuntu}-vm-qa/results/profile-journal-netbird-native.log`.
Both commands returned0 and the four modes each report `result:clean`. Final
`profile-journal-netbird-postchecks.log` also returns0 on both bases: empty
schema5 journal, original unlocked Home shell/login, forwarding0, disabled/
inactive host socket, static/inactive host service and inactive networking unit,
no runtime policy, child1002/home/user-manager drop-in, vendor binary/global state,
provider runtime/state fixture, named namespace, veth, NAT table or routing rule.
Installed package verification and `dpkg --audit` are clean. Native GTK libraries
and fixed QA helper files remain only on the disposable guests.

## Regression and remaining work

All406 profile tests pass on both source bases as root (4 intentional skips) and
ordinary UID (108 privilege-dependent skips). Coverage includes schema migration,
write-ahead order, unresolved creation/stop intents, endpoint receipt mismatch,
changed account, absent runtime and conservative observer-only detachment.
The preceding strict GUI sandbox gate now passes on both bases; details and
historical failures are in VALIDATION_PROFILE_NETBIRD_CLIENT.md.

Next integrate the verified provider with captured graphical sessions, manager/
client environment and overlays. Then complete actual provider-owned wt0/routes/
firewall inventory, connected teardown/recovery and real browser enrollment
acceptance before opening public VPN startup. Dynamic DHCP/DNS, cold main and
partly created GUI recovery, family clipboard and the remaining Wine/Darling/
VMware integrations remain separate migration work. No full-migration success
is inferred from this pre-login gate.
