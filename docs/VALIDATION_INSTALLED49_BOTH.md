# Both installed49 engines and the prepared CPU buffer boundary

Both complete 49-patch engines are built, installed and exercised in the separate
Debian13 and Ubuntu26.04 QA machines. All four build artifacts per base were
verified by size and SHA256. Development package versions are shared between
patch revisions, so explicit reinstallation and build provenance identify the
actual engine. The source input is DE05c6f67, not the later CPU-buffer source.

| Native base | Runtime bytes | Runtime SHA256 |
| --- | --- | --- |
| Debian13 |87791896|848a796242b11a0f92e6a1414387825e9996075e30d3fd6161120a492e7d9ac9|
| Ubuntu26.04 |92683534|0136fe8ddd99d7cf36aad7abbf409627957f69c59ea48bd300d02a742f072842|

The original loader, Cocoa and Qt clients pass on both. Real exported desktop
frames were viewed, including the UTF-8 titles and button contents. The Qt raster
remains identical between bases, SHA256
`d90cf2c330b6cb14b737a913f15a4e4430fe7607b7c79394ba77041b4d3347d6`.
The original dynamic UGENE Qt5.15.10 framework client also constructs QApplication
and QLabel successfully, without replacement framework methods.

## Actual documents and timing

Unchanged upstream TextEditor opens its ordinary document on both bases. Actual
keyboard input replaces its text, saves exactly45 bytes and requests normal
global Quit. Application and Quit helper exit0, without root cleanup. The saved
file remains SHA256
`05786532df55212187f436d1163809d540c98cd0ad30ea1881bfbcbd831bca74`.
The document-only observation is a separate bounded scenario with controlled
close; it must not be confused with the successful save-and-normal-Quit case.

| Viewed Debian49 frame | SHA256 |
| --- | --- |
| Cocoa |75724bd8ca0320811a659e9f743236fd7e1bcc3688f0d9eefd13b8c47809fbd7|
| Qt widgets |a4c0bdf51a152b6167bf61f77fd2c6d0a50a6d57fadf96af887094e3fadfd82a|
| TextEditor original document |cd9a0729c5621f15691ef3efacc0c7ca550364824dc1c2d5d7aa26966ed15831|
| TextEditor saved document |590ca4517ef4aa4c4b3688ad42ccbe89d2286b66c6378e210ca6fba0a6f9db96|

| Viewed Ubuntu49 frame | SHA256 |
| --- | --- |
| Cocoa |d449be583aa8de72b3552b592035c4cf10e34ce5d53348388762dfe7793c750c|
| Qt widgets |595518c4b4249558d11f737c06f2c3dd8529ec8e997d0fa340aa3f643c6df56f|
| TextEditor original document |d35a43f9515d71125b436a02b888f474d3b3b98c5818f688a4543e77585ce8bc|
| TextEditor saved document |aa358e8cd6695f31185614bbb6063dc136c7a3c7dca88dc5ddb8bae5ed09f8c9|

The original Cocoa waits return after about50ms: Debian
0.051370/0.050899/0.050837 seconds, Ubuntu0.050462/0.050302/0.051113.
CFRunLoop's window test requests return-after-source. Both bases return4 for two
ordinary early handled sources, followed by two timed-out returns3 around50ms.
The retained result codes and times validate that distinction; an upper time
bound alone would be weaker evidence. No executable guardian or API override runs.

All four stock utility operations pass, including a fresh uname prefix. This
does not explain or fix the original Debian45 cold uname exit136, which remains
retained. The original53-byte Mac data file is read after normal own-prefix
daemon restart on both49 engines, with unchanged prefix identity.

## Bioinformatics and remaining graphics

The original Intel macOS MUSCLE5.3 executable again performs real FASTA alignment
on both49 engines after its own normal prefix restart, using upstream default
two threads. Its official GNU dependencies remain inside its own Mac prefix.
The validated output is unchanged, SHA256
`8ba71ff96a428a5db26f92776020c939c1c67c827fd1f8d123a3b7d9325fe657`.

Original UGENE53.1 exits0 without a captured viewable window on both: about2.10s
on Debian and2.54s on Ubuntu. Neither is an accepted GUI or FASTA document
workflow. The ordinary dynamic layer client exits1 without a frame on both;
its successful QApplication construction is a different, narrower result.

The next common50/51 source fixes are described in the
[IOSurface boundary report](VALIDATION_IOSURFACE_BOUNDARY.md). Both source-only
stacks pass Git/quilt zero-fuzz apply/reverse, restoring89 and97 files. Five
actual CPU-buffer compilation units pass Clang19 and21. No installed51 engine,
pixel round trip, sharing lifecycle or layer presentation has been accepted.
The next renderer must consume IOSurface pixels instead of assuming CGImage.

Joined immutable artifact identities, ordinary reports and viewed frame hashes
are retained in `out/migration/darling-native49-both-common-cocoa-evidence-v2.json`.
All49 jobs have completed; no duplicate full build or application queue is needed.
Only ordinary functional/source checks ran. No shared/security suite, push,
Forge/distro/ISO/donor change or user VM/Acer action is involved.
