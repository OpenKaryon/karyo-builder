# Updated strict sandbox acceptance on Debian and Ubuntu

This update supersedes the unresolved Ubuntu sandbox result in the historical
report below. Both guests now pass the **default strict** installed GUI gate:
`sandboxed_webkit_renderer:true` and `window_only_gate:false`. The whole migration
is still active; this is not connected-VPN or real account enrollment acceptance.

## Cause and preserving launch policy

Inspection of NetBird v0.82.1 `client/ui/tray_linux.go` found that its Linux startup
helper sets the WebKit sandbox-disable environment variable internally when its
system-wide userns test fails. It first respects an already supplied value.
Ubuntu's global restriction flag therefore triggered that heuristic even though
the ordinary renderer could run with the actual native bubblewrap/AppArmor policy.
The prior `/proc/PID/environ` snapshot was only an exec-time environment view and
did not exclude a later Go `os.Setenv` call. That earlier absence check was not
sufficient to diagnose the cause.

The Karyo GUI wrapper now explicitly supplies
`WEBKIT_DISABLE_SANDBOX_THIS_IS_DANGEROUS=0`, overriding an inherited opt-out and
preventing the vendor helper from writing `1`. WebKit's corresponding zero-value
path preserves sandbox enabling. No binary fork, legacy force flag, sysctl,
AppArmor policy or system-wide userns change was introduced. CLI launching is
unchanged. The proof is the strict renderer observation on both actual guests,
not the environment value alone.

Primary sources inspected:

