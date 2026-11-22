# Migration inventory

The reviewed donor is the Karyo prototype at revision
`716d515b765319981b124fb1812a1e3edb9e0ffd`. Paths below are relative to
that source tree. This map assigns responsibility to reviewed components.

The table summarizes ownership and accepted boundaries; milestone notes below
are chronological and can contain earlier pending labels. Read the linked
validation report for exact source/package/image revisions. A component pass is
not proof of a joined current-HEAD desktop or completion of the whole migration.
Later runtime patches also review donor26bad17, as recorded in DE PROVENANCE.

Current runtime checkpoints include
[unmapped Win32 owners](VALIDATION_WIN32_UNMAPPED_OWNERS.md),
[existing Wine prefixes](VALIDATION_WIN32_EXISTING_PREFIX.md),
[VMware session/lock](VALIDATION_VMWARE_LOCK.md) and
[profile browser enrollment](VALIDATION_PROFILE_NETBIRD_PKCE.md).
The [default Wine close-button milestone](VALIDATION_WINE_CLOSE_BUTTONS.md) now
passes native/runtime, displayed-frame and GDI gates. The
[default child/MDI region milestone](VALIDATION_WINE_CHILD_REGIONS.md) also passes
PE32/PE64 at 96/192 DPI with real input and restored-icon damage checks. Main/owned
compositor frames and caption metrics/icons now pass their native and actual-shell
checks: see [rounded frames](VALIDATION_ROUNDED_FRAMES.md),
[desktop identity](VALIDATION_DESKTOP_ICONS.md) and
[real taskbar rendering](VALIDATION_SHELL_ICONS.md).
[Real third-party PE32/64 applications](VALIDATION_WIN32_APPLICATIONS.md) now pass
common menu/dialog/minimize, icon/identity and file operations on both bases.
[Explicit offline prefix import and existing-user package upgrade](VALIDATION_WIN32_PREFIX_IMPORT.md)
now pass with a real prototype-created win64 source on both bases. Architecture
conversion and arbitrary older-prefix compatibility remain separate limits.
The [native scene-mask API](VALIDATION_SCENE_CLIP.md) now passes both native ABI,
renderer/input and paired-compositor regressions; rounded application frames
are now accepted separately by the linked frame and shell milestones.

