# Migration inventory

The reviewed donor is the Karyo prototype at revision
`716d515b765319981b124fb1812a1e3edb9e0ffd`. Paths below are relative to
that source tree. This map assigns responsibility to reviewed components.

| Donor | Target | Boundary or adaptation | Validation and first result |
| --- | --- | --- | --- |
| `distro/desktop/shared/libopenkaryon-ui` | karyo-de | Split theme/painting foundation first. Retain user settings while using Karyo public names. Desktop entries/icons, common widgets and style are now extracted. Review platform integration separately. | Separate development packages, widget tests and external CMake consumers. Implemented. |
| `distro/desktop/shared/style-plugin` | karyo-de | Widget style and platform dialogs/fonts/icons have distinct responsibilities. | Runtime plugin loads in a separate Qt client on clean Debian. Platform theme/portal migration remains pending. |
| `distro/desktop/shell` | karyo-de | Panel, launcher, notifications and polkit. Review optional power/network service behavior. | Shell migrated with independent libraries, tray/Start/service tests and real headless labwc startup. Real LightDM/Xfce coexistence is accepted on Debian; Ubuntu VM lifecycle acceptance also passes; later application checks remain. |
| `distro/desktop/signin` | karyo-de and optional greeter | Keep lock/PAM/Wayland with the session, make greetd/cage optional. | PAM/Wayland lock migrated without greetd; real wrong/correct password scenario passes. Real display-manager and logind sleep/resume checks pass on the Debian VM; physical devices remain separate. |
| `distro/desktop/apps` | karyo-de | Review each application's dependencies and shared source. Preserve file-local features and freedesktop integration. | All fourteen application families, including Settings and App Center, are independently migrated with native Debian/Ubuntu regressions and installed QA acceptance; later common/runtime fixes retain their own package gates. See DE docs/MIGRATION-REVIEW.md. |
| `distro/distro/packages/openkaryon-shell`, `openkaryon-apps` | karyo-de packaging | Remove mandatory OS defaults/browser policy/greetd from the basic selectable session. | Independent runtime components pass clean Debian VM install/upgrade/remove, actual Xfce coexistence and unchanged host identity/display manager. Remaining apps are added separately. |
| `distro/distro/packages/openkaryon-defaults`, browser/boot/installer packages | karyo-linux | Own OS branding, Calamares, distribution/browser defaults and first-run selections. | Installed-system and image assertions. Pending. |
| Desktop isolation, VMware and runtime packages | Optional system integrations | Preserve privileged helper checks and namespace/DNS isolation. Keep these outside the UI foundation. | Home/Work isolation, clipboard/DnD and Wine/Darling tests. Pending. |
| `distro/tools/build-packages.sh` | karyo-builder | Reuse configure/build/test/stage/dpkg workflow with committed source, one component, isolated output and provenance. | Package stage and external runtime dependency discovery implemented. Shared-library metadata remains a later extension. |
| `distro/tools/build-patched-packages.sh`, `distro/distro/patched` | Builder mechanism and component recipes | Separate execution/cache rules from upstream versions, patches, licenses and owners. | Rebuild compatible labwc/wlroots and VMware packages. Pending. |
| `distro/tools/fetch-pinned-debs.py`, runtime manifests | Builder input validation | Version/hash/architecture checks, redistribution review and explicit local inputs. | Reject missing or mismatched inputs. Pending. |
| `distro/distro/image`, `distro/tools/build-image.ps1` | karyo-linux recipes and Builder stages | Separate package/overlay choices from orchestration. Workstation consumes extra products and private overlays explicitly. | Both images build through the same pipeline. Pending. |
| Image smoke/installed-system checks and desktop-dev tools | Builder QA and component tests | Preserve isolated VM/headless checks and artifact records. Remove personal machine paths. | Boot/install/update checks and manifests. Pending. |
| `ide` | KaryoForge | Owned by a separate agent. The OS/Builder can consume its package as an external input. | Outside this implementation. |

## Reviewed first component

