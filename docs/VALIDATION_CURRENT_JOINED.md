# Current joined desktop package and GUI acceptance

The joined root CMake graph at DE `9abeb50648b6f57bd5156c290a0d9f971d3a2487` builds and packages
39 components on Debian 13 and Ubuntu 26.04. Builder execution uses revision
`e2a2dfbdf42c4a5af11f3b1a3c31404265b2e1e0`. All 78 artifacts, package manifests and shared build
logs match their recorded SHA256 values. The [artifact matrix](VALIDATION_CURRENT_JOINED_PACKAGES.json)
retains exact package versions, sizes, hashes, SDK identities and selected tests.

The recipes derive from the current examples with the source fixed to the
captured commit and the build directory set to the joined root. This verifies
the joined install graph, not every standalone CMake entry. External provider
input and the three Win32/macOS recipes are excluded. No Wine or Darling engine
build, runtime experiment, security suite or broad shared unit suite is run.

## Executed ordinary checks

All 17 explicitly selected CTest groups pass on each native base. They cover
ordinary calculator, Files, Start, tray, Settings, Snipping Tool and absent-camera
behavior, plus the focused network budgets, DNS/carrier refresh, read-only
network inspection and VMware wait diagnostics. This is a selected scope, not
an all-tests claim. The exact names are in the artifact matrix.

On separate desktop-only QA VMs, local APT simulation permits only reinstalling
the existing 22 core desktop packages. Installation preserves their versions,
the running Xfce PID, accounts/groups, PAM, LightDM/display-manager configuration
and the original user-data fixture. Installed regular files and symlinks match
the newly built DEBs. After the GUI roundtrip, all 145 regular payload files per
base match again and native `dpkg --verify` and `dpkg --audit` are clean.

Both native systems complete the ordinary path:

1. End idle Xfce normally; select Karyo in the real LightDM greeter and log in
   with the existing disposable fixture credential. No autologin or credential
   reset is introduced. The actual shell uses the Karyo-only config/association
   views and resolves all six expected native MIME handlers.
2. Open the installed Terminal from the taskbar. A real harmless
   `pkexec /usr/bin/true` request displays the Karyo authentication card, with no
   nested decorated password form. Normal authentication succeeds. Native
   pkexec records the root command and its verified exit status is zero.
3. Open the unchanged text fixture in Files and choose Text Editor through its
   visible Open With menu. The actual editor receives that exact file argument,
   displays its contents and leaves the file digest unchanged.
4. Close the test application windows normally, use Start -> Sign out, and log
   back into the original Xfce choice through LightDM. A fresh Xfce PID runs;
   the Karyo compositor/shell/Terminal are gone, Karyo activation directories and
   Qt overrides are absent, and the native Xfce authentication agent runs again.
   Original data/configuration and the display manager remain unchanged. Only
   the owned temporary status marker is removed.

Actual native frames for login, prompt, editor, Sign out and returned Xfce were
viewed on both bases. Root receipts are under
`/var/lib/karyo-qa/karyo-current-20261124t171724z`; the ignored local acceptance
index joins their hashes, screenshots, artifacts and controller evidence.
One rollback snapshot per desktop QA VM remains available for review.

## Retained fixture limits

The first generic RFB driver used the other QA pair's fixture and disconnected;
the existing correct joined-guest driver then worked. An unbound Terminal
shortcut opened nothing, so the actual taskbar icon was used. The first Debian
status suffix typed shifted punctuation incorrectly; its real authorization
still succeeded and was recorded. Corrected native key mapping then captured a
second normal challenge and an actual zero exit status. No cached authorization
is assumed, policy is not weakened, and these preparation errors are retained.

Windows Computer Use still fails before initialization. Direct Linux-only RFB
permits this desktop acceptance; it does not establish VMware host-window resize
or Windows clipboard transfer. There is no Windows desktop or clipboard input.

This closes the current core package/login/prompt/text-handoff/logout slice.
Optional profile packages are built but not installed on these desktop-only
guests; the separate profile QA pair retains its accepted 0.1.1 baseline.
Changed-carrier packets, external-provider descriptor/lifetime integration,
Home/Work GUI networking and real host clipboard/DnD/display events still need
their own applicable acceptance. The named foreign-editor and ZIP chooser cases
are accepted in the follow-up below. Distribution
sources, ISO outputs and Forge remain outside this work; nothing is pushed.


## Current foreign-editor and ZIP chooser follow-up

The same installed current-source core packages now also pass the two remaining
named chooser cases on Debian and Ubuntu, without rebuilding or reinstalling.
The original text/ZIP fixtures are reused and checked against their earlier
recorded hashes before and after every case.

Files' visible text Open With menu selects the distribution's real Mousepad.
It receives the exact selected file, displays its expected contents and closes
normally. The one-off choice leaves Text Editor as the Karyo text default;
the pre-existing user mimeapps.list remains absent or byte-for-byte unchanged.

Selecting the ZIP updates Details to Archive Manager. Its actual menu launches
the installed Karyo Archive with that exact ZIP argument. The native window
displays note.txt with its expected 40-byte size. No archive is extracted or
changed, and the archive MIME default remains unchanged.

Both sessions then use normal GUI Sign out and ordinary LightDM login to fresh
Xfce. All test applications and the compositor exit. The Karyo association/config
views and Qt overrides are absent, the folder default is Thunar again, all
package versions are unchanged, and account/PAM/display-manager/data/fixture
checks and dpkg audit pass. Both QA machines remain in Xfce.

All five actual menu/application/final frames per base are viewed and hashed.
Root receipts are under
`/var/lib/karyo-qa/chooser-current-20261124t171724z`; the ignored acceptance index
binds these receipts to controller and screenshot evidence. This closes the
named current Text Editor, foreign-editor and ZIP menu scenarios; it does not
claim every MIME/app combination, preference-changing UI, profile sessions or
concurrent same-user sessions. No security/shared suite, compatibility-engine,
distribution, Forge, client-repository or Windows-desktop change is made.
