# Candidate64 process signal replay

DE revision `a261c3710a1c063c0574efb7e2ad2112f1342545` adds a common correction
for default signal replay. It does not change UGENE or introduce an application
profile. The complete Ubuntu engine and its five installed baseline stages now
pass. The complete Debian engine is building; original UGENE GUI acceptance
remains open.

## Observed installed63 behavior

An unchanged original UGENE53.1 launch shows its loading screen, then loses its
windows. A trace of the direct Darling client records control read(fd,4)
returning0 followed by exit_group(1). That is an engine-client error, not proof
that the application naturally returned1.

A separate trace observes the exact captured app's shellspawn parent, verified
by PID/start, UID, executable and argv. It receives a user-originated SIGSEGV,
replays kill(0,SIGSEGV), and dies. Linux PID0 selects the caller's process group.
The emulation source calls this operation "resend signal to self". Thus the
default replay can terminate a launch helper alongside the affected process.
The first signal's origin remains unresolved; the trace does not establish an
application CPU-fault location or working original UGENE compatibility.

A short main-thread snapshot maps to dyld lstat while plugins load. Repeated
mount-table reads alone are not a proved defect. Plain GDB sees an externally
sent main-process SIGSEGV. A descendant-follow attempt instead stops on a normal
child exit and is inconclusive. These original diagnostic records are retained.

## Common source change

Patch0064 replaces group0 with the raw Linux caller PID in both default stop and
terminating-signal replay. It preserves the disposition, signal number, masks
and RPC checks. Only the exact reviewed sigexc.c path enters the recipe footprint.
The checker independently pins darling-xnu revision
`fa29287aa2f0115271e091f1031f53c9e024005d` and its upstream URL. Original upstream
notices remain intact. The patch SHA256 is
`4a09adfbc274743b6aaa929b3183bd07ff49f0d9a347f0d8023fc888d1dcad76`.

Both Debian13 and Ubuntu26.04 source-only checks apply/reverse all64 patches with
zero-fuzz quilt and restore all114 reviewed files. Their receipts explicitly
record unit_tests_executed=false. The positive recipe inventory also records
the already existing native-thread source among the two added files.

Both actual configured CMake variants, emulation and emulation_dyld, provide the
compiler commands and a220-file header/source closure. Its archive SHA256 is
`55dce0770f35c4d512992ffe0cd2dd4103056aedce6fe8617b337c227f8e3699`.
The complete original and candidate translation units pass syntax compilation
with Debian Clang19.1.7 and Ubuntu Clang21.1.8: four checks per base. Each compiler
uses its own builtin headers; project headers and configuration remain exact.
This is whole-unit syntax compilation, not a surrogate runtime or link test.

The complete Ubuntu64 build finishes successfully. Its final log contains both
actual configured sigexc.c compile commands, including emulation_dyld. All four
artifacts have independently verified sizes and SHA256 values. The runtime DEB
is92,721,714 bytes with SHA256
`5a8576cc87e016e705828377dbd06e000b4d9467fa4eeb46effd45c82757cb06`.
No intermediate library is used. The same immutable source now builds separately
for Debian, which still has installed62 until its own gates complete.

Evidence stays under `out/migration/darling-current-inputs-accepted-v44` and the
external `native64-signal-closure`, `native64-signal-{debian,ubuntu}-units` review
directories. No deliberate fault/signal case or shared suite was executed.
Nothing was pushed; user machines, Forge, donor and distro remain untouched.

## Installed Ubuntu64 acceptance boundary

The initial installation stops before APT because guest free space is75MB below
the existing threshold. That failure remains separately preserved. Exactly six
old guest staging DEBs are removed only after their original complete host
artifacts are checked byte-for-byte by size and SHA256. Their paths and retention
receipts remain recorded. No prefix, application, user data or64 payload is
removed; the space threshold is unchanged. The identical controllers then pass.

All five installed stages return0: ordinary Cocoa/Qt, public IOSurface, nested
layer ordering, backing-view display and a same-prefix server restart. The old
server is actually Z; a replacement starts and saved data remain exact. The
unchanged public Darwin pthread client passes all four CHLD/TTOU mask cases,
join, distinct Mach ports and creator-mask restoration. Its own-prefix normal
shutdown succeeds without forced cleanup or changes to protected prefixes.

