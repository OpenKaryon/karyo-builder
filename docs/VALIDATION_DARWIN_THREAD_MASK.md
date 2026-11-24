# Ordinary Darwin pthread mask baseline

DE commitd782ce7 adds an explicitly selected Mac pthread client. Builder
commit5f016b5 adds its `--suite threads` compilation path. The client uses
ordinary pthread creation/join, public signal-mask queries and Mach thread-port
acquisition/release. It does not send signals or induce an application failure.

The clean-source Intel64 Mach-O executable is8936 bytes, SHA256
`70cf58d7205689c7a75e305a010eac67f23ff23d511f13a2ae7afdc3d0b21c6d`.
Its build manifest pins DE revision
`d782ce75290107222499f034e847378a57696589`, source hashes and the existing external
SDK image. The earlier dirty preflight build is retained separately. The clean
manifest correctly remains compiled=true/runtime_tested=false; installed
execution has separate receipts rather than changing that immutable manifest.

## Actual installed62 behavior on both bases

The exact clean client runs through karyo-macos as the ordinary QA user on
Debian13 and Ubuntu26.04, with installed provenance independently checked for
62 patches. All four SIGCHLD/SIGTTOU mask combinations pass on both. Each worker
observes the requested mask, returns its argument and joins normally, and its
Mach thread port is nonzero and distinct from the main thread's port. Port
release succeeds. The creator's mask is unchanged after every join and its
original complete mask is restored at the end. Both application exit codes are0.

Each run starts in its own new launcher prefix and ends with Darling's normal
shutdown API. Protected persistent-data and MUSCLE prefix/server identities
remain unchanged. No captured app process needs forced cleanup.

This is a real Darwin-thread result. The separate native Linux DSO worker test
checks another boundary and cannot substitute for it. The identical Mach-O client
must still run on installed63 before accepting the new thread-mask restoration.
Passing this client does not establish original UGENE GUI behavior.

The index `out/migration/darwin-thread62-both-baseline-evidence-v1.json` has
SHA256 `4066193efdbf45e0e8caf845943b3e3ce1b2caecba1c2d3bd1d19c567f50942a`.
It retains the source/archive identity, actual reports, exit status, normal
cleanup and protected-prefix checks for both native systems.

## Separate Debian backing follow-up

A new ordinary backing-view run uses a fresh Debian62 prefix and the same
unchanged graphics executable. It returns0, reports the expected32/16/4 method
lengths and callback counts, and shows the correct red/cyan frames. Both frames
were hashed and viewed. The report is `out/migration/view-layer62-v2/debian.json`.
Thus the initial exit1 does not reproduce simply because a prefix is fresh.

The first failed result is still retained and its cause remains unresolved.
This follow-up neither replaces that gate nor proves a runtime correction.
The original stopped editor/Qt/UGENE62 queue is not silently resumed. These
independent follow-ups are recorded alongside the successful same-prefix
normal/debugger observations in the earlier boundary report.

The subsequent [installed Ubuntu63 report](VALIDATION_DARLING63_UBUNTU.md) records
the same clean client passing after all five targeted stages. That separate
installed result accepts the Darwin restoration contract on Ubuntu, alongside
observed native graphics-worker masks. No Debian63 engine or original UGENE
acceptance is inferred here. No security/shared suite or intentional crash test ran. No user VM, Acer,
Forge, donor or distro changed, and nothing was pushed.
