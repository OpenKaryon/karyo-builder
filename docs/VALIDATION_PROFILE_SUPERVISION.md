# Installed observed logout and compositor crash supervision

This gate adds normal long-lived supervision of an already observed profile. It
does not complete replay of a compositor already dead at host startup, public
stopped-profile allocation or the whole migration. No push, owner-machine, Forge
or donor changes are performed.

## Exact runtime inputs

Installed DE source: ac3bedac543f97fbff73d6a792ae248afe1bca50.
Source archive SHA256:
06667f0539332622d827c7746f77893b088e72a8ddb012bf753ce499810dee06.

- debian accounts: out/migration/profile-supervision-debian-accounts/karyo-profile-accounts-20261121T201015Z-b13757e4; 81188 bytes; SHA256 171639b3ce87e122685be48c96af4d8402adc2a95e59b01d95855fcb3e0a024e.
- debian host: out/migration/profile-supervision-debian-host/karyo-profile-host-20261121T201027Z-463d03ac; 34668 bytes; SHA256 ddbb0efa99248827a34f936931128a75d3db0ea327d5a3562533553b385a9b74.
- ubuntu accounts: out/migration/profile-supervision-ubuntu-accounts/karyo-profile-accounts-20261121T201127Z-b1c20518; 82458 bytes; SHA256 80a8a526cb0af66f4d70c8fb961b7388eacb5c7ec5d8e84510ff33fe17c5d02e.
- ubuntu host: out/migration/profile-supervision-ubuntu-host/karyo-profile-host-20261121T201139Z-4b80634d; 35078 bytes; SHA256 b28adc7c318845580b723a293b49d8a18327999df7f3f3cec3f11251b510c4fb.

Public DE profiles/tests/installed-supervision.py has SHA256
1042fef0bb403754e86e957f3f701bc8f8cda8c0e6bacc30ec1e4276ac9ade51.
Both guests execute those exact root-owned bytes against installed packages, not
Python source overlays. Earlier journal acceptance remains recorded separately.

## Native lifetime and return boundary

The root host uses half-second select polling instead of an indefinitely blocking
accept. SessionRegistry polls only its captured compositor pidfds. A living profile
is untouched. On observed exit it makes exactly one return decision, then closes
the known graphical session and waits through GraphicalPending/ManagerPending.
Private DNS/network remain until manager teardown acknowledges its natural exit;
no user@UID.service is force-stopped.

ReturnAfterExit checks the held configuration lock, exited pidfd, private journal
account/process receipt, current family ownership, native kernel active VT and
logind seat0 active session/owner. An already changed console/seat is left alone.
Home is selected by current family owner plus matching local UID/name/session.
An expired/locked account is not activated. Protected Home must confirm its actual
compositor lock before activation; identity, policy eligibility and seat ownership
are checked again. Activation must agree in logind and the kernel VT.

If Home is unavailable, the code requires one existing local GUI greeter with
class greeter, seat0, Remote=no and a service UID in 1..999. Its session and console
come from bounded native metadata, never a fixed VT7. This fallback and protected-
Home lock/race boundaries have source tests; the new installed scenarios exercise
Home return. They do not claim native creation of a missing greeter or a new
installed protected-Home-destination authentication roundtrip.

## Source and native acceptance

All 344 profile cases pass on Debian 13 and Ubuntu 26.04 as root (skip3) and
ordinary UID65534 (skip97). New cases cover seat/greeter schemas, Home/greeter
selection, lock-before-activate and failed lock acknowledgement, changed target/
account/seat/VT, no activation over another active seat, manager-pending retry and
listener polling without clients. The first run found a fixture connection Mock
without context-manager support; it was corrected before both complete root/user
runs passed. No failed run is treated as acceptance.

The fixed native fixture creates a proven new synthetic child and captures its
private network/DNS, scoped manager and PAM compositor. It terminates only its
captured child controller, then activates the installed root host using a request
from that exact living Work context. Afterwards no client request drives cleanup.
The actual host pidfd poll observes each of four cases on both kernels:

- Normal logout through labwc --exit, launched in the scoped user manager.
- Compositor SIGKILL through a fresh pidfd after executable/start and logind-scope
  invocation checks against the captured QA receipt.
- Background compositor exit after explicitly returning to the original Home;
  the host logs seat-unchanged and does not reactivate over it.
- Compositor crash while its initial Home-password lock is still shown, with no
  shell or editor and no password entered.

In logout/crash/locked-crash, the host logs return activated and restores the
original Home login on its actual VT8. Exactly one bounded, non-sensitive return
event occurs per case while natural manager teardown is retried. All four cases
finish with an empty journal and original network snapshot. The original main
shell and account/common-PAM bytes are preserved. Native logs are
results/profile-supervision-native.log in each QA directory.

## Compatibility and final restoration

The final ac3beda packages also pass both old living-editor/protected-lock cases,
all six offline closing cases, three preparation cases, six DNS cases, five
network cases and private NET/MNT transport acceptance on Debian and Ubuntu.
Current logs retain their profile-*-native.log names; previous 4a58468-runtime
results are saved with before-supervision prefixes.

Final supervision-postchecks.log confirms original shells36901/97122, logins
595/765 on VT8 active/unlocked, absent temporary child/home/runtime/policy and
private DNS/named namespaces, forwarding0, empty private schema3 journal with
0700/0600 permissions, inactive disabled socket and inactive static service.
All four installed journal/supervision probe hashes, dpkg -V and --audit are clean.
Builder recipes are unchanged; four pinned native DEB builds validate packaging.
C++ is unchanged, so the earlier complete CTest result remains applicable.

## Remaining work

Already-dead/half-closing session replay at host startup, missing greeter creation
and primary Home host-network restart remain explicit runtime gates. The public
stopped-profile operation still needs allocation and typed forwarding ownership/
setup before it is wired to this long-lived host. Physical DHCP/DNS reconciliation,
actual NetBird/PKCE, profile catalogs, family clipboard and remaining Wine/macOS/
VMware integration are still open. Internet/VPN and physical GPU/Wi-Fi/camera/
microphone support are not inferred from this disposable-VM lifecycle check.


The later schema4 gate VALIDATION_PROFILE_FORWARDING_JOURNAL.md joins observed GUI supervision to owned NAT and private DNS/NSS under a synthetic blocking Home policy. This no-NAT supervision probe also passes again on b3e832e. Public allocation/setup and already-dead startup replay remain open.
