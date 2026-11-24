# Installed native thread boundary on Ubuntu

The complete Ubuntu26.04 engine uses the63-patch source at DE revision
`8513964d0c00d6eb5ef1a7e925795c14884a7d98`. The later DE thread-client commit
does not change this immutable runtime input. All four build artifacts have
independently verified sizes and SHA256 values. The runtime DEB is92717532 bytes,
SHA256 `084f5ebd1bb739d56f1a0e874621a3ae22d506a9b9707f2d79099f299a551738`.

The installed mldr matches that verified DEB's exact payload, SHA256
`99d4f8f66a7377017820a74b98a1c81b0dc596105569ebfee9740e81cf2d5845`, and exports
the intended pthread_create symbol. Its installed Build ID is
`29a0396229ce888fe4007fee9d7524ffced68ac8`. The intermediate unstripped ELF has
a different ID; it must not be used to symbolize the installed executable.

## Accepted functional boundaries

All five installed targeted stages pass: ordinary Cocoa/static Qt, public
IOSurface, nested layer painting, view backing, and normal same-prefix restart.
The nine baseline frames were exported, hashed and viewed. Restart preserves
the saved data after the old server has actually reached state Z.

The exact clean Darwin pthread executable documented in
[the two-base baseline](VALIDATION_DARWIN_THREAD_MASK.md) also passes on installed63.
All four public SIGCHLD/SIGTTOU combinations retain their intended masks, normal
join and distinct Mach thread ports. The creator's mask is preserved/restored.
Normal own-prefix shutdown succeeds, with protected data and MUSCLE process
identities preserved. The immutable compilation manifest remains separate from
these installed execution receipts.

The unchanged dynamic Qt client uses the original UGENE Qt5.15.10 frameworks
and its existing prefix. It displays actual text and exits0. Direct observations
of its native llvmpipe worker threads find both Linux signals blocked. This
tests the native graphics path independently of the Darwin pthread contract.
The ordinary upstream TextEditor document is also visibly readable. Both
additional frames were exported, hashed and viewed.

## Open application behavior

The first keyboard editor run saves the exact45-byte text, but the targeted
synthetic quit does not complete before75 seconds. That failure is retained.
A separate focused-XTest follow-up on the same installed63 runtime now performs
open, edit, save and normal Cmd+Q successfully: application0, observer0, no forced
cleanup, and no remaining editor window. The saved45 bytes are exact. Both the
visible saved text and the desktop after exit were exported, hashed and viewed.

The follow-up records actual focus and sends ordinary focused key events rather
than targeting a window with XSendEvent. Both focus handling and quit delivery
differ, so the earlier failure's exclusive cause is not established. No product
change or broad keyboard/host-device compatibility is inferred. The independent
evidence index has SHA256
`7439e98538d13e2d746492933051aae1a3529c4fe0f11d851a4ad4d887576c2b`.

Original UGENE53.1 verifies all12185 original regular members before each trial,
without modifying or re-extracting its bundle. An independent whole-desktop
observation shows its genuine loading screen at2 seconds, but no application
window at10 or25 seconds. The launcher returns1. This is not a usable UGENE
document workflow and is not accepted as GUI compatibility.

The cleanup label saying SIGTERM was sent is not proof that a process was live:
the old observer checks a retained PID/start pair before inspecting zombie state.
The relationship between launcher status, actual app lifetime and cleanup needs
separate diagnosis. A normal debugger observation does not catch a termination
within its bounded interval. The isolated client trace now proves control-socket
EOF: read(fd,4) returns0, then that client exits1. A separate trace of its exact
shellspawn parent observes a user-originated SIGSEGV followed by a default
kill(0,SIGSEGV) replay and death of that helper. The source's "resend to self"
operation actually targets the process group. This establishes collateral
helper termination, but not the origin of the first fault or a working UGENE GUI.
Repeated mount-table reads are retained only as a separate investigation lead.

Evidence is retained in `out/migration/native63-targeted/ubuntu.json`,
`darwin-thread-mask63/ubuntu.json`, `dynamic-qt-layer/ubuntu63-v1.json`, the
editor logs, and `ugene-macos/ubuntu63-observe-v2.json`. The full artifact and
installed-payload index is `native63-extra-ubuntu/index.json` in the external
review-output directory. The accepted-slice evidence index has SHA256
`194fd14e379b78807c357f0228390c8eb37d0eff1bdd11199693740b6afd2e62`.
Initial export schema/Build-ID checks failed before
acceptance; their logs remain separate from the corrected payload comparison.

No Debian63 full engine has been built or installed. The earlier Debian62
initial backing failure remains unresolved despite successful independent
follow-ups. These accepted Ubuntu slices do not complete the whole DE migration.
No security/shared suite, intentional crash, application-specific override,
policy weakening or push was performed. User VMs, Acer, Forge, donor and distro
remain untouched.
