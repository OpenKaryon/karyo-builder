# Actual native desktop roundtrip and session-local agent coexistence

Later Builder packaging and removal results: see
VALIDATION_STANDALONE_SESSION_REMOVAL.md. The current joined QA state there
supersedes the historical running-state statements below.

Separate Debian13 and Ubuntu26.04 QA guests each completed two normal
Xfce -> LightDM -> Karyo -> LightDM -> Xfce roundtrips. Karyo was selected in the
ordinary greeter and the correct fixture password was entered; no autologin,
PAM changes or direct replacement of the display manager was used. The real
labwc, Karyo Shell and Files processes ran, and actual Karyo frames were viewed.

## MIME API and actual bus activation

A small positive client compiles the unchanged DesktopEntry implementation
from DEff9d949 with each native Qt6Core toolchain. In each real Karyo session it
finds all six expected defaults and matching full desktop entries in the private
association catalog. A temporary ordinary-user QA D-Bus service is activated
through the actual session bus and records its inherited environment and the
same API results. These match the direct client's results on both systems.

After normal compositor exit and normal Xfce login, both the direct client and
the independently activated QA service resolve folders to Thunar. Karyo's
association/configuration directories, Wayland socket and Qt platform/style
overrides are absent from the activated Xfce environment. Actual Xfce paths are
preserved, including Ubuntu's xdg-xfce and snap data-directory entries.

All roundtrip preservation checks pass: accounts/groups, PAM/display-manager
configuration and fixture data remain unchanged, the original compositor is
gone, a new ordinary Xfce session runs, and dpkg audit is clean. The positive API
and activation fixtures are ordinary QA-owned files; they do not change system
service definitions. This accepts the tested login/activation/logout slice,
not the chooser UI, concurrent same-user sessions or every profile scenario.

## General autostart conflict found and fixed

MATE's global authentication-agent launcher has NotShowIn=GNOME;KDE, so dex also
started it in Karyo and it raced the shell's own listener. DEf48f22f adds a small
packaged Hidden=true override under Karyo's session data directory and prepends
that configuration view only in the Karyo entry. Its scope is also imported
for ordinary D-Bus activation. The host MATE file is byte-for-byte unchanged.
Normal user autostart preferences keep their higher priority.

After upgrade and a fresh normal login on both bases, there is one Karyo Shell,
no competing MATE process and no duplicate-agent registration warning in the
new session log. The new config scope is first in the shell environment and
reaches the activated QA application. After returning to Xfce, its original
MATE agent really runs again. Positive dex dry-run plans independently confirm
the MATE launch in Xfce and the Karyo-local override, preserving nm-applet and
other unrelated autostarts. The dry run does not execute those programs.

Debian's journal positively records the Karyo authentication-agent registration.
Ubuntu's polkit127 journal contains no registration details; absence
of the warning and the sole shell process are not promoted to a full prompt
acceptance result. An initial diagnostic incorrectly expected a PID in the
journal message. Subsequent ordinary D-Bus introspection was refused by host
policy. Those observations are retained; policy was not weakened and further
introspection is unnecessary. No privilege prompt, denial or bypass case was
run for this change. Full polkit prompt acceptance remains a separate gate.

## Standalone CMake payload and honest package boundary

The session's actual standalone session/CMakeLists.txt configured, built and
installed its component on Debian and Ubuntu with BUILD_TESTING=OFF. Both
generated shell scripts pass dash syntax checks. The installed metadata passes
the native guest desktop-file validator. Every staged source text was compared
with committed DEf48f22f; all payloads and QA DEBs were hashed.

The QA DEBs were constructed with native dpkg-deb from those exact standalone
CMake install roots, including md5sums and the existing package dependencies.
They were installed only in the own QA guests. This was not a Builder package
stage run and is not recorded as such: that stage currently always executes a
CTest scope, while its standalone session target wraps a broader shared suite.
That suite was not run. No fake test pass or silent skip was introduced.

Actual one-package upgrades preserve package versions, existing Xfce PID,
configuration and the host MATE file. Dpkg audit and package verification pass;
dpkg owns the new session-local override. Initial QA attempts retained their
missing desktop validator in the build image, absent staging parent, missing
gdbus, omitted LABWC_PID and failed APT --no-download invocation. Corrections
use the guest's real validator, dbus-send and real compositor environment;
ordinary local APT acquisition follows a simulation permitting only this package.
These fixture/tool failures are not application compatibility results.

| Native QA DEB | Bytes | SHA256 |
| --- | ---: | --- |
|debian|25108|`de249db9f2fa77470c812d0b5de2c96448fa55e9db4c5bd974fb5cfc8a96e88a`|
|ubuntu|25116|`8b10ff39a273830748761ef8b5bd50c727cb4b46cccfa58c459f66b2ae6acf66`|

Detailed local evidence: out/migration/joined-session441-roundtrip-both-evidence-v1.json,
SHA256 `8fa5225d30be4ac8c8a7155acd3a6ba4b2f4790ac987574ccc7651d5f11e5ad5`.
The own joined QA VMs are currently running Xfce. The whole DE migration remains
active: chooser UI, VMware channels/resize/Home-Work, external ExternalProvider broker
lifecycle and applicable hardware checks remain open. Darling56 native engines
are still separate pending work; this session result accepts no UGENE GUI.
No security or shared unit suites ran, and nothing was pushed.
