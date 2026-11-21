# Connected NetBird in a captured profile namespace

Real setup-key enrollment, live journal reattachment and connected-owner teardown
now pass on Debian13 and Ubuntu26.04 in disposable VMware guests. This gate uses
an isolated realm created from public NetBird0.82.1 inputs, without a user account
or private management endpoint. The entire migration remains active; public VPN
startup is still rejected before allocation. All commits remain local.

## Production and native QA provenance

Installed production DE revision: `25273daa8aac34426787a7c78be1cd2b55867ea9`.
Source archive SHA256: `b9731d0501e744c1d833ac44375b518c44939d16630650bf476e6e73975ed438`.
The later QA-only commit `0f9b8d7099c96ab1159cf53c543496a4e56f0ba4` contains the
native drivers; installed packages are not claimed to include that later commit.
Four components were built independently for each base and installed without
activating the public host runtime. All eight builds and both installs returned0.

| Base | Component | Bytes | DE package SHA256 |
| --- | --- | ---: | --- |
| debian | accounts | 94624 | `9703452da6ef27dc678a955f3a9aa535db02ad86f545f325a5ee5d19b3716d19` |
| debian | host | 38168 | `7b5f764db0216c58d86c1beef8e267bf5cd8939f6cf6cf1182fa30e6b43a0b3d` |
| debian | runtime | 38144 | `3cde5faa888073773ea1d543c49efbc0c87ffcfd512dcf1892dc082cae0347b4` |
| debian | client | 37940 | `31a682f5b4fe1f5183974ac2535189c8e34c5898348bdb7db5a27b4459e3331d` |
| ubuntu | accounts | 95980 | `b345491ffb7ef191142f13aa7395210862c299abf3558eaa0588694f2fb673b3` |
| ubuntu | host | 38666 | `b5ff01ec10992a1bebb091887117636c2f5fd7e71d727eadce2b590238dc3a92` |
| ubuntu | runtime | 38666 | `a3a5688982a992ba1c3949d262d270166ae80b526e3204676d8e29d3bd30bcb8` |
| ubuntu | client | 38464 | `4920254995523f3771d5155e041e8d257ff28453c600c6dd55f0f1b2263fe187` |

Exact artifact directories are recorded in
`out/migration/profile-netbird-client-{debian,ubuntu}-inputs.json`. Each directory
retains its own source manifest, environment, dependencies and checksums.

Native probe `karyo-de/profiles/tests/installed-netbird-connected.py` SHA256:
`166f72840a2ddad464bae0a7af02e47de7b4da59fc8f0e8b647c64dd58678beb`.
Server control `karyo-de/profiles/tests/installed-netbird-lab-server.py` SHA256:
`f24df611d413e1caf1d3cd6cef2c37ae86e9d538392c84a1e02b921a8082d97f`.

## Observed gap and ownership model

The first real enrollment created a kernel WireGuard `wt0` plus provider routes,
policy rules and namespace-local nftables state. The prior strict `{lo, eth0}`
verifier correctly rejected the additional link. Calling vendor `down` removed
its link/routes/rules but left some namespace-local nftables objects. That first
observation was diagnostic evidence, not a connected-runtime acceptance pass.

Schema6 now explicitly declares `network.contents = "tunnel"` atomically with the
provider preparation intent, before native provider startup. Declaration survives
provider receipt removal, so interrupted namespace cleanup retains the same
boundary. Schemas1 through5 retain their previous strict device expectations.

The controller owns a fresh pinned network namespace, its proven host/guest veth
pair and the host forwarding objects. A declared namespace may contain one extra
virtual WireGuard or TUN link. Physical, TAP, veth, bridge, dummy, mastered,
duplicate-index and second-extra links are refused. The namespace inode, host and
guest veth kind/alias/index/peer relationships remain authoritative. Unexpected
processes or identity replacements retain resources rather than trigger a sweep.

Provider routes, policy rules and firewall state stay within that owned namespace.
After graphical owners, natural user-manager exit, the exact provider and private
resolver have ended, cleanup deletes the proven empty namespace. It does not
adopt arbitrary host tunnel names or scan/delete global VPN rules. Host NAT and
forwarding receipts retain their existing per-object ownership checks.

## External laboratory inputs and credentials

Official combined-server image:
`netbirdio/netbird-server@sha256:7cf0268831221d2d4cc8ca89ca3d8d9419f890f0abb72c1fa9d00aae07e0b788`.
The extraction-only container never ran and was removed. Extracted server binary:
80375576bytes, SHA256
`0a1276b42c0112098dbf5a16ed0a908e9f0e641b90c303fd736cbc2f841f6439`.

The exact0.82.1 source archive used to inspect server setup and CLI key-file APIs:
9596399bytes, SHA256
`faea65ed0321a285818ad4458da5b0441c6f6f766c9fd963cb7dfc5cd9bf4445`.
Official CLI DEB:15864072bytes, SHA256
`4adff2bbc1529942e914c181badfc17585c78f0532ccaf6c000f5c9300d9a632`.
The verified CLI binary is extracted in QA; vendor postinst/global daemon setup
is never executed. These digest checks are not signed APT-chain acceptance.
No vendor binaries are committed or added to distribution images in this gate.

