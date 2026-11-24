# Installed Debian60 rendering and the remaining Qt startup boundary

The separate complete Debian13 engine built successfully from immutable DE
revision `6110b63a9f363042ff97b02e1dd1b4c273164952`. All four output artifacts
were independently checked by size and SHA256. The runtime DEB is 87821468
bytes, SHA256
`2afbfa76b4c979f182a4c1241e0d7a916c723c8d778d945ce99d59e34b3a7181`.
The native installer passed with adequate free space and no Debian archive
deduplication. Installed61 behavior is not inferred from this package.

## Accepted slices

All four installed targeted stages passed: ordinary baseline, public surface,
nested layer tree and the unchanged early-backing view. Cocoa and static Qt
controls are visible. Public red/cyan, nested blue/blue/yellow and implicit
backing red/cyan frames match their expected pixels. The nine corresponding
frames were exported, hashed and viewed.

Unchanged upstream TextEditor opens its ordinary document with the expected
text visible; that tenth frame was exported, hashed and viewed. A separate
ordinary keyboard scenario saves exactly 45 bytes and exits normally. Its
saved-file SHA256 is
`05786532df55212187f436d1163809d540c98cd0ad30ea1881bfbcbd831bca74`.

## Do not transfer the Ubuntu Qt result to Debian

The client using original UGENE Qt5.15.10 frameworks times out after 18 seconds
at its before-QApplication marker and presents no window. The ordinary queue
ends with status1 at that stage; original UGENE60 is therefore not attempted
on Debian. The successful Ubuntu layered-text observation does not establish
Debian application compatibility.

A read-only resource check finds roughly 760 MB available in the 4 GB guest,
with no swap. Thirty-three still-resident prefixes belong to completed own
echo/defaults/uname checks, as established by their account-owned launch logs
and live server identities. Their normal Darling shutdown preserves every
file and the separate persistent-data/MUSCLE prefix identities and servers.
Available memory rises from 762552 to 2692368 kB. This is QA maintenance,
not a claim that low memory caused the Qt failure.

One unchanged-client retry uses the same prefix, arguments and 18-second limit,
with no second binary upload. It fails immediately because Darling cannot open
the stored server's mount namespace. Read-only inspection identifies PID39361
as a zombie darlingserver whose namespace no longer exists. Pinned startup
source checks existence, comm and account ownership but does not reject zombie
state in getInitProcess. The failed first attempt and retry are both retained;
no PID file was repaired or removed, and no startup product patch was applied.

## Evidence and next boundary

The local index is `out/migration/native60-debian-accepted-slice-evidence-v1.json`,
SHA256 `793482d95b339ee7991435b867f93a39f3963fefa410f71dc92e5e08c05508ac`.
It includes four artifact hashes, ten viewed frames, the saved text, terminal
queue failure, resource receipts, both unsuccessful dynamic-Qt observations
and exact stale-process evidence. This supersedes the Debian-pending paragraph
in VALIDATION_DARLING60_UBUNTU.md without changing its Ubuntu observations.

The next common lifecycle work is stale-server detection and a controlled
restart without losing prefix data, followed by a fresh Qt observation and
original-app testing only after its gate passes. Candidate patch0061 separately
fixes termination reporting and has source/compiler validation on both native
bases; it is not installed. No full61 engine has started. No security/shared
suite or intentional crash test ran. User VM, Acer, Forge, donor and distro
remain untouched, and no changes were pushed.
