# Native Cocoa thread-return follow-up

The complete Debian32 runtime builds, audits, packages and installs in the kernel
QA guest. All four build artifacts are rehashed before installation; existing
packages, accounts, PAM and display-manager configuration are preserved. Real
Mach-O CLI arguments, UTF-8 file I/O and exit17 still pass. The separate old-data
fixture also survives a real runtime stop/update/restart in its existing prefix.

## Actual remaining graphical failure

Cocoa passes the former libm recursion but terminates without its required report
or a captured window. Its launcher returns0; the application actor correctly
remains failed because that code alone is not graphical acceptance. Qt has not
been accepted by this run, which stops at the missing Cocoa JSON.

A bounded capture of this normal Cocoa invocation stops on native SIGABRT in a
worker thread. The real core shows glibc __longjmp_chk and an mldr return address
0x55b2dbbcc5a6; mapping and instruction inspection identify the call at mldr file
offset0x55a1. The original source has one corresponding call, in
__darling_thread_terminate. The core971626080B has SHA256
e0c183e13780ad1010a1f2b0b71d0b0b644aa385176919e1a72b5b247acd56c3.
It is retained only as a local QA artifact, outside source and shipped packages.

The thread entry saves a still-live Linux frame and deliberately switches to its
own Darwin stack allocation. Termination returns to that Linux frame before
unmapping the Darwin allocation and completing the native pthread. The glibc
fortified wrapper assumes a single contiguous stack and rejects this legitimate
transition. DEc094b95 binds only this call to the native libc longjmp ABI; other
calls, cleanup/RPC flow and compiler settings remain intact. There is no
per-application rule.

## Positive functional check

The checker compiles the actual patched termination body and ABI declaration,
supplies ordinary RPC callback implementations, and completes16 genuine live
pthread stack returns on each native SDK. The original Linux frame receives
control and unmaps the old Darwin allocation afterwards. The first harness was
missing stdbool.h; its failed compile is retained. The corrected v2 passes on
Debian and Ubuntu. This is native function-body evidence, not a whole installed
Darling or Mac graphical pass. Full33 builds and normal installed runs are queued
after the current Ubuntu32 build, one complete engine at a time.

## Ordinary packaged Mac utilities

The upstream Mach-O uname prints Darwin and echo preserves UTF-8 on Debian32.
The first checker incorrectly included the one-time prefix-creation message in
the expected program output; the corrected checker permits only that exact
message for the inspected prefix. The initial defaults case also assumed Apple's
-string syntax. A separate v3 uses the supplied OPENSTEP implementation's actual
syntax and full domain/key/value read format. Write returns0, but the next read
still returns2 and cannot find the value. This preference round-trip remains an
open runtime issue; do not claim all stock utilities pass.

`out/migration/darling-mldr-return-evidence.json` records actual32 reports, core
and disassembly hashes, both positive native function-body receipts and the
unaccepted boundaries. `darling-data-upgrade-evidence.json` separately records
the accepted Debian same-prefix data read. Ubuntu32 normal app/data/utility runs
remain queued. Only ordinary functional cases run; no security suites, denied
operations or command-payload checks are included. All commits remain local.


## Complete33 source inputs verified

Source-only preparation v10 passes on both native SDKs. It verifies44 fixed Swift
inputs, applies/reverses33 actual Git and zero-fuzz quilt patches and restores75
pristine source files. The receipt explicitly records unit_tests_executed:false;
no shared suite was run. The clean DE source is c094b95 and the resulting source
bundle is recorded by `darling-mldr-return-inputs.json`. Native full builds remain
queued Ubuntu32 -> Debian33 -> Ubuntu33. A source/functional compiler pass does
not accept the future installed33 runtime or graphical applications.
