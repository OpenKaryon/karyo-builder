# Public desktop menu: native source acceptance

Shell runtime source: 2a777714ec3032be892a2d6304730cf37808a89d.
The following uses hash-recorded native source overlays on the two disposable
VMs. Final clean shell package builds are running; this is not installed DEB
acceptance. Root profile helpers remain from installed bf831b0.

## Inputs and ownership

### Debian

- Native binary SHA256: 3d6a9dd7f626473e7d5f42fceb917a24865fd2b9ff4efc9fbde76af4f1892d1f.
- Wrapper SHA256: ac6bbef45afb446bbcbb5edb1357ceb7bcc7bd8598ba124adac4e5dfe8a60cdc.
- GUI-creation QA driver SHA256: cd677f88d3b7002ac97c9cabf39ab4048d1d6cacf8ad310bd1860fb46d1f40d9.
- Exact changed/runtime file hashes: out/debian-vm-qa/profile-menu-input/record.json.

### Ubuntu

- Native binary SHA256: 861762544fdc84072498540e8ecd4bb4480a26eb6797dcaf3ad1820df86cc697.
- Wrapper SHA256: ac6bbef45afb446bbcbb5edb1357ceb7bcc7bd8598ba124adac4e5dfe8a60cdc.
- GUI-creation QA driver SHA256: cd677f88d3b7002ac97c9cabf39ab4048d1d6cacf8ad310bd1860fb46d1f40d9.
- Exact changed/runtime file hashes: out/ubuntu-vm-qa/profile-menu-input/record.json.

The source runtime files match the committed revision; documentation and
publication of the already-tested QA fixture occur after compiling the overlay.
ProfileControl is owned by the session, while its transient menus and dialogs
are owned by each output-bound panel. Read requests coalesce; mutations serialize.
Separate passwords use stdin and never argv, and response/error bytes are bounded.
Timeouts, retained accounts and uncertain mutations have visible distinct outcomes.

## Actual GUI checks

On both native bases the public desktop button appears without the private
openkaryon-desktops command. Its real click loads only the current account family
and shows the current entry, then opens the creation form. An empty name produces
a visible validation error and creates no account. Entering the reserved fixture
label KQ Switch Work and submitting the real form creates kq-switch-work through
the installed public frontend/native pkexec/root account helper, without a new
password prompt. The root fixture independently verifies actual UID/home, shared
hash, unexpired account and unchanged owner/common PAM, then captures the known
absent-before new child for constrained teardown.

A refreshed menu shows the new child as not started. Selecting it displays
the backend stopped-target message, rather than silently doing nothing. Owned
startup is still pending; this message must not be mistaken for its implementation.
The existing LightDM manager starts the child session for the separate live-menu
test, and its one-time main-session lock is authenticated before the roundtrip.

Actual menu clicks then switch Home to the running child and back on both bases.
Neither unprotected session is locked, the output-bound panels are recreated,
the menu remains usable, and shell PIDs stay unchanged: Debian main/child
35009/35726 (sessions 567/578), Ubuntu 93616/94932 (737/748), VTs 8/9. No terminal
script or root rendering helper substitutes for these real menu clicks.

## Regression and cleanup

The controller test reports 17 passed cases on Qt 6.8 and 6.10, including ordinary
UID 65534 runs. It checks event-loop progress, shared list jobs, stdin-only password,
literal option-like labels, consumer destruction, concurrent mutation rejection,
failed starts, stopped/retained results, malformed/wrong/oversized replies and
deadlines. Four targeted CTests pass on each base. Russian strings compile too.

The updated fixed-host QA driver supports arm/capture around real GUI creation.
Cleanup requires the exact captured new child/home, no child processes/session,
unchanged family/protection and original owner/PAM; only those test objects are
removed. Original passwd/shadow/group/gshadow/common PAM bytes match afterward.
Source wrappers/binaries are removed only after SHA verification. Package checks
and dpkg audit are clean, LightDM is active and both users are signed out.

Evidence: out/{debian,ubuntu}-vm-qa/results/profile-menu-*: listed/create-form/
empty-name/new-child/stopped-error captures, created/first-return/to-child/to-home
and cleanup logs; source stages hold binary and driver hashes. Root-only PAM
recovery and known fixed QA drivers are retained. Nothing is pushed; owner systems,
private donor and Forge are untouched.

Clean native DEB installation acceptance, owned systemd/VT startup and per-profile
network/DNS/VPN/capability/callback/clipboard services remain required. Existing
protected-session behavior was separately accepted with installed helpers in
VALIDATION_TWO_SESSIONS.md, not inferred from this unprotected UI roundtrip.
