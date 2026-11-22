# Matching Debian Wine32/Wine64 installed acceptance

The native i386 recipe uses the same Debian Wine10.0~repack-6 source archives,
reviewed LGPL menu patch, downstream karyo1 revision and epoch1795215210 as the
accepted amd64 build. Builder's native i386 stage verifies actual dpkg and
binary architectures. The output manifest is retained at DE
out/wine/debian-i386/menu-packages/karyo-source-package-20261122T083032Z-a6536565,
SHA256825def67505b9d86d19018e01bcd8603fa011ac30c962116a4afc94542e76d51.

| Runtime architecture | libwine SHA256 |
| --- | --- |
| amd64 | 4daf2ecdde0e3426c30872e1cc1da5feaaf64078e5ce3f1d003eee46dca33a5c |
| i386 | e4f851f29a851c13595db4d5a558150bc982620b03b280610e51b0057125411d |

## Before installation

The driver requires both successful native manifests, identical version, base,
source archives, patch order/bytes and epoch. It permits a dependency-ready QA
image only when its immutable Linux amd64 layer prefix derives from the captured
Wine64 SDK. The original strict exact-image rule stays in place for ordinary
single-source acceptance. This records trusted QA preparation provenance; it is
not authentication of hostile image input.

The component's streaming inspector checks libwine control identities, actual
amd64/i386 fields and Multi-Arch:same, then compares payload content, type, mode
and ownership for every shared file. No files are extracted into a live system.
The actual pair agrees on88 shared paths;786 are amd64-specific and845 are
32-bit-specific. Real tiny-DEB negative fixtures reject differing version,
architecture, shared bytes and mode before installation. All19 component tests
pass as ordinary users on both native Debian and Ubuntu.

## Actual matching install and execution

The image installs both matching native runtime sets in one dpkg transaction.
It includes libwine:amd64/i386, wine64/wine32, optional matching preloaders, and
one64-bit-build copy of all/fonts packages. Development/debug/tools packages
remain build evidence and are excluded from runtime installation. The shared
check runs before unpacking and its receipt remains inside the installed image.

Final actual image ID is
b965e9b516f9b4e7e3eba27b91b73e719a7edd6dff03606d0ed4026b9553ec9d.
The dependency/compiler preparation image is
8e306a7c405d25a769fdacbc938f9c432fb6a250e361bf2e4d3f022511aab9c4.
The own launcher still comes from exact source e782fb0 and the compositor from
the previous native labwc+karyo3 package. Source and runtime evidence keep these
identities rather than claiming a new joined DE installation.

All eight installed stages pass: native Qt, second account/MIME, PE64/MSI64,
keyboard/mouse menus64, PE32/MSI32 and keyboard/mouse menus32. Actual PE headers,
GDI pixels and Unicode file I/O are verified. Literal arguments, private D-Bus,
removed Linux Qt variables, native UID/capability/NoNewPrivileges, extracted icon,
registered relaunch/prefix reuse and exit42 assertions are retained. Every menu
is observed as POPUP_MENU/inputfalse with repeated navigation. Both bitnesses
use the same ordinary-user launcher policy, not per-application settings.

Every stage has fresh temporary user storage, private D-Bus and its own headless
compositor/Xwayland, read-only root, no capabilities or network. The Windows
fixtures never run as root. Neither host nor existing VM/user APT, namespaces,
prefixes or graphical sessions are changed by preparing the QA image.

## Retained preparation failures and evidence

The first read-only archive inspector lacked private /tmp for dpkg-deb; its
failure is retained. The v2 inspection adds only temporary private storage and
passes. The first combined installed image reached successful native Wine
coinstallation, then failed compiling the own PE32 because the64-bit Debian SDK
correctly had no i686 MinGW compiler. A separate QA preparation layer adds it;
no Wine source/package/assertion changes are made to get the v2 pass.

Local wine-debian-coinstalled-acceptance-v2 contains frozen actors, source/build
input hashes, native artifact records, shared-file receipt and every actual
stage log/frame. wine-coinstallation-shared-v2 retains the separate ordinary-user
real-archive comparison. Earlier image/inspection failures remain at their
original paths. No native binary, initialized prefix or credential is committed.

This closes matching native32/64 runtime acceptance on clean Debian, alongside
Ubuntu's separately accepted native WoW64. It does not establish existing-user
migration, legacy prefix import, actual Wine hidden-owner palette/minimize,
Windows-like frame/child styling, full taskbar association or Darling. The full
DE migration remains active and no push/fetch or ISO rebuild was performed.
