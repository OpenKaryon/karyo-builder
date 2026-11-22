# Native Qt macOS picker and MIME integration

The optional Qt6/C++17 karyo-macos frontend now passes native Debian13 and
Ubuntu26.04 package, real Wayland window and MIME/GIO acceptance. It consumes the
separate karyo-macos-core backend and the shared Karyo window/style/widgets.
Actual Darling and macOS application compatibility remain unproven by this
milestone: the running engine boundary is explicitly a Linux test fixture.

## Sources, builds and installed payload

Regular HEAD-based core0.1.0-2 and frontend0.1.0-2 packages use committed DE
bfe8f85f263f7b5d0f22116f86429cff3a3f0fe1, source archive
7628c72b2c15aa8018e72adc5e1b192eaec7d61d6e5526f38bd9692364da80e4. Native examples/macos-core.json stays
a Python-only component; examples/macos.json builds the separate GUI component
with its declared core, Wayland/SVG/icon/MIME dependencies.

| Base | Core DEB SHA256 | Frontend DEB SHA256 |
| --- | --- | --- |
| debian | c017272e00a0e55b773c7346ce6cee803e1b075fe91e2a04d624fe4951f2d8d2 | 0a00de4ee25a6c32f9789be9915e70661e035d89019c5ebf3af84044975c7543 |
| ubuntu | e241196fbd57fd98e7dba24f6496e0374fd0e57dde6f95dff1fde40d59b7617e | 7f525a20f2e199bac3fff835fe1a8846d0d0fd93243641941bdfa0a2aca69cdf |

Installed accepted image IDs:

- Debian: sha256:4d0fdcf5f60435d4cc2907c49adcb6de95c58d770d37ef95142e48f40434c5a8.
- Ubuntu: sha256:2c7616cd4e631c9b1b7b92c24bbe4a1309f20a1f3f9810dbc0ea17807fa78748.

Both complete regular GUI package builds pass 74/74 CTest entries; each separate
core build passes its policy entry. The ordinary-UID backend suite passes 35/35
on both bases. The Qt lifecycle suite reports 17 passes including init/cleanup,
covering relative leading-dash paths, UI responsiveness, missing-runtime refresh, malformed/oversized/timed-out
metadata, startup/inspection failures, live close guard, literal arguments,
transient-state notice, selected-file autostart, inline exit23 diagnostics,
chunked UTF-8, bounded output without line breaks and close during preflight.

The 29 Russian messages are compiled into the frontend. Root-run UI fixtures
are synthetic helpers, not a supported root application-launch mode. Actual
installed frontend runs below are ordinary UID 1001 on a private Wayland display.
The original own-code icon and embedded Lucide notices are installed separately;
no Darling, Apple SDK/binary, application or private profile is in these packages.

## Real coinstallation and retained data

The driver verifies native identity, source/archive, DEB size/digest and every
actor/helper before installing. Real dpkg upgrades an existing core0.1.0-1 to2
and installs the frontend; apt-get check and silent dpkg -V for both pass.
A synthetic ordinary-user existing-data file retains bytes, mode, uid and exact
mtime. This is package/user-data preservation, not an old Darling-prefix format
conversion or actual engine-upgrade result.

The parent also contains the existing Wine integration. Its
/usr/share/applications/karyo-mimeapps.list keeps the same digest and package
owner, and the system folder default is unchanged. The frontend registers its
custom Mach-O handler through XML and a desktop entry; it does not own or replace
that Win32 defaults file. No directory MIME type is captured. Desktop-file
validation now succeeds without diagnostics; the frontend has one primary
Utility category and uses the existing file-text glyph in its chooser.

## Installed core without a frontend

The a6054f4 core2-only checkpoint passes 12 public-entry checks on both bases, including
actionable --gui and no-argument errors when the optional frontend is absent.
Existing credential, isolated-Python, argument, capability, log and data/inode
checks remain. See the earlier [core report](VALIDATION_MACOS_CORE.md) for the
original0.1.0-1 checkpoint and its clearly identified Linux fixtures. The core
Python modules, configured entry and CMake install boundary are byte-identical
between a6054f4 and the final bfe8f85 package source; the latter also passes its
regular policy build and all real GUI/core calls below. Older CLI receipt
provenance is retained rather than relabeled as a new headless package result.

## Actual Wayland frontend and MIME lifecycle