Nine real baseline frames are exported, independently SHA256 checked and viewed:
readable Russian Cocoa/Qt controls, red/cyan public surfaces, nested blue/yellow
painter order and red/cyan backing views. Installed mldr, dyld and kernel-library
bytes match the verified64 DEB. The installed mldr still exports pthread_create
and has Build ID29a0396229ce888fe4007fee9d7524ffced68ac8;64 changes the signal
libraries, so an unchanged mldr identity is expected.

Original UGENE53.1 still verifies all12185 original regular members. In its fresh64
prefix, the genuine splash is visible at10 and25 seconds. The captured app is
actually sleeping, not a zombie, before the45-second observation limit. The
observer then terminates only its own captured fixture process. This does not
repeat the earlier early exit, but neither a main window nor a document workflow
is accepted. Observer status0 is not application success. Read-only preferences
show20 of51 external tools checked and13 valid, including detected versions;
that is evidence of startup progress, not proof of the remaining delay's cause.

The accepted-slice index is `out/migration/native64-ubuntu-accepted-slice-v1.json`,
SHA256 `7dd58c130df58001c3e37eac7a447d5440581c3f260ccec74016af402b87c2dc`.
It links full artifacts, installed stages/payloads, actual thread and lifecycle
receipts, frames, the original space failure and the retained UGENE observation.
The prior Debian62 initial backing exit1 remains unresolved; this Ubuntu pass
does not replace it or complete the whole desktop migration.

## Ordinary application follow-up on installed64

The unchanged upstream TextEditor now passes opening, keyboard editing, exact
45-byte saving and focused XTest Cmd+Q on64 as well: application0, observer0,
no forced cleanup and no remaining editor window. Both actual frames are
exported, SHA256 checked and viewed. The saved text has the same SHA256
`05786532df55212187f436d1163809d540c98cd0ad30ea1881bfbcbd831bca74`.
This does not rewrite the earlier63 targeted synthetic-input timeout.

The original MUSCLE53 binary also completes the same ordinary alignment on64
at its default two threads, then shuts down its fresh prefix normally. Exact
output matches the separately recorded63 scientific result. Existing saved-data
and MUSCLE prefix identities remain intact; neither app code nor dependencies
are patched. See [the scientific boundary](VALIDATION_MUSCLE53_FRESH.md).

A separate normal QtCore5.15.10 client links against the unchanged original
UGENE framework. It launches one echo child from the main thread, then three
from each of two Darwin threads. All seven start and finish normally with exact
21-byte stdout, both workers join and the new prefix shuts down with status0.
Protected prefixes remain unchanged. This bounded positive scenario passes;
it does not establish every asynchronous QProcess or UGENE scheduler path.

Original UGENE's corrected longer observer still times out after120 seconds.
Actual frames at10,45 and100 seconds show the same splash. Its preferences record
20/51 tool checks and15 valid tools in this particular trial, with unchanged
preference bytes across those observations. Root snapshots at15,60 and105 seconds
inspect only the captured app's UID and mount namespace. They find no live tool
child, while the app remains sleeping. A prior120-second observer mistakenly
retains the old2/10/25 frame schedule; its empty unprivileged DPREFIX list does
not prove that processes are absent. Both incomplete and corrected records stay.

A separate ordinary GDB snapshot is detached normally. Exact installed64 kernel
bytes and a verified Mach-O TEXT vmaddr/fileoff0 mapping identify recv-message
RPC wait and other nearest symbols. GDB warns about PID namespaces and cannot
fully unwind these Mach-O frames: an apparent deeper faccessat or mutexwait
address is not an established caller chain or root cause. An earlier late
attachment finds the owned PID already gone and changes no process.

For one further ordinary launch, the app's native console logging is enabled
using UGENE_PRINT_TO_CONSOLE=1, confirmed in the exact
[official53.1 Main.cpp](https://github.com/ugeneunipro/ugene/blob/1131c46e1d6fc6b8737418ed2b325030bd8d9984/src/ugeneui/src/Main.cpp).
The fetched read-only source files match their Git blob IDs. This is logging,
not a runtime compatibility profile. The journal shows tool validation advancing,
including ordinary tool errors, then stops during further scheduling. The app
still reaches the bounded timeout; the final partial line is not proof of the
blocking operation. Original UGENE GUI remains unaccepted.

The follow-up index `out/migration/native64-ubuntu-app-followup-v1.json` has SHA256
`f0c62baf24e96b6ef94a3442d4b0bac35847b2f69ff1ce29d2eb6b0a7d3d5b1c`.
It preserves the host-only observer syntax mistake, earlier schedule defect,
successful ordinary application slices and inconclusive diagnostics separately.
