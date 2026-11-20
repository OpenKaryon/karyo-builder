# Common widgets and session preparation validation

Validated on 2026-11-20. DE source HEAD: `f1bcee0`; shared widgets were
introduced in `6895ef6`. Builder recipes use repository HEAD and record the
resolved revision. KaryoForge and the private prototype are unchanged.

## Migrated components

- `Karyo::Widgets`: window frame/controls, tabs, navigation, password entry,
  popup menu, search and tooltip helpers. Component: widgets-development.
- `Karyo::Style`: reusable Qt style and opt-in client frames. Component:
  style-development. Runtime plugin has its own style-runtime component.
- `karyo-session-entry`: launcher, Wayland desktop entry, keyboard/renderer
  helpers and labwc configuration. Component: session-runtime.

All four recipes build through the installed Builder CLI in the Debian 13
Docker environment. They follow `examples/widgets.json`,
`examples/style-development.json`, `examples/style.json` and
`examples/session-entry.json`. Each build runs all six DE CTest targets.

## Checks and results

All six CTest targets passed: foundation, desktop entries/icons, shared widgets,
Qt style plugin, optional client frames and session-launch contract. The
session suite uses command fixtures to test missing programs/configuration,
user settings, session-scoped environment, private D-Bus fallback, exit status
and bounded shell restarts. It does not launch a real desktop.

Installed development packages were consumed by separate CMake projects using
only installed headers, archives and exported targets. Both widgets and style
consumers ran offscreen. A separate Qt-only executable loaded the installed
style through QStyleFactory; it continued working after removal of the widgets
and style development packages. No source checkout or SDK is required by this
runtime executable.

A fresh debian:trixie container installed only the two runtime DEBs via APT
with --no-install-recommends. Derived ELF dependencies, labwc, D-Bus and
Qt Wayland resolved successfully. The Qt-only executable loaded the style.
The installed launcher reported the absent karyo-shell and karyo-lock programs
without reporting absent configuration. Installation and removal preserved
seeded display-manager configuration, a separate existing session entry and
/etc/os-release byte for byte. This verifies package ownership boundaries,
not complete coexistence with a running login manager.

GPL source attribution is retained and the separately named Lucide license
is installed alongside runtime resources. Staging contains no /etc overlay,
OS identity, browser policy or display-manager replacement.

## Captured packages

| Package | Bytes | SHA-256 |
| --- | --- | --- |
| karyo-widgets-dev_0.1.0-1_amd64.deb | 63536 | 51265f574eb7a9cf6a2ce90337401b1fde24c1634da57a3260011f9d1eb86978 |
| karyo-style-dev_0.1.0-1_amd64.deb | 44580 | c7128b900df7aefb274b4c8309278ae6c1ab7144e1e2a724ea3ce6a4559e3119 |
| karyo-style_0.1.0-1_amd64.deb | 113816 | 1ae5073c2cd4b436f65111876cf0bf146fe281cbfff396108d77c1ee6abac5d0 |
| karyo-session-entry_0.1.0-1_amd64.deb | 15480 | d0c967f550051440f1aad0986c98d5bf2e13a99a28823f8bd5a74bde07b8ac9a |

Build records are under out/shared-widgets, with each run's source revision,
environment, dependency list, SHA256SUMS and build.log. Installed-consumer and
clean-runtime logs are under out/shared-widgets-qa. These output directories
are local ignored artifacts. The packages still use the initial development
version; release versioning and immutable tagged inputs are a later milestone.

## Remaining acceptance

A complete selectable session still needs the migrated shell, notifications,
tray, polkit integration, dependent file services/catalog and PAM/Wayland lock.
TryExec=karyo-shell hides the preparatory entry until the shell is installed.
The optional greeter and OS defaults remain separate products.

Review compatible labwc/wlroots and portal providers, then test actual login,
locking, suspend, logout, upgrade and removal alongside an existing desktop on
clean Debian. Container fixture checks do not replace that VM acceptance.