| Donor | Target | Boundary or adaptation | Validation and first result |
| --- | --- | --- | --- |
| `distro/desktop/shared/libopenkaryon-ui` | karyo-de | Split theme/painting foundation first. Retain user settings while using Karyo public names. Desktop entries/icons, common widgets and style are now extracted. Review platform integration separately. | Separate development packages, widget tests and external CMake consumers. Implemented. |
| `distro/desktop/shared/style-plugin` | karyo-de | Widget style and platform dialogs/fonts/icons have distinct responsibilities. | The donor is a QStylePlugin, not a platform-theme plugin. Independent native style loading is accepted; GTK/wlr portals stay external session dependencies. Karyo provider selection and actual VM FileChooser/ScreenCast checks are recorded in VALIDATION_SESSION.md and VALIDATION_UBUNTU_VM.md, with final joined-HEAD deployment still separate. |
| `distro/desktop/shell` | karyo-de | Panel, launcher, notifications and polkit. Review optional power/network service behavior. | Shell migrated with independent libraries, tray/Start/service tests and real headless labwc startup. Real LightDM/Xfce coexistence is accepted on Debian; Ubuntu VM lifecycle acceptance also passes; later application checks remain. |
| `distro/desktop/signin` | karyo-de and optional greeter | Keep lock/PAM/Wayland with the session, make greetd/cage optional. | PAM/Wayland lock migrated without greetd; real wrong/correct password scenario passes. Real display-manager and logind sleep/resume checks pass on the Debian VM; physical devices remain separate. |
| `distro/desktop/apps` | karyo-de | Review each application's dependencies and shared source. Preserve file-local features and freedesktop integration. | All fourteen application families, including Settings and App Center, are independently migrated with native Debian/Ubuntu regressions and installed QA acceptance; later common/runtime fixes retain their own package gates. See DE docs/MIGRATION-REVIEW.md. |
| `distro/distro/packages/openkaryon-shell`, `openkaryon-apps` | karyo-de packaging | Remove mandatory OS defaults/browser policy/greetd from the basic selectable session. | Independent runtime components pass clean Debian VM install/upgrade/remove, actual Xfce coexistence and unchanged host identity/display manager. All fourteen application families now have their own package/installed-QA milestones; later joined HEAD remains a separate gate. |
| `distro/distro/packages/openkaryon-defaults`, browser/boot/installer packages | karyo-linux | Own OS branding, Calamares, distribution/browser defaults and first-run selections. | Installed-system and image assertions. Pending. |
| Desktop isolation, VMware and runtime packages | Optional system integrations | Preserve privileged helper checks and namespace/DNS isolation. Keep these outside the UI foundation. | Optional profile, Wine and VMware integrations now have separate native/installed milestones. Darling, enabled host channels, physical resize/multioutput, remaining VPN lifecycle and arbitrary older-engine/architecture compatibility still have open gates. Explicit prototype-prefix copy and existing-user package upgrade pass VALIDATION_WIN32_PREFIX_IMPORT.md. Windows styling and tested real-application operations have their linked native and actual-shell acceptance records. |
| `distro/tools/build-packages.sh` | karyo-builder | Reuse configure/build/test/stage/dpkg workflow with committed source, one component, isolated output and provenance. | Package stage and external runtime dependency discovery implemented. Shared-library metadata remains a later extension. |
| `distro/tools/build-patched-packages.sh`, `distro/distro/patched` | Builder mechanism and component recipes | Separate execution/cache rules from upstream versions, patches, licenses and owners. | Implemented [source-package stage](SOURCE_PACKAGE_STAGE.md), compatible native labwc/wlroots pairs and matching Wine32/64 builds. Component runtime and exact dependency acceptance are recorded separately. |
| `distro/tools/fetch-pinned-debs.py`, runtime manifests | Builder input validation | Version/hash/architecture checks, redistribution review and explicit local inputs. | Implemented exact native input/hash/architecture checks and the inert [vendor-package stage](VENDOR_PACKAGE_STAGE.md). Product versions, payload selection and redistribution review remain component-owned. |
| `distro/distro/image`, `distro/tools/build-image.ps1` | karyo-linux recipes and Builder stages | Separate package/overlay choices from orchestration. Workstation consumes extra products and private overlays explicitly. | Both images build through the same pipeline. Pending. |
| Image smoke/installed-system checks and desktop-dev tools | Builder QA and component tests | Preserve isolated VM/headless checks and artifact records. Remove personal machine paths. | Installed standalone-DE Debian/Ubuntu session, coexistence, upgrade/remove and component QA are implemented with exact manifests. ISO boot/install-image checks remain a later distribution/image stage. |
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

## Initial boundaries (historical)

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


Actual S256 enrollment now passes through cold real Chromium on Debian and
MiniBrowser/WebKit on Ubuntu, using ordinary HTTP/HTTPS XDG browser association
and the installed asynchronous opener without a BROWSER override. The real
private callback, successful browser page, Connected CLI/provider, strict native
renderer sandbox and connected logout/Home return are proven. See
VALIDATION_PROFILE_NETBIRD_PKCE.md for exact QA, safe native reports/frames,
retained fixture failures and external-IdP/onward-UI/Home-tunnel limits. Older
browser-PKCE pending labels below are historical for this tested boundary.



Configured NetBird children now start through the public desktop switcher, with
trusted optional-payload preflight before allocation and a fixed actionable
missing-provider error. Debian/Ubuntu installed public cold launches, ordinary
private CLI, persistent-state reuse, existing switches, logout/crash/protected
teardown and actual connected enrollment/logout pass. See
VALIDATION_PROFILE_PUBLIC_NETBIRD.md for exact artifacts and root-only context
fixture limits. Older public-VPN gated labels below are historical; actual
browser PKCE, onward UI/tray and Home-tunnel interaction remain open.



Scoped provider desktop/catalog identity now passes real Work-only GIO lookup,
correct NetBird title/taskbar icons and strict sandboxed GUI on Debian and Ubuntu.
Schema7 preserves exact legacy/new manager policy through prepared/live/closing
recovery, including actual connected-provider controller SIGKILL and teardown.
See VALIDATION_PROFILE_NETBIRD_CATALOG.md for current production packages, exact
provenance, the retained Ubuntu GUI environment assertion failure and limits.
Browser PKCE, Home-tunnel interaction and public VPN activation remain open.


