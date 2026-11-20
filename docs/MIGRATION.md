# Migration inventory

The reviewed donor is the Karyo prototype at revision
`716d515b765319981b124fb1812a1e3edb9e0ffd`. Paths below are relative to
that source tree. This map assigns responsibility to reviewed components.

| Donor | Target | Boundary or adaptation | Validation and first result |
| --- | --- | --- | --- |
| `distro/desktop/shared/libopenkaryon-ui` | karyo-de | Split theme/painting foundation first. Retain user settings while using Karyo public names. Desktop entries/icons, common widgets and style are now extracted. Review platform integration separately. | Separate development packages, widget tests and external CMake consumers. Implemented. |
| `distro/desktop/shared/style-plugin` | karyo-de | Widget style and platform dialogs/fonts/icons have distinct responsibilities. | Runtime plugin loads in a separate Qt client on clean Debian. Platform theme/portal migration remains pending. |
| `distro/desktop/shell` | karyo-de | Panel, launcher, notifications and polkit. Review optional power/network service behavior. | Shell migrated with independent libraries, tray/Start/service tests and real headless labwc startup. Hardware/display-manager acceptance remains pending. |
| `distro/desktop/signin` | karyo-de and optional greeter | Keep lock/PAM/Wayland with the session, make greetd/cage optional. | PAM/Wayland lock migrated without greetd; real wrong/correct password scenario passes. Actual display-manager and suspend checks remain pending. |
| `distro/desktop/apps` | karyo-de | Review each application's dependencies and shared source. Preserve file-local features and freedesktop integration. | Files selection/service, archive passwords/cancellation and app regressions. Pending. |
| `distro/distro/packages/openkaryon-shell`, `openkaryon-apps` | karyo-de packaging | Remove mandatory OS defaults/browser policy/greetd from the basic selectable session. | Clean Debian install/upgrade/remove and unchanged host identity/display manager. Pending. |
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
The session is now independently runnable; real login-manager acceptance and
a stable shared-library ABI remain later work.

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
