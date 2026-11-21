# Installed isolated NetBird pre-login service

The NetBird provider now has a verified native pre-login primitive. This is not
connected-VPN/public provider acceptance, and the whole migration remains open.
No push, Forge, donor, Acer or owner-VM modification was performed.

## Exact inputs

Installed production DE source: `540760c8c00d410d6544f62e1d070865f0af2b3b`.
Source archive SHA256:
`56b74268b7bae76fb09c7f85c2c4c2e383f5b3c67cef6bcb2074569886332861`.
All final six package builds and both installations returned zero. Manifests and
artifact paths: `out/migration/profile-netbird-prelogin-{debian,ubuntu}-inputs.json`.

| Base | Component | Bytes | DE package SHA256 |
| --- | --- | ---: | --- |
| debian | accounts | 89108 | `79c841c501704c353f9780e80d6fede6822ba0d1ec2ddf52f935dc47d48f4bf6` |
| debian | host | 36672 | `fc3693abf41bf0e385682f00687133b46b69c2b440072598eb694dc727f9c3a8` |
| debian | runtime | 36636 | `d2c24032b639a97dbcafcf64bd47cdeb65663379850d3ee55727e5d659f9a9f6` |
| ubuntu | accounts | 90430 | `29d943e9fd567463c8e8fc54f4beff61b0c4f7309f7aff77f4014f7adabbab7f` |
| ubuntu | host | 37162 | `7f5296574c77baa0028268b19da6361d3ab6c03fab1b9902fbf01a8d95d420d5` |
| ubuntu | runtime | 37130 | `68a15930fd145b19aa041099e9ac4afcaa7ee373d4768c01dc99b2ae99c8728f` |

The external NetBird client was obtained from the official APT Packages index:
https://pkgs.netbird.io/debian/dists/stable/main/binary-amd64/Packages

- CLI `pool/netbird_0.82.1_linux_amd64.deb`: 15864072 bytes, SHA256
  `4adff2bbc1529942e914c181badfc17585c78f0532ccaf6c000f5c9300d9a632`.
- GUI `pool/netbird-ui_0.82.1_linux_amd64.deb`: 12077840 bytes, SHA256
  `88b36705e8bdd8c297722412ef801519ad9f9b829efd44594d004d35fbe9a937`.

Both archives were checked against their published sizes/SHA256. The GUI was
only downloaded, not installed or executed. This HTTPS package-index comparison
is not a claim of signed APT metadata-chain validation or a complete future
Builder external-input contract. Index/selection and archives are ignored local
QA inputs, not repository payloads or bundled upstream binaries.

The actual CLI binary was extracted into each disposable host after verifying
the vendor deb digest. Native testing deliberately did not execute its maintainer
scripts: inspection confirmed that clean install AND upgrade call system-wide
`netbird service install` and `netbird service start`. Merely depending on the
vendor package would therefore not preserve inert DE installation. Future
provider/distribution packaging must address that activation explicitly.

## Provider behavior

`NetBirdState` creates or verifies a private root-owned 0700 state directory under
`/var/lib/karyo/profile-vpn/UID/netbird`. A root 0600 ownership stamp records the
local account fields and actual home device/inode. Changed account/home identity,
unsafe permissions, symlinks, hardlinks, replacement directories and unstamped
preexisting state are refused. State is kept across ordinary runtime leases; the
product never recursively adopts, chowns or deletes opaque VPN data on a retry.

`NetBirdScope` starts a new pinned transient native service. Its root process uses
only the captured private profile network, mounted private resolver directory,
private resolve1 D-Bus address, per-profile persistent state and a root/group-750
runtime directory. Service InvocationID, PID/start/executable/cgroup/namespace and
Unix socket native inode/peer credentials are verified. The service lacks
SYS_ADMIN/SYS_MODULE and cannot reach the host NetworkManager/system bus. It
neither installs, stops nor adopts an existing system-wide NetBird service.

Public `VPN=netbird` cold startup now fails before resource allocation until the
complete provider lifecycle is ready. This closes the former silent fallback to
an ordinary unprotected network. Public no-VPN cold startup remains separate.

## Actual Debian 13 and Ubuntu 26.04 acceptance