The optional inert vendor package now exists as a real Builder `vendor-package`
output with pinned public inputs, exact file selection and no upstream control
hooks or activation data. Actual dpkg install, ordinary CLI/strict sandboxed GUI,
synthetic private callback and clean purge pass on Debian and Ubuntu; see
VALIDATION_PROFILE_NETBIRD_VENDOR.md. Real browser PKCE, Home-tunnel interaction and public profile activation remain
open; scoped desktop/catalog/icon identity is accepted by the later gate above.


Actual IPv4 exit-node forwarding now passes with both bases in router and client
roles: ordinary TCP/UDP reaches a captured endpoint outside the selected router
profile, with the expected remote host, masqueraded source and wt0 default route.
See VALIDATION_PROFILE_NETBIRD_EXIT.md. This does not establish arbitrary Internet/
IPv6 exits, Home-tunnel interference, browser PKCE or final public packaging.


Actual ordinary peer traffic and private NSS now pass between Debian and Ubuntu
profile namespaces: TCP and UDP by overlay address and peer name, proven wt0
routing/counters, with private names and endpoint absent in Home. See
VALIDATION_PROFILE_NETBIRD_PEERS.md for exact QA/report provenance and cleanup.
This does not establish exit-node/Home-tunnel interaction, browser PKCE, final
vendor/catalog integration or public VPN activation.


Actual controller SIGKILL with a connected provider now also passes on Debian
and Ubuntu: the real socket-activated host restores unchanged living native
receipts and Connected status, then supervises logout/crash/background/initially
locked teardown; an interrupted closed graph also reconciles. Both original
six-mode pre-login matrices were repeated. See
VALIDATION_PROFILE_NETBIRD_CONNECTED_RECOVERY.md. This does not establish a second
SIGKILL of an already-running systemd host, all connected mutation boundaries,
peer payload/DNS/exit-node behavior, real browser PKCE or public VPN packaging.


The newest provider gate now includes actual setup-key enrollment against an
isolated disposable NetBird realm, one explicitly delegated kernel tunnel,
fresh-journal live reattachment and connected-owner teardown without `down` on
Debian and Ubuntu. See VALIDATION_PROFILE_NETBIRD_CONNECTED.md for schema6,
exact artifacts, laboratory credential lifetime, preserved fixture failures and
native/source evidence. This supersedes older connected-ownership pending labels
only within that tested boundary. Actual connected host-SIGKILL recovery, peer
payload/DNS/exit-node traffic, browser PKCE, final vendor/catalog packaging and
public VPN activation remain open, as does the full migration.


The latest accepted gate now includes explicit optional runtime activation and
public stopped-child startup on Debian and Ubuntu. See
VALIDATION_PROFILE_PUBLIC_RUNTIME.md for exact packages, root/ordinary source
regressions, real public-helper cold launches, private DNS/TCP, existing switches,
initial protection and logout/crash cleanup. Earlier paragraphs below preserve
the order of accepted layers; their former public-wiring pending labels are
superseded by that gate. The whole migration remains incomplete for cold main
login, interrupted GUI startup, dynamic network/provider integrations and the
other explicitly listed remaining features.


The first actual NetBird provider primitive now passes isolated pre-login service,
state reuse, Work socket/Home denial and private NET/resolver acceptance on Debian
and Ubuntu; see VALIDATION_PROFILE_NETBIRD_PRELOGIN.md. Configured VPN startup fails
before allocation until provider/tunnel journal, connected teardown and client/
callback/GUI integration are ready. The external vendor package's global service
activation is an explicit remaining packaging decision, not an inherited base-DE
installation side effect.


Ordinary provider client endpoints and asynchronous browser handoff now have
installed real CLI/GUI and synthetic private callback evidence on both bases;
see VALIDATION_PROFILE_NETBIRD_CLIENT.md. The strict renderer-sandbox gate now
passes on both bases after preserving the sandbox against the vendor Ubuntu
bootstrap heuristic. Schema5 pre-login provider ownership and controller recovery
also pass; see VALIDATION_PROFILE_NETBIRD_JOURNAL.md. Actual provider enrollment,
connected tunnel ownership/recovery and public VPN integration remain open.

