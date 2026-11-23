# Installed52 native engines on Debian and Ubuntu

Both complete52 engines built, passed package/input audits and were explicitly
reinstalled into their separate native QA guests. The immutable source bundle
records DE `7d13ab5a287fea7e2b0e820c0103a0c14214a791`. All four artifact sizes and
SHA256 values were checked again when joining the results. Same development
version strings are not used as proof of matching runtime bytes.

| Base | Runtime bytes | Runtime SHA256 |
| --- | ---: | --- |
| Debian13 |87844984|79666ffe7defe5dbfc990906d6b3e49fd08ba239e1d1650fba8debc017a745b7|
| Ubuntu26.04 |92705884|e0badbefed5979c09399a4f11c6138065dcba1cd0147ddc55cbaf7705893cf2a|

The actual loader, Cocoa and static Qt checks pass on both, using the ordinary
argument profile. UTF-8 titles, labels, button signals and raster rendering pass.
Each Cocoa client reports79 event iterations. All eight ordinary application
frames were exported, hash-checked and viewed; the Debian frames add:

| Debian frame | SHA256 |
| --- | --- |
| Cocoa |f8a10f194c69d80dc3c1f79c98af1021c8fc3acf04d0db5e17a75b926f091555|
| Qt Widgets |1f1fe41ffd7d4aa80bf564d31ec20b47cd6270134b8ead32e3a8a6d36a2dfaa8|
| TextEditor opened document |d802c624b72b13ba7fc6f84188d7de24797dd898127b7f207e8f93089feea564|
| TextEditor edited document |be1f44f3c2c2c36d6806702a79ed9fd546e8a42d03a69a367bab5a8beadcde1f|

The four stock utility operations pass on both. Original TextEditor saves the
exact45-byte edited text and exits through normal global Quit, with helper0 and
no remaining application cleanup. Its separate document-only bounded observation
uses controlled termination and is not a normal Quit result. The saved-file hash
on both is `05786532df55212187f436d1163809d540c98cd0ad30ea1881bfbcbd831bca74`;
Qt's rendered raster remains
`d90cf2c330b6cb14b737a913f15a4e4430fe7607b7c79394ba77041b4d3347d6`.
Successful52 rechecks do not explain or fix the original Debian45 cold uname136;
that earlier cause remains open.

Debian NSEvent waits are0.051613/0.051901/0.052236 seconds. Its CF window loop
returns4 for two early handled sources, then3 after0.050641/0.051588 seconds.
The aggregate checks the lower bound only for actual timeout results3. The
original53-byte data file is read after its own server changes25178 to27322,
preserving prefix identity. Original Mac MUSCLE5.3 performs the same three-sequence
FASTA alignment with its default two threads after its own server changes25941
to27966. The shared ordinary Cocoa APIs and unchanged dynamic Qt framework client
also pass on both. Detailed Ubuntu results remain in the
[Ubuntu52 report](VALIDATION_INSTALLED52_UBUNTU.md).

## Confirmed service boundary; graphical application still unaccepted

On both52 engines, public IOSurface layout succeeds but creation exits1 with
`Cannot obtain IOSurfaceRoot!`. The later lifecycle and two-color layer clients
are not executed after that failed prerequisite. The separate dynamic Qt layer
client exits1 without a captured frame on both.

The same public matching client on both bases finds the real IOSurfaceRoot class
through enumeration, but a direct query for the same name returns no object.
Debian uses the clean four-client build; its matching executable is byte-identical
to the earlier Ubuntu diagnostic build. Both queries use valid public inputs and
their own consumed dictionaries. This directly supports the common0053 fix to
the unsupported binary single-service RPC, without any method replacement.

Original UGENE on Debian52 exits0 after about2.37 seconds, with no frame captured.
The first Ubuntu52 attempt reaches a45-second controlled termination, but its
viewed compositor frame shows no application content. Two later Ubuntu52 attempts
with timed2/10/25-second observations exit0 after2.83 and2.06 seconds, before late
frames. Neither a zero exit nor viewable X11 metadata proves GUI/FASTA acceptance.

The precise UGENE release source explicitly enables the layer path before
QApplication in [Main.cpp at release1131c46](https://github.com/ugeneunipro/ugene/blob/1131c46e1d6fc6b8737418ed2b325030bd8d9984/src/ugeneui/src/Main.cpp).
The cause of its early0 exits is not established by this source statement or by
the independent IOKit failure. No application settings or original libraries are
changed to conceal either boundary. The queued53 UGENE observer retains timed
frames and still requires visual review and an ordinary document workflow.

## Frame coordinates and test-environment readiness

The first Debian52 Cocoa observation retained its initial X11 coordinates before
the window manager centered the actual displayed window. The observer now reads
geometry after settling and compares it again after capture, retrying movement.
Both installed52 guests pass a focused ordinary loader/Cocoa/Qt regression with
that observer. All four new frames were exported and viewed, with content
coordinates matching their actual centered windows. This prevents future pixel
checks from sampling a stale desktop position; it does not make an empty frame
an accepted GUI. The actor is a separate test input, not a modified runtime.

The Ubuntu resource inspection finds no cgroup PID-limit events or kernel OOM
messages. A review of63 idle Darling servers identifies40 completed own QA
prefixes with matching owner, path, logged application and PID/start identity.
Normal shutdown of those40 restores available memory from about0.92 to2.30GB,
without deleting prefix files. The persistent-data and MUSCLE upgrade prefixes
are excluded. The subsequent UGENE early exit persists, so memory cleanup is
readiness work rather than a proven application fix.

All24 original52 build/application controllers are terminal. No duplicate52
builds are needed. Ubuntu53 is now the sole full engine build, with Debian53
queued behind its verified artifacts. Each base has one queued sequential
ordinary53 pipeline; do not start an additional main actor alongside it. The
common53 source/three-unit compiler checks already pass on both, but installed53
matching, CPU pixels, cross-process lifecycle and layer presentation remain
unproven. Broader joined DE, VMware and VPN gates remain separate.

Machine-readable identities and ordinary reports are retained in
`out/migration/darling-native52-{debian,ubuntu}-common-cocoa-evidence-v1.json` and
`out/migration/darling-native52-both-common-cocoa-evidence-v1.json`.
Only ordinary functional/source checks ran. No shared/security unit suite, push,
Forge/distro/ISO/donor modification or user-machine operation is involved.
