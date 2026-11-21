# Installed living graphical session journal reattachment

This gate preserves a living isolated desktop across controller restart. The
complete public profile runtime and overall migration remain unfinished. All
commits are local, with no push or changes to owner machines, Forge or the donor.

## Exact runtime inputs

Installed DE source: a173b1e0cd9bb3357a0a14ad9174a6544ef6bbd9.
Source archive SHA256:
03181d0001ccda52d072ccd9af544b0a078151b9be73a8be6e02ca9f7e486c2a.

- debian accounts: out/migration/profile-session-journal-debian-accounts/karyo-profile-accounts-20261121T191342Z-d9689311; 77216 bytes; SHA256 70d241401b7f9f78ec579f52ab75db88f6e097fb088e56878b8047c326bbc06c.
- debian host: out/migration/profile-session-journal-debian-host/karyo-profile-host-20261121T191401Z-2f946e1d; 33280 bytes; SHA256 da5b14c515bf70a5b5766c547de789a7cab5d2cbaa7c120783ae9822f7559900.
- ubuntu accounts: out/migration/profile-session-journal-ubuntu-accounts/karyo-profile-accounts-20261121T191341Z-934ea954; 78308 bytes; SHA256 5da25cfc5be11ce8f814714aa5cb04e293530fd7d60099ef6cf600cfb3cc3229.
- ubuntu host: out/migration/profile-session-journal-ubuntu-host/karyo-profile-host-20261121T191401Z-51ac44e4; 33704 bytes; SHA256 0e3c3448ef687d67715ccad24dacd893ffe27678634505e402143f126624dcd5.

The published DE profiles/tests/installed-journal-session.py has SHA256
233aeb33be484be753f49b57ae7aa6172ea9ba65841b23d26651b26b7264641e.
Both guests execute those exact root-owned bytes against installed packages;
there is no Python source overlay. Basic two-mode acceptance before adding the
editor is retained in profile-session-journal-basic-native.log for both guests.

## Ownership and restart behavior

Schema 3 records the prepared user-manager policy directory/file inodes and fixed
bytes, then captures the coupled manager/PAM/graphical identities after native
startup. Receipts include unit invocations, process start/executable identities,
logind owners, graphical scope invocation, VT and trusted entry/compositor paths.
New observers use current pidfds and revalidate private resolver mounts and
native manager policy. Restoring observers does not start or stop those resources.

Namespace consumers must be under the captured graphical logind, user-manager
or original transient PAM service cgroup. Root sudo descendants remain valid
within those captured scopes. Unrelated consumers, changed anchors and unresolved
process churn retain resources instead of signaling processes or assuming absence.

SessionRegistry holds verified restored observers through the host accept loop
and excludes only those tokens from offline DNS/network recovery. Native entry
can reauthorize its caller again immediately before activation. Session records
prevent lower DNS/network cleanup from running ahead of the GUI/manager lifetime.

## Native acceptance on Debian 13 and Ubuntu 26.04

The fixed-host root probe prepares a proven new synthetic UID1002 child. A
captured child Python controller owns its private network, resolver/bus, scoped
user manager and PAM compositor. Only that captured controller receives SIGKILL.
A new observer restores the same living graph; then an actual socket-activated
installed host restores it before answering a request from the captured Work
network/mount/logind context. The host retains manager and compositor pidfds.
The root QA client is not an interactive PAM/polkit authorization acceptance claim.

Two independent modes pass on each base:

- Unprotected GUI: the same manager, compositor, shell and installed editor PIDs
  survive both observer and host startup. The editor is activated by the scoped
  user manager, so its app.slice process is a real additional namespace consumer.
  The external driver types KaryoUnsavedJournalProof through only this QA VM's
  RFB console. Source-file bytes stay OriginalJournalFile plus a newline. The
  unsaved cache hash is 39bd6412702c0d834f277c513993bc3e24fa60ec2e0d3c64f8083c1a5e902730
  before and after; screenshots visibly retain the text and unsaved indicator.
- Home-password policy: the same lock PID and compositor remain locked, without
  a shell or editor. The fixture never supplies a password or unlocks the desktop.

Known orderly teardown first returns to the original validated main login, closes
only the captured graphical session, waits for natural user-manager exit and then
closes its private DNS/network. It does not stop an arbitrary user@ service.
Original account/common-PAM bytes, main shell/session and full network snapshot
are restored. Each base's results/profile-session-journal-native.log contains
both successful cases. Results/session-journal-editor-{initial,ready,after}.png
provide visual evidence. Earlier DNS six-case, network five-case and host/private
network/mount transport probes pass again on the final schema-3 runtime.

Read-only postchecks pass on both guests: original main shells 36901/97122,
logins 595/765 on VT8 active/unlocked; child account/home/runtime/drop-in absent;
no named namespace or private resolver runtime/configuration; forwarding remains
0. The socket is disabled/inactive; its service is static/inactive. Private root
journal is empty schema3, directory 0700, files 0600. Installed probe hashes,
dpkg -V and dpkg --audit are clean. An initial postcheck incorrectly expected a
static service to be disabled; correcting that expectation changed no runtime.

All 309 profile tests pass on Debian and Ubuntu as root (skip3) and ordinary
UID65534 (skip89). Builder recipes are unchanged, with the existing 38-case result
retained and four new native DEB builds validating current packaging. No C++ code
changed, so the previously accepted full CTest suite is not redundantly rerun.

## Remaining gates

Prepared/incomplete or interrupted-closing session receipts currently retain
resources; they need explicit reconciliation. Automatic logout/crash return,
primary Home host-network restart, full long-lived allocation/public stopped-
profile wiring, forwarding/DHCP/DNS reconciliation, actual NetBird/PKCE lifecycle,
profile catalog overlays, family clipboard and remaining Wine/macOS/VMware
integration are still open. Native live-GUI acceptance does not claim Internet,
VPN routing or physical GPU/Wi-Fi/camera/microphone validation. Distribution image
assembly and Forge remain owned by their separate products.


The later preparation-recovery gate in VALIDATION_PROFILE_PREPARED_JOURNAL.md reruns these living editor/lock scenarios on bcff209 packages. Original a173b1e logs are retained with before-prepared prefixes; closing/logout supervision remains open.
