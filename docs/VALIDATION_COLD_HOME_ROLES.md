# Cold Home role lifecycle through LightDM

The previously accepted application role gate preserved the original Home GUI
and used an ordinary installed helper/resolver probe for Home. This subsequent
gate closes the fresh graphical Home startup boundary on both Debian 13 and
Ubuntu 26.04. It is a native login-manager gate, not a nested compositor or a
relabelled stopped Work profile. Personal VM, Acer and Forge remain untouched.

## Exact source and scope

Production remains the effc7cbaf3c71403f925ab2026a20d102f10d6c9 accounts/session-entry
packages recorded in VALIDATION_APPLICATION_ROLES.md. Other installed host/runtime/
provider components remain the accepted d140e14 build. No production package was
rebuilt for this QA-only step. The new DE actor is
profiles/tests/installed-cold-home-roles.py, SHA256:
daa1576b9cce3795a0c18a2086b4224b92839b984f276f24f4bd515024f57d99.

The fixed-host root actor creates safe absent-before Home/Work/common/never
application and autostart entries and uses the existing captured child-account
fixture only for family role metadata. It creates no child GUI or tunnel. An
absent-before temporary QA LightDM autologin configuration selects the real
karyo session for karyoqa. It neither changes the account password nor replaces
or weakens PAM. Unprotected Home is the intended mode for this gate; interactive
password-protected entry has separate acceptance.

Before each new login, it stops the actual QA LightDM, waits for all old UID1001
processes and logind sessions to end and verifies /run/user/1001 is gone. The
native manager and D-Bus therefore really restart as well as the compositor.
It then starts the same LightDM service and requires a new active, unlocked
Home with exactly one compositor, shell and Files instance. Bounded state waits
do not restart an unchanged live operation merely because observation expires.

## Accepted scenarios on both bases

1. With trusted role metadata and a Work family member, a cold actual Home
   starts only Home/common marker programs. Work/never markers do not appear.
   Shell, Files and native activation receive matching private role-prefixed
   XDG_DATA_DIRS/XDG_CONFIG_DIRS. The expected Hidden=true masks exist.
2. The actor validates and removes its exact owned role-policy file, then ends
   the entire Home login/manager/runtime again. A second actual LightDM login
   contains no karyo-applications cache or stale catalog in shell, Files or
   activation. Normal policy-free dex now runs all four safe marker entries.
3. It removes only the captured known desktop entries, marker helper, temporary
   LightDM autologin configuration and runtime markers, restores the child
   settings and uses the original captured account teardown. Original account,
   password and common-PAM bytes match; all original LightDM configuration and
   the selected display-manager symlink match. The final normal Home remains
   active. Package verification and dpkg audit are clean.

The native actor writes a private root0600 phase/identity receipt at
/var/lib/karyo-qa/cold-home-roles.json for review. A completed receipt remains as
QA evidence; it is not application state. Do not blindly repeat the gate over
an existing receipt or output log. First inspect terminal/live state and preserve
that evidence. Fixture mismatches stop cleanup for review instead of broad
resource deletion.

## Deliberately advanced QA baselines

| Base | Previous Home shell/login/VT | Accepted roles Home compositor/shell/login/VT | Final policy-free Home compositor/shell/login/VT |
| --- | --- | --- | --- |
| Debian13 | 36901 /595 /8 | 288266 /288344 /1628 /7 | 288515 /288593 /1631 /7 |
| Ubuntu26.04 | 97122 /765 /8 | 406133 /406297 /1806 /7 | 406521 /406670 /1808 /7 |

The previous fixed Home process identities are intentionally no longer live;
this is not a regression in the prior preservation gates. Current postchecks
use these newly captured exact identities, require the completed root receipt
and recheck account/PAM/LightDM hashes, rather than simply accepting whatever
process happens to be present. Original postcheck source and earlier immutable
evidence are preserved separately. Subsequent gates must use the new baseline.

Final postchecks on both bases also require empty journal schema7, forwarding0,
inactive runtime/host services, disabled inactive host socket, no child account,
private NET/DNS/veth/NAT/provider state or role fixtures, and clean installed
package verification. The optional network runtime was not enabled for this
cold Home test.

## Evidence and limits

Ignored Builder evidence:

- out/migration/cold-home-roles-evidence.json: exact actor/result/evidence hashes.
- out/migration/cold-home-baselines.json: final native process/login identities.
- out/{base}-vm-qa/results/cold-home-roles-native.log: both complete native logins.
- out/{base}-vm-qa/results/cold-home-roles-postchecks.log: final exact baseline
  and absent-resource/package checks.
- out/{base}-vm-qa/results/cold-home-roles-final.png: final actual native Home;
  both images were viewed and show the usable Karyo panel and desktop.

An initial local source-generation escape error was rejected by AST parsing
before any VM mutation. After correction, each native gate ran once and passed;
there is no failed native run concealed by rerunning. All observation handles
were consumed as terminal. Credentials or private profiles were not used.

The real graphical Home role startup/removal boundary is now accepted. This does
not establish real vendor application behavior, onward NetBird GUI/tray, a
provider-specific Home VPN, dynamic physical DHCP/DNS or the remaining
family clipboard/Wine/macOS/VMware integrations. Those remain part of the active
full migration. No push occurred.


Subsequent generic real Home WireGuard plus public Work NetBird peer/DNS/packet
acceptance passes both bases; see VALIDATION_REAL_HOME_VPN.md for exact scope and
remaining external client, exit-node and reconnect boundaries.
