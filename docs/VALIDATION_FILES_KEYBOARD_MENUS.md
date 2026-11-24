# Files keyboard menus on installed Debian and Ubuntu sessions

The standalone Files revision `9998e8f1adb9a8502fae1f3e5d0dd34641a18485`
fixes the keyboard-menu gap observed in VALIDATION_FILES_CHOOSER_NATIVE.md.
This is a bounded follow-up on separate Debian 13 and Ubuntu 26.04 QA systems.

## Reproduction and correction

The first implementation explicitly registered both Shift+F10 and Menu.
Its focused Qt tests passed, but the installed Wayland application revealed
two stacked popups for the real Menu key. The native QPA context event was
independent of the shortcut, and its pointer position could select the wrong
menu context. Preserve this failed native observation rather than calling
the first source-only result sufficient.

The final implementation handles keyboard context events on the focused view
and viewport, anchors them to the selection, and consumes them once. Shift+F10
uses the same path. An existing popup is not duplicated; an inline rename
editor retains its own editing menu. Mouse context-menu routing is unchanged.

Only the ordinary `files-keyboard-context-menu` CTest group ran. The expanded
native-event reproduction failed three cases before the correction and passed
all 13 QtTest cases afterward on both native bases. Details and Icons modes,
empty/selected states, shortcut/native-event duplication and rename focus are
covered. No shared or security suite ran.

## Native packages and visible behavior

The real Builder Files package stage built revision 9998e8f separately for
each distribution, with `--build-only` explicitly reporting CTest not-run.
Package SHA256 values are:

| Base | Bytes | SHA256 |
| --- | ---: | --- |
| Debian | 368340 | bb78d49ba558a5b3a5b3acfbf4f9851bf4e0b4a7afbcab95f655131eab0f515b |
| Ubuntu | 416372 | 0e4eba4c3d006faf637a5234814acd1c12fe9b7d25109a76a870946c2e24ceaf |

Each same-version update used APT reinstall at the normal login screen. The
installed ELF matched the actual native DEB member and differed from the old
binary. A new ordinary LightDM Karyo login then ran the updated application.

In actual Details mode on both systems, Menu and Shift+F10 show exactly one
file menu below the selected note. Clearing selection with Ctrl+Space changes
the keyboard menu to New folder/New text file and the other folder actions.
F2 starts inline rename; Menu then opens the line editor's Cut/Copy/Select All
menu. Escape cancels it without changing the original file or name. All eight
menu frames were captured, hashed and viewed.

Selection was established through the ordinary public `karyo-files --select`
entrypoint. Earlier remote-pointer attempts hit the toolbar or background
instead of the intended row; adding a motion delay did not resolve that
observation. This report does not accept a pointer-input fix. Actual Icons-mode
UI was not exercised in this follow-up; its evidence is the focused source test.

## Session return and evidence

Both systems returned through normal compositor exit and correct-password
LightDM login to fresh Xfce sessions. Accounts, PAM and display-manager files,
the original user-data marker, note/ZIP fixtures and MIME preferences retained
their hashes. No Karyo compositor or shell remained; Xfce had no Karyo Qt
platform/style overrides. Dpkg audit was clean. Both final Xfce frames were
captured, hashed and viewed; the intended final Files package remains installed.

Root receipts are under `/var/lib/karyo-qa/files-context459`; final receipts
have `final460-` names and do not overwrite the failed initial observations.
The local index is `out/migration/files-keyboard460-both-evidence-v1.json`,
SHA256 `7da6a99e03e865ade8ad8196c42d0dd449e0656dc3fe79fbcafc9be2c80bc289`.
It records exact packages, source results, preservation receipts and ten viewed
frames. This accepts only the described keyboard menus and session roundtrip,
not every menu action, profile, VMware channel or the complete DE migration.
No authentication policy changed, and no user VM, Acer, Forge or distro was
modified. All commits remain local.
