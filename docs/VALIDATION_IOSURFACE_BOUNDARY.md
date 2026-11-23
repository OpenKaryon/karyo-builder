# Installed IOSurface allocation boundary

## Source implementation prepared, installed graphics still pending

DE common0050 fixes the dispatcher that otherwise cached its first selector.
An ordinary create/lock/lookup/unlock/release sequence with two service objects
fails on the original body and passes on the changed body using both compilers.
The actual component compiles with Clang19 and Clang21 against the exact generated
header closure. Both native source-only50 stacks apply/reverse all patches with
Git and zero-fuzz quilt, restoring89 files. No shared/security unit suite ran.

DE common0051 adds real IOKit-owned CPU backing files, per-process mappings and
an explicit versioned response. It implements ordinary layout queries, public
sizes and IDs, create/lookup, references, usage counts and modification seeds.
Allocation no longer requires an EGL context. The original notices are retained.
All five changed units compile with both compilers using recorded input hashes.
That is not a linked or installed51 engine. Its source-only stack passes both
bases, applying/reversing51 patches and restoring97 files.

Apple's process usage query remains distinct from the global in-use boolean.
The service tracks every caller increment/decrement, while each framework handle
balances its own outstanding increments. Lock/unlock provide CPU visibility and
modification seeds, without claiming exclusive locking or GPU synchronization.
Shared attachments, planar storage, Mach-port transfer and GPU import remain
unimplemented. The private protocol needs a matching framework and service;
existing prefix upgrades require separate actual evidence.

The next source boundary is layer presentation: the current renderer assumes
CGImage contents and must explicitly consume IOSurface pixels. No installed51
pixel round trip, cross-process lifecycle or original UGENE GUI is accepted yet.
The installed48 failures below remain retained evidence rather than overwritten
by source-only or compiler results. Ubuntu49's original UGENE also exits0 without
a captured visible frame, and its ordinary dynamic layer client exits1.

## Observed on Debian and Ubuntu

The product-owned positive client in Karyo DE's
`integrations/macos/tests/iosurface` requests a 17 by 9 BGRA buffer through public
macOS APIs. Build it with `tests/acceptance/build-macos-probes.py --suite iosurface`
and an external Mac cross SDK. The default applications suite is unchanged.

The exact same Intel Mach-O ran as the ordinary QA user on both installed
48-patch Darling engines. Both returned exit 1 and this report:

```json
{"probe":"iosurface-buffer","passed":false,"stage":"layout","stride":0,"allocation":0}
```

The worker exited normally, without timeout or application cleanup. No framework
functions, classes or original application bytes were replaced. No security
suite was executed. The immutable cross-build manifest records source hashes,
Mach-O/archive hashes and SDK identity. Runtime receipts are retained separately
under `out/migration/public-iosurface48/{debian,ubuntu}.json`.

The client stops at this failed ordinary layout contract, before allocation.
It therefore proves neither success nor a particular failure inside the later
creation, locking or pixel access operations. Those are retained as subsequent
positive stages for a future actual implementation.

## Source evidence and limits

In root Darling revision `60ba801decee7a00782f74f6be4c8ffb013f79ff`,
`src/frameworks/IOSurface/src/stubs.m` returns zero for both alignment functions.
Apple documents that alignment must round up to a suitable value, with identity
for properties without alignment requirements. A zero stride for a nonempty
ordinary image is not a compatible implementation.

The pinned IOKit daemon is
`src/external/iokitd` revision `5549ac4cd2db923c256f016a1381b3bfb716730a`.
Its `src/IOSurface.mm` constructor validates dimensions and format, but its
storage allocation code is disabled. `src/IOSurfaceRoot.mm`'s `createSurface`
constructs an object without filling the expected response buffer. Lock,
unlock, lookup, release and use-count operations return `KERN_NOT_SUPPORTED`.
The framework's `IOSurfaceObjC.m` expects a populated response describing
mapped storage. Consequently, supplying nonzero alignment alone cannot establish
a correct buffer lifecycle, and must not be reported as graphical compatibility.

The ordinary dynamic Qt layer client with original UGENE Qt 5.15.10 frameworks
also exits 1 during `QLabel::show()` on Ubuntu48. Its diagnostic variant, using
unbuffered output and ordinary `STUB_VERBOSE`, last reports two alignment calls.
This locates a concrete missing contract but does not prove that it is the sole
cause of the exit. Original UGENE remains unaccepted; a window title without a
visible frame is insufficient.

## Next implementation boundary

A general implementation needs consistent allocation layout and sizes, actual
storage and mapping, populated creation responses, working lock/unlock and
release semantics, and then a pixel round trip through the public APIs. Layer
presentation must subsequently display those pixels. Cross-process sharing,
lookup and GPU interoperability need their own functional evidence; a local
buffer cannot be presented as a substitute. Preserve upstream notices and use
common patches, without application-name selection or fake success values.

Only after the unchanged original application produces a visible reviewed frame
and opens an ordinary FASTA document can its GUI workflow be accepted. The
successful original macOS MUSCLE alignment on both bases is a separate CLI result.

Primary contracts:

- [Apple IOSurfaceAlignProperty](https://developer.apple.com/documentation/iosurface/iosurfacealignproperty(_:_:))
- [Apple IOSurfaceGetPropertyAlignment](https://developer.apple.com/documentation/iosurface/iosurfacegetpropertyalignment(_:))
- [Qt Cocoa IOSurface graphics buffer](https://github.com/qt/qtbase/blob/5.15/src/plugins/platforms/cocoa/qiosurfacegraphicsbuffer.mm)

- [Apple process-local usage count](https://developer.apple.com/documentation/iosurface/iosurfacegetusecount(_:))
- [Apple CPU access boundaries and modification seed](https://developer.apple.com/documentation/iosurface/iosurfacelock(_:_:_:))
