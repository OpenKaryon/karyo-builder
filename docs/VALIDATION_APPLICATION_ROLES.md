# Optional application role visibility: installed acceptance

This gate moves the generic Home/Work launcher and autostart mechanism out of
the private Workstation provisioning script. It does not migrate personal or
corporate configuration. Forge remains independently owned; its desktop ID in
the non-installed example is data only. No application binaries are copied per
desktop. The base DE is unchanged until an administrator installs explicit role
metadata and marks a family member WORKSTATION=yes.

## Product and package boundaries

Product source: effc7cbaf3c71403f925ab2026a20d102f10d6c9.
Source archive SHA256:
03310174ece18fa09467aafe5b4385102968bcd9898312a93c4c149ba69888f1.
The later DE commit only adds the native QA actor and documentation.

The optional accounts component installs karyo-application-catalog. The helper
uses the real UID and trusted existing family/settings metadata. Other family
members select Home; unrelated families remain unaffected. A versioned optional
/etc/karyo/application-roles.json maps desktop-file basenames separately to home
and work lists for applications and autostart. Both roles retain a common entry;
an empty list masks it in both. It creates only standard Hidden=true masks in an
ordinary user's private content-addressed runtime directory. Unsafe or changed
cache entries are retained and reported. It writes no privileged configuration,
launch command, vendor state or service definition.

The session waits for initial PAM, prepares the catalog, prepends its share and
config roots and imports those fields into activation before normal clients and
dex. User-level XDG override precedence is retained. Visibility is a desktop
preference, not an executable permission boundary; accounts/PAM/network isolation
have separate enforcement. No default role manifest is installed by this package.

The session-entry recipe now selects the independent session CMake directory.
Its existing package name, installed paths and session-runtime component remain
unchanged. The configuration/data package no longer requires configuring the
whole Qt application graph just to ship session launch data.

The mechanism follows the freedesktop [desktop entry Hidden key](https://specifications.freedesktop.org/desktop-entry/latest/recognized-keys.html)
and [autostart directory and precedence rules](https://specifications.freedesktop.org/autostart/latest/).

## Builds and source checks

| Gate | Debian 13 | Ubuntu 26.04 |
| --- | --- | --- |
| Profile source suite, root | 447, 4 skipped, exit0 | 447, 4 skipped, exit0 |
| Profile source suite, ordinary UID65534 | 447, 114 skipped, exit0 | 447, 114 skipped, exit0 |
| Session launch contract | 13 cases, pass | 13 cases, pass |
| Standalone session configure/build/ctest/install | pass | pass |
| Full-project CMake configure | pass | pass |
| Builder native accounts/session packages | pass | pass |
| Installed cold public Work role acceptance | pass | pass |
| Final original Home/runtime/package checks | pass | pass |

Builder host tests:47, 2 skipped, exit0. Source tests cover trusted and malformed
metadata, family role derivation, shared entries, independent autostart rules,
atomic concurrent publication, exact cache reuse and retained unsafe contents.
A CMake missing quote discovered during integration was fixed before the product
commit. The corrected installed component was checked on both bases. Qt's
pre-existing private-Wayland build warning is not a new application-role failure.

| Installed artifact | Debian SHA256 / bytes | Ubuntu SHA256 / bytes |
| --- | --- | --- |
| karyo-profile-accounts_0.1.0-1_amd64.deb | 1da8defc2509246fd644f30eccd11607902fb30e239bdfeb093ac146edeadbea /98220 | a6a55b0b7724f6a4ec425742970e1f9013b547091918fafd75e7d19072c6a4f8 /99704 |
| karyo-session-entry_0.1.0-1_amd64.deb | 1308b7c33fd9a779845c8d2083477ae406d5f8efd9d9c973eb97042d0113afc6 /23240 | f5e073cba8babf20b0c5b9ab0763b472bc60e789b50a2624b51097a18dc5e129 /23668 |

Only these two new production components were installed. Other host/runtime/
client components remain the previously accepted d140e14 build. Source manifests,
package hashes and installation logs are retained under ignored migration output.
Accounts, passwords, common PAM bytes and the chosen display manager are unchanged.
No global provider daemon or optional runtime is activated by package installation.

## Native fixture and evidence

DE profiles/tests/installed-application-roles.py SHA256:
88f6a656937f64261da92e7d933d0bb3f4cd0ef839b0e09fd50c76d99ae99966.
It accepts only the fixed disposable root QA hosts, creates absent-before safe
launcher/autostart entries and a temporary Work account, and uses the installed
public runtime for cold launch and existing-session switches. The fixture has no
corporate endpoints, credentials, Forge binary or real vendor commands.

Both bases verified:

- The ordinary installed Home helper selects Home, reuses its exact cache and the
  real GLib resolver sees Home/common while suppressing Work/never entries.
- A fresh actual Work shell, Files and user-manager activation receive matching
  role-prefixed XDG roots. GLib sees Work/common while hiding Home/never.
- Native dex really executes Work/common marker programs. Home/never markers do
  not run; this checks actual autostart rather than parsing expected text alone.
- Home-to-Work-to-Home switches reuse the running session/runtime token. Work
  logout returns to the unchanged original Home and removes the scoped graph.
- Created desktop entries, manifest, helper, Home cache, child/home/settings and
  captured runtime activation are removed after validation. Native runtime and
  socket finish inactive/disabled, forwarding returns0, journal7 is empty, and
  dpkg verification/audit are clean. Original Home remains active and unlocked.

Initial native runs passed behavior but failed their own cleanup by calling the
ordinary user's cache validator as root. Its correct ownership rejection was
retained; the QA actor now validates as the real Home user. Exact known fixture
contents and captured runtime receipts were checked during recovery, both hosts
were restored, then the complete final actor was run successfully on both. A
recovery-script quoting error was a syntax-only fixture failure before execution.
It is not presented as a product fix or as a successful initial run.

Evidence locations, relative to Builder:

- out/migration/application-catalog-{base}-{root,ordinary}-tests.log
- out/migration/application-catalog-{base}-cmake-fixed.log
- out/migration/application-catalog-builder-tests.log
- out/migration/application-catalog-{base}-inputs.json and build/staging folders
- out/{base}-vm-qa/results/application-catalog-install.log
- out/{base}-vm-qa/results/application-roles-native.log
- out/{base}-vm-qa/results/application-roles-native-fixture-failure.log
- out/{base}-vm-qa/results/application-roles-fixture-recovery.log
- out/{base}-vm-qa/results/profile-supervision-netbird-postchecks.log

Here base means debian or ubuntu. Logs describe the exact checks and preserved
failure; acceptance does not rely on new screenshots in this step.

## Remaining acceptance boundaries

The first role gate preserved the original Home GUI and used its installed
ordinary helper and native resolver in a fresh probe process. A subsequent
actual cold LightDM Home gate now also passes role startup and policy removal
on both bases; see [VALIDATION_COLD_HOME_ROLES.md](VALIDATION_COLD_HOME_ROLES.md).
The Work graphical session and native autostart in this first gate were genuinely cold. Actual Bitwarden/Mattermost/
ExternalProvider GUI acceptance and real Home tunnel interference are not claimed by
safe marker fixtures. The earlier real Work NetBird PKCE gate remains valid,
but was not rerun as part of this role-only gate. Further VPN/clipboard/runtime
integrations and the full migration plan remain active. No push occurred.
