# Captured network inspection checkpoint

DE revision `9abeb50648b6f57bd5156c290a0d9f971d3a2487` adds the fixed read-only
`desktop-network-info` helper to the optional accounts payload. It uses the
existing current desktop peer, ownership lock and captured service graph. The
JSON records actual namespace identities, the child resolver identity and only
the configured family's physical forwarding peers. Temporary descriptors are
closed after inspection. No namespace, desktop, resolver or VPN is created.

## Executed checks

On Debian 13 and Ubuntu 26.04, nine focused model/transport cases and the fixed
policy metadata case pass. CMake's `profile-network-info` entry passes on each
base; staging verifies the executable helper and its exact policy path. The
models use the real current kernel namespace descriptor but synthetic captured
login/service owners. They do not establish real graphical authorization or
distinct-profile namespace acceptance.

All fourteen native 0.1.3 DEBs build successfully. Each accounts build passes the
four selected CTest groups: command budget, live DNS, carrier refresh and network
inspection (31 cases per base). The remaining six packages per base are
explicitly build-only. All artifact hashes match their manifests; exact internal
profile dependencies are 0.1.3-1, while session-entry remains 0.1.0-1.

| Base | Artifact | SHA256 |
| --- | --- | --- |
| debian | `karyo-profile-accounts_0.1.3-1_amd64.deb` | `49b0a77d85529cd8bfa7a49f5576941947d6b84daa463bb5a68225ef85b78ff2` |
| debian | `karyo-profile-clipboard_0.1.3-1_amd64.deb` | `84f8764f41b7ce58bb1fefdfff9e649616ff6e6e1c37356e0a7fd9230208ba79` |
| debian | `karyo-profile-host_0.1.3-1_amd64.deb` | `881dd21390975c6ada8ed9abd1916bfebb12dd20a5a07f88449a157ff854ca12` |
| debian | `karyo-profile-netbird-client_0.1.3-1_amd64.deb` | `97e477df4d710badedf3700251a0e6fcc257514cf1ed397a75fa0557febfa5d9` |
| debian | `karyo-profile-password-sync_0.1.3-1_amd64.deb` | `7a7e0225b26d2dfa6eb06dc2a615d89ce2d0efb73c6b994f1e612341ce213898` |
| debian | `karyo-profile-runtime_0.1.3-1_amd64.deb` | `d8b642472c65a08ba9e1f3155545603b8e3c5fe964753e3114fd8bf1b79b9e39` |
| debian | `karyo-profile-session_0.1.3-1_amd64.deb` | `c33bbdc3fae4f70b3c810f0c0221a812ec39671c84e194e3b4632ba2861ef6df` |
| ubuntu | `karyo-profile-accounts_0.1.3-1_amd64.deb` | `41ea53471e4d3f945315d3c3273855700f75e4bb51d26948c2fec6abfde97a9f` |
| ubuntu | `karyo-profile-clipboard_0.1.3-1_amd64.deb` | `11f573b630b665481d1f39e166556ea3137d181ac7146382720062679aa5edd5` |
| ubuntu | `karyo-profile-host_0.1.3-1_amd64.deb` | `29cbea4b22d682743411de16f0da210cba28d06b127e56ea0f2f64c61ba8994c` |
| ubuntu | `karyo-profile-netbird-client_0.1.3-1_amd64.deb` | `f5d1f529bad5b37d84a318e2f0036e4d0b8f356353893ba05255dac893f302fa` |
| ubuntu | `karyo-profile-password-sync_0.1.3-1_amd64.deb` | `e8ffcecca1d8571f8eaacb94f4758cfccc02bb7e3d4ac9885547f881763c8b56` |
| ubuntu | `karyo-profile-runtime_0.1.3-1_amd64.deb` | `c32d665dab2027b3c40eb79f046c1b98e4bf90ce4f301c5fb7ff7070b620e824` |
| ubuntu | `karyo-profile-session_0.1.3-1_amd64.deb` | `8c7a5cd38630b556c4eebbad81e1bb89d4ed2b752b5577c86b419ede931e10bb` |

## Remaining boundaries

The response is explicitly `inspection_only`. This does not implement provider
descriptor transfer, worker registration, revocation or cleanup. No external
client is changed or accepted by these checks. Real caller/profile inspection,
provider lifecycle and simultaneous external VPN use remain separate gates.

These packages have not replaced the accepted installed 0.1.1 sets on the QA
VMs. Native changed-carrier packet acceptance remains pending the user's choice
of the existing dedicated QA guests with exact restoration or full disposable
clones. The stopped nested-systemd bring-up is not retried. Wine, Darling,
distribution sources and ISO outputs are unchanged.
