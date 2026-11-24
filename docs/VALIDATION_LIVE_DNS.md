# Live physical DNS and bounded startup

DE revision `5122590f44e7df093ce5389239541141165b1662` supplies the profile
0.1.1 runtime. The earlier startup deadline correction is included. This
checkpoint covers DNS-only physical changes; address/gateway replacement and
real external VPN-client compatibility remain separate work.

## Source and build acceptance

The focused source group passes 26 cases on Debian 13 and Ubuntu 26.04:
four shared-deadline cases, twelve existing startup cases and ten live-DNS /
monitor cases. Both native kernels also pass actual physical route/DNS discovery
and the four command-deadline cases without installed-file or host DNS changes.

All seven profile recipes now use 0.1.1-1 with consistent exact profile-family
dependencies. The unrelated session-entry dependency retains its existing
version. Fourteen native DEBs build successfully. Each base runs the selected
`profile-live-dns` and `profile-network-budget` CTest groups in its accounts
build. The other six packages per base are explicitly build-only; their
manifests record CTest not-run rather than a complete-suite pass.

| Base | Artifact | SHA256 |
| --- | --- | --- |
| debian | `karyo-profile-accounts_0.1.1-1_amd64.deb` | `94bcd0f6a01e6276afe5c7f4eff7e6c38b617e940cc334b11f9b2410f390a5cc` |
| debian | `karyo-profile-clipboard_0.1.1-1_amd64.deb` | `92e17696a484ee5f6100a69a98cea1f7770746d5fac8c644f85205fdec17d215` |
| debian | `karyo-profile-host_0.1.1-1_amd64.deb` | `24982bf78bae8f9fe5c41324ff31bc5412015c1026c9cf66e142e0272057f66e` |
| debian | `karyo-profile-netbird-client_0.1.1-1_amd64.deb` | `ab883d67f588fbbf65bd4162d10db1b61043d8d95aa348a555d51918ac63cd42` |
| debian | `karyo-profile-password-sync_0.1.1-1_amd64.deb` | `2b992c756fcc1fea9fc13e3c7cbd4374123a4aa019590bbf9a04acb305c4adaa` |
| debian | `karyo-profile-runtime_0.1.1-1_amd64.deb` | `0545849e56926b43e28b6a59b73a0354528ca8815444ce337c35784009613de9` |
| debian | `karyo-profile-session_0.1.1-1_amd64.deb` | `aaf265ea195317f393be1616067f69994435025f7be31afb4cd19e78cc376325` |
| ubuntu | `karyo-profile-accounts_0.1.1-1_amd64.deb` | `bade64c26322bc343eecd25e3d342f5a8c500d5cfa9079a09908a9156bfb8ee0` |
| ubuntu | `karyo-profile-clipboard_0.1.1-1_amd64.deb` | `9de52f5f9257f7a601f7925ed759340b3ac56d360c9179d089667060817bb61d` |
| ubuntu | `karyo-profile-host_0.1.1-1_amd64.deb` | `ea81bfb4ee3ec691d6bd7cc9dd8afa031cb6151b3fecb20d23d518de71242729` |
| ubuntu | `karyo-profile-netbird-client_0.1.1-1_amd64.deb` | `ac8a508a26cbde315912aaf98cfe36e3e459c3be69017ed8897f0f40b85cc0bf` |
| ubuntu | `karyo-profile-password-sync_0.1.1-1_amd64.deb` | `481164696da04b02cd30f7f2d1140e2f959ab022f421c98a800d0a10505e464b` |
| ubuntu | `karyo-profile-runtime_0.1.1-1_amd64.deb` | `1ebb3c0d931f9c6301ecbbce5f7186d33c64a8e71fcc14aa369ace6f8715a083` |
| ubuntu | `karyo-profile-session_0.1.1-1_amd64.deb` | `f895c873917d58a2cf6eefda335b2a8d359004bbee90aab2e5404e2ef7247d61` |

## Native package and lifecycle acceptance

`tests/acceptance/check_live_dns.py` is a root-only disposable-host fixture. It
accepts a native DEB and its SHA256, extracts its payload and optionally requires
that every installed payload file match before importing the installed code:

```sh
sudo python3 -I check_live_dns.py --package NATIVE_DEB --sha256 SHA256
sudo python3 -I check_live_dns.py --package NATIVE_DEB --sha256 SHA256 --installed
```

Both native bases pass staged-DEB and actual installed-runtime execution. The
fixture uses an explicitly modelled account, real namespace/link resources,
private D-Bus and systemd-resolved units, a real namespace-local WireGuard link
with its own DNS/search domain and a live native sleep process. It verifies:

- Changed DNS servers/search domains on the owned physical eth0 link.
- Unchanged WireGuard-link DNS, live client process, private bus/resolver PIDs,
  runtime identities and configuration file inodes.
- Journal schema 8 reopening and return to the original physical DNS seed.
- Complete removal of its owned resources with unchanged host resolver and
  original namespace inventory.

This is a real private-DNS lifecycle result, not a real external VPN connection,
Internet DNS payload test or full graphical Home/Work transition. Retry after a
transient private-bus failure and deferred polling are covered by the focused
source cases.

APT simulation accepts all seven native packages on each base as seven upgrades
with no additions or removals. Actual upgrade from 0.1.0-1 to 0.1.1-1 then passes,
with exact native payload comparison and retained original-package backups.
Account databases, common PAM files, active LightDM and the inactive profile
host are unchanged. Both guests began and ended at the greeter with no running
Xfce session or retained profile; preserving that absence is not a fresh-Xfce
login result.

Preliminary host-driver failures are retained separately: one assumed Xfce was
already running, and another omitted the extraction parent during post-upgrade
comparison. The latter triggered a successful exact-package rollback on both
bases. Extraction was verified separately before the final successful upgrade.
These driver failures are not counted as passing deployment observations.

Final installed-runtime receipt SHA256 values are
`7d2c591f27d85b98b623d8e5fb71d2b42eaf1efb64e8f4b36e987080ceeae836`
(Debian) and
`c7217d3716a8512c65367fce93ebe47e1d7a0886f433dbdb5e1aa4b874498f69`
(Ubuntu). Their common native actor has SHA256
`6c8936d984398263967c5106ac54830b27379ead8ca76bf2a9c5cf1c59950324`.

## Remaining stage work

Complete owned route reconciliation for physical address/gateway changes,
external provider context/lifetime integration, joined current-source profile
and privilege-prompt/chooser acceptance, and real VMware host-channel/display
scenarios. Distribution images and Forge are outside this stage. Wine and
Darling remain unchanged and are not used as additional completion gates.
