# Scoped MIME recommendations: actual package upgrades on both bases

Nine affected components were rebuilt from clean DE7a1700a in the joined graph
for Debian13 and Ubuntu26.04. All18 DEBs, their manifests, paired global/private
desktop entries and the session-owned MIME catalog were checked by size/hash.
Only calculator-expression-units ran; the shared DesktopEntry unit suite and
security scenarios were not executed. Forced joined builds do not establish
standalone component entrypoint acceptance.

Seven already installed base packages were actually upgraded on each fresh QA
guest beside Xfce: Files, Archive, Editor, Reader, Photos, Player and session entry.
The optional Win32/macOS DEB metadata was inspected without installing engines.

## Cache and existing installation preservation

Earlier manually staged draft metadata was first restored to the original434
package state, checking original dpkg md5sums. Fourteen global launchers were
restored from their exact backups; seven unowned draft files were individually
saved in a root QA backup. All22 existing core packages passed dpkg verification
before upgrade. The old global MIME cache was regenerated before APT to reproduce
the old implicit Xfce default. There was no manual cache regeneration after APT.
The real desktop-file-utils /usr/share/applications trigger refreshed the cache;
its SHA changed on both bases. This exercises the actual upgrade path.

Every recorded preservation check passed on both systems: all package versions,
accounts/groups, PAM/display-manager configuration, the existing Xfce PID/start
time, fixture data and the user's absent or unchanged mimeapps.list. Dpkg audit
and verification of the seven upgraded packages are clean.

## Actual scoped query results

| Context | Folder default |
| --- | --- |
| Existing Xfce, no explicit preference | thunar.desktop |
| Explicit Karyo data-directory scope | karyo-files.desktop |
| Explicit user Thunar choice inside Karyo scope | thunar.desktop |
| Explicit user Karyo Files choice outside Karyo | karyo-files.desktop |

Karyo's scoped text/PDF/image/audio/ZIP defaults resolve to Editor, Reader,
Photos, Player and Archive respectively. The private catalog has no generated
mimeinfo.cache, and dpkg owns its mimeapps.list through karyo-session-entry.
The earlier Added-Associations-only variant failed without a private cache;
the final catalog contains explicit session defaults as well as added choices.

## Remaining gates

These are real rebuilt-package, trigger and xdg-mime results. They do not yet
accept Karyo's own DesktopEntry chooser, a normal Karyo login, activated app
environment, logout back to Xfce, profile sessions or optional compositor
features. The two own joined QA VMs are running for those checks. Whole migration
acceptance and hardware/VMware integration remain open; no user VM was changed.

The detailed local evidence index is
out/migration/joined-mime436-installed-both-evidence-v1.json (SHA256
`911d6e23851390f469e9f7385038320d3b121299cb71227255a0a8cf257d5018`). The package receipts live in external QA output
joined-head434-vms/{debian,ubuntu}/mime436-upgraded.json.
