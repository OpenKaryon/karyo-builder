# Installed NetBird provider and captured graphical owner

The pre-login NetBird provider now participates in the captured desktop lifecycle
on Debian13 and Ubuntu26.04. Both actual six-mode lifecycle acceptance and the
strict real GUI/client/handoff gate pass. This is still not remote enrollment,
connected-tunnel ownership or public VPN activation, and the complete migration
remains active. All commits stay local; Forge, donor, owner VM and Acer are untouched.

## Exact production inputs

Installed DE revision: `4ab22ad8bf58fd78fb54e0b8033fcf2740fbc90e`.
Source archive SHA256: `e6aa9bcabb002804e1312c984c7adb13ea9fd21e97fe032ac9898c977043d6a4`.
All eight package builds and both inactive installations returned0. The native
QA changes were later committed separately in `289719b`; installed production is
not claimed to come from that later QA-only commit.

| Base | Component | Bytes | DE package SHA256 |
| --- | --- | ---: | --- |
| debian | accounts | 93752 | `980b24c883cd4e051b9503b11a5cf29ad07f7b0349eddcd295b3ab1f930e4351` |
| debian | host | 37744 | `00a0b8f2424af121a4a737aaea65ff811c05709cedfd18915ed74fe2f2c20c16` |
| debian | runtime | 37716 | `c646d5fff59dd56050437dd4a380ec4570104abcc2ec72197e777b01c9d78d88` |
| debian | client | 37516 | `3d8234df61fae6487aa7aeac73c388fc05d3c8b347741a713bee23892b8b045c` |
| ubuntu | accounts | 95112 | `09027d58281c5edd680ad67e00cbf52cca9c2a9a9a68755e66cd438397082b0a` |
| ubuntu | host | 38220 | `c710af627641d4867bffd7922fbce17cf48528bde6ae1da411a727692b0c07c6` |
| ubuntu | runtime | 38208 | `66ef9add09aa17a85d76d67f48e2ae53b1d54343f8e1e9891768c140f3840cdc` |
| ubuntu | client | 38024 | `c648fcfd6f822e22ef1962a6d39db9633e934164f40be991e8613aefe9986d77` |

Exact artifact manifests/paths are recorded by
`out/migration/profile-netbird-client-{debian,ubuntu}-inputs.json`; individual
output folders keep their immutable source identity after later pointer updates.

Native lifecycle probe `karyo-de/profiles/tests/installed-supervision-netbird.py`
SHA256: `5ce7acafce5e4ab6dbe21791d42fa20a74e3c9fcc75399f11a3c49292f1a625b`.
Updated GUI probe `karyo-de/profiles/tests/installed-netbird-client.py` SHA256:
`165dabebcd3f8df96db4986ff61892f4df5483236339c0712f0381daf2fd09c9`.

External NetBird0.82.1 CLI/GUI archives are the same reviewed inputs documented in
VALIDATION_PROFILE_NETBIRD_PRELOGIN.md. Exact binaries were extracted in disposable
guests after digest checks, without vendor postinst/global service activation,
and matching temporary binaries were removed after successful cleanup. No setup
key, private management URL, real account credential or profile was imported.
This is not signed APT metadata-chain acceptance or a final vendor packaging policy.

## Resulting ownership behavior

`JournalSession` verifies and observes an acknowledged provider before publishing
manager-preparation intent. Session restore captures that same live provider
alongside its manager and graph. Namespace inventory revalidates it before and
after inspection, accepting only the exact verified provider main PID outside
known resolver and graphical/user-manager scopes. Another root/ordinary process
is not accepted merely because a provider is present. Unknown identity or
consumer changes retain resources instead of bypassing checks.

The native user-manager policy and graphical entry receive the same endpoint,
derived from the validated network token. Ordinary manager-launched clients need
no manually injected `KARYO_NETBIRD_ENDPOINT`. Plain profiles gain no provider
environment. Restore reconstructs that exact policy from the provider record;
it does not overwrite a mismatching legacy/foreign policy. No new arbitrary
path, command or credential field is added to journal schema5.

After GUI exit, the captured manager must end naturally. The host then closes the
provider before private DNS, forwarding and namespace cleanup. Prepared and
closing session recovery can observe that verified pre-login provider while
still rejecting unknown consumers. Provider state remains persistent in product
code. The QA driver explicitly deletes only its previously absent state fixture,
after receipt/namespace teardown and an exact captured directory/stamp check.

## Native lifecycle matrix

