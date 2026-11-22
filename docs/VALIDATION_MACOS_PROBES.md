# Real Mac application probe compilation

The existing installed macOS core/picker tests use an explicitly identified
Linux engine fixture. Those tests do not prove Darling compatibility. Product
probe sources now live in DE's integrations/macos/tests/probes: an Intel64 Mach-O
libSystem CLI, a Cocoa application bundle and a static Qt Widgets bundle.

The CLI checks startup, UTF-8 temporary file I/O and literal argv and supports
--exit17 for real exit-status acceptance. Cocoa checks an ordinary window,
UTF-8 text, button target/action and a bounded event loop. Qt checks its visible
window, timer, button signal, UTF-8 text and raster output. These tests are not
installed desktop applications or additions to distribution images.

## Independent build

Use a separately prepared local Linux amd64 cross SDK with o64-clang and static
Qt5 qmake; the driver does not alter that SDK, Forge or its source repositories.

```sh
python tests/acceptance/build-macos-probes.py --de-source ../karyo-de \
  --image LOCAL_STATIC_QT_MACOS_SDK --output out/macos-probes
```

The driver resolves the immutable image ID, runs as UID65534 without network,
capabilities or privilege escalation, keeps the SDK/root/input read-only and
limits CPU/memory/processes plus writable temporary storage. It creates a new
output folder, retains inputs/build logs even on failure and removes only its
own named container on timeout. No host credentials or Docker socket are
mounted. Native tar creation preserves bundle links/executable modes without
extracting a Unix tree onto Windows.

The post-build archive gate verifies all three actual MH_EXECUTE/x86_64 Mach-O
headers, member hashes, paths, modes and contained bundle links. Regression
controls reject Linux ELF, arm64, dylibs masquerading as executables, duplicate
members, escaping paths/links and privileged/writable payloads. The complete
Builder suite passes69 cases on each native base; Windows passes69 with its two
existing native-only skips. No new host/guest runtime acceptance is inferred.

## Recorded compilation

- DE source: 793695dcdcec36fc2417c02527b549da8a9c4cee (probe inputs clean).
- Cross SDK: sha256:4bfaf1eb25e15355258071ca76f0ba5d86779677746783598eb8077d680cc7b6.
- Probe archive SHA256: f40f309cfdcb1532419bde01c96d81795672fc1e0c606d0befe3f35c44086e01.
- Driver, every source and output/log member hashes are in manifest.json.
- Local final build: out/macos-probes/macos-probes-20261122T221038Z-f37ffa43
  under the task artifact directory on C, rather than the Builder checkout.

The initial build retained its macdeployqt Exec format error: that executable
itself targets macOS in this static SDK. Static Qt linkage requires no runtime
framework deployment. The corrected build checks the static Core archive and
links all three probes successfully; receipt runtime_tested remains false.

## Required next runtime gate

Complete and audit each base's native Darling engine package, install it in
the separate Debian/Ubuntu kernel QA guest, and invoke these exact artifacts
through installed /usr/bin/karyo-macos as an ordinary desktop user. Check real
CLI argv and exit17 propagation, per-account/display prefix behavior and
data persistence, inherited no-new-privileges refusal, and Cocoa/Qt reports
plus visible-window evidence. Compilation and fixture-only wrapper acceptance
do not substitute for these kernel/bootstrap/application checks.