The captured provider is now joined to the graphical/session-manager lifecycle
and inherited client environment. Debian and Ubuntu pass six native preparation,
logout/crash, protected/background and closing cases, plus the strict actual
journaled GUI/CLI/synthetic callback gate. See VALIDATION_PROFILE_NETBIRD_SESSION.md
for exact artifacts and scope. Connected provider state, real enrollment, public
VPN activation and vendor/catalog packaging remain required.


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


## Accepted optional Home/Work visibility

The generic optional application-role mechanism now belongs to DE accounts and
session components; the recipe selects its standalone session CMake entry.
Debian 13 and Ubuntu 26.04 passed447 profile source checks,13 session contracts,
native package installation, an ordinary Home resolver/cache check and a cold
public Work graphical/autostart gate. Shared binaries are not duplicated and no
private Workstation configuration is migrated. See
[VALIDATION_APPLICATION_ROLES.md](VALIDATION_APPLICATION_ROLES.md) for exact source,
package hashes, actual client/activation environment checks, retained fixture
cleanup failure and restored host state. Actual vendor clients and simultaneous real Home tunnels remain distinct
pending gates. Fresh graphical Home role startup and removal are now accepted
through real LightDM on both bases; see
[VALIDATION_COLD_HOME_ROLES.md](VALIDATION_COLD_HOME_ROLES.md).


## Accepted real Home tunnel with public Work peers

A real Home kernel WireGuard/DNS/TCP tunnel and two actual public Work NetBird
peers now pass simultaneous native Debian/Ubuntu packet and resolver acceptance.
Both Work peers exchange TCP/UDP by IP/private FQDN, keep external DNS/HTTPS and
cannot resolve Home's private QA zone. Connected logout and captured Home tunnel
teardown restore original state. See
[VALIDATION_REAL_HOME_VPN.md](VALIDATION_REAL_HOME_VPN.md) for exact actors, retained
QA failures, on-demand peer synchronization, final postchecks and the separate
ExternalProvider/kill-switch, simultaneous exit-node and live reconnect boundaries.
No production package changes are claimed by this QA-only step.


## Accepted optional family clipboard

The separate profile-clipboard package and post-PAM ordinary Wayland adapter now
pass actual Home/Work text, byte-exact PNG, sensitive-local preservation,
outsider denial, confined broker restart and running-session reuse on Debian13
and Ubuntu26.04. Installation enables nothing; clipboard sharing is an explicit
family opt-in independent of network isolation. Captured QA fixtures are removed
and both original Home sessions remain intact. See
[VALIDATION_FAMILY_CLIPBOARD.md](VALIDATION_FAMILY_CLIPBOARD.md) for artifact hashes,
source regressions, retained fixture failures and native cleanup. Earlier broad
pending clipboard labels refer to the previous inventory snapshot. X11/VMware,
rich/file transfer and unmarked-secret detection are not accepted by this gate.


## Accepted optional X11 / Wayland clipboard transport

DE's standalone integrations/clipboard component now preserves timestamped text,
PNG and lazy local file-copy URLs with independent native packaging. All21 real
ordinary Xvfb/headless-labwc cases pass from source and installed packages on
Debian13/Ubuntu26.04; full DE builds pass70 CTest groups. Original Home and
account/PAM/display-manager settings remain unchanged, and captured fixtures are
removed. See [VALIDATION_XCLIPBOARD.md](VALIDATION_XCLIPBOARD.md) for exact hashes,
request/resource bounds and sensitive-selection behavior. This protocol component
does not complete VMware host exchange, active-seat vmusr handover, drag/drop,
HGFS or display following; these remain explicit subsequent integration gates.


## VMware native-session coordinator source prepared

The optional independent VMware session component now derives identity from the
native process/logind session and coordinates foreground vmusr/clipboard workers
across cooperating active unlocked desktops. It has separate packaging and a
Karyo-only XDG stock-autostart mask. Eleven ordinary agent cases,14 session contracts,
all71 DE CTest groups and native package builds pass on both bases. See
[VALIDATION_VMWARE_SESSION.md](VALIDATION_VMWARE_SESSION.md). This is a source/package
gate; actual installed Home/Work handover and VMware host payload exchange remain
pending, along with privileged file transfer, drag/drop, HGFS and display following.


## Installed VMware coordinator handover accepted