On fixed Debian QA host `karyo-de-acceptance`, explicit preparation starts one
transient server as UID1000 with an empty capability bounding set, NNP, strict
filesystem protection and dedicated previously absent data directory. HTTP uses
the private VM address `192.168.230.163:18443`; no host port publication is added.
This HTTP realm is for disposable testing, not a deployment recommendation.

A random owner/password/PAT and limited ephemeral setup key exist only in guest
private files (root0600 admission/control; server-private UID1000 data/config).
The host runner transports the admission key through SSH stdin/process memory;
CLI receives `--setup-key-file`, never the key value as an argv argument. No real
account credential or user VPN profile is imported. Logs/reports exported for
review omit admission material and configuration secrets.

The helper captures directory/binary inodes, binary SHA, native PID/start time,
service invocation and cgroup before observing readiness or stopping it. Cleanup
first requires an empty profile journal/namespace inventory and stops only the
verified native service; it removes only its previously absent captured fixture.
Public staged binary inputs and fixed QA helpers may remain, without credentials.

Primary references inspected for this fixture:
- [Automated self-hosted setup](https://docs.netbird.io/selfhosted/automated-setup)
- [Version-pinned combined server source](https://github.com/netbirdio/netbird/tree/v0.82.1/combined)
- [Version-pinned CLI source](https://github.com/netbirdio/netbird/tree/v0.82.1/client/cmd)

## Native matrix and evidence

On both bases, the real ordinary client launched by the captured user manager
inherits its endpoint and completes setup-key enrollment with exit0 and JSON
`daemonStatus=Connected`. Kernel observations show an actual WireGuard device.
The network verifier, provider service and live consumer inventory all accept
the unchanged native identities.

The driver releases observers, closes the journal and creates a new journal
instance in the same root controller PID. It reattaches the same live provider,
user manager and graphical owner without restarting them, verifies consumers,
and confirms a second actual status remains Connected. It then returns Home,
closes the graph/manager/provider/DNS/forwarding/network while connected, and
checks original host routes/rules/nft/resolver and account/common-PAM hashes.
It never invokes `netbird down` in this acceptance path.

Both first runs against the manually prepared realm and repeated runs against
the committed control helper's freshly created realm passed. Safe final kernel
reports (the local physical/NAT addresses are diagnostic data):

| Base | Report under `out/<base>-vm-qa/results/` | SHA256 |
| --- | --- | --- |
| debian | `netbird-connected-kernel-25273da.json` | `06fdddd2db9791ef9fddc27a93ef2622fe59dc2bca23c6e4f166fddb01be11d9` |
| ubuntu | `netbird-connected-kernel-25273da.json` | `6783b8297302e11ca80da465afced07fe74aaec1c367f4cc900fd2c55288c14b` |

`netbird-connected-native.log` on both bases records successful final cleanup.
Debian `netbird-lab-helper-validation.log` records fresh prepare/status success;
`netbird-lab-helper-cleanup.log` confirms server/data/credentials/binary removal.
Final `profile-supervision-netbird-postchecks.log` on each base returned0: the
original Home shell/login remains active/unlocked, journal6 is empty, forwarding0,
host socket disabled/inactive, host/runtime inactive, dpkg verify/audit clean.
No temporary child1002, home, manager policy, provider/state/binary, namespace,
veth/NAT, lab server, admission or connected/observation fixture remains.

## Preserved fixture failures and limits

Initial manual setup omitted a physical server data directory, producing an
explicit SQLite open failure; the fixture now creates it first. A subsequent
readiness poll used GET `/api/setup` (POST-only), although the captured server was
alive. Readiness now uses GET `/api/instance` and a direct no-proxy HTTP client.

The first bounded helper used MemoryMax512M and was OOM-killed; this is recorded
in `netbird-lab-helper-512m-failed.log`. Raising the bound to1G kept the service
alive, but the35s readiness deadline expired while it initialized. Authoritative
PID/listener/API inspection subsequently proved that same captured process was
ready; it was not another OOM or reason to launch a duplicate. The helper now
allows120s and verifies native liveness during polling. Fresh prepare/status,
both repeated client runs and captured cleanup passed after those corrections.
Failed fixture logs remain alongside successful evidence.

Eight new tunnel boundary tests bring discovery to425 cases on each base: root
passes with4 skips and ordinary UID65534 with109 skips (privileged checks remain
in the root/native gates). Logs:
`out/migration/netbird-connected-{debian,ubuntu}-{root,ordinary}-tests.log`.
No C++ code changed in this wave; these are Python runtime/ownership changes.

This gate does not establish actual controller SIGKILL/systemd host recovery
while connected, peer payload/DNS/exit-node behavior, userspace TUN native
acceptance, browser PKCE completion, final GUI/tray enrollment, vendor inert
packaging/catalog overlays or public VPN startup. Prior pre-login host-crash and
strict renderer/synthetic callback gates remain separate evidence. Those open
boundaries and the rest of the full migration must still be completed.
