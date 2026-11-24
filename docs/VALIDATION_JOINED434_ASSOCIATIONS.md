# Joined HEAD native components and scoped MIME associations

The clean DE6ecdfaaad6335fe0e613459fa04e702e51b6e37e joined graph produced41
native component packages on each Debian13 and Ubuntu26.04 base. All82 artifacts
were rechecked by size and SHA256. Only the ordinary calculator-expression-units
test was selected; other test targets compiled but their suites did not run.
Recipes that normally use standalone subprojects were temporarily directed to
the joined root. These builds do not revalidate standalone entrypoints.

## Fresh native installation alongside Xfce

Two new disposable VMware QA guests were built from rehashed cached Debian and
Ubuntu cloud images. Each has3GiB RAM, two CPUs and a24GiB sparse test disk. They
use a separate new QA SSH key and serial-verified host-key fingerprints. No user
VM, Acer, Forge, donor checkout or distribution ISO was changed.

An initial minimal VM topology caused VMware to fail before boot; restoring the
already proven PCI bridge layout fixed both own VMXs. Initial Debian bootstrap
also found policykit-1-gnome unavailable, so the QA Xfce baseline uses candidate
mate-polkit plus pkexec. These are retained preparation failures, not changes to
Karyo distribution dependencies. Six inert, exactly hashed old Debian seed DEBs
were removed from the own fixture before installation; none had been installed.

Both guests then installed22 base Karyo component packages including all14 app
families. The19 remaining optional/SDK packages were built but not installed.
Existing user data, users/shadow lines, groups, PAM/DM/account files, terminal
alternative and the running Xfce process identity were preserved. No preexisting
package was removed and dpkg audit remained clean. This does not yet accept a
current-HEAD Karyo login, its custom compositor protocols or all optional apps.

One real coexistence failure was found on both guests: with no user mimeapps.list,
the implicit folder handler changed from thunar.desktop to karyo-files.desktop.
No explicit user preference had been written; globally registering the new
MimeType changed the unconfigured fallback. The preservation gate correctly
failed rather than treating this as a successful installation.

## Common session-scoped fix

DE66cc9a0 keeps launchers visible globally while moving their full MIME metadata
into a Karyo-specific XDG data directory. The same source entries generate a
session-only mimeapps.list containing defaults and Added Associations. Karyo's
launcher prepends this directory; the autostart activation import receives it.
Application visibility catalogs can still prepend their filtered view.

Native CMake configuration and actual metadata installation pass on both bases,
including the session's language-less install graph. Each generates34 files for
the fixture, including optional handlers. Draft generated metadata applied to
the actual22-package QA installations gives these results on both bases:

| Ordinary scenario | Actual result |
| --- | --- |
| Xfce folder default | thunar.desktop |
| Karyo folder default | karyo-files.desktop |
| Karyo text/plain | karyo-editor.desktop |
| Karyo application/pdf | karyo-reader.desktop |
| Karyo image/png | karyo-photos.desktop |
| Karyo audio/mpeg | karyo-player.desktop |
| Karyo application/zip | karyo-archive.desktop |
| Explicit Thunar choice in Karyo | preserved |
| Explicit Karyo Files choice in Xfce | preserved |
| Actual user's mimeapps.list | remains absent/unchanged |
| Private mimeinfo.cache | absent; recommendations still work |

The first Added-Associations-only variant passed with a manually generated
private cache, then failed after that cache was removed. It is retained as a
failed design check. Explicit defaults in the session-only list remove that
dependency while retaining higher-priority user preferences. An earlier fixture
copy also stopped at an LF/CRLF difference; normalized text comparison confirmed
the same launcher before the scoped change. Its logs and original backups remain.

These are actual CMake metadata/GIO-xdg behavior checks, not acceptance of rebuilt
packages. Nine affected native component rebuilds are now queued from clean
DE7a1700adaa27148f37f87a7b59b0098dc9be6447, with only the same calculator test
selected. Package upgrade, Karyo's own DesktopEntry chooser, actual bus activation
and logout back into Xfce still need their separate checks.

Both new QA guests were gracefully powered off after results were saved, freeing
their6GiB host VMEM while Darling builds continue. Their disks and backups remain;
the existing Darling QA guests stay running. Do not confuse these four own QA
VMs with the user's working Karyo VM.

## Evidence and remaining scope

The local index is `out/migration/joined-head434-mime-evidence-v1.json`, SHA256
8c4e784aecf30f5b01b6ee3b4772e38dea138aafc66a225b2f16f78923232e67.
It records both verified41-package manifests, installation receipts and both
positive six-handler/explicit-choice checks. In the task's local QA output,
`joined-head434-native-builds`, `joined-head434-vms` and
`scoped-associations-v3-{debian,ubuntu}` retain logs, exact files and backups.
`joined-mime436-native-builds/state.json` tracks the affected-package rebuilds.

The broader goal remains active: latest joined session behavior, VMware enabled
clipboard/drag-drop/resize and Home/Work integration, external ExternalProvider broker
lifecycle, applicable real-hardware limits and actual Darling app compatibility
are not closed by this component result. No security or shared unit suites ran.

Actual rebuilt-package follow-up: [installed MIME upgrade results](VALIDATION_INSTALLED_MIME_ASSOCIATIONS.md).
