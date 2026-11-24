# Native standalone session packaging and removal

The later GUI reinstall and current QA running state are recorded in
VALIDATION_FILES_CHOOSER_NATIVE.md; the removal results below remain historical.

The explicit Builder build-only mode now produces the real standalone
session/CMakeLists.txt package on Debian 13 and Ubuntu 26.04. This follows the
earlier normal login/logout roundtrip in VALIDATION_SESSION441_ROUNDTRIP.md.
It closes the packaging and tested removal slices without treating skipped
CTest execution as a passed suite.

## Build-only mode is observable

The positive native acceptance client exercises the unchanged default test mode,
a selected ordinary QtCore fixture test, and a build-only two-package set. All
three modes complete on both bases. Build-only configures BUILD_TESTING=OFF and
never invokes CTest; the manifest reports ctest=not-run, ctest_scope=none,
ctest_regex=null and dpkg_deb=passed. The extracted build-only executable also
runs normally. Default and selected-test behavior retain their prior semantics.
No shared or security unit suite is part of this acceptance.

## Actual standalone package and installed payload

The real session package is built through Builder from committed DE f48f22f,
using --build-only and session/CMakeLists.txt rather than the joined root.
Every one of its 11 installed payload files has exactly the same SHA256 as the
standalone CMake payload used for the previously accepted real session roundtrip.
The later graphics-only DE changes do not change this payload.

| Base | Builder DEB bytes | SHA256 |
| --- | ---: | --- |
| Debian | 24648 | `0c60b4691c19b01d4331c0501ac94f8a6dc595442dc74a021e3ed54b50036cec` |
| Ubuntu | 25108 | `b93cf82b4790535563df05a6a09a3a75c24b2f4fe28dc3a77ec7e6d09eec674f` |

Both packages were actually installed in the separate joined QA guests.
Explicit SHA256 verification confirms all 11 installed files, and package
versions, accounts, PAM/display-manager configuration, user fixture data and
the existing Xfce process are preserved. Dpkg audit is clean. These Builder
DEBs do not contain md5sums; an empty dpkg -V result alone is therefore not
used as proof of payload integrity. The explicit file comparisons supply it.

## Ordinary removal and a new Xfce login

APT simulation and actual removal target precisely the 22 Karyo base packages
that were newly installed by this QA exercise: appcenter, appcenter-catalog,
archive, calculator, camera, clock, editor, files, fonts, lock, monitor, photos,
player, reader, session, session-entry, settings, shell, snip, software, style
and terminal, each with the karyo- prefix. APT removes exactly that set and
changes no other installed package version. This is remove, not purge;
dependencies are retained and autoremove is not used.

Both guests preserve accounts/groups, foreign PAM/display-manager files,
fixture data, existing user Karyo/openkaryon preferences and MIME preferences.
The display manager and terminal alternatives are unchanged. LightDM remains
active, Xfce remains available, and Karyo's session entry, private association
catalog and session-local MATE autostart override disappear as package-owned
files. The existing Xfce process stays alive throughout removal.

After ordinary logout, the correct QA password is entered at the normal
LightDM greeter. A new Xfce process starts on both bases. Its actual desktop
frames are captured, hashed and viewed. The native DesktopEntry client resolves
folders to Thunar; a genuinely activated user D-Bus service obtains the same
API results and Xfce environment. Karyo association/configuration directories,
Wayland socket and Qt platform/style overrides are absent. No compositor is
left running, foreign configuration and fixture data still match, and dpkg
audit remains clean. Debian retains 863 packages and Ubuntu 1110, including
intentionally retained dependencies.

## Evidence and limits

Detailed hashed evidence is in
out/migration/standalone-session-removal445-both-evidence-v1.json. Root receipts
remain under /var/lib/karyo-qa/remove-joined445 in each own joined guest.
The fresh-login snapshot is historically named before-karyo.json by its QA
template; it actually records Xfce after removal, before the new login.
One host exporter initially used the older session441-xfce-api-v4.json output
name. The immutable root receipts and separate logs preserve both runs; the
removal export is separately saved as remove445-xfce-api-v4.json.

The two joined guests now run Xfce with those 22 Karyo packages removed.
This does not accept a fresh Karyo login after removal, purge/autoremove,
concurrent same-user sessions, chooser UI, full privilege-prompt interaction,
VMware channel/profile scenarios or the complete DE migration. The older
Darling QA pair is separate and unaffected. No user VM, Acer, Forge or distro
was changed, and no security/shared unit suite was executed.
