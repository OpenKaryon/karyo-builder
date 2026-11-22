# Public stopped-profile NetBird startup

The public desktop switcher now starts a configured VPN child through the same
journaled provider, private DNS/forwarding, manager and graphical lifecycle used
by recovery. Actual Debian13 and Ubuntu26.04 acceptance passes before-login and
connected ordinary-client scenarios. Installing the base or optional payload
does not activate the runtime or start a global provider.

## Production and user behavior

DE production revision: `d140e14c4a1c2b4c364691628ea3ca2674a578a5`.
Source archive SHA256: `14393190246361d7180eb7bb3f851e0abbf764f0a73e336498e745cf295666e3`.
The first implementation is `a3da7ca`; the subsequent production commit carries
the fixed public prerequisite error across the sanitized host protocol. Later
`e0680d1` adds native QA and clarifies documentation only.

`VPN=netbird` requires trusted root-owned native CLI/GUI, scoped wrappers,
asynchronous opener and fixed private catalog before any allocation. A missing
or untrusted payload yields a typed `provider-unavailable` response; the client
reconstructs only the fixed instruction to install the optional Karyo NetBird
provider and client packages. Arbitrary native errors remain sanitized. No
account, namespace, manager or provider state is created for that failure.

For an authorized stopped family child, the runtime builds network, physical
forwarding and private resolver first, then the journaled provider, then its
graphical owner. The complete scope enters the registry before activation or
release of duplicate preparation observers. Partial-start mutation records remain
authoritative; an error never sweeps uncertain services or erases receipts.
Existing running-session switches allocate no new service. Plain profiles keep
their former path.

Explicit administrator runtime activation is still required. The fresh provider
can remain NeedsLogin while the Work desktop starts; enrollment is initiated by
its ordinary scoped client, outside the controller's configuration lock.
Credentials are neither imported from the user system nor serialized into the
host journal. A normal unscoped Home client cannot reach Work's endpoint.
Persistent profile provider state is reused only for its stamped account/home
generation. The separate inert vendor package does not install upstream global
services, activation hooks or launchers.

## Source and native artifacts

All438 profile tests pass on Debian and Ubuntu as root (4 skips) and ordinary
users (113 skips). Logs are
`out/migration/public-netbird-{debian,ubuntu}-{root,ordinary}-tests.log`.
These cover public provider ordering, missing payload before allocation,
duplicate observer release, partial graphical failure retention, sanitized
protocol responses and actionable fixed helper output, with existing profile
authorization and malformed-packet checks unchanged.

Four native components per base (accounts, host, runtime, client) were rebuilt
and installed from the exact production revision. Existing session/password
components were retained. Pointers are
`out/migration/profile-netbird-client-{debian,ubuntu}-inputs.json`.
Each output directory contains its build manifest.

| Base | Component | DEB SHA256 | Manifest SHA256 |
| --- | --- | --- | --- |
| debian | accounts | `a230cc78bf5ebab9204ab793dc6da0a748033e051ea0a02070a0dadb99b7d216` | `56478903591eb7f76788ff093e52d2365c4253fd1453045aecb9a32ade50114d` |
| debian | host | `c0cd45b9aa90033b333010b1d97cd820e9ef424a1ab52bbe5e9523f3f89703c6` | `ca6305f3172936a265f4332cf071e3677b420778021c0ca8c224ba684f5f4ea5` |
| debian | runtime | `8e5cc412f2c5edd3c5baa9db4073566e5b15d575f9477c04ee12e8b8e90bf69c` | `46f90f6e705b4889078d0a22b87b8431eb2e751fc6a2b0e1ee6ce7fb27c43f06` |
| debian | client | `9e5cb3c73663c2afc6273c899c4dd9e1541f60474b4a8ea399aab5fd6df9be86` | `eec955022781bfd657e8a6af6ee4b4a6850b8b87b6b75ac7cabeccf2684446f4` |
| ubuntu | accounts | `32a06ee7a4ddc666dc5b87ff9887cd004ee3f1f60c0ef370bcd2ada9d0416d28` | `248b611c9745b0d5d558a9a8716704b9e1cb383f4fcb063f3e99f91ec4ec48c5` |
| ubuntu | host | `7c7ad68cc62b41d98959a598f276ddd634dab03a3d24834111e0564360284916` | `48d25b59262b5f9e302dde2132769480f583d581aa1f64c5bafb727e86d25798` |
| ubuntu | runtime | `56630281477f6ebab3db478d1fdd84aaea87479b83bfdcf18b6bc8e0172628d2` | `2a0dfdbdd55d3492dba657a7d33316d60984b52b4ed77955c4bbadd901fe85b8` |
| ubuntu | client | `fd6683922fbbbffacbaf985c327e585dd6a12261538da4f6531f4a76740c1560` | `4f32983585de5b56ce63c1977febda77409eaff33c026a44550a61bd9084d834` |

