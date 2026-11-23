# Actual native CLI execution and the graphical libm follow-up

The complete Debian31 engine now runs actual Intel Mach-O code through the
installed ordinary desktop launcher. The loader probe reaches Mac main,
preserves literal arguments and completes its UTF-8 file-I/O contract. Repeat
launch returns0 and a separate real --exit17 run returns17. This is native
application execution, not an inference from package installation or compilation.

The first functional actor stopped after the successful loader because a removed
QA scenario left a stale marker reference. Correct that reference, preserve the
first log and rerun against the same existing prefix scope. The retry establishes
the recorded CLI cases; its result remains passed:false because Cocoa exits1
before writing the application report. The independent Qt diagnostic times out.
Neither graphical application is accepted yet.

## Actual common graphical failure

The normal Cocoa launch loads its real executable and AppKit libraries. The
captured core at the first fault contains repeated __sincos_stret frames at
RSP/RBP0x7fffff600000, the bottom of the eight-megabyte virtual stack. Exact
libsystem_m mapping and offline LLDB identify the function, bounded to20 frames
to avoid an unbounded recursive unwind. Its installed instructions at offset
0x5c88 call its own0x5c80 entry. The float variant is equally recursive.
__exp10 at0x5cd9 jumps to its own0x5cd0 entry; __exp10f calls that entry.

The original root source implements scalar sin/cos pairs and pow(10,x). Modern
Darwin library-call optimization rewrites those implementations into their own
ABI helpers. DEcd2d6a2 adds patch0032, -fno-builtin in only the libm CMake scope.
Release optimization and flags outside libm remain intact; the original scalar
functions and public return structures are unchanged. This is a general math
implementation fix, with no per-program rule or runtime injection.

The core623757144B, SHA256
a1668067b8a87192c9918c867b1f2f2e035835b33d1b0c6fa87b6468b8e1430f,
was streamed to a local QA directory and rehashed. It is not committed or shipped.
The first debugger attempt timed out while trying an unbounded all-thread unwind;
discard its altered-execution status as acceptance evidence. The second bounded
capture saved the core before backtrace, detached and observed the same normal
launcher exit1. The app process closed; ordinary per-prefix runtime services
remain available as designed. No other desktop or application's process was killed.

## Executed functional compiler checks

The numerical checker compiles the exact selected sincos.c and exp10.c and uses
the float/double structure declarations from the original header. Both native
SDKs pass30 ordinary calls across six helpers, including their pi variants.
Actual Darwin LLVM output retains calls to scalar sin/cos/sinf/cosf/pow rather
than the helper itself. Early checker iterations encountered quoted-CMake-token
and aggregate-return IR parsing mistakes; the v4 run retains successful compile,
numeric and LLVM artifacts on both bases. It executes no deliberately bad or
privilege-related case and is not presented as whole-engine runtime acceptance.

Source-only preparation v9 also completes on both SDKs:44 fixed Swift inputs,
32 actual Git and zero-fuzz quilt forward/reverse patches,74 pristine source
files restored and unit_tests_executed:false. The new source bundle and local
source revision are in darling-libm-inputs.json. Complete builds are queued
strictly Ubuntu31 -> Debian32 -> Ubuntu32; no two complete engines run together.
Normal application runners wait for their exact32-patch manifest before installing.

The evidence index is out/migration/darling-libm-evidence.json. CLI/runtime logs,
root debugger receipts, local core/hash, bounded symbolication, exact native
disassembly and positive source/compiler artifacts remain separate. Required
next evidence is actual normal CLI/Cocoa/Qt on both installed32 engines, displayed
frames, existing-prefix/upgrade and additional-account behavior. The overall
migration remains active; all commits stay local and nothing is pushed.


## Native CLI confirmed on both bases

Ubuntu31 completes build/audit/package and installs on the normal QA guest with
existing package versions and account/PAM/DM configuration preserved. The same
ordinary functional actor now executes actual Intel Mach-O code on kernel
7.0.0-43-generic. Its Mac loader reports passed:true, the ordinary invocation
returns0, and the separate --exit17 program returns17. Debian's corresponding
cases run on kernel6.12.117+deb13-amd64. Both use real Mac main, argument and
UTF-8 file-I/O code, rather than a Linux substitute or an engine-presence check.

The current overall actors still fail at Cocoa exit1, before its report; neither
result implies a Qt or graphical pass. Ubuntu's exact libsystem_m also contains
self-recursive float/double sincos calls and the exp10 self-jump, confirmed from
its actual built binary. This establishes the compiler defect on both engines;
the bounded Cocoa core separately establishes its real fault on Debian.

`out/migration/darling-native-cli-both-evidence.json` retains both normal runtime
reports, exact actor/kernel/package inputs, rehashed build artifacts and math
disassembly fingerprints. It explicitly accepts only CLI and leaves GUI false.
The complete Debian32 engine is running, followed by the queued Ubuntu32 engine;
their normal CLI/Cocoa/Qt runs remain required. No security suite or denied
operation is part of these normal application cases.
