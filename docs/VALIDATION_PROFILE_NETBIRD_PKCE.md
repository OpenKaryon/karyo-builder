# Actual cold-browser PKCE in a publicly started Work desktop

Installed Debian13 and Ubuntu26.04 now pass actual NetBird S256 authorization
with a cold real browser, the ordinary XDG default-browser association, private
callback, successful browser page and a Connected ordinary scoped client.
This is distinct from earlier synthetic callback and setup-key gates.

## Exact code and runtime boundary

This wave changes native QA and documentation only. Production remains the four
profile components from `d140e14c4a1c2b4c364691628ea3ca2674a578a5`, archive SHA256
`14393190246361d7180eb7bb3f851e0abbf764f0a73e336498e745cf295666e3`,
installed as recorded in VALIDATION_PROFILE_PUBLIC_NETBIRD.md. The inert vendor
package and upstream0.82.1 binaries are unchanged. No upstream source patch,
personal profile or system-wide NetBird service is used.

Native browser actor `profiles/tests/installed-netbird-pkce.py`:
`ef74e7b200e08661a6b3b09016466c48bad0eacf15a45dab8a8e6bcb04ff86ba`.
Extended public driver `profiles/tests/installed-public-netbird.py`:
`76c72d9b3fd4d22009871aeee57d95bba3302bda2feb299402e5ecbc83cca584`.
The public driver delegates only its new explicit PKCE case to the actor;
previous missing-payload, pre-login and setup-key modes retain their behavior.
Native QA commit: `5a42b88`.

The last production source regression is still438 cases as root/ordinary users
on each base (4/113 skips). It was not rerun and mislabeled as a new source gate
for this QA-only wave. Both new scripts compile and their actual installed paths
and root-owned hashes are checked by the expanded final native postcheck.

## Real browser path

The normal public helper starts Work and its captured provider/catalog/manager.
The new absent-before QA child owns a private browser fixture. The final test
selects a user desktop entry as the default HTTP and HTTPS handler with xdg-mime
and verifies the associations. It does not set BROWSER or force a generic
desktop environment: the ordinary Karyo user manager supplies the real context.

The ordinary scoped CLI invokes NetBird up against the disposable realm without
a setup key. NetBird emits an actual S256 authorization request through the
installed asynchronous opener and system xdg-open. The selected ordinary XDG
handler starts a new real browser session via the already-ready native driver.
There is no browser session before the request; only the automation driver is
prestarted. The browser fixture is fresh, without existing cookies or login.

Debian uses native Chromium156.0.8078.79 and matching ChromeDriver156.0.8078.79.
Ubuntu uses native MiniBrowser/WebKit2.52.6 via WebKitWebDriver2.52.6 with explicit
private mode and sandbox enabled. Actual browser form controls receive only the
ephemeral owner email/password of our own isolated realm. No HTTP script submits
credentials or fabricates the browser callback. The real callback handler
exchanges the authorization code and verifies state/PKCE normally.

The native Work listener on port53000 becomes available while the host/Home
listener remains absent. The browser loads the genuine Login Successful page,
the CLI exits0 and the public driver independently requires actual daemonStatus
Connected. Existing Home/Work switches preserve the provider receipt; connected
logout cleans up and returns the original Home/VT.

