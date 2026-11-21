# Optional greeter acceptance checkpoint

This is local review evidence, not a completed migration or release. All machines
are disposable QA guests. The owner's working VM, laptop and KaryoForge were not
changed. No commits were pushed and no host APT configuration was modified.

## Native packages and font installation

The first 24-component greeter/font wave uses exact DE
`90df39b13e7004d7efaa61b14c6dc4d81f137786` and source archive SHA256
`20bbc0d99f934bf69dc8af1d6cc2e60e31cbc65b5713d2bca9188dba426a66c0`.
Both clean native builds pass all 66 CTest entries before staging. Per-package
manifests, artifact hashes and collision checking pass. Debian installs 23 packages
because its main-only QA guest deliberately omits optional karyo-archive-rar;
Ubuntu installs all 24 with its existing multiverse component. Reinstallation
consumes the checked local artifacts even though package versions remain 0.1.0-1.

Both installed font runtimes resolve IBM Plex Sans/Mono Regular to the supplied
original TTFs through fc-match. dpkg verification of greeter/fonts/lock/App Center/
Settings is clean, and dpkg --audit reports no incomplete package transactions.
Fonts retain the original SIL OFL notices. This proves installation and fontconfig
resolution; native payload tests separately verify all 16 files and glyph coverage.

Installing karyo-greeter leaves LightDM active and its default-display-manager
and display-manager.service selection unchanged. The Karyo package installs no
active greetd config, service, account or PAM policy. greetd and cage were separately
installed for the explicit QA scenario with temporary startup inhibition restored
afterwards. Their distro PAM policies were retained without authentication bypass.

## Actual greetd/PAM findings and fixes

The initial installed frontend exposed two issues that fake-daemon tests did not:

- cage on Ubuntu aborted on an initial client fullscreen request before xdg_surface
  initialization. Showing the normal frameless window lets the kiosk size it and
  removes the assertion. Debian also renders correctly with that change.
- An incorrect password terminates its PAM worker. greetd 0.10 can then report an
  error while cancelling that configuring session. The controller retries cleanup
  only once after explicit auth_error and still waits for positive cancellation
  before another attempt. Repeated cleanup failure stays terminal. Native cases
  cover failed-worker cleanup, blocked early reuse, fresh credentials and bounds.

The corrected frontend corresponding to DE `dc0ddfe799ab336da3f9fb3a1ca597062c84f472` was tested as a named
`/opt/karyo-qa/greeter-live/karyo-greeter` overlay. It is not the installed 90df39b
package binary. All 66 current native CTests pass on Debian 13 and Ubuntu 26.04;
the authentication test executable also passes all 13 reported Qt cases as UID 65534.

| Actual disposable guest scenario | Debian 13 | Ubuntu 26.04 |
| --- | --- | --- |
| Distribution greetd / cage | 0.10.3-4 / 0.2.0-2 | 0.10.3-5 / 0.2.1-1 |
| Kiosk renderer | pixman on VMware virtual DRM | pixman on VMware virtual DRM |
| Greeter language / theme | English / light | Russian / dark sage |
| Wrong password shows error and allows retry | Passed | Passed |
| Correct password after denial launches Karyo | Passed, GUI session182 | Passed, GUI session345 |
| New shell belongs to authenticated UID 1001 | PID12762 | PID49133 |
| Last account/session saved after start | Passed | Passed |
| GUI Start > Power > Sign out returns to a fresh greeter | Passed | Passed |
| Original LightDM restored after testing | Active, original symlink | Active, original symlink |

Only public disposable fixture credentials were used. Russian/dark appearance
adoption reads a small correctly owned public test file, not the user's home.
The initial QA setup accidentally made the service account's .config root-owned;
correcting that fixture enabled saving the greeter's own appearance configuration.
Automatic theme publication from normal sessions remains a separate integration.

The temporary greeter used a separate config, manual systemd unit and a ten-minute
restoration watchdog. Both manual services and timers were stopped and original
LightDM restored. Service logs and screenshots remain in ignored QA result trees;
no secrets or personal profiles are copied into source or packages.

## Other real Wayland finding

The Ubuntu terminal close button was blocked by its tooltip's native popup when
the compositor placed that popup over the anchor. Widget mouse transparency alone
did not clear its native input region. DE 96ed297 also sets
Qt::WindowTransparentForInput. A rebuilt named QA terminal overlay closes on the
first real VNC click and exits normally on both guests. Native widget and terminal
regressions pass. The installed 90df39b wave precedes this shared-tooltip change.

## Installed follow-up: package acceptance

The corrected 24-component sets from exact DE
dc0ddfe799ab336da3f9fb3a1ca597062c84f472
were built cleanly and pass all 66 source-revision CTests on both bases.
Their source archive SHA256 is 9d66d4ecb65951c06a1f7435a17883f2ff332ae6f54f6c0a616cf0d726aa446c.
Debian installs/reinstalls 23 artifacts (optional RAR omitted), Ubuntu all 24;
every input package and manifest hash is checked before and after transfer.

