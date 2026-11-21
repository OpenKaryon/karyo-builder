# Installed switching between two user sessions

Runtime inputs: profile-accounts bf831b0, shell bb46dfc, lock 283cce4,
session-entry 156d1aa and native labwc +karyo2 on Debian 13 / Ubuntu 26.04.
Exact account/shell DEB hashes are in VALIDATION_PROFILE_FRONTEND.md and
VALIDATION_INSTALLED_SHELL_HOTPLUG.md; this check uses those installed packages.

## Controlled QA preparation

A fixed-root fixture, restricted to the two disposable acceptance hostnames,
asserts that its child name/home/metadata do not exist and captures original
account/common-PAM bytes and the main local identity/password fingerprint. It
creates the shared child through the actual installed AccountProvisioner, with
no owner password change. Private/root QA state is mode 0600. The driver source
is now public in DE profiles/tests/installed-two-sessions.py.

- Driver SHA256: 089de42c785ada5e1831a40a5403f7cf3f0e5f1366e9367153cfa9a57e595fe8.

Both sessions are started by the existing native LightDM Seat0 SwitchToUser
interface. This is an intentional existing-session helper test, not acceptance
of the still-unimplemented owned-session/network startup. LightDM itself locks
the initial main session when opening another login; that one-time lock is
authenticated before testing the unprotected Karyo roundtrips.

## Actual graphical caller and behavior

Real terminals launched from each native panel call installed karyo-desktops
and native pkexec, with the actual per-user graphical cgroup/session. Family
JSON contains exactly the main and new child; switch JSON reports changed=true
and the actual target VT. SSH rendering helpers are not authorization evidence.

| Base | Home session / VT / Shell PID | Work session / VT / Shell PID |
| --- | --- | --- |
| Debian | 518 / 8 / 32074 | 537 / 9 / 33049 |
| Ubuntu | 684 / 8 / 87639 | 703 / 9 / 89619 |

Both unprotected policies pass Home-to-Work and Work-to-Home activation with
LockedHint=false in both sessions. Changing only the child policy to home then
requires an actual compositor lock before it becomes visible. The returned
password form is visually inspected on both guests. WrongQA42 is rejected with
the visible PAM retry error; the known shared QA Home password opens the existing
session. Leaving the now-protected child confirms its lock before showing the
unprotected Home. A second entry again shows a fresh password form and successful
authentication restores the same child shell. Main/child Shell PIDs never change.

One Ubuntu reverse-command attempt did not reach the previous terminal PTY:
the result JSON retained its earlier mtime and there was no new helper process.
The gate was not accepted from that attempt. After visibly focusing a new tab,
the actual command runs and its fresh JSON/active/LockedHint checks pass. The
original failed assertion and inspection capture remain in the QA results. This
observation is not a proven helper failure or a claim of broad terminal-input QA.

## Teardown and remaining gates

Known GUI scripts/JSON are checked and removed. Only the captured new child is
terminated; its processes/session must disappear before cleanup. The fixture
rechecks local identity, home device/inode/UID, exact family/protection and main
password/PAM before removing its own unchanged metadata and running non-forced
userdel. Original passwd/shadow/group/gshadow and every common PAM file match
their pre-test bytes; dpkg audit and package verification are clean. No temporary
child/home/family/protection/state remains. Main QA sessions remain open.

Logs and captures are under out/{debian,ubuntu}-vm-qa/results/two-sessions-*;
input records include the exact driver hash. Root-only earlier PAM recovery and
the fixed QA driver are retained for further tests. Nothing is pushed; Forge,
private donor and owner systems are unchanged.

This accepts installed existing-session switching, including protected entry
and re-entry, on the tested two-user virtual-display setup. It does not close
shell menu wiring, own systemd/VT startup, per-profile network/DNS/VPN, capability
reset, callbacks, clipboard or the remaining Windows/macOS/VMware integrations.