Theme/paint uses Qt Widgets, per-user QSettings and ordinary painting APIs.
Public headers now use karyo/ui and Karyo::Ui. User settings keys remain
compatible with the prototype. No system services or privileged helpers are introduced.

The donor bundled all shared widgets statically into applications. The first
public foundation exposes a small installed static target with headers and
CMake dependency metadata. This proves packaging and downstream consumption.
The session is independently runnable and actual Debian login-manager acceptance
passes. A stable shared-library ABI remains later work.

Initial configuration reload was corrected during migration: following settings
now applies the current accent immediately. Other retained functions preserve
the donor behavior. No fonts/icons are embedded in this slice.

## Next boundaries

Shared widgets and the Qt style have independent packages. The shell and
PAM/Wayland lock are now migrated; karyo-session assembles their runtime packages
with the compatible karyo-session-entry configuration package. XDG autostart
uses dex once per compositor session, and Karyo-specific portal preferences
leave other desktops' selection intact.

See VALIDATION_SESSION.md for installed runtime acceptance and the retained
hardware/login-manager gates. Package the reviewed compositor extension and
optional system integrations separately. The patched labwc/wlroots pair still
needs dedicated package/version compatibility checks; stock labwc runs the
session, with layout-cycle extension controls unavailable.

The first session milestone is clean Debian installation, session selection,
upgrade, removal and coexistence. Builder proceeds through package, repository,
standard image and Workstation image, recording inputs and acceptance.
The private pipeline remains the working reference during this migration.

## Application packaging during local review

examples/terminal.json, camera.json, photos.json, calculator.json, clock.json,
editor.json, reader.json, player.json, monitor.json, snip.json, archive.json and files.json select
independent runtime components from current DE HEAD. They declare Wayland/icon
plugins and applicable non-ELF data requirements (including the native Debian/Ubuntu
QTermWidget data package alternatives); native ELF dependencies follow
the selected build base. The real terminal package has been built separately on
Debian 13 and Ubuntu 26.04. The remaining application packages are undergoing
VM acceptance; source-level regressions already run on both native bases.

The local review phase intentionally creates commits without pushing. See the
DE review checklist for pending components and the distinction between native,
virtual-device and physical-hardware acceptance.

The separate Ubuntu 26.04 VM now passed real session selection/login, lock and
suspend, polkit, tray, file/capture portals, package upgrade/removal and Xfce
coexistence. See VALIDATION_UBUNTU_VM.md for source revisions, fixture corrections
and limits; native compilation alone is not used to claim those results.

Archive integration uses external distribution 7zip and 7zip-rar executables,
not copied engine source. The native build/test images include the separate RAR
codec (Debian non-free / Ubuntu multiverse) so encrypted RAR regressions are run,
not skipped. That image repository configuration is confined to Docker; DE
packages never enable repositories on the installation host. Codec licensing
and installation remain separate from the GPL application source.

examples/archive-rar.json packages the optional codec integration separately.
Its explicit dependency on distribution 7zip-rar is useful where the distribution
component is enabled; the base Archive package does not silently edit sources.
The addon contains documentation, not a bundled codec or second copy of Archive.

See VALIDATION_APPLICATION_WAVE.md for the current installed app/Files package
snapshots, real GUI/clipboard/extraction checks, native hashes and QA fixture
corrections. The full goal remains open for the optional greeter and reviewed compositor/system
integration packages; Settings and App Center installed acceptance is recorded
in VALIDATION_APPLICATION_WAVE.md.

examples/settings.json selects the independent Settings runtime, and
examples/software.json selects its optional authorized APT integration. The
latter owns one fixed-path helper and polkit action, with explicit Python/APT/
pkexec dependencies. App Center will consume the same component, so packages do
not duplicate privileged files. Native source tests do not replace installed
package and real-agent acceptance for this new integration.

See VALIDATION_GREETER.md for the corrected installed 24-component font/greeter
wave, real PAM wrong/correct-password and login/logout, terminal close and
App Center retry checks, restored LightDM and exact artifact hashes. Later shell
appearance publication has a distinct source/native and pending-runtime gate.

## Current optional profile integration gates