The exact d74a8a8 coordinator/session packages now pass real Home and cold Work
handover on both native guests. Actual identities, capability removal, inherited
channel reservations, background release, killed-child recovery, parent-death
release, existing-session reuse and captured teardown pass without replacing the
original Home or root tools process. See
[VALIDATION_VMWARE_SESSION.md](VALIDATION_VMWARE_SESSION.md) for executed actor hashes,
the corrected first Terminal cleanup and retained vendor mount. These QA VMs keep
host copy/paste/HGFS disabled in VMX, so host payload/privileged file transfer,
actual GUI lock/unlock, drag/drop, HGFS/display following and other-DE handover
remain explicit subsequent integration gates.


## Joined native VMware GUI lock accepted

Both installed guests now pass protected cold-entry and real manual Wayland
lock/unlock with separate temporary Work credentials. Wrong passwords keep the
coordinator/workers closed initially and workers stopped on manual lock; correct
authentication restores the same session/coordinator. Captured credentials/policy
and account/runtime resources are restored. See
[VALIDATION_VMWARE_LOCK.md](VALIDATION_VMWARE_LOCK.md) for the exact native actors,
inspected denial frames and preserved first Ubuntu release-observation race.
This closes the earlier GUI-lock pending label for these cases; enabled host
payload, privileged transfer, drag/drop, HGFS/display following and other-DE
integration remain distinct open gates.


## Installed preferred-mode following accepted on activation

The new optional worker now passes real Work activation, manual-mode retention,
background release and preferred-size restoration on Debian and Ubuntu. A
Debian-only custom-mode output format exposed and fixed a parser defect before
acceptance. See [VALIDATION_VMWARE_DISPLAY.md](VALIDATION_VMWARE_DISPLAY.md) for
exact source/artifacts, the preserved initial failures and networkd recovery,
and limits: actual host resize/multi-monitor events and real GUI lock of the new
display child remain separate gates. Earlier lock/handover evidence keeps its
original runtime revision; it is not silently relabeled as a new joined pass.


The generic Win32 hidden-owner palette/minimize compositor slice now has native
Debian/Ubuntu before/after, four-palette and normal/startup-lock protocol evidence.
See [VALIDATION_WIN32_OWNED_WINDOWS.md](VALIDATION_WIN32_OWNED_WINDOWS.md) for exact packages, the retained Ubuntu API/XID
fixture corrections and the still-open real Wine runtime/installed upgrade gates.


## Optional ordinary-user Windows launcher accepted

The independent launcher now has real native Wine64 EXE/MSI, Unicode, icon/menu
registration, prefix reuse, exit status and installed Qt dialog acceptance on
Debian13/Ubuntu26.04. Fixed prototype slots are replaced by actual Unix-account
storage, with Karyo-scoped MIME defaults preserving user preferences. See
[VALIDATION_WIN32_RUNTIME.md](VALIDATION_WIN32_RUNTIME.md) for exact artifacts,
retained fixture/frontend corrections and limits. Actual full application menu/
owned-palette styling,32-bit Wine, legacy prefix import, installed user upgrade
and Darling remain open; this is not a new ISO or completion of all runtimes.


## Native generic Wine menus accepted

Reviewed LGPL Wine source recipes now rebuild both native bases without private
profiles or per-application rules. Installed Debian PE64 and Ubuntu PE64/PE32
runtime plus keyboard/mouse menu gates pass; observed popups have the correct
nonactivating X11 type. See [VALIDATION_WINE_MENUS.md](VALIDATION_WINE_MENUS.md)
for exact source/artifacts, the honest metadata-only baseline and signed Ubuntu
generator-data preparation. Matching Debian i386 Wine is being built separately;
actual owned palettes, window styling, user deployment and Darling remain open.


## Matching native Debian32/64 Wine accepted

The explicit i386 recipe now builds the same native engine version/patch/epoch.
All88 shared libwine files match, both architectures coinstall in one transaction,
and actual PE32/PE64, MSI and both menu modes pass in the disposable Debian image.
See [VALIDATION_WINE_COINSTALLATION.md](VALIDATION_WINE_COINSTALLATION.md) for exact
artifacts, negative fixtures and preserved preparation failures. User deployment,
legacy prefixes, actual owned palettes/styling and Darling remain separate gates.


## Real Wine owned palettes accepted for a mapped framework owner