## Installed public acceptance

Native driver: `karyo-de/profiles/tests/installed-public-netbird.py`,
SHA256 `8ca0242c2e8f024f5e87b9a59965e34c6a6d773a7ccf478e90ef6ef0c0917fb7`.

The fixed disposable-host driver invokes the actual installed public
`desktop-switch` helper through the existing captured QA session/cgroup context,
then reaches the real socket-activated host and RuntimeSwitcher. It does not
replace runtime classes or call JournalSession directly. This root-only context
fixture tests installed host peer authorization and IPC; it does not repeat the
separately accepted interactive polkit/password UI gate.

On both bases the missing-package case returned1 with fixed package guidance and
left an empty journal, no private namespace, no child runtime and no provider
state. The native forwarding policy was restored afterward.

With the real dpkg-installed inert vendor package, ordinary manager-launched CLI
reached NeedsLogin in Work. The journal contained exactly one schema7 profile
with captured provider, tunnel contents, forwarding and private catalog.
Manager endpoint/XDG environment matched the captured context; Home ordinary
CLI was denied. Actual public cold launches passed logout, compositor crash
and initially protected crash. Persistent state device/inode remained identical
across these fresh launches while service invocation changed. Home/Work existing
switches retained the exact ownership token/provider record. The real host
supervised teardown and returned the original Home/VT.

The connected case then started a new Work through that same public helper,
enrolled using an ordinary scoped CLI and a fresh laboratory setup-key file,
required actual daemonStatus Connected, switched to Home and back without
replacing the provider, and logged out while connected. The host removed its
captured resources and retained the original Home/network/accounts. No explicit
provider down or manual namespace network mutation was needed. In the JSON log,
ordinary_status is the initial NeedsLogin observation; connected=true is printed
only after the subsequent explicit Connected assertion passes.

The laboratory realm was the same pinned unprivileged native NetBird0.82.1
server used by prior gates, recreated with fresh disposable credentials. No
personal user credential or production management realm was used. This is real
setup-key enrollment, not actual browser PKCE.

## Evidence and final state

Immutable logs under `out/{base}-vm-qa/results/`:

| Base | Evidence file | SHA256 |
| --- | --- | --- |
| debian | public-netbird-missing-d140e14.log | `a3f7b3dcde581803cb70f41da3c5fe1cfa3d8818d980ff608ee273b7ef8e7694` |
| debian | public-netbird-prelogin-d140e14.log | `55cc2300aa7bb836e54e93570bc40f09f2eb8d91b088a779778e9ef8b3468ff6` |
| debian | public-netbird-connected-d140e14.log | `3d259ceac115393b003604380a95c404e6b1165186aa45b04c37fcd14703dcc3` |
| debian | public-netbird-postchecks-d140e14.log | `3f4702d3e21b3fcc2f5fd1f05249301ac5f322f29cfd2e4ed99e02d417ab9033` |
| ubuntu | public-netbird-missing-d140e14.log | `a3f7b3dcde581803cb70f41da3c5fe1cfa3d8818d980ff608ee273b7ef8e7694` |
| ubuntu | public-netbird-prelogin-d140e14.log | `5d3bfd195494016ddd7868c869ef6879f26cfd6bf4be11e88204a3ce19f25f2b` |
| ubuntu | public-netbird-connected-d140e14.log | `8277a15593254cba2fce686d3154ae4451e9a88e1cdc11aef0518a3a811152ff` |
| ubuntu | public-netbird-postchecks-d140e14.log | `a3e02aa79e1149717c06a48d75e6cbffb8faf3e50d5618a8d0f05ec275235a50` |

All six native invocations returned0 on their first run. The ignored runner
captures its own runtime-policy inode/contents, enablement symlinks and baseline
forwarding/interface sysctls, then removes only that activation after the empty
journal. Matching vendor package purge checks original route/rule/nft/resolver,
accounts/common-PAM and display-manager snapshots. Temporary provider state,
child account, admission key, realm/server/data/owner/PAT and binary were removed.

Final postchecks pass on both guests: the original Home shell/login remains
active and unlocked, schema7 journal empty, forwarding0, socket disabled/inactive,
host/runtime inactive, no child/provider/vendor/NET/veth/NAT/laboratory/activation
fixture, exact installed public QA helper, and dpkg verify/audit clean.
The packaged private provider catalog remains intentionally outside global
application directories. Public staged inputs and fixed root QA helpers remain
only on these disposable hosts.

## Remaining full migration boundary

Public NetBird startup is now wired; previous gated labels in older evidence are
historical. Actual browser PKCE, onward GUI/tray flow and Home-tunnel interference
still need their own checks. Cold Home/partial graphical recovery, dynamic DHCP/
DNS, remaining profile application roles, family clipboard, Wine/Darling/VMware
and the other full-plan work remain active. No ISO rebuild, push or change to
Forge, the private donor, owner VM or Acer was performed.
