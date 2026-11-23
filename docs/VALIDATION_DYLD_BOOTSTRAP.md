# Dyld entry follow-up and functional source-only preparation

Both complete native30 engines now build, audit and package on Debian13 and
Ubuntu26.04. Their manifests and all four artifacts per base were rehashed;
`out/migration/darling-thirty-patch-native-package-evidence.json` retains them
separately from the earlier29-patch engines. This accepts engine construction,
not real application compatibility. The Ubuntu30 engine was not installed.

Reinstalling Debian30 leaves existing package versions, account/PAM/DM hashes
and prefixes intact. The actual ordinary-user launcher detects the runtime and
inspects the real Intel Mach-O sample, but a fresh application prefix aborts
before the sample's main. No CLI/Cocoa/Qt result is marked passed. The actor now
contains only normal functional application runs; its earlier NoNewPrivs case
has been removed from the still-unaccepted draft.

## Actual next initialization failure

The current core is11247304 bytes, SHA256
0834c7afa3120b6a9ee3ce67673fffc61c4e1bb67f3227deec8c719022a37bcd.
LLDB loads the exact runtime modules with explicit Mach-O triples. The first
Libsystem failure is gone; the new stack is
`dyldbootstrap::start -> __stack_chk_fail -> dyld::halt` before vchroot main.
Mapped instructions store the original guard at FP-0x30, invoke __guard_setup,
then compare it at function return. Offline analysis reads the saved value0
and the dyld guard0xe7d3824983a114e8. The v2 exploratory read used FP-0x28;
v3 corrects that offset to the one established by the actual instructions.

The exact orphan was captured by PID383864, start, executable, argv, UID and
namespace identities, cored and stopped via pidfd after proving there were no
other namespace consumers. Prefix files remain. Root receipts and local raw
cores are QA evidence, not files shipped in packages or committed to Git.

DE56f3e71 adds patch0031 to only the dyld entry function and independently pins
darling-dyld63f667cf06d7ed59553adebb0c8d70a117135ac9. Ordinary dyld functions and
global compiler options remain unchanged. The actual patched entry body is
compiled with functional startup callbacks on both SDKs. It returns normally,
preserves literal argv/envp/apple vectors and executes callbacks in order. These
are positive function-level checks, not a claim that the whole engine or real
Mac applications already work.

## Preparation without the unit suite

`tests/acceptance/check-darling-inputs.py --source-only` performs the native SDK,
Swift recovery and actual patch application/reversal steps. It explicitly skips
the shared unit suite and records `unit_tests_executed:false`; that field must
remain visible when the receipt is consumed. The default full preparation mode
still runs its existing suite and records true. Neither mode implies a runtime
application pass.

The first31-source attempt used the old driver and unintentionally ran the
shared Debian suite; it stopped at the stale expected patch-count30 assertion.
Its failure is retained under `darling-current-inputs-accepted-v7`. The assertion
is updated to31, but this is not presented as a new full-suite pass. Following
the user's functional-only request, the separate v8 run uses --source-only on
both bases and contains no unit.log. It verifies44 Swift inputs and all31 patches
with real Git and zero-fuzz quilt, restoring73 original selected source files.

The evidence index is `out/migration/darling-dyld-bootstrap-evidence.json` and
the actual joined preparation receipt lives in
`out/migration/darling-current-inputs-accepted-v8/acceptance.json`.
The new source bundle is recorded in `darling-dyld-bootstrap-inputs.json`.
One complete Debian31 engine is now building; after it completes, build the
same bundle on Ubuntu and run normal installed CLI/Cocoa/Qt applications on
each native kernel. Do not convert function-level or build-only evidence into
real application acceptance. Commit locally; do not push.