- [NetBird v0.82.1 Linux GUI bootstrap](https://github.com/netbirdio/netbird/blob/v0.82.1/client/ui/tray_linux.go).
- [WebKitGTK 2.52.6 process-pool sandbox policy](https://github.com/WebKit/WebKit/blob/webkitgtk-2.52.6/Source/WebKit/UIProcess/glib/WebProcessPoolGLib.cpp).

## Exact sandbox acceptance inputs

Installed production DE revision: `8a09bb0991743951c95cf9ed25f0a1c0a447737d`.
Source archive SHA256: `27e7812175a3526d4e564d7142ae6de67e23842ab83ea0d2a439c043917a67c5`.
All eight package builds, both inactive installs and both strict native runs
returned zero. The source test was then committed separately in `f2ee8a9`.
Later provider-journal packages replace these installed packages; see
[provider journal acceptance](VALIDATION_PROFILE_NETBIRD_JOURNAL.md).

| Base | Component | Bytes | DE package SHA256 |
| --- | --- | ---: | --- |
| debian | accounts | 91252 | `10c04077a6626ea2f904b507878ada57984edb9cefb3edbce2d9d8cdf2190e9a` |
| debian | host | 37252 | `32701659ed2c9d7a5b8fdff5f267eae4908c0a3cdbb7b24ced4c1c0ddff49661` |
| debian | runtime | 37196 | `57fe17f8aedf16e4a2acf3da82793b0b8d2472b6447eaf6e43579c0f71edde13` |
| debian | client | 37012 | `bf86024d35ba62df03e4ec451b48c95701f8ec6a8f625d6fab888e9d2efbbad5` |
| ubuntu | accounts | 92586 | `ebbe871b98ebb7d5d78d305a226d8f5a767e7a14d19aea5d392728c0efb44d2c` |
| ubuntu | host | 37704 | `6833a813a32740dd2e933ed7830c91e4d879ca6ab672979065d7dc42ef554a6a` |
| ubuntu | runtime | 37718 | `f59abd900e8a0ddaffa33b36c4a1074d172a297da7a467f96023d500e449edd7` |
| ubuntu | client | 37504 | `eccc67deb095c1732d1c492df01491cb13f45bbdc4efaab3e133e39a38c6e5cf` |

Native probe SHA256: `a5088e455e8afe4b350bb07503731d44d4145f19fb03533ff0b487cf3160e231`.
The vendor archives and native WebKitGTK dependencies remain the reviewed inputs
in the historical report. Vendor maintainer scripts were not run.

Both ordinary CLI/context checks, real welcome-window rendering, zero ambient/
inheritable capabilities and the asynchronous synthetic private-loopback callback
also pass. The default renderer gate additionally observes NoNewPrivs1,
seccomp2 and a user namespace distinct from the ordinary GUI parent. Real remote
PKCE/enrollment, interactive main-window/tray behavior and connected DNS/exit-node
operation are still separate work.

Preserved logs and visually inspected frames:

- `out/debian-vm-qa/results/profile-netbird-client-native-8a09bb0.log`;
  `netbird-client-8a09bb0.png` SHA256 `899cef12dd9610559951c1f7df6718534fabca435614db3cbc19b7030afd968e`.
- `out/ubuntu-vm-qa/results/profile-netbird-client-native-8a09bb0.log`;
  `netbird-client-8a09bb0.png` SHA256 `e0bf96d94cd2d2ad898bf54c2e2cc73d7981fa89a79471d6bf27aeb91562a453`.

Earlier failed/window-only logs are kept below and in ignored QA outputs as
historical evidence, not the current acceptance result. Both strict runs cleaned
their captured graph/provider/network fixtures and exact temporary binaries.

---

# Installed private NetBird clients, GUI and browser handoff

The ordinary client layer now has real installed CLI/GUI acceptance on both bases.
The strict renderer-sandbox check passes on Debian and remains open on Ubuntu.
This is not connected-VPN or actual OAuth/PKCE enrollment acceptance; the whole
migration remains active. No push, Forge, donor, Acer or owner-VM change occurred.

## Exact production and package inputs

Installed DE revision: `a201654499fac9cbb934a1cbb952364521ab545c`.
Source archive SHA256:
`0b5d48d12fa38bd7c55053b0623ed8df935aa83ed49dfcf1727d7af30b8fd1e5`.
All eight final package builds and both inactive installations returned zero.
Exact paths/manifests: `out/migration/profile-netbird-client-{debian,ubuntu}-inputs.json`.

| Base | Component | Bytes | DE package SHA256 |
| --- | --- | ---: | --- |
| debian | accounts | 91092 | `c4600b2a838a7e925db8bed4445c0407d55f2c1d242859ece42c63135e7a83a0` |
| debian | host | 37196 | `278595384cd1b224e0d4d541f674c2e366c8f752c77362cfdc7e7a54faf06c56` |
| debian | runtime | 37128 | `75f480450e589f1c1256cddc4321b2f558ccd9cda6dc301c7fa7147743bf012c` |
| debian | client | 36940 | `955aab0c5c3201a801ad31efcda07de47a05844e9a87774befc7cd29b5760867` |
| ubuntu | accounts | 92412 | `e524db9980e7e273763617a9f74af2786393225f7777324a305850be75b0366b` |
| ubuntu | host | 37646 | `b24eede36b7b7f9befd97168614e9e65d981982a2789845f43a1507c993c6683` |
| ubuntu | runtime | 37634 | `74bcab378b6f73ad439a0f662d5f587e30ff0a1a50cd27fdaf40c1c118e67da0` |
| ubuntu | client | 37432 | `2f8b13a7c9f6119a359059ac2887199ca9ee61d737800e7310c141fd532071ac` |

Actual external NetBird 0.82.1 CLI/GUI archives and digests are the same reviewed
inputs recorded in VALIDATION_PROFILE_NETBIRD_PRELOGIN.md. Their binaries were
extracted only in the disposable guests after digest validation, without vendor
maintainer scripts or global NetBird installation. Matching temporary binaries
were removed after each completed gate. GUI dependencies were installed via the
native guest APT backend, preserving the display manager: Debian WebKitGTK6
2.54.0-1~deb13u3; Ubuntu WebKitGTK6 2.52.6-0ubuntu0.26.04.2. No global AppArmor,
unprivileged-userns or sandbox-disable setting was changed.

Final native probe `karyo-de/profiles/tests/installed-netbird-client.py` SHA256:
`6f9936d8de3ecab7b4c212a98bf5433b6996e87a52e7fdacc7dfce45b2610376`.

## Product behavior

A verified provider publishes root-owned endpoint metadata in its private runtime
directory. The ordinary client validates the exact schema, root-owned file/parents,
UID/group, current native network, private resolver mount identity, socket inode
and root peer PID. Wrong desktop context or caller-supplied daemon overrides are
rejected. No private provider state or credential is published. These launch
checks prevent accidental wrong-context clients; socket/filesystem permissions
and the upstream daemon remain the actual access-control boundaries.

`karyo-netbird-cli` and `karyo-netbird-gui` run the external binaries through
setpriv with inheritable/ambient capabilities cleared. They preserve the ordinary
capability bounding set and do not set NoNewPrivileges or disable WebKit sandbox.
Only those clients get the private opener PATH. Its HTTP(S)-only handoff starts
native xdg-open without waiting for the browser and never logs authentication
URLs or codes on failure.

The separate optional client package depends on accounts helpers, util-linux and
xdg-utils; installation does not pull in a vendor package that enables a global
daemon. Actual external binaries and public provider activation remain explicit
provider/distribution integration work.

## Installed behavior observed on both bases

The fixed root QA driver creates a controlled unprotected private graphical Work,
then starts the verified provider and ordinary clients in that session. This is
a direct owned-lifetime fixture, not a public VPN activation or journal-recovery
test. The daemon remains unenrolled; no private server/profile/setup key is used.

Both guests passed:

- Correct UID launched from the host network/resolver is refused by the wrapper;
  the same ordinary UID launched through its scoped user manager can use the CLI.
- Actual NetBird GUI maps a window, renders its first-run welcome content and
  remains in the private network/resolver. Its real process has UID1002 and zero
  inheritable/ambient capabilities. This does not claim completed onboarding,
  interactive main-window/tray behavior or remote authentication.
- The installed opener hands off a synthetic HTTP URL to the native xdg-open
  path. A deliberate cold test browser waits, while the driver only then opens
  a listener on Work's loopback port53000; the browser reaches that later listener
  in the exact same private namespace. Handoff must return within2seconds.
  This proves nonblocking handoff/loopback context, not actual NetBird PKCE/OIDC.
- Exact GUI unit stop, provider stop, Home selection and natural manager teardown
  close the graph in ownership order. Known previously absent QA state/binaries
  are removed explicitly; product state persistence is unchanged.

VM-only RFB frames were captured without host focus and visually inspected. They
show the NetBird welcome window; the example image inside it says Connected as
static welcome artwork and is not evidence of a real connection.

- Debian frame: `out/debian-vm-qa/results/netbird-client.png`, SHA256
  `83a777b9a0b0b62275fe8d7ab490eacb2fb0f4427dc3077c1a540079218721c8`.
- Ubuntu frame: `out/ubuntu-vm-qa/results/netbird-client.png`, SHA256
  `45d33a392d2183a2491f248a72f68733090302d7da950b9009837b75b62635fe`.

## Strict sandbox result and preserved failures

The default probe additionally requires a WebKitWebProcess with NoNewPrivs1,
seccomp filter mode2 and a user namespace distinct from the GUI parent. Debian
passes that strict mode. Ubuntu's actual renderer was NoNewPrivs0/seccomp0 in the
same user namespace; strict mode failed and remains an open integration issue.
None of the inspected sandbox-disable variables, Snap flags or Flatpak/container
markers was present. The cause is not proven; do not label it an AppArmor or
compiled-out-backend finding. Package rules and upstream sources were inspected,
but that inspection does not supersede the actual failed runtime criterion.

Ubuntu's final separate `--window-only` run explicitly reports
`sandboxed_webkit_renderer:false` and `window_only_gate:true`. It proves only the
functional client/GUI/handoff behaviors above. It is not a strict sandbox pass.
The previous strict failures and sanitized process diagnostic remain in
`profile-netbird-client-sandbox-check-failed-native.log`,
`profile-netbird-client-sandbox-raw-native.log` and
`netbird-sandbox-diagnostic.json` under Ubuntu results.

Initial frame confirmation also timed out on both guests. Those failures are
preserved in `profile-netbird-client-frame-timeout-native.log`. Automated VM-frame
acknowledgement subsequently passed. One pre-allocation logind inventory failure on Debian coincided with a harness
that repeatedly opened SSH sessions. Transient session churn is the likely cause,
not a captured session-ID diagnosis. The final harness removes that observation
churn with one persistent SSH channel for ready/frame ACK. The product
inventory checks were not weakened. All known failed QA resources were verified
clean before retries; failures were never recorded as passing gates.

Final logs: `out/{debian,ubuntu}-vm-qa/results/profile-netbird-client-native.log`.
Final baseline checks: `profile-netbird-client-postchecks.log`: original active
unlocked Home, no child/provider/GUI/vendor/state/namespace/veth resources,
forwarding0, empty schema4 journal, inactive host/runtime units, clean installed
DE package verification and dpkg audit on both guests. Native QA preserves and
restores captured IPv4 conf values and account/common PAM bytes.

394 source tests pass on each base as root (4 intentional skips) and ordinary UID
(106 privilege-dependent skips). Builder's38 tests retain one platform skip; the
new recipe and eight actual package builds pass. No C++ behavior changed.

## Remaining work

Resolve the Ubuntu renderer-sandbox criterion. Join durable provider/tunnel
receipts, owned wt0/routes/firewall inventory, connected teardown and real client
launch/callback to the long-lived host before public VPN activation. A configured
VPN profile continues to fail before allocation instead of silently using an
ordinary network. Actual PKCE/connected DNS/exit-node, app overlays and family
clipboard remain open, along with cold main startup, interrupted GUI recovery,
dynamic DHCP/DNS and the remaining Wine/Darling/VMware migration items.
