# Libsystem guard seeding: native diagnosis and source controls

The actual first Debian runtime abort is now symbolicated offline using the
captured core and exact installed Mach-O modules. LLDB identifies
`libSystem_initializer -> __stack_chk_fail -> __abort` before vchroot main,
before launchd and before the requested Mac probe. The initializer's saved cookie
is zero; its global guard has been seeded while that same frame remains alive.
The immutable core and mapped runtime instructions prove the mismatch.

The pinned Libsystem initializer invokes `_libc_initializer`; the pinned Libc
source at5a38c8dabf9e76b39407c24bc13134e33e5594e6 invokes `__guard_setup(apple)`
during that initialization. The inherited stack-protector instrumentation tries
to compare values from before and after guard setup. This is not evidence of an
application buffer overflow or a program-specific compatibility requirement.

DE `cb4732931d9c578d8af6cff2fc2ad0a8a5aa59e2` adds patch0030 with no_stack_protector on only this constructor.
Other functions in its source file, ordinary guest functions and native ELF
bootstrap hardening retain their protection. The module is independently pinned
to Libsystem08df454b6eb0df9400aa4c39839a7efd6efd2c3c and only its init.c is added
to the reviewed patch footprint. No environment or application-name rule is added.

## Executed controls

- The original bootstrap attribute, compiled with global stack protection,
  fails before main when its callback seeds the guard.
- The attribute read from the actual patch lets that bootstrap return normally.
- The same corrected binary still detects a guard change in an ordinary protected
  function. Darwin LLVM IR confirms protection on that function and its omission
  only from the initializer.
- All31 native source/packaging cases pass in both SDKs. All30 patches apply and
  reverse through real Git and zero-fuzz quilt, restoring72 pristine source files.
  The44 Swift inputs and full pinned source closure remain unchanged.

The joined current source proof is
`out/migration/darling-current-inputs-accepted-v6/acceptance.json`; it is rehashed
alongside its native logs and current patch0030 before updating the local source
evidence alias. The core/analysis hash and executed boundaries are indexed by
`out/migration/darling-bootstrap-guard-evidence.json`. The core is local QA data;
it is not committed or distributed. Its two exact orphan QA init processes were
already stopped through captured pidfd identities and their prefix files retained.

This accepts the diagnosis and compiler/source correction. The corrected full
engine build, installed native bootstrap and real CLI/Cocoa/Qt acceptance remain
required on both bases. The ongoing Ubuntu build atfd69c79 has only29 patches;
its result must not be mislabeled as this new30-patch runtime. It independently
tests the earlier mixed-format LTO correction. No second full engine build runs
in parallel; the prepared30-patch bundle is queued for the next native build.