The bounded browser automation follows the [W3C WebDriver protocol](https://www.w3.org/TR/webdriver2/).
Backend options were checked against installed driver/MiniBrowser help and the
[WebKitGTK driver documentation](https://manpages.ubuntu.com/manpages/noble/man1/WebKitWebDriver.1.html);
the browser actor never disables sandbox for a passing result.

## Native renderer proof and safe evidence

For both backends the root observer finds actual renderer descendants of the
captured driver, requires NNP1, seccomp2, a user namespace distinct from the
parent and zero ambient/inheritable capabilities. It exports only safe native
IDs, cgroups, sandbox flags and roles, never full command lines or process
environments. Final JSON contains four sandboxed Chromium renderers and one
sandboxed WebKit renderer. The supplied PNG is the browser content screenshot;
the callback query is removed from browser history before capture. Both final
frames were visually inspected and show genuine Login Successful content.

Authentication URL, state/code/token values and owner password are not exported.
The driver stdout/stderr is null, its request logs are disabled, and temporary
credentials reach the guest through private stdin/root600 files, then a child600
file. No personal user data or production identity provider is involved.

| Base | Immutable result under out/{base}-vm-qa/results | SHA256 |
| --- | --- | --- |
| debian | netbird-pkce-xdg-d140e14.png | `726ba76ca57dab52aab01bfe026baaf3be9693df8f558836ea9157a49cd33200` |
| debian | netbird-pkce-xdg-d140e14.json | `9f662571044557a7d07bf58a6640bdfc8cb0daa2c730dbd67cb418df6b6d1003` |
| debian | netbird-pkce-xdg-d140e14.log | `72acdab6cd1ea989721172e8fbe7ab1aafb5c7fa9b28a42e57e22cc091d0d945` |
| debian | netbird-pkce-postchecks-d140e14.log | `3f4702d3e21b3fcc2f5fd1f05249301ac5f322f29cfd2e4ed99e02d417ab9033` |
| ubuntu | netbird-pkce-xdg-d140e14.png | `913cc07b318dd282206474e83a3c70c60eeaed9278541ff64353d3e82ccdab88` |
| ubuntu | netbird-pkce-xdg-d140e14.json | `7e37c129ae1a2b0c3030abbbd0683a1d108f511cdcde76646d88813685afaf5a` |
| ubuntu | netbird-pkce-xdg-d140e14.log | `c49503acc3fd03be24621a344cbe27ddbaf7e8f47aff1a8b7230dfd9ddc410a2` |
| ubuntu | netbird-pkce-postchecks-d140e14.log | `a3e02aa79e1149717c06a48d75e6cbffb8faf3e50d5618a8d0f05ec275235a50` |

Earlier browser-variable runs also passed on both backends and remain as
`netbird-pkce-browser-variable.{log,png}`. They are superseded by the final
ordinary XDG association gate above.

## Preserved fixture failures and exact cleanup

The first Chromium run completed browser login but its initial overnarrow
renderer discovery failed to locate the real process roles. Native descendant
and role observation was corrected; the same strict sandbox conditions remain.
The first Ubuntu run used a MiniBrowser profile option absent in its installed
version and was cut off by the outer public helper's old25-second timeout.
The QA now uses the installed private/sandbox options and an explicit bounded
PKCE deadline. An additional explicit Wayland backend is a QA launch choice;
inspection showed the manager already supplied Wayland environment, so no
missing-Wayland product defect is claimed.

Both first logs remain `netbird-pkce-first-fixture-failure.log`. Exact known
failed-profile logout, captured state/activation/admission cleanup and matching
vendor purge succeeded before retry; cleanup logs are retained separately.
There was no blind restart of a live driver or server after an observation
timeout. A capability probe against the same captured invalid-option driver
also timed out, confirming that waiting alone did not create a browser.

The Ubuntu browser-tools install command returned1 only because it asked for
an unsupported driver --version after apt succeeded. Independent dpkg verification
confirmed all three requested packages installed. The original install log is
retained. This is not labeled a DE/package-install failure.

Final native runs returned0 for both browser-variable and ordinary XDG cases.
Captured browser session/driver shutdown completed; the child/browser state,
user browser association and credentials disappeared with the acknowledged QA
child. The matching inert vendor package was purged; captured runtime policy,
enablement links and interface sysctl defaults were restored. The owned
realm/server/data/owner/PAT/setup key and binary were then removed.

Expanded postchecks return0 on both bases: original Home shell/login active and
unlocked; empty schema7 journal; forwarding0; socket disabled/inactive; host and
runtime inactive; no child/private NET/veth/NAT/provider/vendor/activation/browser
credential fixture; current QA helper hashes and dpkg verify/audit clean.
Safe root600 JSON/PNG reports and fixed QA helpers remain only in the disposable
guests. ChromiumDriver and Ubuntu WebKit driver/API libraries are QA tools;
this wave adds no browser or automation dependency to a DE package.

## Remaining scope

The accepted IdP is the embedded identity service of our own pinned NetBird realm.
This is not evidence for every external IdP/MFA/proxy configuration. Onward
NetBird GUI/tray interaction after login, Home-tunnel interference, remaining
profile application roles, dynamic DHCP/DNS, cold Home/partial graphical recovery,
family clipboard, Wine/Darling/VMware and the rest of the full migration remain
active. No push, ISO rebuild or Forge/donor/owner VM/Acer change was performed.
