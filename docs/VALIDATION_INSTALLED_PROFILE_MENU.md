# Installed public desktop menu acceptance

Exact shell runtime: 2a777714ec3032be892a2d6304730cf37808a89d.
No source wrapper or binary overlay is present. Profile helpers are installed
from bf831b0 during this GUI gate; lock remains 283cce4, session-entry 156d1aa,
and native labwc is +karyo2. Console primitive packages are a later separate gate.

## Exact inputs

### Debian

- Output: out/migration/profile-menu-final-debian/karyo-shell-20261121T130058Z-26453408.
- Source archive SHA256: 0714a92afaddc3a6c04a3e447011be5e0618cebc99d0ebe6fba8bcb4dfb27199.
- DEB SHA256: 6a6edb4b63190dc338479fdbe4ec082e828ded18ad6c85034d1d6455092a8111.

### Ubuntu

- Output: out/migration/profile-menu-final-ubuntu/karyo-shell-20261121T130100Z-a99c2c86.
- Source archive SHA256: 0714a92afaddc3a6c04a3e447011be5e0618cebc99d0ebe6fba8bcb4dfb27199.
- DEB SHA256: 9dcd6bc4c756666d1cae80c969ed3bd94a450907301244bb25a4e2f3cf8c59cc.

## Installed graphical acceptance

Both clean native builds pass all 69 CTests. No-remove installation verifies
source/artifact hashes, absent overlays, unchanged accounts/common PAM/default
manager and clean dpkg verification/audit. Real LightDM login starts the actual
/usr/bin/karyo-shell. Its profile menu loads the current own-family entry.

The actual creation form submits the reserved KQ Switch Work label without
a new-password prompt. Installed native pkexec/account helpers create the real
absent-before kq-switch-work account, confirmed independently by the fixed root
arm/capture fixture: actual identity/home, shared hash, unexpired state and
unchanged owner/PAM. The fixture then enables child Home protection before its
first graphical session starts. Existing LightDM provides that bootstrap; this
does not substitute for the still-pending owned stopped-session launcher.

The cold protected child is observed active/locked, with exactly one flagged
labwc and initial karyo-lock --on-start, and no shell/Files. Its actual password
form is inspected on both guests. Correct Home authentication starts the child
shell. Actual installed-menu clicks leave it locked before showing Home. The
separate one-time main lock imposed by LightDM is authenticated before testing
the next entry. Clicking the child again shows a fresh password form; actual
authentication opens the same shell, and another menu click returns Home.

| Base | Home session / Shell PID | Child session / Shell PID | VTs |
| --- | --- | --- | --- |
| Debian | 595 / 36901 | 603 / 37602 | 8 / 9 |
| Ubuntu | 765 / 97122 | 774 / 98421 | 8 / 9 |

Both shell PIDs remain unchanged throughout the installed-menu transitions.
This complements earlier source unprotected UI roundtrips and installed-helper
wrong-password/required re-entry checks rather than inferring those from a
single successful login. No root rendering helper stands in for real menu clicks.

## Cleanup and scope

Only the captured QA child is terminated and removed after identity/home,
no-process/session, exact metadata and original-owner checks. Original
passwd/shadow/group/gshadow/common-PAM bytes match afterward. No child, family
or protection metadata remains; dpkg checks are clean. The main GUI stays open
for subsequent read-only/native-console work. Known QA drivers and root-only
earlier PAM recovery are retained.

Evidence: out/{debian,ubuntu}-vm-qa/results/profile-menu-final-* logs and
listed/first-locked/protected-reentry captures. Exact inputs/SHA are in
profile-menu-final-input. This closes installed public-menu listing/creation
and running-profile switching/protection for the tested native environments.
Owned systemd/VT startup, network/DNS/VPN/capability/callback/clipboard and the
remaining compatibility integrations are still required. Nothing is pushed;
owner systems, Forge and the private donor are unchanged.
