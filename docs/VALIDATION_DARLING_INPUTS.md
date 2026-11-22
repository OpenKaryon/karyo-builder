# Current Darling source and native build status

The current reviewed series contains29 common patches. The joined gate
out/migration/darling-current-inputs-accepted-v4/acceptance.json passes on both
native SDKs:28 source/packaging cases, all44 verified Swift inputs, zero-fuzz
quilt plus Git application/reversal of29 patches and71 byte-identical restored
source files. Native tool versions are recorded independently; source effects
must agree. Log hashes were checked after both SDK jobs completed. Earlier
sections below preserve historical smaller gates and their original counts.

The ordinary Debian3.0(quilt) producer rechecks the current input/proof hashes
and emits per-base source-package recipes. Sequential full Debian builds found:

| Native attempt | Observed failure | General correction |
| --- | --- | --- |
|1|GNU quilt rejected incomplete context at fuzz0|Refresh only0001/0006 context; preserve exact source effect|
|2|ELF -z flags reached the Mach-O linker|0023 separates native flags and retains ELF hardening|
|3|objc4 debug metadata disagreed with Release NDEBUG|0024 matches standard build modes|
|4|Foundation used exception variables as format strings|0025 retains format-security with literal formats|
|5|Ruby self-included remapped __FILE__|0026 uses the adjacent header, retaining reproducible path maps|
|6|Screen forwarded an existing message as a format|0027 treats it as literal data; collect independent Ninja errors|
|7|Thirty additional Screen diagnostics and dyld's relative libunwind lookup table|0028 fixes every observed diagnostic;0029 confines no-jump-tables to static bootstrap unwind|

The seventh build reached26425/26426 Ninja steps and correctly failed. Both
native compiler suites reject all thirty original Screen calls and execute the
replacements with percent characters unchanged. A native CMake control proves
the unwind option remains confined to its target and preserves switch behavior;
Mach-O LLVM IR shows the default relative table and its absence with the option.
Optimized compilation, native hardening and dyld chained fixups stay enabled.
Exact extra module pins include libunwind alongside objc4/Foundation/Ruby/Screen.

The eighth complete Debian engine build is running with the29-patch DSC. No
completed engine package, staged ELF/bridge audit or real Mac execution has been
accepted. The complete Ubuntu engine build remains subsequent work. Source
preparation and isolated compiler controls do not establish successful dyld
linking or runtime compatibility.

Real Intel64 Mach-O CLI, Cocoa and static Qt Widgets probes compile from clean
DE sources in a separate immutable cross SDK; see
[VALIDATION_MACOS_PROBES.md](VALIDATION_MACOS_PROBES.md). Each base's native core
is installed in its separate kernel QA guest with verified probes staged under
the ordinary graphical account. Both absent-engine controls remain negative.
Positive SUID/namespace/bootstrap, actual CLI/Cocoa/Qt, prefix/upgrade/multiuser
and visible-window gates are still required. Account/PAM/DM/shell and unrelated
package snapshots survived core setup. The working Karyo VM, Acer, donor, Forge
and distribution checkouts remain untouched.

---

# Native Darling source preparation

This gate prepares the optional macOS runtime's reproducible inputs. It does
not compile/install Darling, execute a Mac application or establish its SUID,
namespace, display or prefix behavior. Those remain separate native gates.
The product source, policies, patches and notices live in Karyo DE's
integrations/macos/runtime; Builder owns generic source snapshots and SDK
orchestration. No distribution/Forge checkout or user installation is changed.

## Fixed input identity

- Darling:60ba801decee7a00782f74f6be4c8ffb013f79ff.
- Cocotron:c8d38d16a9f613d300157bebbab2b9501bc0c274.
- Swift:471514f4b4985a604b192e1facac9bbc53dedad3.
- Complete closure:161 repositories,292917 tracked files.
- Inventory source.tar.gz SHA256:
  9991624da4e72530f844e14aafae91e196505a3e98b65f047e9bafdd48379d09,
  bytes780871273, build_ready:false with44 unresolved Swift pointers.
- Materialized source.tar.gz SHA256:
  da3f1745d149802418fdb3878561dd8a36f4440a7f86775cf0e60c0b96735458,
  bytes785407024, build_ready:true with all44 objects verified.
- Official binary input archive SHA256:
  a4405582a17d3e6b50b6751dc0d5d741f8e23848b014d1ad20731b2efbe7a55f,
  bytes123429806. The exact public release URL is fixed in DE's preparer.
- Recovered Swift payload total:16128448 bytes. Original Swift license SHA256:
  770af8291f708538d8ff885a0bbc4e045cd700531741c4f99528d435c14d7f55.

The source recipe explicitly declares only two external symlinks: the root
Developer/usr/bin/git link and libxslt's original Automake INSTALL documentation
link. All other escaping links fail. Native checks stream source/DEB archives
as data without extracting the external links or installing the upstream DEB.
Exact patch hashes and upstream component notices are preserved.

## Native environments

