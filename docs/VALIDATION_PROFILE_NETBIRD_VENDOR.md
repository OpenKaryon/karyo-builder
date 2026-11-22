# Inert NetBird provider package and actual installed GUI

Builder now has a data-only vendor stage and a pinned optional
`karyo-netbird-provider` example. Debian13 and Ubuntu26.04 packages were built
offline, installed with real dpkg in the isolated guests, exercised through
ordinary scoped CLI and actual sandboxed GUI, then purged with original Home and
host network/account state restored. Public VPN startup remains gated.

## Exact production and packaging inputs

Builder implementation revision: `6c86302a6e4033d9c1ea145eb4f6b8b6282da3c3`.
See VENDOR_PACKAGE_STAGE.md for the contract. The DE runtime remains the previously
installed eight packages from `25273daa8aac34426787a7c78be1cd2b55867ea9`, archive
`b9731d0501e744c1d833ac44375b518c44939d16630650bf476e6e73975ed438`.
DE HEAD `a46e381` contains later QA only; no DE production changed in this wave.

The vendor inputs are the same official NetBird0.82.1 CLI/UI archives used by the
preceding runtime gates, each matched by exact hash and native package identity:
- CLI DEB: `4adff2bbc1529942e914c181badfc17585c78f0532ccaf6c000f5c9300d9a632`.
- UI DEB: `88b36705e8bdd8c297722412ef801519ad9f9b829efd44594d004d35fbe9a937`.
- Upstream root LICENSE: `8343fe949e32a30e2261c4f0967365271d08c4644e879dec5b998d1af666fdb3`,
  extracted from the pinned source archive recorded in the connected gate.

The generated package version is `0.82.1-1karyo1`; its complete regular-file
payload is exactly:
- `usr/bin/netbird` and `usr/bin/netbird-ui` (unchanged vendor bytes, executable);
- `usr/share/pixmaps/netbird.png`;
- `usr/share/doc/karyo-netbird-provider/LICENSE.netbird` (unchanged notice).

Upstream control files, install/remove scripts, desktop entry and polkit action
are excluded. Only generated control/md5sums enter the output control archive.
The recipe requires scoped Karyo client wrappers and the actual upstream GUI
GTK4/WebKitGTK6 dependency family, provides the versioned netbird names and
conflicts with the raw upstream packages. Existing global installations are not
silently adopted, replaced or imported by this stage.

| Base | DEB bytes | DEB SHA256 | Manifest SHA256 |
| --- | ---: | --- | --- |
| debian | 20417724 | `23e05623d8a143f01ef5e662308dbabd0e2ef949bcb367818935bdfd31533c03` | `67cef5534d491c6df2fb49d000fa4b3710c5b7e22e3cd77ff0f8e9e9508dd1b2` |
| ubuntu | 22113674 | `9d75f64275ca813e327ece33d2588ef22d191fd167330cd4220815361863d594` | `33f45cb9c6a432fa9882effab595a0906feb547da1f67c7ee0893b9496a927b4` |

Immutable output folders and checksummed native manifests are pointed to by
`out/migration/vendor-stage-{debian,ubuntu}-input.json`. Current runner hashes in
each manifest were compared against the committed implementation. Different
native tool/compression versions produce different DEB bytes; selected input
binaries/icons/license remain identical.

## Source and native build checks

All47 host Builder tests passed with2 Windows platform skips. All43 applicable
native tests passed without skips on each base, including native symlink cases,
regular-file selection, forbidden activation/escape/link/mode cases, captured
input identity and native receipt tampering. The four Git export-input fixtures
require host Git and passed in the full host suite; native build images omit Git,
so they are not mislabeled as tested inside those images.

Both actual Docker vendor-package runs returned0 with network disabled, read-only
captured inputs, empty capabilities and NNP. Initial test harness staging omitted
example fixtures, then exposed absent native Git for those four host cases.
Those failed logs are preserved; corrected staging/native selection and the full
host suite are the final evidence. No product runtime failure was hidden.
Logs: `out/migration/vendor-builder-{host,debian,ubuntu}-tests.log`,
`vendor-stage-{debian,ubuntu}-build.log` and retained failure variants.

## Real dpkg and graphical acceptance

On each guest, preflight required absent vendor payload, global unit/state,
upstream desktop/polkit/autostart entries and known QA install fixture. The input
DEB checksum and exact generated control archive were verified before dpkg.
Actual installation resolved using already-present dependencies and did not
modify host route/rule/nft/resolver, account/common-PAM or display-manager snapshots.
No `netbird.service`, global provider state or upstream privilege/launcher data
appeared. dpkg verification/audit passed. A normal Home client invocation without
the captured endpoint was denied before reaching a provider.

The previously accepted native driver
`karyo-de/profiles/tests/installed-netbird-client.py`, SHA256
`165dabebcd3f8df96db4986ff61892f4df5483236339c0712f0381daf2fd09c9`, then used the installed
package binaries rather than manually extracted temporary files. Both guests
passed actual ordinary CLI, wrong-context rejection, captured Work network and
resolver identity, zero ambient/inheritable GUI capabilities, real GUI window
and a WebKit renderer with NNP/seccomp/distinct user namespace. The test did not
use the weaker window-only gate or disable the sandbox. VM-only RFB frames were
captured/acknowledged and visually inspected without taking host input focus.

The existing nonblocking private callback test also passed; it remains synthetic,
not actual provider browser PKCE. The visible Connected label is static welcome
artwork, not enrollment evidence. Generic title/taskbar icon fallback is still
visible in the captured welcome: provider-specific scoped desktop/catalog identity
has not yet been published, and icon/menu/tray acceptance is not claimed here.

- debian `out/debian-vm-qa/results/netbird-packaged-client-6c86302.log` SHA256 `056bbe903c50ad6e5b60a3facb66d76f7de956c3586b0c297e0e97e185901d0b`.
- debian `out/debian-vm-qa/results/netbird-packaged-client-6c86302.png` SHA256 `b199be4a7097bce68a1f9c16901002cf6b64f06e60960509441e894564c9d24e`.
- ubuntu `out/ubuntu-vm-qa/results/netbird-packaged-client-6c86302.log` SHA256 `359692b9a112e36d6ddcc2ea34fa939b78b59c73e9bd2cbdfced3feb71d886e0`.
- ubuntu `out/ubuntu-vm-qa/results/netbird-packaged-client-6c86302.png` SHA256 `d6ec84096e91423163b9592232cb0450b58552c512ea55e2874e3a412551ec30`.

After successful GUI exit, profile owners/state/account were cleaned, the exact
installed vendor package was purged and its files/fixture removed. Final original
host network/account/display-manager snapshots matched. Both comprehensive
postchecks returned0: original Home active/unlocked, empty schema6 journal,
forwarding0, host socket disabled/inactive, host/runtime inactive, dpkg clean,
no child/provider/private NET/veth/NAT/QA install fixture, vendor files or state.
Public staged package/manifests and fixed QA helpers remain only in disposable QA.

## Remaining integration

The inert package is now a real reusable Builder output, not a source-only plan
or a distribution-image side effect. It is not yet wired into public VPN profile
startup or the final optional application catalog. Next are scoped desktop/menu/
icon identity and GUI launch defaults, real browser PKCE, Home-tunnel interaction,
then public stopped-profile provider activation and its native acceptance. Other
full migration features remain active. No push, donor/Forge/owner VM/Acer change
or distribution ISO rebuild was performed.
