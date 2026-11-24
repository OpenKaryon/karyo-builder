# Installed main-login acceptance

This checkpoint advances beyond the inactive PAM-library check in
[the earlier report](VALIDATION_MAIN_ENTRY.md). It tests installed profile
packages with actual LightDM and an existing standalone Karyo desktop baseline
on independent Debian 13 and Ubuntu 26.04.1 QA VMs. It is not the complete
simultaneous VPN acceptance matrix.

## Build inputs and installation

The five recipes are `profile-accounts.json`, `profile-session.json`,
`profile-host.json`, `profile-runtime.json` and `profile_login.json`. Their source
is DE revision `01ab67f0e1aff7b175f802ea08877129c4a87744`; the profile-session
payload is then corrected with the exact configuration-directory change in DE
revision `a2ca9fe`. Captured manifests retain the source archive, recipe bytes,
patch hash and resulting package checksums.

Both bases execute the unchanged native `build_package` core from Builder
revision `e26efce`. Docker SDK startup remains unavailable; these are native QA
builds, not a successful Docker CLI run. CMake stages the named components,
native ELF dependency discovery handles the PAM library and native dpkg installs
the resulting artifacts. The account project remains compiler-free; the PAM
library uses the separate C++17 build.

Installation leaves the LightDM/common-session files unchanged, creates no
main-account policy and starts none of the profile services. Debian initially
lacked nftables; installing its declared native dependency completes package
configuration without removing another package. Dpkg audit is empty afterward
on both bases.

Installed acceptance exposed a real path error: the profile-session PAM policy
was under `/usr/etc/pam.d`. Rebuilding with the resolved GNU system configuration
directory places it at `/etc/pam.d/karyo-desktop`, records that path as a Debian
conffile and removes the obsolete payload on upgrade. The installed runtime
prerequisite check then passes on both bases. The corresponding lock destination
is corrected in DE source, but this gate does not rebuild the lock executable.

| Base | Package | Bytes | SHA256 |
| --- | --- | ---: | --- |
| Debian 13 | karyo-profile-login 0.1.0-1 | 24152 | `238d12af40d120b92825d510e015e8f0dee75f3b3ca0674bfd695c6489cdefd4` |
| Ubuntu 26.04.1 | karyo-profile-login 0.1.0-1 | 26332 | `508050688697cd26e77976312c9616b84bbe75df66722d4c645629e575e08f0d` |
| Debian 13 | karyo-profile-runtime 0.1.3-1 | 44036 | `026c6a828f6dded0080ea4ae4edcd1d7e184e9dabcac8f66da44c1e519bf5bc7` |
| Ubuntu 26.04.1 | karyo-profile-runtime 0.1.3-1 | 44712 | `1eaa8fab4e7d8f5b1e6e1fab18020327c2a0ad75bb9f8bfb65c2d4d1be1809fd` |
| Debian 13 | corrected karyo-profile-session 0.1.3-1 | 44076 | `632648f15e7d7daae8ed007f7e13cbeff6f5b057f617ebe1021cf080e25ca5e9` |
| Ubuntu 26.04.1 | corrected karyo-profile-session 0.1.3-1 | 44704 | `51d6f01f228c2e3cf080331c65a830769164db8e3d6045e0be696a238ac423d5` |

## Actual login and lifetime observations

The QA workflow creates its own temporary account and password. With LightDM
stopped and the account offline, explicit runtime/main-login activation records
the original PAM content and enables only that account. The stock GTK greeter
authenticates normally and starts the installed Karyo Wayland session.

The real root LightDM PAM parent, graphical shell and native user manager use
the captured private namespace and resolver mount. A fresh ordinary-user process
activated by that manager resolves public DNS, completes verified HTTPS and
exchanges real TCP and UDP payloads with a controlled endpoint bound to the other
VM's physical address. Wayland captures show the actual Karyo desktop on both
bases; no fixture compositor substitutes for it.

The actual installed host service is restarted while the graphical session
stays open. Its controller PID changes. The shell PID, login, namespace, resolver
inode and manager/DNS service lifetime identities stay the same, and the packet
checks pass again. This is a native service restart, beyond reopening a journal
inside the earlier harness.

Ordinary compositor logout closes the real PAM stack. Logind and its user
manager finish naturally; the host removes its captured temporary manager policy,
DNS, forwarding and namespace. No forced user-manager stop substitutes for that
lifetime check.

While main-login policy remains enabled for the same account, a second normal
LightDM login selects stock Xfce. That session and manager retain the host
namespace and resolver, and no private runtime receipt or manager policy appears.
After Xfce logout, explicit removal restores exact original LightDM PAM content.
QA cleanup removes the temporary account/home, stops its echo endpoints, disables
the test runtime and restores the previous forwarding value. The profile packages
remain installed but inactive for the next acceptance stage.

## Remaining scope

Fifty selected functional source cases pass on both bases, including a later
account-reselection correction after completed main-login removal. That later
temporary-configuration check is separate from the package inputs above. The
security suite is not run.

This gate covers one managed main desktop and a sequential Xfce login. It does
not establish simultaneous real Home/Work VPNs, private network-service/socket
views, upstream WireGuard/OpenVPN/NetBird worker lifetimes or IPv6. Those remain
required before the requested network-isolation objective is complete. No VPN
client or server runs in this main-login gate.