Actual /usr/bin/karyo-greeter was verified through /proc/PID/exe and dpkg -V.
It passes wrong-password recovery, correct-password Karyo login, GUI Sign out
and return to a fresh greeter on each guest. Debian GUI session205/shell14330
and Ubuntu session369/shell51955 are from these installed packages, not overlays.
The installed terminal also exits on its first close-button click on both bases.

Installed App Center was launched through the real Karyo Start menu. Cancelling
an ncdu installation authorization shows its failure notice; starting a new
attempt clears that old notice before the new real polkit card appears. The
second attempt was also cancelled, App Center closed normally and ncdu remained
uninstalled. This closes the later retry-notice acceptance gate on both guests
without installing or updating any unrelated system package.

Both original LightDM services and display-manager symlinks were restored.
Temporary greetd services and watchdog timers were stopped. dpkg verification
for greeter/fonts/lock/App Center/Settings/Terminal is clean, and dpkg --audit is
empty. Screenshots greeter-installed-{denial,authenticated,logout-returned},
terminal-installed-close-{before,after} and appcenter-installed-retry-cleared
are retained in the ignored per-base QA results.

| Installed greeter ELF | SHA256 from running /proc/PID/exe |
| --- | --- |
| Debian | 5dca2b392f14398562f1ae2727e9e5680e81c5e32807233fff98c0fc42b0f289 |
| Ubuntu | a9671ecc249998cf23aad2ec04dd0724d175f099d33b0b25f088f03659de614d |

## Remaining migration gates

Public appearance publication is now also accepted from installed shell/greeter
packages at exact DE 47265656bfda30a5c2cfbbce80eb899ac1c9b220. Both clean
pair builds pass all 67 source-revision tests and retain checked manifests.
Source archive SHA256: 74524e3c48988621ceca8a3605585a8d3c23e2a66d16ce45b3c53cdcee4e07f1.

A normal LightDM login starts /usr/bin/karyo-shell and creates its actual public
publication: root-owned directory mode1733, karyoqa-owned file UID1001/mode0644,
initial light/terracotta values. Changing theme and accent through the real
Settings UI immediately republishes dark/moss on Debian and dark/sage on Ubuntu.
No test process writes the publication values during this installed scenario.

The installed /usr/bin/karyo-greeter then adopts those exact values under real
greetd/cage, confirmed in its own configuration and inspected screenshots.
The user's private home settings were not read by the greeter. The prior Ubuntu
public fixture was first replaced by the real shell's startup publication, so
this result does not accidentally reuse that earlier manually written theme.

Both LightDM services/symlinks were restored again after testing; temporary
greetd/watchdog units stopped, dpkg verification and audits clean. Screenshots
appearance-session-start, appearance-settings-published and
appearance-greeter-adopted are retained in each ignored QA result tree.
This closes the installed public-appearance integration gate on both bases.

Remaining broader goal: reviewed compositor layout/window-snapshot extensions,
optional profile/account/network/DNS/clipboard integrations and the retained
existing-window Files activation gate. VM renderer and native fixtures do not
establish physical GPU, camera, microphone, Wi-Fi or Bluetooth acceptance.
Distribution boot/browser/installer/image work is separate; this checkpoint
does not rebuild an ISO or change KaryoForge.

## Current installed artifact checksums

Shell and greeter use the later appearance-publication 4726565 pair; the other
packages remain from the accepted dc0ddfe wave. All hashes were checked against
native build manifests and transferred artifacts.

