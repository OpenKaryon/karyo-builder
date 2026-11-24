# Carrier replacement source and package checkpoint

DE revision `c8a572bb03aa307063185dc0c8e7d0892da586ee` implements journaled
replacement of the physical address, gateway and interface for a live private
profile. It retains the namespace, resolver processes, table/chain identities
and source/return selectors. It pauses only owned forwarding traffic while
routes and private DNS change, then publishes the new policy atomically.

Schema 9 admits only captured transition contexts. Interrupted work can be
reattached, retargeted after another carrier change, or removed after the
profile's consumers close. Missing old-address routes and link-down flags are
handled without adopting unrelated route rows. This is source/package evidence;
native changed-carrier packets and graphical lifecycle are still open.

## Executed checks

The focused 34-case source group passes on Debian 13 and Ubuntu 26.04. Its eight
carrier cases cover new address/interface/gateway, gateway-only replacement,
the same-interface address change, automatically removed old-address routes,
reattachment after a command failure, another target during an unfinished
transition, a further change after DNS acknowledgement, and offline teardown.
The new CMake/CTest `profile-carrier-refresh` entry also passes on both bases.

Firewall fixtures are captured native nftables policies for initial, paused
and replacement states. Their synthetic token/interface/address identities are
normalized for deterministic replay. Source cases do not represent native
packet delivery or real hardware DHCP.

All fourteen native 0.1.2 DEBs build successfully and match their recorded
SHA256 values. Accounts builds run only the selected budget, live-DNS and
carrier CTest groups (22 cases per base). The remaining six packages per base
are explicitly build-only, with CTest recorded as not-run. Exact internal
profile-family dependencies are aligned to 0.1.2-1; session-entry remains at its
existing unrelated version.

| Base | Artifact | SHA256 |
| --- | --- | --- |
| debian | `karyo-profile-accounts_0.1.2-1_amd64.deb` | `95d88d4e1daac5378992e2711193553c8a7db3316190878fda9e34d42c7e863f` |
| debian | `karyo-profile-clipboard_0.1.2-1_amd64.deb` | `2c042aaa76b9f03af6701d6b1534fa1acce8513653873600744a5b77b406b080` |
| debian | `karyo-profile-host_0.1.2-1_amd64.deb` | `26a5b40fa4cdf51d4ee1fca5ca45847daa6ebf0b58ecb45a8da847eee0c4834d` |
| debian | `karyo-profile-netbird-client_0.1.2-1_amd64.deb` | `5946c2806d093c653234cf8a2f521a988cf1f6582b8620a5c99c7f92c2f945a2` |
| debian | `karyo-profile-password-sync_0.1.2-1_amd64.deb` | `78d8ffe67659c9f285f732d2a63416ab314a0b9675813f0498cc1523f4ddc80f` |
| debian | `karyo-profile-runtime_0.1.2-1_amd64.deb` | `e29ca2334db8de5f1c64ae5df6f2c99894bf701c9235ffa21dc48646da791766` |
| debian | `karyo-profile-session_0.1.2-1_amd64.deb` | `9b09f3c513b8739aa7c22f331fd85c59d4c6e4d56a923671f7bbf4b5b989940a` |
| ubuntu | `karyo-profile-accounts_0.1.2-1_amd64.deb` | `1a962c9a4679d43786c7a6b208c10882cf66bdc86fccfd82667621e6a7719d39` |
| ubuntu | `karyo-profile-clipboard_0.1.2-1_amd64.deb` | `e89919ea4d643626def654c2b581e78cd8f3ce9bfc2fa598f7368283dfc9a4cf` |
| ubuntu | `karyo-profile-host_0.1.2-1_amd64.deb` | `43b38c1737c9f34466df9497bf49cb868e1206a98c7c2fdad1783732fe999f48` |
| ubuntu | `karyo-profile-netbird-client_0.1.2-1_amd64.deb` | `f8df88919b16916d0ad723f31ea1991463fd531e436a79ace2fa7df2a85233e6` |
| ubuntu | `karyo-profile-password-sync_0.1.2-1_amd64.deb` | `954940b65faa9abe8aeea4dac938c750857d34a2d306bf5df9d74fc2fe60d986` |
| ubuntu | `karyo-profile-runtime_0.1.2-1_amd64.deb` | `05d2348612e0c208eba2844c126864c4cda19bae42b9c13805975444dbbb4104` |
| ubuntu | `karyo-profile-session_0.1.2-1_amd64.deb` | `6c3ad30ce2f8fcf5969ed442598f6fce3aaf1519a27a14b61147a95dc0193af1` |

## Native boundary still open

The additional minimal nested-systemd fixture creates private namespaces and
changes forwarding only inside its own network namespace. Its system bus
activation fails, so transient-service acceptance did not complete. This bring-up
path was stopped after bounded diagnostics. All such instances are terminal;
outer guest PID 1 and forwarding were preserved. No packet/lifecycle pass is
claimed from those runs.

The user was asked to choose between ordinary packet acceptance on the existing
disposable QA guests with exact network restoration, or complete disposable VM
clones. That choice remains pending. The 0.1.2 packages have not replaced the
accepted installed 0.1.1 profile sets. No new installed, upgrade, graphical
Home/Work or real external-client acceptance is claimed here.

The native DNS fixture now accepts an explicit `--version` for exact staged or
installed package identity checks. Its previous 0.1.1 default is unchanged; the
new option alone does not establish a 0.1.2 native pass.

Remaining work includes that native packet gate, the generic external-provider
context/lifetime API and real-client boundary, VMware host payload/display
scenarios, and final joined current-source graphical acceptance. Distribution
images, Forge, Wine and Darling are outside the current work.