The existing headless-labwc harness creates a new ordinary-user private bus,
Wayland display, runtime/config/data directories and home. Root/source are
read-only, network is disabled, all capabilities are dropped and NoNewPrivs is
set. It runs the actual installed regular Karyo shell together with the new
frontend; compositor and shell versions retain their earlier captured runtime
provenance, rather than being rebuilt or relabeled here.

Both --gui and no-argument public core commands open the configured native Qt
frontend without an engine. The visible Russian missing-engine notice, title,
body, controls and panel icon are captured. Both foreign protocols observe app
ID karyo-macos and title Приложения macOS. Standard close requests terminate these
idle controllers with status 0 and create no prefix state.

GIO recognizes a real synthetic Intel-header file with a Unicode/literal-$()
filename as application/x-karyo-mach-o. The registered default query resolves
to karyo-macos.desktop. A private user override resolves to another desktop ID
and retains its exact bytes; removing only that QA override restores the normal
candidate. GIO open then launches the real native frontend for the selected file.

For the running-state boundary, an explicit ordinary-user Linux engine fixture
in a private PATH records the real core arguments and credentials. It proves
literal /Volumes/SystemRoot application path forwarding, all four application
UIDs 1001, cleared capabilities and unchanged NoNewPrivs 1. The real backend writes
its scoped metadata/logs and leaves engine-leaf creation to the engine. This
fixture deliberately does not run the graphical shell script as macOS code.

The installed public GUI path also starts from a real relative Unicode filename
beginning with a dash. Its application arguments begin with a literal -- and
include -platform/-style with deliberately invalid Qt values, quotes and an
embedded newline. The native controller remains on the requested Wayland platform;
the actual core forwards every value unchanged to the fixture, including the
mapped absolute Darwin path. The standard argument terminator keeps the relative
filename positional during both inspection and execution.

A standard foreign-toplevel close request reaches the native Qt window while
that fixture is live. The same frontend PID, mapped window and engine survive;
the visible close-first notice is captured. Only the fixture's own stop file
ends it. The actual core records exit 0, the controller remains visible with its
finished state, and a subsequent normal close removes it. GIO launches are
asynchronous, so detached frontend disappearance is observed rather than
inventing an unavailable child exit status. Representative screenshots from both
bases were inspected: translated layout is legible and the original app icon
appears in the real taskbar. No physical mouse click or real macOS execution is
claimed from the standard Wayland close request and synthetic engine.

## Reproduction, failures and limits

Run tests/acceptance/check-macos-picker.py with --source <DE checkout>,
--runtime-acceptance <accepted old-core native image receipt>, --core-package
<regular core2 output>, --picker-package <regular frontend2 output> and a fresh
--output folder. Parent images must contain the existing core1 and Wine fixture
so upgrade/coinstallation assertions cannot silently become fresh installs.
All source, native artifact, actor, driver, install-proof and receipt hashes are
captured. Final outputs are out/migration/macos-picker-installed-<base>-v2;
joined evidence is out/migration/macos-picker-evidence.json. The new core-only
receipts are macos-core-gui-dispatch-<base>-v1. Builder's50 host tests pass with
its two pre-existing native-only skips on Windows.

Targeted GUI v1 caught a QA wait before the constructor's deferred status query
had started. The final test waits for the actual response and adds an explicit
8-second timeout case; v2 passes both native suites. Before package capture,
review also found the proposed shared defaults-file collision with Win32; the
final source uses handler registration and the actual coinstallation assertions
prove that owner/content stay unchanged. A stronger installed before-control then exposed a real argument bug: both
old frontend packages aborted while trying to load the application's deliberately
invalid Qt platform option. QApplication had consumed the application's options;
a second parser step could also discard its leading --. The final controller
gives QApplication only its own program name, parses the captured original values
once and protects positional filenames at the backend boundary. The new five-stage
installed after-gate passes on both native bases, including leading-dash filenames
and literal separator/Qt-like arguments. Before failures remain under
macos-picker-arguments-before-<base>-v1 with no accepted receipt. The complete
74-entry native suites were rerun for both final packages. No engine workaround,
app-specific rule, disabled sandbox or personal profile was needed.

Darling's pinned native stock build,21 source patches, Swift/licenses, native
bridges/dlopen dependencies, engine privilege bootstrap and actual CLI/Cocoa/Qt
programs on both bases remain the next integration. Existing Darling-prefix
compatibility and engine upgrades require their own evidence. Full real file
manager interaction and a joined current-HEAD installed desktop retain their
broader acceptance gate. VMware/VPN lifecycle and physical-device limitations
also remain part of the wider active migration.
