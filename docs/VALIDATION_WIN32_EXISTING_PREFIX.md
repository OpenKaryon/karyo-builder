# Existing native Wine prefix architecture

The launcher used to set WINEARCH=win64 on every launch, including a previously
initialized private prefix. The corrected policy selects win64 only before a
system.reg entry exists. It removes inherited architecture overrides and lets
Wine validate existing metadata. The product does not parse/rewrite a registry
or convert a prefix. This is a prerequisite for later import, not import itself.

## Source and package evidence

The runtime policy commit is 236dd5a3504d4b9deeaf1cd2588b9a5fe26be1f4. Its new
regression first failed on the old policy for win32, win64 and an unannotated
registry; all 17 launcher tests then passed on native Debian13 and Ubuntu26.04.
Both standalone win32 package builds exported that exact Git HEAD and passed
their native CMake/CTest stage. Uncommitted Wine appearance recipes/actors were
not part of those Git exports or this acceptance claim.

| Base | Launcher package SHA256 | Package manifest SHA256 |
| --- | --- | --- |
| Debian | `64695d701612913706803aeef41b801d89d5fc76550bfc50f3ffe2900d3f7d9d` | `44fae4c1ef7bc205e1de210261807910a7cfa8bd086bcc5a1a678f77cc30f608` |
| Ubuntu | `648b2d459c3e2b9069f204f90274128d09dd93b3f4d11a7900c992843f5c9297` | `a1a8b86a585bdacfcc425bd79581f446a75e009fd403b66e9a0315f8aabc732e` |

The QA host freezes an accepted native runtime receipt, checks its immutable
image ID and verifies the replacement package's native OS and SHA256 before
installing it in a disposable image. Dpkg verifies the installed launcher.
Only QA image preparation runs as root; Wine initialization and both application
launches run as UID1001 with no capabilities, no new privileges, no network,
read-only system root and a fresh private home/runtime/session bus. No host
display, existing Wine prefix, personal data, credentials or user VM is forwarded.

## Actual before/after

The native actor creates a prefix through Wine, waits for that prefix's native
wineserver to exit, then observes the persisted architecture. It writes a data
marker before launching the same real PE32 twice through karyo-win32. Each
positive run requires the executable's own PASS output, unchanged architecture
and preserved marker. A deliberately inherited WINEARCH=win64 cannot select or
change an existing win32 prefix through the corrected launcher.

- Debian baseline v4: initialization/wait0, two launcher results1, with actual
  `WINEARCH set to win64` / `32-bit installation` diagnostics. This is accepted
  reproduction of the failure, not a passing old product.
- Debian positive v3: initialization/wait0 and both real application launches0
  in the existing win32 prefix, using the installed corrected package.
- Ubuntu positive v3: initialization/wait0 and both real PE32 launches0 in an
  existing win64 prefix under the distribution's WoW64 engine.

Final actor SHA256 is
`4722c5f3b83613f93a612251a95b3c4adfc22ca47100239014a20b976a7c2854`.
Post-run inspection of the immutable accepted images additionally verifies the
actual executable's PE machine332 / optional-header magic267 (i386 PE32), not
only its filename. The Debian before/after binary SHA256 is identical:
`95570635dbd71ef60bffb607ee834ee244ee52b6cd05b23e2069d0369d383914`.
Ubuntu's native fixture is
`3372c17c71d798c1c4933e176f8fbffe820e0b36caa8035b04e0e3c00d29b016`.

Local evidence is in out/migration/wine-existing-prefix-evidence.json and the
wine-existing-prefix-debian-baseline-v4 / debian-v3 / ubuntu-v3 directories.
Package outputs are win32-prefix-architecture-<base>-v1. The 17-test logs are
wine-prefix-architecture-<base>.log. Receipts retain the full image IDs, source
revision, package hashes, actor bytes, per-stage codes and actual engine logs.

## Retained preparation corrections and limits

The first actor read system.reg before wineserver flushed the registry; that
failed observation is retained. Waiting for native initialization fixes the
fixture's lifecycle rather than changing product behavior. Ubuntu preparation
then exposed two incorrect Debian assumptions about its server's path/package;
its server actually belongs to wine64 in the native multiarch library path.
The final actor resolves this from dpkg-query and passes both native bases.
Older failed/preliminary outputs are preserved and are not the final matrix.

The native engines here are still the accepted Wine+karyo1 versions, with the
paired compositor/library stack of the unmapped-owner milestone. This does not
accept the concurrently building Wine+karyo2 caption changes. It proves console
PE32 prefix reuse, not a complete GUI application or joined current-HEAD DE
installation. Pure win32-prefix compatibility on Ubuntu, arbitrary legacy import,
conversion, real third-party applications and existing-user upgrade remain open.
No push/fetch, Forge change, user/QA VM deployment or ISO rebuild was performed.
