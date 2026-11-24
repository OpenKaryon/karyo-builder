# Darling 56: real hosted surfaces and remaining GUI failures

The complete 56-patch native Darling packages build and install on both
Debian 13 and Ubuntu 26.04. All four output artifacts per base are independently
checked against their recorded size and SHA256. Runtime provenance records
56 patches, four native ELF components and 21 native bridges. The immutable
runtime source is DE ff9d949, not the later session or graphics follow-ups.

## Accepted functional slice

The ordinary installed baseline passes on both systems. Cocoa and static Qt
windows show their actual UTF-8 text and buttons. An unchanged upstream macOS
TextEditor opens a document, accepts ordinary keyboard input and saves exactly
45 bytes, SHA256
`05786532df55212187f436d1163809d540c98cd0ad30ea1881bfbcbd831bca74`.
Actual desktop frames are exported, hashed and viewed on both bases.

The separate positive IOSurface clients pass dictionary matching, CPU buffer
layout and pixel preservation, and owner/reader/after-release lifecycle checks.
The hosted root layer retains its original surface through both redraw phases
and releases it after detachment. The float opacity ABI checks pass. Actual
captured center pixels are exactly [224,64,32] then [32,176,192], on both bases;
both frames on each base are exported, hashed and viewed. This accepts that
root-hosting slice, not every layer hierarchy or a complete application GUI.

## Failures retained as failures

The dynamic client linked to UGENE's unchanged Qt 5.15.10 frameworks returns
normally from its event loop on both systems, but its actual captured viewport
is blank light gray. The expected label is absent. Both frames are viewed;
a successful event-loop return is not a successful GUI.

The original Intel macOS UGENE 53.1 bundle is reused from its existing QA
location. Every one of its 12,185 regular file hashes is verified before each
launch, and the original FASTA fixture is unchanged. No archive is uploaded or
extracted again, and no app-specific library replacement is introduced.
Ubuntu exits with status 0 after 1.816 seconds without a captured UGENE window.
Debian produces no captured UGENE window and reaches the ordinary 90-second
timeout, after which the owned process is terminated. Neither is accepted as
UGENE GUI compatibility. The successful MUSCLE FASTA CLI scenario is separate.

A later read-only readiness check finds Debian's retained launch log still at
prefix setup, with an owned bootstrap bash rather than a captured ugeneui
process. Available guest memory is about110 MiB before retirement. The exact
obsolete bootstrap is subsequently matched by UID, executable, PID/start and
full arguments and terminated through its pidfd. Normal darling shutdown then
stops24 proven idle QA prefixes on each base, preserving prefix directories,
MUSCLE and the persistent-data fixture. Debian available memory rises to about
900 MiB. This motivates resource preparation; it does not establish the cause
of the original timeout or convert it into an application compatibility pass.
Ubuntu separately retires only three inert staged upload copies after their
host originals and exact guest SHA256/size are verified, reclaiming523,890,653
bytes. Extracted original applications, prefixes, results and data are retained.
Readiness logs are under the local native58-{debian,ubuntu}-readiness directories.

A separate positive retry after that preparation rechecks all12,185 original
regular hashes and starts the unchanged app with the unchanged FASTA on both
bases. The original ugeneui now creates a viewable600x320 window, captured at
10 and25 seconds on each system. All four actual frames are exported, hashed
and viewed: the content is black, with no document text or usable controls.
The ordinary45-second run deadline expires, and the exact owned mldr process
is captured and cleaned through its pidfd. Neither a successful wrapper exit
nor a viewable window is accepted as a usable UGENE GUI. The earlier90-second
Debian bootstrap timeout and Ubuntu early exit remain separate retained results.
The paired retry evidence is out/migration/ugene56-readiness-both-evidence-v1.json.

Two additional ordinary positive clients identify common graphics defects in
the installed 56 runtime. A grandchild surface is clipped while the same
surface renders when reparented at unchanged visible coordinates; a later
opaque sibling still overlays it. Another client records that implicit backing
creation bypasses the public setLayer override and pending CALayer display
callbacks do not run. Its expected image remains blank. These observations
motivate common patches 57 and 58; their source application/reversal and native
compiler checks pass on both bases. Those checks alone do not accept a changed
runtime. The immutable 58-patch full build and installed positive checks are a
separate pending slice. No source edit is tailored to UGENE or Qt names.

## Evidence and scope

The local hashed evidence index is
out/migration/native56-both-accepted-slice-evidence-v1.json. It records each full
manifest, baseline, public surface/lifecycle result, regression report, original
UGENE result and reviewed frame. Earlier installer key-path typos and the
initial layer-client fixture failure remain distinct diagnostic records.
No security/shared unit suite ran, no policy was weakened, no user VM or Acer
was used, and nothing was pushed. The full DE migration and UGENE GUI remain
open work.