| Native base | SDK immutable ID | GCC | Clang/LLVM | CMake |
| --- | --- | --- | --- | --- |
| Debian13 | c7938116757e87deeb0c2e079c9d92e9c4a6a558da5bd5c0f961233afd93c49c |14.2|19.1.7|3.31.6 |
| Ubuntu26.04 |5bd95b9a7e79268dfc36e6aa65090d5876a07ac820efcd196c410e4f28fc91c5 |15.2|21.1.8|4.2.3 |

Both SDKs use their own distribution's headers, compiler and libraries; neither
reuses the other base's Linux binaries. The acceptance driver resolves local
images once, then runs their immutable IDs as UID65534 with zero capabilities,
no-new-privileges, no network, a read-only root and read-only input mounts.
Only a bounded executable /tmp and the selected output mount are writable.
Executable /tmp is needed for a freshly compiled harmless native ELF check.
No Docker socket, host credentials or broad home directory is mounted.

The SDK probe checks26 pkg-config modules, records all installed package versions,
compiles and executes an amd64 Linux ELF, and compiles an Intel Mach-O object.
The latter is object emission, not linking or executing a Mac application.
The source-unit suite has13 cases per native base. Real recovery independently
verifies all44 Swift payloads against the snapshot's original pointer blobs;
provenance and payloads match between bases. The complete21-patch stack applies
in private selected-file shadows, reverses and restores all52 original files
exactly. The source archive remains unchanged; both patch reports match.

Standalone core CMake/CTest also passes both entries on the previously accepted
installed GUI images, covering35 backend and13 source-input cases. The frontend
unit fixture explicitly selects a missing picker, eliminating accidental GUI
launch depending on what is installed on the test host. The generic Builder
suite passes65 cases on both native bases; Windows has its two existing native
symlink skips. Core source-input Windows checks have one native DEB skip.

## Repeat the gate

```sh
docker build -t karyo-darling-source-builder:debian environments/darling-debian13
docker build -t karyo-darling-source-builder:ubuntu environments/darling-ubuntu2604
# Follow DE's runtime README to prepare INVENTORY, COMPLETE and OFFICIAL_DEB.
python tests/acceptance/check-darling-inputs.py \
  --inventory INVENTORY --complete COMPLETE --de-source ../karyo-de \
  --archive OFFICIAL_DEB --output out/darling-inputs-NEW \
  --debian-image karyo-darling-source-builder:debian \
  --ubuntu-image karyo-darling-source-builder:ubuntu
```

Only a successful joined run writes acceptance.json. It records immutable SDK
IDs, complete native package versions, script/input hashes, source manifests,
Swift/policy receipts and log hashes. Deliberate unit fixtures use small fake
archive constants internally; the public real-input path has no identity bypass.
The first joined attempt retained its noexec-/tmp failure without a success
receipt; the final driver explicitly enables execution only in bounded /tmp.

For the local review, the successful result is
out/migration/darling-inputs-accepted-v2/acceptance.json and its per-base SDK,
unit, Swift and patch logs. Earlier per-base Swift and patch checks are retained
separately; the joined result uses the complete source and final committed
policy bytes. A build-ready snapshot means source completeness only. Native
Debian source packaging, full engine compilation, ELF/bridge dependencies,
SUID/binfmt/license installation audits and real CLI/Cocoa/Qt application tests
remain pending. Build sequentially if physical Docker storage is limited;
this preparation did not prune other projects' images or caches.

## Source-version extension

DE's additional patch0022 supplies complete revision metadata for source
archives without Git administrative files. The native input driver reads the
reviewed series length instead of freezing the old21 count. A second joined
result, out/migration/darling-source-version-accepted-v1/acceptance.json, passes
14 input cases on each base and verifies22 forward/reverse patches restoring
53 source files. Source-version CMake tests execute the actual added block,
including malformed revision rejection. The original21 patch hashes and all
source/Swift input identities remain unchanged. This is still preparation,
not evidence of a compiled or working Darling runtime.

## Actual zero-fuzz quilt consumer

The first normal native source-package attempt stopped at patch0001, although
Git's shadow gate had passed. An isolated GNU patch2.8 control rejected the
original hunk at fuzz0 and accepted it only at fuzz1. Context-only regeneration
was needed in0001/0006; the complete resulting source bytes match the original
Git applications. Remaining patch bytes were preserved.

DE's verifier now executes both Git and actual quilt push/pop at fuzz0, compares
their complete patched bytes and checks pristine restoration. The joined
out/migration/darling-quilt-accepted-v2/acceptance.json succeeds for all22 patches
and53 selected files on both bases, including20 source/packaging cases per base.
The driver retains quilt0.68/0.69 separately and compares every source/result
field strictly. Its regression rejects changed source hashes, patch identities,
file results, missing tools and weakened fuzz proof. The full Builder suite now
has66 cases. The earlier joined-v1 correctly retained per-base successful
results but no overall acceptance when its overly strict comparison included
native tool-version differences.

The ordinary Debian source build then reached actual Clang/Ninja compilation
and failed at a Mach-O link because Linux -z relro reached ld64. That is a
separate real build issue, not an input-identity failure. DE's subsequent common
ELF/Mach-O linker-boundary patch has its own23-patch/55-file zero-fuzz native
receipts and21-case unit runs. The native source-package build is repeated with
that correction; compilation/install/runtime acceptance remains pending.
