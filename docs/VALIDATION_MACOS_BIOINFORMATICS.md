# Original macOS bioinformatics programs on native Darling

The original Intel macOS MUSCLE 5.3 executable now performs a real sequence
alignment on both native Debian 13 and Ubuntu 26.04 with the installed48
Darling runtime, following the earlier45 baseline. Version reporting and alignment return 0 without a timeout or
forced application cleanup. The accepted cases cover both one requested
thread and the upstream default, which reports two threads on these QA VMs.
UGENE's graphical interface remains a separate, unaccepted target.

## Verified application and its ordinary dependencies

The [official release asset](https://github.com/rcedgar/muscle/releases/tag/v5.3)
muscle-osx-x86.v5.3 is an unmodified Intel x86_64 Mach-O executable, 1859392 bytes,
observed SHA256
0cfd18b7f7a95b5101ba8e86b4c50fce654247fce26deb6522eb4bb03744d70e.
This is the hash of the downloaded official HTTPS asset, not an independently
published upstream checksum. The executable reports `muscle 5.3.osx64 [d9725ac]`,
built November 10, 2024. It is not a Linux build or a local recompilation.

Its load commands require the Mac GNU GCC 11 runtime under
/usr/local/opt/gcc@11/lib/gcc/11. The initial attempts on both systems fail
before application initialization because that dependency is absent. Three
unchanged libraries were obtained from the official Intel Monterey Homebrew
GCC 11.5.0 bottle, whose published SHA256 is
af5d635ec43e4fc786abafe5f963ea26ac147ac10880d3ab4e2eea49948051cc.
The 145004389-byte bottle matches that digest. Its
[official formula metadata](https://formulae.brew.sh/api/formula/gcc@11.json)
records GPL-3.0-or-later WITH GCC-exception-3.1. COPYING, COPYING.LIB and
COPYING.RUNTIME accompany the three libraries in each own QA prefix.

| Library | SHA256 of unchanged bottle member |
| --- | --- |
| libgcc_s.1.1.dylib |75cc9a8de085839cb451d2af97c132e4fa908a5c1774bbcbde28ab640e42dca9|
| libgomp.1.dylib |0921107193013bd49cee5034110e8a95d26e109996e180d18919e426c960b350|
| libstdc++.6.dylib |a8b6be2f8440e1ebeb5efa9717911e7224cb91ab66ab77f64af54c716b00e9b5|

No application or library bytes, dependency load commands or application
settings are rewritten. The libraries are installed only in the application's
own QA Mac prefix; the shared Linux runtime and other prefixes are unchanged.
Neither MUSCLE nor this GNU runtime is added to a Karyo product package.

## Actual calculation and result checks

The [upstream align command](https://drive5.com/muscle5/manual/cmd_align.html)
reads FASTA sequences and writes aligned FASTA. Three synthetic nucleotide
sequences of lengths 21, 20 and 20 exercise an insertion/deletion case:

```text
>one
GATTACAGATTACAGATTACA
>two
GATTACAGATACAGATTACA
>three
GATTACAGATTACAGATACA
```

The actual unmodified application is launched through karyo-macos, first with
`-align input.fa -output aligned.fa -threads 1`, then without the threads
override. Both cases on both systems preserve all input identifiers and every
original nucleotide when gaps are removed. All rows have equal width 21 and
include gaps. The four actual output files are byte-identical:

```text
>two
GATTACAGATA-CAGATTACA
>one
GATTACAGATTACAGATTACA
>three
GATTACAGATTACAG-ATACA
```

The input SHA256 is
6446a6539a2f6ccfaa12377e55fb09ac1acb3b873d9960996e6adf735c6b5408.
The output SHA256 is
8ba71ff96a428a5db26f92776020c939c1c67c827fd1f8d123a3b7d9325fe657.
These checks establish execution, file I/O, residue preservation and the
observed default-thread scenario. They do not certify scientific optimality,
large datasets, all MUSCLE commands or arbitrary Mac application compatibility.

Receipts are out/migration/muscle-macos53/base-deps-v3.json and
base-default-v4.json. Each records actual runtime provenance, full commands,
exit statuses, output data and hashes. All successful root cleanup records are
null. Earlier missing-dependency attempts remain in base-v1.json.

The installed48 regression is retained separately in base-installed48-v5.json.
Each test normally restarts only its own existing MUSCLE prefix before running
with the new shared engine, so an old resident server cannot supply the result.
Ubuntu server 16937 becomes 20845; Debian 22076 becomes 23651. Both default-thread
calculations return 0, require no cleanup, and produce the same output SHA256.

The second attempt, base-deps-v2.json, retains a QA installation error: files
were copied into the physical overlay upper directory while its own Darling
server still had the earlier filesystem view mounted. Linux saw the files,
but Mac ls did not. A normal shutdown/start of that exact own prefix refreshes
the view and enables the accepted calculation. Debian server 21847 becomes 22076;
Ubuntu server 16222 becomes 16937. This does not restart other application
prefixes or delete any files. Future dependency provisioning should operate
through the guest filesystem or stop its own prefix before host-side edits.

## Remaining graphical application work

The [original UGENE53.1 Qt diagnosis](VALIDATION_COMMON_COCOA48.md) still applies.
A further ordinary-file diagnostic and temporary SIGABRT report confirm a
lazy bind failure for CGColorSpaceCopyPropertyList in the CoreGraphics
framework. A function in a separate helper does not satisfy that two-level
framework bind, so the earlier helper experiment is not an installed fix.

DE 05c6f67 adds the nullable query to the actual framework. It reports no
representation because the current backend retains no encoded color profile,
rather than inventing calibrated metadata. The complete 49-patch input passes
Git and zero-fuzz quilt application/reversal on both SDKs, restoring 88 pristine
files. That is source acceptance only. Its installed execution, IOSurface
rendering, UGENE window and FASTA workflow remain open. Ordinary48 native
build/application checks are still collected independently of this later patch.

All changes remain local. Shared policy/security suites are not executed.
