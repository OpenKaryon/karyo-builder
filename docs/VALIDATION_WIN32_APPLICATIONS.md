# Real Windows applications on both native desktops

Official 7-Zip26.06 and Notepad++8.9.9.1 PE32/PE64 builds pass real operations
through the installed public Karyo launcher and shell on Debian13 and Ubuntu26.04.
Eight final application/base/architecture cases pass. This extends the own-PE
fixture milestones; it is not a claim of universal Windows application support.
No runtime, Wine prefix policy, application-specific rule or compositor patch
was needed. Only DE QA and Builder acceptance/reporting change in this checkpoint.
No Git push/fetch, distro/ISO, Forge, user VM or Acer changes were made.

## Exact optional QA inputs

Publisher releases: [7-Zip26.06](https://github.com/ip7z/7zip/releases/tag/26.06),
[Notepad++8.9.9.1](https://github.com/notepad-plus-plus/notepad-plus-plus/releases/tag/v8.9.9.1).
The fixed manifest includes exact size, GitHub asset ID, URL and SHA256 digest.
The Notepad++ digests also match the release-body checksums. Upstream license
links are preserved; complete upstream distributions/notices stay with ignored
QA files, rather than being incorporated into DE source or packages.

| Input | Version | SHA256 |
| --- | --- | --- |
| 7zip-64 | 26.06 | 9b697f65ecc2d9b0152f5ee96d72dde522a7827690349d9307935dacf40f42ec |
| 7zip-32 | 26.06 | 5e38f80c3752de43887e7a99ad10668c14bf64dcc929a636510b54616ea7dec7 |
| notepadpp-64 | 8.9.9.1 | cbcefa34677e10fe6dd19802f7d6b3b9860cd6de62afeaae7680e09c51b47779 |
| notepadpp-32 | 8.9.9.1 | 7b48fceec762e80c2bc781a59739403f7af8b6136ed0ffc369a2680c535ab78a |

The standalone fetcher passes both fresh downloads and existing-byte verification.
It refuses inconsistent existing inputs rather than overwriting them. No binary
is executed on Windows, added to a native package, or baked into the runtime image.

## Final actual cases

- 7-Zip installers run as the ordinary QA account in private prefixes. Their real
  CLI creates a Unicode-named 7z archive and extracts it; the resulting file bytes
  exactly match the original UTF-8 text. The installed real File Manager opens it.
- Notepad++ portable distributions open a Unicode-named document. Actual Win32
  Unicode input replaces its text and Ctrl+S saves exact expected UTF-8 bytes.
  The 32/64-bit saved-file hashes agree between the two native bases.
- Each of the eight actual windows receives six pointer visits over three menu
  headings. Three distinct popup positions are required, and each transition
  waits for a changed position. All 48 final popup observations are actual
  POPUP_MENU windows with input=false. A repeated observation of one unchanged
  popup cannot pass the gate.
- Every main window minimizes without application death, restores as the same
  window, opens a genuine owned Options/Open dialog through normal accelerators,
  dismisses it with Escape, and exits normally with status0.
- Both actual foreign-toplevel protocols report the expected registered Karyo
  desktop ID in every case. Real PE icon extraction succeeds, the source PNG
  hashes/sizes are retained, and representative caption/taskbar/menu/dialog and
  saved-document screenshots were visually inspected. This is not a per-pixel
  reference comparison of arbitrary third-party icon artwork.
- Executable PE machine headers and hashes establish actual PE32 and PE64 use.
  Original input hashes, all captured actor sources, final screenshots and native
  receipt hashes were rechecked. Builder's 50-case host suite completes with two
  native-only skips on Windows.

## Test corrections retained as evidence

The first observer assumed cross-process menu introspection could retrieve item
rectangles. Native Wine10 win32u/menu.c grab_menu_ptr rejects OBJ_OTHER_PROCESS;
get_menu_item_count returns-1. The checked original Debian source archive has
SHA256e87ff2971c9b2e79fc63341f044d7513e66f3c3782b49609746428caa87c6ee6.
The final actor therefore measures actual rendered menu words and uses the
private Wayland pointer. This is a test-observation correction, not a product
Wine patch or a skipped menu test.

The second observer incorrectly activated the owner before sending Escape,
stealing focus from the dialog. The generic QA helper now preserves an active
window of the same application and otherwise uses its last active popup. v3
passed the functional cases; v4 additionally passed both actual foreign IDs.
Visual/data review then caught a weak word grouping that split File and visited
only two headings in Notepad++. Final v5 increases the glyph grouping gap and
requires three distinct popup positions plus changed geometry on each transition.
v1/v2 failures and v3/v4 weaker receipts remain retained; only v5 closes this gate.

No external application code injection, product rule, registry theme override or
private program configuration is used. The own helper only observes standard
window/owner properties and sends ordinary Win32 input/close requests.

## Runtime and reproduction

The runtime is reused unchanged from the actual-shell icon checkpoint:

- Debian sha256:4d90035c84371fdf164f8418dc2b3a56810564cccd633241453709ef978683bb.
- Ubuntu sha256:18b0614bd47b85a12601c69e6fde711f7752f09409b136cdd4b4c771c5ad5f4e.

Exact native compositor/library/Wine4/Win32/shell packages are recorded in
VALIDATION_SHELL_ICONS.md and the inherited runtime receipts. No unchanged native
source or runtime is rebuilt just to run external applications.

    python ../karyo-de/integrations/win32/tests/fetch-third-party-inputs.py \
      --output <pinned-qa-inputs>
    python tests/acceptance/check-win32-applications.py --source ../karyo-de \
      --runtime-acceptance <accepted-shell-icons-runtime> \
      --inputs <pinned-qa-inputs> --output <new-output-directory>

The driver verifies/copies inputs, freezes actor/harness/inspector/observer/XML,
checks a captured Linux amd64 actual-shell image, and uses UID1001, fresh homes,
private display/bus, network none, read-only root/source and no capabilities with
no-new-privileges. Apps execute only in that disposable environment. Each public
launcher log and bounded engine diagnostics are retained on failure.

Ignored out/migration records: real-win32-applications-<base>-v5 contains final
receipts, exact inputs, actor copies and screenshots; real-win32-applications-
evidence.json joins the eight verified cases and runtime identities. The initial
review metadata and fetch-contract outputs preserve official source hashes.
real-win32-builder-tests.log records the host suite.

## Remaining scope

These releases and operations do not establish all Windows programs, external
network/updater behavior, physical GPU/fractional DPI, arbitrary legacy-prefix
import/conversion, or existing-user upgrade. Darling runtime, remaining enabled
VMware host channels/DnD/HGFS/resize/multioutput, VPN lifecycle and the final joined
installed DE remain active. The old platform-theme/portal pending label is reconciled: donor and target use
QStylePlugin, while session-owned provider configuration selects external GTK/wlr
portals. Native session recipes and prior real VM FileChooser/ScreenCast evidence
are linked by the inventory; this does not replace final joined-HEAD deployment.