| Package | Debian SHA256 | Ubuntu SHA256 |
| --- | --- | --- |
| karyo-style | 72b0516393181633551ab7f4444f2570f2afaef82a73c02628676d448e1e15d6 | 6ee8e07428ec3ef534d12533e11c00539c77937bd6a906e6d51c5ab9e4d3221d |
| karyo-shell | 2c8d2d5a20f9440e0997bd0a09184ac4fc3ae5f6004c39a62194a68f03addec4 | 0fbe41548be4eef8d1929aa164f2b39ff28fd4ae644e3190dc4880a97a495ec2 |
| karyo-lock | 3c8fcee3167f46aa53388be184159595b57c80e7456bdddb80527fa24c75d206 | db31f2329de09a99ee48650189aa70420be37c7af895a3178af2b9d321ec2b2b |
| karyo-session-entry | 74b431142c67e2a341c750e5b5b55e17f7fcdf60d2be3e1e07ab1d73c802fa69 | 01364730aaeb77ff51ff1ad2879c61d33a85da074f5f8b3d3cf5d6158fa50a2e |
| karyo-session | 6351eaaad639331356635dc75ff8b53f05fc9008d01266aa0745eb4e8fba2ead | 23cbadc07c21dc59ca12fbcbe0cea2412f212d89a1b3242f8e83e7cc6fc000db |
| karyo-terminal | b70cd88eaeafc0780e7387e770f3d08b9fe5cabb6a1b80a1d60dceefe4223567 | 89dccacdddb300b875feb99f4fdbc0159bbfd53269901ae10d2af0b6eff3a633 |
| karyo-camera | dc54bbc87d256680c1615a254525f5dc0a293cd4651372b13765eff0972400a7 | 23254314257f51ce24bf3b0a920ee70fe8f05c28c421d0ae6ff6583de934e5bd |
| karyo-photos | fa1c9ae4680035c7a24c7d08a24bc66a1869a51b39e623db11b37ab5f1fa0e3c | 615763058320535ac492586c8b1960ae4e0b4c33e4be377c0790045f6ea6c637 |
| karyo-calculator | 0cac290d1644952a946aafc7520a887dc94d4993f88705680b66a59a4e497b39 | a62deab0a070010f5417015bb5f4cee63d877aa2d36373d4da27142043cd3a05 |
| karyo-clock | f62993c93826e4eb3ce6aae687e3a7e53cc8e1b4e1babf2f8281135c73e38b32 | c74860a9dca60e9fc91405b221ff1a3304d0f4295e5ab28b43176eb79abb2503 |
| karyo-editor | c1e5779886496d158a723ec15613771b76a8c970e554586c6c404221003c7c9d | 510fd4e4b4aa06ef4546003236b8c4f9479faa79d91195c3afe9e5cfd427c447 |
| karyo-reader | b8e91cebf04069e799c0005d00f771506d048e08271f4537f382d19a8f9769af | d035d9ec325fd2caafc41ffd213f486631cb1dd04ca0042a90fe2e0c4bd787ad |
| karyo-player | d7507b895dc983a88fa8619cf865997dde658a83cdc1bf9781fd08132155c71a | ec51213b756e82fefb46db9936ef8f1ca2aac0dd31f2c9cd0747e33c2d9d6a3f |
| karyo-monitor | 39c70d3fcfb6e9a907ec0ff879cb24cbbbf20caabd810ec6966662276b92d535 | 853cf68ffe91f957450ad909708720fb2fbf0daa1985de25f1851e2ff99815d0 |
| karyo-snip | 695bd1ba17defc417a0edbe37c0942a35491b010f9b85025b8b970dcd5cedd8c | c8cda0b9580836689cdab21ad9e1a9848b6957aada0006ce94cece22720edd15 |
| karyo-archive | 2b7718b7b57c79c5d2c9cfd696fb111841162e1ff2c026881955eab0a237099c | 607eb7bfdbd81b1c68150b5452c6dc7aee0b3ba85bfc0bb6c48bc7f23b1d39d3 |
| karyo-archive-rar | 62736447c8c0ad83550d0baacb0a4a674215cd416b480bb7a78c2ba5609b6d40 | e7f594f4e5c8d89196b3ec9491417512d949a71fef5d6f9acaa71fc88c0ee2d9 |
| karyo-files | 33a68efa0d8dab1d4e73dd1122d1bf90744f832c2779ed0a88784def7bcd3053 | 4b1fa97ef77e0c738869415b75ba188853fb707fa45696097e089bcdfc228068 |
| karyo-software | 96aeffb8ade8436122dadf961453b20efc1323de6fff42b13fa93242b2ef7d7f | 86caaa2d4b7ea30b94fa9b45501578b1fe7a5b71ac94d9cda803292cfb797643 |
| karyo-settings | ea3267bdf76df06590b92c9208f98e8938831638dacdc313bc42acc68c4e61c3 | 46a43888845b3800f88e4184cf8d336eb663e6ab1c88636d5e51348954bcf55e |
| karyo-appcenter | a6fe89aa0524b3953a68317e0535a10baa55e6513c736f0347058e2f6a001c09 | bf8702982bd4300087cd01f49b3ea716259a7f59d9965a54b74c58213bfac45c |
| karyo-appcenter-catalog | 1f040e68775ca08671b0905fc897e9184ba6c1f8a755ac8db4f6dcbc9b2bec68 | dd12a96a6d95aaf1d3a36f8c47d33533cf946cc3d8c442ee71cc085573e9238b |
| karyo-fonts | db11f94e1b6813982a3503aa30478661cb169c36b989e2af23d15d810048caaf | bf07cd696df7c67b20b683ba4306e63df2ce5f07bbc62cd3d3b3877ff3566d8b |
| karyo-greeter | ceadd7e23566fa6877f63447d952dd6f2701cfbef101f3f4710321f369198ff8 | 48e2489ab8067d19db638edeb9a7a6dedee845dd713f187eb19437847a806209 |
