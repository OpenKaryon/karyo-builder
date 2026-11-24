# Inactive main-login package checkpoint

The later [installed main-login acceptance](VALIDATION_MAIN_LOGIN.md) covers
actual LightDM entry, native controller restart and ordinary Xfce coexistence.
The evidence below retains the earlier inactive-library checkpoint.

The `examples/profile_login.json` recipe packages the optional session-only PAM
handoff library from DE revision `91aafcffe43b3a653ba079af1d1f95902dfc2e87`.
The recipe follows source HEAD by default. It installs no PAM configuration,
service, authentication policy or launcher; dependencies are discovered from the
native ELF payload through the existing Builder package function.

## Execution and artifacts

Both packages were built in the independent networking QA copies using the
unchanged `build_package` implementation from Builder revision `be60fd7`.
Docker SDK startup was unavailable, so these runs are native guest execution of
that packaging core, not a claim that the normal Docker CLI path ran. Inputs
include checksummed partial Git archives and the captured recipe bytes.

Each run configures a Release build with one job, runs only the
`profile-login-module-abi` CTest and stages the named component. The native
`dpkg-shlibdeps` database determines runtime dependencies. The test harness is
built for explicit acceptance but is not included in either package.

| Base | Artifact bytes | SHA256 |
| --- | ---: | --- |
| Debian 13 | 23444 | `cdac8ca8bd0fca777de2e26c309c0077346a8bcbc3ad2f94e0810d2204815c14` |
| Ubuntu 26.04.1 | 25508 | `941e5a819659dac15c269b734bfc8e9bb4e311a99211954523a5b2bdb9ef9717` |

Both artifacts are named `karyo-profile-login_0.1.0-1_amd64.deb` and are retained
under separate native-base output directories. No package is published.

## Installed acceptance

Both runs install the actual package, verify its payload, load the installed
library's session-only ABI and execute the real-PAM fixture against that
installed library. A temporary account authenticates through `pam_unix`; entry
joins the captured network/resolver before `pam_systemd` starts its manager.
Ordinary direct and user-manager-activated clients pass namespace, resolver,
DNS and TCP/UDP checks. Closing restores the privileged parent's original
namespaces, and the fixture removes its captured temporary resources.

Same-version reinstallation, payload verification and removal then pass.
Checksums of the existing PAM and LightDM configuration trees remain unchanged.
The installed library disappears, the temporary PAM/controller endpoints are
absent, and `dpkg --audit` stays clean. The separate account-only CMake project
also still configures without enabling a C++ compiler by default.

## Limits

Only the PAM library is installed in this checkpoint. Network/controller Python
actors are source fixtures, not the production host broker. No original account
is entered, no real LightDM login is performed, and no upstream VPN is started.
Persistent main-session ownership/recovery, full service/socket isolation,
physical uplink/IPv6 and simultaneous installed graphical/VPN acceptance remain
required. The component must not be activated in a production PAM stack yet.