Both native bases now pass real PE32/PE64 late palettes, unrelated-frame return,
NormalState-preserving minimize/restore, focus quiescence and a real-click-based
foreign-process focus probe. Native labwc/wlroots lifecycle corrections preserve
the existing library ABI. See [VALIDATION_WIN32_PALETTES.md](VALIDATION_WIN32_PALETTES.md)
for exact inputs, retained failures and the separate unmapped-owner limitation.
Actual third-party application deployment, legacy prefixes, Windows-like styling
and the broader remaining integrations still require their own acceptance.


## Fully unmapped Win32 owners accepted with a paired native runtime

A checked parent-hint refresh now distinguishes missing WM_CLASS from unread
explicit identity. Native labwc depends on the matching native wlroots package;
actual dpkg rejection of an unpaired upgrade and subsequent paired installation
are verified. Real PE32/PE64 pass mapped and fully unmapped layouts on both bases,
alongside ten X11 models, protocol/lock gates and unchanged exported ABI. See
[VALIDATION_WIN32_UNMAPPED_OWNERS.md](VALIDATION_WIN32_UNMAPPED_OWNERS.md).
Styling, legacy imports, third-party apps, existing-user upgrade and remaining
system/runtime integrations still need their own acceptance.


## Existing native Wine prefix architecture accepted

New prefixes retain the win64 default, while existing registries remain Wine's
architecture authority. Real Debian win32 before/after and Ubuntu WoW64 PE32
reuse pass with installed source236dd5a packages and preserved data markers.
See [VALIDATION_WIN32_EXISTING_PREFIX.md](VALIDATION_WIN32_EXISTING_PREFIX.md).
This does not close legacy import/conversion, pure win32 Ubuntu compatibility,
new caption-engine validation or complete current-HEAD desktop deployment.


## Default Wine close buttons accepted on both native bases

Matching Wine+karyo2 packages now pass Debian multilib coinstallation, all
runtime/menu gates and real mapped rendering of red/white default close buttons.
The same frozen before/after fixture and actual compositor-frame assertions pass
on Debian and Ubuntu, alongside existing owned-palette gates. The new launcher
also passes existing-prefix reuse with both new engines. See
[VALIDATION_WINE_CLOSE_BUTTONS.md](VALIDATION_WINE_CLOSE_BUTTONS.md) for exact native
inputs, retained preparation errors and the still-open rounding/custom UI,
legacy-import, real-application and complete installed-user deployment gates.


## Native per-view Windows frame theme foundation

Both native labwc recipes now independently select Windows captions by generic
XWayland class while preserving the Linux theme. Pixel-measured mixed themes,
late class reversal, reload and previous-package negative controls pass on both
bases, alongside all model/protocol gates and eight real Wine PE32/64 palette
runs. See [VALIDATION_WINDOW_THEMES.md](VALIDATION_WINDOW_THEMES.md). Final icons,
caption button assets/geometry and client/lower rounding remain the next slice.


## Packaged Windows caption controls

Native Debian/Ubuntu packages now install independent SVG controls and share
46/24 logical-pixel button measurements across render/layout/input. Actual pointer
edge actions, narrow windows, previous-package controls, native theme/group/lock
regressions, eight Wine palette runs and eight real menu runs pass. The native QA
installer also preserves an existing wlroots SDK and leaves headerless images
headerless, requiring apt-get check in both cases. See
[VALIDATION_CAPTION_BUTTONS.md](VALIDATION_CAPTION_BUTTONS.md). Rounded client frames are covered below;
registered application icons remain separate work.


## Native floating Wine frame corners

Ordinary and structurally owned Wine windows now have rounded top/bottom corners
on both native bases, with matching input masks and square max/fullscreen states.
The Debian XWM follows newer native property-deletion semantics with unchanged
public ABI. Actual corner/state/metadata/input and caption-control matrices,
square controls, native model/lock gates, twelve real Wine palette runs and eight
real menu runs pass. See [VALIDATION_ROUNDED_FRAMES.md](VALIDATION_ROUNDED_FRAMES.md).
Application icon matching and the remaining full migration gates stay open.


## Offline legacy-prefix copy and real package upgrade accepted

