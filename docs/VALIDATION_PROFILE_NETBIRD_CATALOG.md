# Scoped provider catalog, icons and schema-7 native recovery

The standalone DE now publishes an optional provider desktop identity only in
its captured NetBird desktop. Actual Debian13 and Ubuntu26.04 acceptance proves
Work-only GIO discovery, the real GUI app identity and correct title/taskbar
icons, strict renderer sandbox, and connected-provider recovery. This stage
does not enable public VPN startup or claim real browser PKCE or tray behavior.

## Production boundary

DE production revision: `7cd9292d1aa190223e4590b7e8973684c0209f8b`.
Source archive SHA256: `8bb1f9ae731d002a0591f2f62412a88916a87c1e0476d603ec0f7333639cf05d`.
Four native components (accounts, host, runtime, client) were rebuilt and
installed per base; other existing session/password/runtime activation packages
were retained. Later DE commits change native QA only. The inert provider
packages and pinned public inputs from VALIDATION_PROFILE_NETBIRD_VENDOR.md are
unchanged and were installed temporarily for the real GUI acceptance.

The client component installs `org.wails.netbird.desktop` beneath
`/usr/share/karyo/profile-catalog/netbird/applications`, outside global application
directories. Its executable is the scoped `karyo-netbird-gui`, its icon is the
vendor netbird icon and its StartupWMClass matches the observed app identity.
Only a captured provider manager and its graphical owner receive that fixed
XDG data prefix followed by default `/usr/local/share:/usr/share` roots.
Plain Home receives no provider catalog. Root-owned packaged data is required
before manager preparation; no user launcher/path is accepted as policy.

Schema7 records the literal `session.catalog = "netbird"` before native manager
preparation, requires a captured provider and preserves that exact variant in
prepared, living and closing recovery. Schemas1–6 remain readable. Old sessions
without the discriminator reconstruct the exact legacy manager policy; matching
files are never rewritten to the new variant. Promotion never downgrades after
session removal. The GUI preserves the upstream DMABUF renderer default while
keeping the explicit sandbox enabled and removing inherited capabilities.

## Exact native component artifacts

Pointers: `out/migration/profile-netbird-client-{debian,ubuntu}-inputs.json`.
Each output directory contains the matching checksummed build manifest.

| Base | Component | DEB SHA256 | Manifest SHA256 |
| --- | --- | --- | --- |
| debian | accounts | `0f8520667acc1910bd2779b16ba9406bbcffa60e38874b6fe1ee9957998a6c37` | `37d8a4ad1c3c2605e92665294c3a438a52f63df62bbe80c2e87d97f6c6ee8362` |
| debian | host | `6be950d6f4489007e1bf30cf04c8c4749af6bfff6f979903c639c1873af5f5b0` | `b4c35e5e10a590968531ac8f9438568c7a442a9fcb4dc5ff9d47c57bd13bd127` |
| debian | runtime | `0f5eaea983ffd63465d4c4cfc3ea1b781769a344e1a4817a306de0dbb5a3ef5a` | `2db3c5d3dda82adbb7957d594c89ff74c29691910ae2e9cd5dbb9d220af621a2` |
| debian | client | `0dffd16e78cfceb12c9bea67e8415b8228edaed9e638c352fb831fb6acfd8fec` | `2fc5d5605c1f909dfe737d2d3764ac1440eb34967885f58c0e072678f69b31a6` |
| ubuntu | accounts | `86977c3e1a9deadeb05c17d60ca803892509862566e676db7dbb3b7d01b1f455` | `1bb1a4713ea4d4b9de98d7fc373d49608773023d9769cfea506c98d8f2aa5b6b` |
| ubuntu | host | `d804788a4e1eb47d2235d04eb9a6da2beee9b5775895c3cc461a0c4c4e64358d` | `652e0f8cb1ec6d450c684406ddc667d62aa333922477ed477e6417bcb2535f06` |
| ubuntu | runtime | `ddc481d20903c569516187e71289f0bfc004a7e47fb281188572381b5ac5d921` | `15570abcc4d5f5851eaebe3ff39a8dff06690f7dd609a32f88e4f64a6e00b9af` |
| ubuntu | client | `7b44914a68f37ba544b07d00a25a332a2edbbe7e2898640ceb8274627e147fef` | `07a07dfa1f824b1b266a353a90a55427868045333f762b958c47591e14c7ef80` |

## Source and installed acceptance

All432 profile tests passed as root (4 skips) and as ordinary users (113 skips)
on each base. The new cases cover fixed typed catalog selection, publication
before manager mutation, root-owned resource rejection, real native policy-file
legacy/new compatibility and mismatch refusal without rewrites, plus journal
promotion/persistence. Existing service, authorization and DNS checks still pass.
Logs: `out/migration/catalog-{debian,ubuntu}-{root,ordinary}-tests.log`.
Four actual offline native component builds and their dpkg installs per base
passed; original host route/rule/nft/resolver, accounts/PAM and display manager
were preserved and activation remained administrator opt-in.

Installed client QA SHA256:
`e882d097916371ecfd7ea103f55abb11b33410c50fba306aac10be8887728479`.
Actual ordinary manager-launched GIO lookup discovers the private desktop in
Work and cannot discover it in Home. A real NetBird0.82.1 GUI reports
`org.wails.netbird`; VM-only RFB frames show the orange NetBird icon in both
window title and taskbar. The real WebKit renderer retains NNP, seccomp and a
distinct user namespace with zero ambient/inheritable GUI capabilities.
CLI endpoint/context rejection and synthetic asynchronous private callback pass.
No window-only or sandbox-disabled fallback is accepted.

