# Independent session runtime acceptance

Validated on 2026-11-20 on Debian 13 amd64. The public repository now builds a
runnable Wayland shell and PAM lock independently of the prototype. Forge is
maintained separately and is not part of this migration.

## Components and package entry point

The shell includes wallpaper, desktop file operations, taskbar, Start search,
status-notifier tray, notification history, polkit prompts and quick settings.
The lock uses ext-session-lock-v1 and the signed-in user's PAM authentication;
the optional greetd greeter is excluded. Russian catalogs are embedded.

Install karyo-session to obtain karyo-shell, karyo-lock, the compatible
karyo-session-entry configuration package, Qt style and declared portal/runtime
requirements. The desktop entry can be selected alongside an existing login
manager. OS identity, browser/boot policies and privileged private integrations
are outside these package boundaries.

Example builds use the installed Builder CLI and resolve source HEAD at the
start of each build:

```sh
karyo-builder package examples/shell.json --output out/session-acceptance
karyo-builder package examples/lock.json --output out/session-acceptance
karyo-builder package examples/style.json --output out/session-acceptance
karyo-builder package examples/session-entry.json --output out/session-acceptance
karyo-builder package examples/session.json --output out/session-acceptance
```

## Automated and graphical checks

The final source passes eleven CTest targets: foundation, desktop entries/icons,
shared widgets, Qt style, client frames, launcher contract, PAM policy, lock error
layout, tray activation/menu, Start filters and shell-service policies. Builder's
nine host tests pass through the installed Python package. Every package build
also runs the DE tests before producing a successful artifact.

A genuine headless labwc session runs under an unprivileged disposable account
at 1280x720 using pixman. Installed binaries open Start, receive the compositor's
lock confirmation, reject a wrong password, accept the fixture password through
real PAM and exit through the compositor. Screenshots were inspected. A discovered
error-message overlap was fixed and has geometry coverage at 720p and 1080p.

The session is tested both in the build environment and using only runtime
packages in clean debian:trixie. The latter has neither cmake nor Karyo headers.
XDG autostart uses dex and launches its fixture once. A Qt-only external consumer
loads the installed style. Its native QIcon SVG check fails without the separate
icon engine and passes with the explicit qt6-svg-plugins runtime dependency;
embedded resources alone would have concealed that missing dependency.

The clean container has no systemd user manager. A second scenario supplies a
fixture PipeWire process, observes GTK and wlr portal activation and reads the
ScreenCast interface version (5). This verifies backend selection and interface
availability, not an interactive capture stream or physical audio devices.
Expected service-disconnection messages during fixture teardown are retained
in the logs. Physical suspend/logind and GPU behavior are separate gates.

## Installation, configuration and removal

APT resolves runtime requirements with --no-install-recommends. The lock PAM
file installs in /etc/pam.d, with generated Debian conffiles metadata. A locally
modified PAM file survives reinstallation. A separate Builder runtime fixture
is upgraded to a new package version with a changed shipped default; the local
configuration survives and the new default is saved as .dpkg-dist.

Package removal removes the session executables and Karyo portal selection,
while preserving modified conffiles. Purging the fixture packages removes those
owned configuration files. Seeded display-manager configuration, another session
entry and /etc/os-release remain byte-identical through installation/removal.
This establishes ownership boundaries, not actual login-manager coexistence.

The reproducible clean-container harness is tests/acceptance/session-bundle.sh.
It requires a disposable debian:trixie container, runtime DEBs at /packages and
karyo-de/tests at /checks. It deliberately creates test-only users and policy
fixtures inside that container. Source exports, toolchain inventories, dependency
lists, build logs and SHA256SUMS accompany each package under out/session-acceptance.
Clean runtime logs and screenshots are retained under out/session-bundle-qa/results.
These artifacts are local ignored outputs.

## Remaining acceptance and migration

Real LightDM/Xfce coexistence, repeated Karyo logins, PAM locking, guest logind
suspend/resume, polkit, tray, interactive file selection, a live Chromium/PipeWire
stream and package upgrade/removal are now accepted in a fresh Debian VM.
See [the VM report](VALIDATION_DEBIAN_VM.md) for the launcher defect found and
fixed, actual evidence and fixture limitations. Physical sleep devices, multiple
physical outputs and accelerated GPU paths remain hardware gates.

Stock labwc runs the session. The retained custom layout-cycle protocol needs
the reviewed compositor extension; its click control is disabled when the
extension is unavailable. Package that compatibility layer separately. The
indicator and system keyboard configuration remain in the shell/session boundary.

Apps such as Files/Settings, the optional greeter, repository/ISO stages and
optional namespace/VMware/compatibility runtimes remain subsequent products.
The shell reuses only the file-job/type primitives it needs; the command-line
application catalog is optional XDG data, not imported App Center source.

## Captured runtime artifacts

All packages below use the initial development version 0.1.0-1. Source commits
are resolved at build start; subsequent documentation/tests do not rewrite them.

| Package | DE source | Bytes | SHA-256 |
| --- | --- | --- | --- |
| karyo-shell | 5a084fb | 518308 | 6c04f8a5c91d1a40a9e50bb0215e34007add61e45a3e7b9927f04081b820d340 |
| karyo-lock | 4220358 | 140756 | 923bf1a7a2411aa6c69ab12dbae844a2c81d0c40603793c724b082f830adcb43 |
| karyo-style | 5a084fb | 113856 | e6eeaee0b4c84480865a9417289451a480fc67d132a51bcca4639017d1193901 |
| karyo-session-entry | 942adca | 16496 | 9476002f44be7b1de57176f70094c6f25b97adb6f4a401282523e598e05aee80 |
| karyo-session | 942adca | 14148 | 22a6c2580453a929951929be16740ddb6068a3dc2ff46af1a6bbc80f301a73c5 |

The final lock contains the password error layout fix. The final shell/style
packages declare qt6-svg-plugins, and their updated runtime install passes the
native SVG consumer plus the PipeWire/portal and PAM session scenario. The
configuration-only packages retain the earlier source snapshot; their runtime
entry and dependency contract remain compatible.