The public launcher now previews/copies an explicitly selected stopped prefix
without replacing source or existing destination data. Native package upgrades
from0.1.0-1 to0.1.0-2 preserve a complete pre-existing ordinary-user tree on both
bases. A real old launcher session-2 prefix installs 7-Zip, rejects import while
active, copies unchanged file bytes, launches through inherited/registered new
profiles and preserves both source and new edits on repeat refusal. See
[VALIDATION_WIN32_PREFIX_IMPORT.md](VALIDATION_WIN32_PREFIX_IMPORT.md) for exact
artifacts and retained preparation failures. This does not convert registry
architecture or establish arbitrary engine compatibility or final joined HEAD.


## Optional Intel macOS launcher core accepted

A separate account-scoped karyo-macos-core package now preserves the prototype's
Mach-O/.app inspection, short/display-specific Darling profiles, scoped fixed
script and direct-child output contracts without the old two-slot authority.
Native33-case ordinary-user regressions and ten installed public-CLI checks pass
on Debian and Ubuntu. See [VALIDATION_MACOS_CORE.md](VALIDATION_MACOS_CORE.md)
for exact inputs and clearly identified Linux subprocess fixtures. Shared Qt
picker/MIME and actual Darling engine/runtime acceptance remain open.


## Shared Qt macOS frontend and MIME accepted

The separate Qt6/C++17 frontend now uses shared Karyo windows/style,29 Russian
messages and custom Mach-O handler registration. Native74-entry complete builds,
35 ordinary-user backend cases,17 QtTest results and actual installed
Wayland/shell/MIME/close-guard checks pass on both bases. Core-only GUI errors,
existing user data, Win32 defaults ownership and folder/user associations are
preserved. See [VALIDATION_MACOS_PICKER.md](VALIDATION_MACOS_PICKER.md) for exact
packages and explicit Linux-engine fixture limits. Actual Darling/macOS engine
acceptance remains open; this does not complete the broader migration.


The stronger installed macOS picker gate now includes a relative leading-dash
filename, literal leading -- and Qt-looking application options. Old frontend
packages abort in that before-control on both bases; final0.1.0-2 packages pass
after Qt initialization is isolated from the application's captured arguments.
Both complete native suites and the five-stage Wayland/MIME gate pass again.
See VALIDATION_MACOS_PICKER.md for exact before/after artifacts and fixture limits.


## Common Darling source closure and real application probes prepared

The independent runtime now owns its complete pinned recursive source closure,
verified44 Swift binary inputs and26 reviewed common patches. Both native SDKs
pass the joined source gate, including actual zero-fuzz quilt/Git application
and reversal with59 pristine files restored. Normal per-base Debian source
recipes feed sequential native engine compilation; real compiler failures are
fixed generally while retaining hardening and reproducible paths. No finished
engine/native dependency audit or application execution is claimed yet.

Real Intel Mach-O CLI, Cocoa and static Qt Widgets probes compile separately
from clean DE sources. Core packages and verified probes are prepared in the
two native kernel QA guests; absent-engine controls correctly remain negative.
See [VALIDATION_DARLING_INPUTS.md](VALIDATION_DARLING_INPUTS.md) and
[VALIDATION_MACOS_PROBES.md](VALIDATION_MACOS_PROBES.md). Actual engine install,
SUID/namespace bootstrap, application/prefix/upgrade and visible-window checks
remain open, together with the broader VMware/VPN/final-joined migration gates.


## Installed optional system HGFS accepted on both native kernels

The independent optional shared-folder package restores /mnt/hgfs without
privileging the ordinary VMware session agent. Both native package builds,
13 source ownership cases and both integrated VMware groups pass. Actual host
file exchange and newly cloned private-mount inheritance, NoNewPrivs1 on the
root FUSE child, disabled-host skip, same-type replacement preservation,
administrator disable on reinstall and disconnected-host purge pass on Debian
and Ubuntu. Account/PAM/DM/fstab/shell/root vmtools state remains unchanged;
temporary host shares/runtime flags are restored.

The first real runs exposed an EIO foreign mount and immediate old mount ID/
device reuse; the accepted helper checks kernel metadata first and binds to the
non-recycled64-bit mount identity. See
[VALIDATION_VMWARE_HGFS.md](VALIDATION_VMWARE_HGFS.md) for exact current actors,
packages, receipts and retained controls. This closes the system HGFS slice;
enabled clipboard payloads, drag/drop, actual resize/multi-monitor behavior,
actual Home/Work GUI integration, VPN lifecycle, Darling and final joined HEAD
still need their own applicable gates.
