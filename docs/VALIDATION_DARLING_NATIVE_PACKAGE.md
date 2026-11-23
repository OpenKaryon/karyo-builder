# First native Darling package and mixed-format build flags

The full Debian13 engine build now passes all26426 stock targets, including dyld,
staged installation, standard stripping/debug separation, the native dependency
and hardening audit, and binary packaging. The audit accepts4 native ELF files
and21 native dynamic bridges. The fixed pinned source,44 recovered Swift inputs
and29 zero-fuzz patches retain the existing
[source-input proof](VALIDATION_DARLING_INPUTS.md) and current compiler controls.

The successful native output is
`karyo-source-package-20261123T002908Z-dd9bd194`. Its main runtime package is
87807156 bytes, SHA256
`9f8ecae7bf4efcf2e7a20898d365dd822851451f6013df34fbe844dd7530a3b2`.
The separate debug-symbol package is3716640 bytes, SHA256
`0334f90c689167dadaa65f9401b2c1bd071662523edb7bf1484e477f2fa68acf`.
All four manifest artifacts, including buildinfo and changes, are rehashed.
This build uses the DWARF5 packaging fix at DEd74641e, before the later LTO fix.

## Real installation and honest runtime boundary

The runtime is actually installed on the native Debian QA guest, with its
audited root-owned4755 ELF bootstrap. Existing package versions, account/PAM/
display-manager configuration and original Home are preserved. Only the runtime,
libgif7, mesa-vulkan-drivers and xdg-user-dirs are added. Installed provenance
confirms the4-ELF/21-bridge audit; dpkg verification is clean.

The actual ordinary graphical UID1001/caps0/NoNewPrivs0 actor passes installed
launcher status and input inspection, then aborts during bootstrap in about0.2s
before the Mach-O probe reaches main. It reports runtime_attempted=true,
runtime_tested=false, passed=false and complete=false. Cocoa, Qt, prefix/upgrade,
multiple-account and displayed-window acceptance have not passed. A root-only
trace and preserved core are diagnostic artifacts, not runtime acceptance.
Only two exact captured orphan QA init PIDs are stopped via pidfds after their
start, UID, argv and private namespace identities are checked. Prefix files and
the original Home remain untouched; no kernel security setting is changed.

## Ubuntu default LTO boundary

The first Ubuntu26.04 full build rejects dpkg's default -ffat-lto-objects flag
under Clang21's x86_64-apple-darwin20 target. DEfd69c79 selects
`hardening=+all optimize=-lto` in the actual package rules. Ordinary optimization,
compiler security checks, native link hardening and the staged audit remain.

All30 source/packaging cases pass on both SDKs. The new control runs the actual
rules through make and dpkg-buildflags, compiles a real Mach-O object and runnable
ELF, and reproduces Ubuntu's unmodified flags as a compiler negative control.
These tests are independent of the pending full Ubuntu rebuild and failed first
runtime. A fresh checksummed DSC fromfd69c79 retains the same source/patch inputs
and records the new rules SHA; it is rebuilding in the native Ubuntu SDK.

Exact native artifacts, installed receipt, failed runtime and current compiler
log hashes are indexed by `out/migration/darling-debian-native-package-evidence.json`.
This accepts a Debian engine package boundary, not Mac compatibility or a
completed engine on both bases. Joined current-HEAD DE acceptance remains open.
