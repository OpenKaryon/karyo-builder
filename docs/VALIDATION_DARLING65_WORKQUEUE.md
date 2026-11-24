# Candidate65 workqueue entry

DE0399c08 adds a common x86-64 workqueue reentry correction after the natural
[Debian64 guard-page failure](VALIDATION_DARLING64_DEBIAN_BOUNDARY.md).
It does not modify UGENE, the scientific executables or any application profile.

The exact original bsdthread_register.c has SHA256
`dd6059651c9d7544e1df1d4054defaa7c75aef38907d6165877485ce41b9a355`.
The existing XNU pin is `fa29287aa2f0115271e091f1031f53c9e024005d`.
The reset described by workq_kernreturn is absent from its jump helper. Reused
threads therefore retain their prior syscall frames. Actual manual fault frames
show that accumulation below the active workqueue entry.

The allocator places each workqueue pthread object immediately above its
downward-growing stack. Candidate65 restores the aligned stack top from self,
clears the old frame pointer and pins the target in r10 before jumping. The
rdx stack-bottom metadata and all six entry arguments are preserved. Exact
installed start_wqthread disassembly confirms that the raw entry creates its
own fake return address and frame. The32-bit branch remains unchanged/untested.

Only the exact bsdthread_register.c path joins the reviewed footprint. Patch
SHA256 is `3d849ed774c3dfab30571b1f6564343e552a40593a07becbf08a5909a11f7d8e`.
The positive source inventory has65 patches,115 paths and the same two existing
added source files. Original notices and unrelated entry paths remain intact.
Builder's positive source-input controller accepts the newly reviewed65-patch
recipe; its previous64 ceiling rejected the first host preflight before Docker.
That record is preserved separately from the subsequent actual source checks.

A native positive ABI fixture uses the exact raw-entry prologue and ample512KB
space for64 ordinary reentries. There is no guard/fault case. On both Debian and
Ubuntu, the original helper completes with8064 bytes of stack drift. The
candidate completes at one stable stack position with all arguments preserved.
This first replay uses `-O0`. Its native helper source hash is
`6c38fbd3152b39d22832fb547762e28becdc02efa219eb414b903b973fe5c43c`;
the packaged patch adds explanatory comments without changing those instructions.
Evidence is external `native65-workqueue-abi/result.json` and its exact C inputs.

The real configured kernel and dyld objects both use an effective `-O3` after
the packaging `-O2` flag. A second replay uses the same exact C inputs with
`-O3`, `-DNDEBUG` and the applicable native hardening flags. Both Clang 19 on
Debian and Clang 21 on Ubuntu complete 64 normal reentries: the original drifts
4032 bytes, while the candidate stays at one stack position. All six arguments
remain exact. This replay does not run a Darwin application or create a fault.

Source-only acceptance v46 also completed on both bases: all 65 patches apply
with zero fuzz, reverse cleanly and leave the 115 reviewed original paths
pristine. No unit suite was executed. The actual applied BSD register source
has SHA256 `bd4afbcc3e965b319ebe95f9879cadcdde9a6834d154945a08d4187a0976716f`.
The captured configured source/header closure contains 225 files, archive SHA256
`e7b42760338d895fefd014c82b1b257ea527abf26945a1c201330fd600f679b8`.
Each native compiler passed all four whole translation-unit syntax checks:
original/candidate source, each with the actual kernel/dyld configuration.
Those checks use `-fsyntax-only`; linked objects and runtime success are not
inferred from them.

The independent input/source/ABI index is external
`out/migration/native65-source-ABI-evidence-v1.json`, SHA256
`5169d3500e679caa48136394c23b7ea6086c8a8a276df7750dbfb0ef736aff13`.
It records source-only v46, both ABI replays, the actual configured commands,
immutable source preparation and the prepared runtime controllers. The later
whole-unit receipts are `native65-workqueue-{debian,ubuntu}-units/result.json`.

These are bounded source/compiler/ABI results. The complete native Debian65
engine is still building. Its sole postbuild queue requires both whole-unit
receipts and independent full-artifact verification before installing and
running the five ordinary targeted scenarios, followed by the Darwin thread
client. Actual exported frames still need visual review. Ubuntu65 has not been
built, and both own QA systems still have64 installed at this checkpoint.
Original UGENE GUI acceptance and earlier Debian62/64 failures remain open.