Later native evidence supersedes the initial inventory's broad pending label
without declaring the complete integration finished. Installed account/PAM
policy, public profile controls, two already-running sessions, initial protection
and output lifetime have distinct accepted gates. See
VALIDATION_INSTALLED_PROFILE_MENU.md and VALIDATION_TWO_SESSIONS.md.

Owned namespace, physical forwarding, private resolver and DNS service-controller
libraries now have installed Debian/Ubuntu acceptance. The offline user-manager
network/resolver/capability scope additionally passes native PAM and ordinary
password sudo checks. See VALIDATION_PROFILE_NETWORKS.md,
VALIDATION_PROFILE_FORWARDING.md, VALIDATION_PROFILE_DNS.md,
VALIDATION_PROFILE_SERVICES.md and VALIDATION_PROFILE_USER_MANAGER.md.

Controlled graphical startup/explicit owned teardown now also passes installed
Debian/Ubuntu unprotected, Home-password and separate-password GUI roundtrips.
See VALIDATION_INSTALLED_GRAPHICAL_PROFILES.md. The public stopped-profile
operation, persistent runtime recovery and automatic logout return are still
required. The optional root-only host transport now has separate installed
peer acceptance in VALIDATION_PROFILE_HOST.md; public helper wiring and owned
resource orchestration are not enabled yet. Actual NetBird lifecycle/callback, profile catalog
overlays, family clipboard, Win32/macOS runners and remaining Wine/VMware
integrations stay open. Distribution branding/installer/images and Forge remain
assigned to their separate products.


The first typed ownership journal now has installed SIGKILL recovery acceptance
on Debian and Ubuntu, including actual host socket startup reconciliation. See
VALIDATION_PROFILE_JOURNAL.md. This schema owns network leases only; remaining
DNS/service/manager/graphical/forwarding receipts and complete profile runtime
supervision are still required before public stopped-profile wiring.


Schema-2 private DNS file/unit checkpointing now passes installed reattachment,
interrupted cleanup and real host startup recovery on Debian and Ubuntu; old
network-only and private-context transport scenarios remain compatible. See
VALIDATION_PROFILE_DNS_JOURNAL.md. User-manager/graphical/forwarding/VPN receipts,
proven live GUI consumers and complete profile supervision still remain open.


Schema-3 manager/PAM/compositor receipts now preserve living unprotected and
initially locked desktops through controller SIGKILL and actual host restart on
Debian and Ubuntu. A manager-activated editor keeps its PID and unsaved text.
See VALIDATION_PROFILE_SESSION_JOURNAL.md. Interrupted transitions, automatic
logout return and complete public runtime/forwarding/VPN integration remain open.


Acknowledged offline manager preparation and unstarted login-start intent now pass actual SIGKILL and host startup recovery on Debian and Ubuntu. See VALIDATION_PROFILE_PREPARED_JOURNAL.md. Interrupted policy removal/graphical closing and the complete public runtime remain open.


Recorded offline login-close/manager-close reconciliation now passes six actual SIGKILL boundaries and host startup recovery on Debian and Ubuntu, including partial policy unlink/directory removal. See VALIDATION_PROFILE_CLOSING_JOURNAL.md. Active close supervision, automatic logout return and full public runtime integration remain open.


The actual long-lived host now supervises observed logout/compositor crash without client traffic, returns only from the owned active seat/VT to Home, and naturally tears down captured manager/DNS/network leases. Installed Debian/Ubuntu normal, crash, background and initial-lock cases pass; see VALIDATION_PROFILE_SUPERVISION.md. Public allocation/forwarding and already-dead startup replay remain open.


Schema4 forwarding ownership now passes native live reattachment, all seven interrupted delete ACKs and actual host recovery on Debian/Ubuntu. Joined private mounted DNS/NSS, NAT and GUI lifecycle also pass with a synthetic blocking Home policy. See VALIDATION_PROFILE_FORWARDING_JOURNAL.md, including the preserved cold-UDP failure and bounded diagnostic limitation. Explicit forwarding setup/public startup and the remaining runtime/provider integrations stay open.