Both guests passed all six modes with the actual vendor daemon and persistent
state directory reused across the leases. In every created graphical profile,
the manager, compositor and shell/initial lock inherit the derived endpoint, and
a real ordinary `karyo-netbird-cli status --json` launched by the scoped manager
without a manual endpoint override returns `NeedsLogin`.

| Mode | Native boundary and result |
| --- | --- |
| prepared | Kill controller after acknowledged manager policy preparation, before graphical login. A fresh registry reconciles the policy/provider/DNS/forwarding/network, with no fake graphical adoption. |
| logout | Kill controller after complete GUI startup; activate the installed root host through its socket, then perform actual labwc logout. The host reattaches the same provider and graph and returns Home exactly once. |
| crash | Same host reattachment, then pidfd-SIGKILL the captured compositor. Home is restored and cleanup completes without a client connection. |
| background | Activate Home before the captured Work compositor exits. The host records seat-unchanged instead of stealing the active seat. |
| locked-crash | Initially protected Work has an actual lock and no shell. The restored host observes its compositor crash, returns Home, then closes the complete provider graph. No password is bypassed for interactive entry. |
| closed | Kill controller after recorded graphical closure and natural manager exit, leaving its captured policy and live provider. A fresh registry finishes only that acknowledged closing transition and lower layers. |

The prepared/closed cases directly exercise a fresh installed `SessionRegistry`;
the four living cases use the actual socket-activated root service and a request
from the captured Work context. The driver verifies original Home shell/login,
exact journal handover, provider-state generation, host routes/rules/nft/resolver,
account/common PAM restoration and unchanged active seat where applicable.

Logs: `out/{debian,ubuntu}-vm-qa/results/profile-supervision-netbird-native.log`.
Every mode reports complete cleanup; both commands returned0. The existing
systemd socket-trigger notice is expected during explicit QA service stop; its
captured socket is stopped afterward, with final state checked separately.

## Journaled real GUI and browser handoff

The strict GUI probe now starts the provider before the captured session, uses
inherited endpoints for ordinary CLI and GUI launches, and verifies the living
namespace consumers while both are running. Its wrong-context check still
explicitly selects the endpoint from the host network, proving refusal rather
than merely a missing environment variable.

Both guests pass actual rendered welcome window, zero inheritable/ambient GUI
capabilities, native private NET/resolver, and WebKit renderer NoNewPrivs1,
seccomp2 and distinct user namespace. Both report sandboxed renderer true and
window-only false. The nonblocking synthetic cold browser callback still reaches
a listener opened later on Work loopback. The GUI fixture stops its exact user
unit, closes graph/manager, then provider/DNS/forwarding/network in that order.

VM-only RFB captures were visually inspected without host focus:

- Debian `netbird-client-4ab22ad.png`, SHA256
  `bee86622459176d5385308c86ba0a55e4b72aba7444ae834721a4fede4b9a635`.
- Ubuntu `netbird-client-4ab22ad.png`, SHA256
  `205d2cc79d4e73b6e5844ee45677b532d0ad2e070d20b72d71a8aecb7b446b08`.

Frames and preserved `profile-netbird-client-native-4ab22ad.log` reside under each
VM's `results` directory. The Connected word in welcome artwork is static and is
not evidence of a real VPN connection. No completed onboarding, tray/main-window
interaction, OAuth/PKCE enrollment, connected DNS or exit-node acceptance is claimed.

## Regression, final state and remaining gates

All417 profile tests pass as root (4 intentional skips) and ordinary UID (108
privilege-dependent skips) on both source bases. The new tests cover the exact
provider PID, revalidation, failure before manager preparation, derived policy,
unknown offline consumers, observer-only detachment and teardown order.

Final `profile-supervision-netbird-postchecks.log` returns0 for each guest:
original Home active/unlocked, empty schema5 journal, forwarding0, host socket
disabled/inactive, host service static/inactive, networking unit inactive, no
runtime policy or temporary child/home/manager drop-in/provider/runtime/state/
binary/namespace/veth/NAT/routing-rule/visual-handshake fixtures. Installed DE
package verification, native probe hashes and dpkg audit are clean. Only the
previously installed GTK libraries and fixed root QA helpers persist in QA.

Next complete provider-owned wt0/routes/firewall inventory, connected teardown/
recovery, real browser enrollment and distribution/catalog/vendor packaging
before opening public `VPN=netbird` startup. It continues to fail before
allocation with no ordinary-network fallback. Dynamic DHCP/DNS, cold main and
partially created graphical recovery, family clipboard and remaining Wine/
Darling/VMware work remain explicit full-migration requirements.
