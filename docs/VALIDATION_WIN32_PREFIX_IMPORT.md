# Native offline prefix import and package upgrade

The public launcher from DE945ac8c68107236a0e97740d45edd2ca213a7d56 now passes
actual existing-user package upgrade and explicit prototype-prefix import on
Debian13 and Ubuntu26.04. This is an optional ordinary-account integration; it
does not install Wine, alter user profiles automatically or create an ISO.

## Package and runtime inputs

The regular examples/win32.json recipe builds version0.1.0-2 independently on
both native bases from committed HEAD945ac8c. Both manifest source archives are
4c9f15ef164689f3498a36d3a69100fda8d785d0802d5cb5bae135c178092ba3.

| Base | Native DEB SHA256 | Accepted installed image |
| --- | --- | --- |
| Debian13 | 8d29316199274102367db052f2a8e64ea023d41e603a2dff3210d1006c31392c | dd3af7970e144c57fdd1bd1196744b6426dc3dc7b41049a7339203e6175bd376 |
| Ubuntu26.04 | 63b22b8c1c70aa57e867d06e021258ea3375232d1f4ea5d5db3a1c685b33c74d | 6b47210b21e206555dd7d6e3ec68184dd5d26010fbd5ea113bc58ada82a0d4d4 |

The image IDs have the sha256: prefix in machine receipts. Their parents are
the accepted real-application/actual-shell images from
[VALIDATION_WIN32_APPLICATIONS.md](VALIDATION_WIN32_APPLICATIONS.md); Wine, native
labwc/wlroots and the actual shell were unchanged for this slice. Windows input
is the checksum-locked optional official 7-Zip26.06 x64 installer from the
existing third-party manifest, never a product payload.

## Real upgrade before application testing

In each disposable image, the old installed launcher0.1.0-1 first creates a real
profile, menu record and synthetic Unicode user file. The Windows probe runs as
UID1001 with no capabilities and NoNewPrivs, not as the package-installing root
process. After Wine exits, QA snapshots every file hash, mode, nanosecond mtime,
uid/gid and symlink target. A real dpkg upgrade to0.1.0-2 preserves that complete
user tree exactly; apt-get check and silent dpkg -V also pass.

A trusted QA-only PAX archive restores those pre-existing bytes/metadata into
the fresh runtime home. The restored tree is compared again before a registered
public launch. A fresh engine log must contain the actual Windows probe PASS
and NoNewPrivs1; retaining a marker without executing the probe cannot pass.

## Real legacy prefix, copy and GUI

The frozen own-code prototype launcher26bad17 creates a real win64 session-2
prefix and installs 7-Zip as the ordinary account. The full unchanged body and
provenance are in DE tests/fixtures; no private donor checkout is needed. QA
waits for Wine's final registry flush, then starts the installed old application.
Import while that GUI is active must fail with the actionable close-applications
message, leave the GUI alive and create no destination.

After normal close and server exit, the public inspect/import commands copy the
offline source into a new flat application profile. All1866 regular file hashes
match; source contents, metadata, owners and links remain unchanged. Preview
creates no destination. Inherited profile selection ignores spoofed HOME and
old session-slot variables. The copied real EXE opens with the actual shell,
then opens again through --registered; both foreign protocols expose
karyo-win32-legacy-copy and both windows close normally with status0.
Representative caption/taskbar screenshots were inspected on both bases.

New edits in the imported profile survive a refused repeat import. The original
source still equals its stopped snapshot and there are no unpublished staging
directories. Native ordinary-UID policy/import regressions pass33/33 on each
base, including source changes, competing publication, external links, multiple
Windows users and unknown/bad registry architecture. Builder's50 host cases pass
with the two pre-existing native-only skips on Windows.

## Reproduction and evidence

Run tests/acceptance/check-win32-prefix-import.py with --source <DE checkout>,
--runtime-acceptance <accepted actual-shell receipt folder>,
--launcher-package <regular0.1.0-2 package folder>, --inputs <verified QA inputs>
and a fresh --output folder. It records all actor/driver/install-helper hashes,
package source/native identity, before/after upgrade proof and runtime receipts.

An optional --prepared-upgrade <accepted previous output> reuses only the exact
immutable package layer when parent, native package provenance, install-helper
hash and in-image upgrade proof match. All user-state restoration and actual
application checks still rerun in a fresh ordinary-user home, private display
and bus, with network disabled, read-only root/source, dropped capabilities and
NoNewPrivs. It does not relabel older application results.

Final local outputs are out/migration/prefix-import-installed-<base>-v4; v3
contains the original successful package build/upgrade layers. Their hashes are
joined in out/migration/prefix-import-evidence.json. Both v3 and final v4 pass
four application stages on each base.

Retained failures are preparation/QA corrections: v1 USTAR rounded mtimes to
seconds, fixed by PAX without weakening comparison; v2 attempted the busy-source
case before the old installer/server flushed system.reg. Minimal Ubuntu excludes
documentation globally, and dpkg -V can report missing files with status0, so
the QA installer explicitly includes this package's documentation and requires
empty verification diagnostics. v3 passes; v4 additionally requires a fresh
actual post-upgrade probe PASS and verifies reuse of that same immutable layer.

## Limits

Import is an explicit offline copy, never an automatic migration or a global
filesystem snapshot. External mapped data is not copied implicitly. Cross-account
Windows-user aliases have policy-test coverage, not a real renamed-account GUI
claim in this matrix. The source registry architecture stays unchanged: pure
win32-to-WoW64 conversion and arbitrary older engine compatibility are not
implemented or established by this win64 prototype fixture. The prior Debian
pure-win32 and Ubuntu WoW64 PE32 reuse evidence retains its own exact scope.
Darling, remaining VMware/VPN lifecycle and final joined current-HEAD session
acceptance remain part of the wider active migration.