The exact root-owned probe `karyo-de/profiles/tests/installed-netbird-prelogin.py`
has SHA256 `d14c2b0029b5eb291723e2e5d6fa413dbb988c6b0ca95186e7f026c2a09b73d8`.
It runs only on the two fixed disposable QA hosts. No account/profile/setup key,
private management URL, imported credential or successful remote enrollment is
used. Opaque generated local state stays inside the guest and is removed with
the known disposable fixture.

Both guests passed two independent Network -> Forwarding -> DNS -> NetBird
leases. Each lease verified actual daemon and ordinary Work status `NeedsLogin`,
Home socket denial, the daemon's private resolver mount and bus environment,
absence of SYS_ADMIN/SYS_MODULE, verified stop and lower-layer cleanup. The second
lease reused the same persistent state inode and ownership stamp. Every lease
preserved the exact host routes/rules/nft/resolver snapshot.

Socket readiness is not a saved-profile initialization barrier: the final probe
requires both root and ordinary-client status to converge to NeedsLogin within
20 seconds. It does not weaken the check to accept a transient/failed state.
The product status method still returns the actual upstream state rather than
blocking until login; future UI must display pending states honestly.

Final logs: `out/{debian,ubuntu}-vm-qa/results/profile-netbird-prelogin-native.log`.
Installation logs use `profile-netbird-prelogin-install.log`. Account/common PAM
and default manager preservation, private state/namespace removal, forwarding0,
empty schema4 journal, inactive runtime/host units, original active unlocked Home,
no external CLI/global NetBird state and clean dpkg verification were checked.
A complete IPv4 sysctl snapshot was captured/restored by this probe as well.
The explicit root QA cleanup removes only its previously absent known state and
matching external binary; product state persistence remains unchanged.


The existing public no-VPN cold-start probe was also rerun on these exact final
540760c packages on both guests. All logout, crash and initially locked cases,
private DNS/TCP, existing Work/Home/Work switches and automatic cleanup passed.
The latest `profile-public-runtime-native.log` now records this later regression;
the earlier 8167a9f package receipts remain the historical public-runtime inputs.
After that explicit activation, QA cleanup again removed the known policy,
disabled/stopped the units and restored forwarding0. Logs:
`profile-netbird-prelogin-final-postchecks.log` in each guest's results directory.
The full sysctl snapshot assertion above belongs to the pre-login probe, not to
an unrecorded full pre-enable snapshot of this later public-runtime regression.

## Preserved failures and evidence limits

The first Debian probe mistakenly read `daemon_status` rather than the actual
v0.82.1 JSON field `daemonStatus`. Its provider was stopped successfully, but the
probe retained lower-layer journal receipts. Exact production `recover_profiles`
reconciliation then removed those known offline leases, and the fixed QA state
was cleared. The failed log remains `profile-netbird-prelogin-schema-failed-native.log`.

A later immediate second-lease status assertion failed on both bases; those logs
remain `profile-netbird-prelogin-restart-failed-native.log`. Each failure's owned
service/lower leases/state/account were removed, and the leftover matching CLI
fixture was explicitly verified before removal. The original failed snapshots
were not recorded as passing. The bounded eventual-NeedsLogin checks subsequently
passed both complete leases on both bases. This does not prove a specific upstream
startup timing cause; it proves that the immediate snapshot was insufficient and
that the final readiness criterion converged without a provider code workaround.

385 source profile tests passed as root on each base (4 intentional skips) and as
ordinary UID (106 privilege-dependent skips). The extra root skip is CAP_CHOWN in
the cap-dropped containers; actual root/group-1002 socket access and isolation
were mandatory native checks, not skipped. Prior Builder/C++ acceptance remains
applicable; no Builder implementation or C++ behavior changed in this gate.

## Still required

Durable provider/tunnel receipts and root-host recovery, owned wt0/route/firewall
inventory, connected teardown, ordinary client/GUI launch, asynchronous browser
handoff and actual PKCE callback must be joined before public VPN activation.
The provider primitive currently retains a connected/changed namespace through
the strict base network guard rather than deleting unknown interfaces. No real
exit-node, connected VPN DNS, GUI/callback or family clipboard success is claimed.
Cold main login, interrupted GUI recovery, dynamic DHCP/DNS, app overlays and
remaining Wine/Darling/VMware integrations likewise remain open in the full goal.
