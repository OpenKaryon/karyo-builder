# Real Mac application data across a runtime update

The actual Intel Mach-O loader now has ordinary `--write-data BASENAME` and
`--read-data BASENAME` modes. It writes a new UTF-8 file in its Darwin HOME,
flushes it before exit and reads back the exact 53-byte content. The default
argument, temporary-I/O and exit17 cases remain unchanged. The source is DE
f1b893123bb4176f287016bb94cd11c546403738; the sample producer records a clean
source tree and the immutable existing Mac cross SDK. Native Linux source-only
logic checks pass on both compilers, separately from the actual Mac runs below.

## Before the update

On the Debian and Ubuntu kernel QA guests, the installed 31-patch Darling engine
executes both modes through public `/usr/bin/karyo-macos` as the normal graphical
UID1001. Each real Mac report identifies macos/x86_64, write/read success and
53 bytes in the same file. The two fixture environments are dedicated to this
check and contain no user work. Their directory identities, exact executable,
scope, source/archive hashes and installed engine provenance are retained.

- Debian prefix: `/home/karyoqa/.karyo-macos/a7ecdbcb19a6733c6/d6d716442/p`.
- Ubuntu prefix: `/home/karyoqa/.karyo-macos/a926619b336490977/df0904540/p`.
- Both guest root receipts: `/var/lib/karyo-qa/darling-data-before.json`.
- Local receipts: `out/migration/darling-data-upgrade/{debian,ubuntu}-before.json`.
- Evidence index: `out/migration/darling-data-upgrade-evidence.json`.

The clean Mac sample archive SHA256 is
76b8de5c5e6021945b1a251b6926ff82db2d202d36fa0a8e5809a7a47b988a2b;
its loader SHA256 is
52ccc90ae9186b957cf341c32409b245b63cda3b39ae963c32fcd85b27179c60.
Existing GUI acceptance samples are unchanged in separate input directories.

## Required after-update evidence

After the full 32-patch engine finishes installation and its normal application
run, stop only this idle fixture's old runtime with Darling's public shutdown
command. Restart the same application path and display scope, then read the same
file. Record distinct old/new runtime process identities, unchanged prefix
directory identity, exact file path/content and new package provenance. This
prevents an old still-running runtime or a newly created environment from being
mistaken for an upgrade pass.

The Debian post-update read passes on the installed32 engine. The old fixture
server PID385103/start20981018 stops through public shutdown; PID385670/start
21076204 starts for the same prefix identity2049:666516. The actual Mac program
reads the original53-byte file successfully. Its root receipt is
`/var/lib/karyo-qa/darling-data-after.json`; the local counterpart is
`out/migration/darling-data-upgrade/debian-after.json`. Ubuntu also passes the same real update/restart/read with its original prefix
identity2049:803696. Both read reports identify the unchanged53-byte Mac file.
Its local receipt is `out/migration/darling-data-upgrade/ubuntu-after.json`.
This data result does not establish graphical application acceptance. Only normal functional
application cases execute in this work; no security suites or denied-operation
scenarios are included. All commits remain local; Forge, distro and user systems
are outside this change.


After relocating the powered-off Debian QA VM and booting it again, the same
actual Mac program reads that original file from the same prefix identity.
Package/account/PAM/display-manager hashes are preserved and the temporary QA
autologin file is removed. The relocation receipt remains an unshipped local
artifact; this adds a real reboot/data observation, not graphical acceptance.