One initial Ubuntu QA assertion expected byte-identical GUI XDG roots. Native
observation showed only the standard appended `/var/lib/snapd/desktop` root;
the private prefix and fixed manager/compositor environments were preserved.
The QA now permits exactly that measured Ubuntu GUI suffix. Production policy
was not changed. The failed runs and selected-environment diagnostic remain in
`netbird-catalog-first-environment-failure.log` and
`netbird-catalog-snap-data-observation.log` in the Ubuntu results directory.
The failed install fixture was verified and purged before the corrected run.

The actual six-mode pre-login matrix passes on each base: prepared legacy policy,
logout, compositor crash, background, initially protected crash and interrupted
closed graph. The later connected matrix enrolls via an ephemeral laboratory
setup key, verifies delegated kernel tunnel and schema7/catalog, then restores
the unchanged living provider/manager/graphical identities in a fresh journal.
Closing the connected profile succeeds without an explicit provider down.
The real socket-activated host also passes controller SIGKILL plus logout/crash/
background/initially protected teardown, and a closed graph reconciles. Each
living restore retains Connected status and the exact native ownership receipt;
Home returns once, or stays untouched if already active in the background.

Connected probe SHA256:
`afa100da199abc72425bf62c055bde659f8b507fdff3e10d13603637c11af9d2`.
Connected recovery probe SHA256:
`3489442b7fa73b2029f1987b8d2c50c47148ad47b86eaa307cf78867fe7ba5c4`.
The original six-mode pre-login probe was the earlier accepted SHA
`3e9f3b92898d14e1b1750d1b9fc90cb1ffb5f9c498aafb5b2b93b71e55e0c108`.
The only later changes require schema7/catalog in the connected branch.

## Evidence and cleanup

Immutable copies below are under `out/{base}-vm-qa/results/`.
Only safe kernel/report data is exported; laboratory owner credentials, PAT,
authentication URLs/codes and setup keys are not published.

| Base | Evidence file | SHA256 |
| --- | --- | --- |
| debian | netbird-packaged-client-native-7cd9292.log | `71cefa49d21ffefd221cd50f9b95e91a9194ca350ba712bc4f135bd42cce6b26` |
| debian | netbird-packaged-client-7cd9292.png | `ee721bc8d0cdb9636698b0fd3bbf5d0bd1b70ce0bbf32e71f08e91a0f14dc779` |
| debian | profile-supervision-netbird-native-7cd9292.log | `5b28b947c2f9da42e6bfbb5d2f982b7a6106e57a1e0577012b2e6336c2470d73` |
| debian | netbird-connected-native-7cd9292.log | `433a4b4a4258b516ce7113e09f02500ab7b1417a4ae14524f6b7c70596943a9f` |
| debian | netbird-connected-recovery-native-7cd9292.log | `405ad537aaf2d993d6bc902e552cff42a3b86c8a9c3f9b5a016720881070f2dd` |
| debian | netbird-connected-kernel-7cd9292.json | `d180c484dee672f1fb589916635a13031b1f95947fafc88df86857388f4ae7c3` |
| ubuntu | netbird-packaged-client-native-7cd9292.log | `22d66649ecf494e809037309017516b90b0208dbdca6438a4dba98c4f3960d3f` |
| ubuntu | netbird-packaged-client-7cd9292.png | `607a500bb5b4d06fab7f3df018773e67746472e109767d963e28513c92171f19` |
| ubuntu | profile-supervision-netbird-native-7cd9292.log | `a51ce4f7ca02f15abe3b30c0fa96add268faef1d23a72e64810d7ab9e70cb9a8` |
| ubuntu | netbird-connected-native-7cd9292.log | `cb78ab2c66fcfa72c16111499eab5ca993941c9ef4b1fefc504bfda2d7fad4b6` |
| ubuntu | netbird-connected-recovery-native-7cd9292.log | `746098161ebdb07b7a75b4aca6e205ace56bf5ec25d5b7171eccc64917ec7337` |
| ubuntu | netbird-connected-kernel-7cd9292.json | `834087beb7928fc92a494c4ed6afd4d6b5b1d8eb0ff90115cb67aed700885a2a` |

After successful GUI checks the inert vendor package was purged. Both connected
matrices removed their captured child/provider/network/DNS/NAT and admission
fixtures; account/common-PAM snapshots and original Home/native network matched.
Captured laboratory cleanup removed its unit, binary, realm, data, credentials
and keys. Postchecks pass on each base: original active/unlocked Home, empty
schema7 journal, forwarding0, host/runtime inactive, socket disabled/inactive,
no child/provider/vendor/NET/veth/NAT/laboratory fixture and dpkg verify/audit clean.
The packaged private catalog intentionally remains; it has no global launcher.
Public staged inputs and fixed QA helpers remain only in disposable QA guests.

The welcome Connected label is static artwork, not browser authentication proof.
Real enrollment here uses a laboratory setup key. Actual browser PKCE, onward GUI
flow/tray behavior, Home-tunnel interference and public stopped-profile provider
activation still need their own integration. Remaining full migration features
are active; no push, donor/Forge/owner VM/Acer change or ISO rebuild was performed.
