# Installed initial protected-session acceptance

Runtime source: 156d1aa. Native compositor integration: 5abf930, +karyo2.
Only two disposable VMware QA guests are changed; no owner system or Forge.

## Exact inputs

### Debian

- DE source: 156d1aa722bd752e32fa09371b06a5647654cba0.
- Source archive SHA256: b411dc418e736ccac499822d7cf2419a628f07eefa7322fa24f4818beef9eaf3.
- Fixture SHA256: 83c17b7ca7f9db4f907ffc96b33cbac6a1c4acf8abb8cc50ad65479c0717af95.
- karyo-lock_0.1.0-1_amd64.deb SHA256: 51314a05067674b2f376bba398437b5cf42dbc39d97d87eb8df85ee799290e4c.
- karyo-shell_0.1.0-1_amd64.deb SHA256: 109709bf8dabc9f25b7bee09c64c38bb02fb6d530b007ab57ecafc3916081ab0.
- karyo-session-entry_0.1.0-1_amd64.deb SHA256: 5294429acf8f205596d8574c6162faf7bfc85f405788135e6a797adde561cbc0.
- labwc_0.8.3-1+karyo2_amd64.deb SHA256: e28aa21e27bc188a574655839122b46ca9add0deaff2e2a382af545fdd1dd7e2.

### Ubuntu

- DE source: 156d1aa722bd752e32fa09371b06a5647654cba0.
- Source archive SHA256: b411dc418e736ccac499822d7cf2419a628f07eefa7322fa24f4818beef9eaf3.
- Fixture SHA256: 83c17b7ca7f9db4f907ffc96b33cbac6a1c4acf8abb8cc50ad65479c0717af95.
- karyo-lock_0.1.0-1_amd64.deb SHA256: 3edca75fc5d8d81820e539fe27db73ca56fb9b71671b876842accea647462f22.
- karyo-shell_0.1.0-1_amd64.deb SHA256: 63c4562b8a07e3253dee785e36238386a84e3e9c2d54aa2639b4f6c296916718.
- karyo-session-entry_0.1.0-1_amd64.deb SHA256: 6f7eeeca1ccac3390d3817429016613f53ccf746233bed6799b4684a8bc8b93e.
- labwc_0.9.3-1+karyo2_amd64.deb SHA256: 8b8a5cfdd44ff63871ebf5b97b9f43457567a8e280535c65c30c46410ddc1764.

## Accepted initial gate

Both clean native package sets run 68/68 CTests. Manifest/DEB hashes are checked
before no-remove installation of lock, shell, session-entry and native labwc.
Account databases, all common PAM stacks and the default-manager link stay
unchanged; dpkg audits and verification are clean. Only the existing QA user
receives temporary mandatory root protection; its credentials never change.

Actual LightDM login starts one labwc --startup-lock and karyo-lock --on-start.
LockedHint is yes, with no shell or Files. Native VNC Super release and Print
do not launch shell or Snip. A wrong password leaves that state intact and shows
the normal PAM error. Killing only the identified initial locker via pidfd ends
the compositor, starts no normal clients and returns to LightDM. A second login
without restarting the manager again requires the initial password. Correct
PAM authentication then starts the real shell/Files and clears LockedHint.

Debian first encountered a busy DRM device after the earlier manual greetd QA.
The failed attempt is retained in startup-first-attempt.log; it is not acceptance.
A clean QA LightDM restart resolved that state, and later crash/relogin passed
without another restart. Ubuntu also used a clean manager before its new run.

## Distinct open VT-return defect

A later root-policy lock-on-leave check leaves the active graphical VT and
returns, with the legacy password environment unset and no lockOnLeave preference.
Both guests confirm LockedHint while inactive. Debian displays a password form
on return and accepts the password without restarting the shell. Minimal Debian
has no chvt utility; the corrected QA uses VT_ACTIVATE from its native Linux
header rather than installing a package.

Ubuntu vmwgfx removes/recreates every output during that transition. The old
lock UI stays secure but shows only its wallpaper, because screenAdded creates
a decorative view and the original interactive screen disappeared. Correct
typing cannot unlock that missing form. This is a real open product defect,
not a passed VT-return test. It does not invalidate the separately observed
initial PAM gate. Generic output-lifecycle handling is being corrected.

The Ubuntu run is explicitly aborted, the user session terminated, and only
the known root metadata/state removed after original account/PAM hash checks.
Debian finishes its successful return test and removes the same fixture. Both
original LightDM managers are active; package verification and audits are clean.

Evidence under out/{debian,ubuntu}-vm-qa/results includes startup-session-install.log,
startup-policy-native.log, startup-lock-on-leave.log and startup-{locked,wrong,
failed-closed,unlocked,return-locked}.png. The wallpaper-only Ubuntu return
capture and log must remain visible in review until its regression is closed.
Production two-profile switching, fresh child sessions and network isolation
remain separate gates.
