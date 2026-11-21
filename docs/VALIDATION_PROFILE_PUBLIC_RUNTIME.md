# Installed public isolated desktop runtime

The optional runtime now has public stopped-child startup, rather than only
library fixtures. The whole DE migration remains active and incomplete. No
pushes or changes to Forge, the donor, Acer or the owner's VM were made.

## Exact inputs

Installed production DE revision: `8167a9f4ca81c6c112bedc2bdda20b08904372b5`.
Source archive SHA256:
`097c8c059ad57ec5fec83fada348b0618795b679dbe268521b7fd50db38a800f`.

All six Builder builds and both installations returned zero. Manifests and exact
output paths are indexed in
`out/migration/profile-public-runtime-{debian,ubuntu}-inputs.json`.

| Base | Component | Bytes | Package SHA256 |
| --- | --- | ---: | --- |
| debian | accounts | 87316 | `4ead17e58547897a9a0d7d66476bf1fa0873ba59852cb579bd218c6b0a078ceb` |
| debian | host | 36324 | `20b7a09493e17e3040059c719aa4a78d6887d4fa08930a65f4ed7918f0f62238` |
| debian | runtime | 36264 | `c27ea37d585738866f8a3172e826da7fbd364059d0bb1aaee300620c1f807c0b` |
| ubuntu | accounts | 88610 | `944484f23b09740066e4fa2496836b48f5989402bfdafb9e4f5ae6325fb240af` |
| ubuntu | host | 36784 | `09497d6b49b2b25a9bbc2205a28ad4a661baef2412dca70a6ce2900a27386ae4` |
| ubuntu | runtime | 36748 | `81e536f47b82bea2ba774c10285a2f4031900eb18b62b291e024ea13e694a9ce` |

The root-owned installed public probe is
`karyo-de/profiles/tests/installed-public-runtime.py`, SHA256
`3be27e4ef96458f2400d7ea68058db6cdfe40916c4299ecdb68d152cedea1d83`.
It runs only as root on the two fixed disposable QA hosts. SHA is checked before
installation; the Python isolated-mode entry does not load writable QA modules.

## Implementation and activation boundary

`profile-runtime` is a distinct installation component and Builder recipe.
Its payload includes an inactive networking service, an ordering drop-in for
the root host and `karyo-profile-runtime enable|apply`. Package installation does
not enable forwarding/services, replace the resolver, create accounts or alter
PAM. Exact account databases, common PAM and default display manager were
compared before/after both installations and remained unchanged.

The administrator must deliberately configure a supported resolved backend and
run `sudo karyo-profile-runtime enable`. Preflight validates root host namespaces,
trusted executables, the fixed controlled PAM entry, resolver service identity,
units, physical IPv4 underlay and physical-link DNS before publishing the root
0600 opt-in policy. Native activation then enables forwarding and the host socket.
Both QA hosts passed explicit enable and actual systemd oneshot execution.
Enablement symlinks persist; reboot acceptance was not performed in this gate.
There is no production stop hook that resets a global sysctl owned jointly with
container/VPN software. No automatic resolver migration is implied.

The public switch helper still requires local pkexec caller validation. When
the explicit policy is enabled it sends only version, operation and validated
target name to the root-only Unix socket. The host separately derives the
native peer's login/account; no supplied UID, namespace, path or executable is
accepted. Existing sessions use lock-before-switch. A stopped eligible child
allocates Network -> Forwarding -> DNS -> Manager/PAM/GUI, then joins the host's
lifetime registry before activation. A lost caller after allocation retains
receipts; uncertain native resources are not swept or silently recreated.
A stopped Home/main is still the login manager's responsibility and does not
get a private NAT namespace.

## Debian 13 and Ubuntu 26.04 results

The installed `desktop-switch` helper was executed from captured active Home and
Work login cgroups, with Work clients additionally entering its captured NET/MNT
context. This root-only QA fixture exercises real installed local authorization
and independent host peer derivation, not a mock request. It does not claim to
exercise an ordinary user's interactive polkit/password prompt in this gate.

Both guests passed all three cold-start cycles:

- Unprotected Work cold launch, actual shell readiness, mounted NSS DNS
  `getaddrinfo(example.org)` with two IPv4 answers and TCP to `1.1.1.1:443`
  from private source `10.231.0.10`. Work -> Home -> Work public switches kept
  the same runtime ownership token and did not report fresh startup. Normal
  compositor logout returned to the original Home and cleaned all layers.
- A new unprotected Work cold launch with the same DNS/TCP checks, followed by
  a verified compositor pidfd SIGKILL. The host observed exit without another
  client request, returned Home and naturally closed manager, DNS, NAT and netns.
- A new Home-password-protected Work cold launch: one lock process and native
  LockedHint were required, while shell/editor processes had to remain absent.
  Verified compositor crash returned Home and cleaned the owned graph. Actual
  password entry remains covered by the earlier graphical-profile acceptance,
  not by this protected cold-start test.

Each cycle left the exact original Home login/shell and native active VT intact.
Account databases/common PAM were restored by the fixed absent-child fixture.
Both final native runs returned zero; logs are
`out/{debian,ubuntu}-vm-qa/results/profile-public-runtime-native.log`.
Installation logs use the corresponding `profile-public-runtime-install.log`.

Final explicit QA cleanup stopped and disabled the known test runtime/socket,
removed its exact opt-in policy, restored global forwarding=0, and verified an
empty schema4 journal, no private namespaces/NAT/child runtime/manager drop-in,
no QA child account, original active unlocked Home and clean dpkg verification.
This is deliberate disposable-test baseline cleanup, not a product disable hook.
Full pre-enable IPv4 sysctl snapshots were not captured in this gate; do not
interpret the final forwarding=0 assertion as a byte-for-byte sysctl regression.

## Source regressions and remaining work

375 profile tests passed as root on each base (3 intentional skips), and as an
ordinary UID on each base (99 privilege-dependent skips). Builder's 38-test
suite passed with one platform skip; recipe loading and six real package builds
also passed. No C++ behavior changed; prior full CTest acceptance is retained.

Still required before the full profile integration is complete: cold main
session handling, already-dead/half-started GUI startup reconciliation, physical
DHCP/DNS refresh, actual per-profile VPN state/services and callback/GUI capability
handling, profile app overlays and family clipboard. Real Wine/Darling runners,
VMware integrations and remaining compositor/Wine patches remain separate open
migration items. The schema4 synthetic blocking-Home NAT gate remains separate
and is not replaced by these ordinary-underlay public-helper tests.
