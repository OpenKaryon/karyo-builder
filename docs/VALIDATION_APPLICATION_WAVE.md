# Native application wave acceptance

This is a local review checkpoint, not a completed migration or release. No
owner VM or physical laptop was changed. All VM inputs are public disposable
fixtures; package manifests and screenshots are retained under ignored `out`.

## Source and installed packages

The first 17-component package sets use exact DE
`21fdf2e4e0636d2ef17d0a8a72dce42475762bee`. Native builds configure, compile and
run CTest once per set, then stage each component separately and reject duplicate
file ownership. The first wave passes all 31 then-current CTest entries.
Debian installs 16 of these packages: the optional RAR integration is deliberately
omitted because the QA image enables main only. Ubuntu installs all 17 using its
existing multiverse component. No package rewrites APT source configuration.

The later Files plus session-entry sets use exact DE
`231bcff29796042ae0a810d6b5a212935af1a893` and pass all 38 CTest entries on each
base. Both install successfully with verified input hashes. The session-entry
reinstallation consumes the local artifact even at the same package version.
Build inputs and per-package manifests remain in
`out/migration/{de-wave,files-wave}-{debian,ubuntu}`. Each record contains native
image identity, resolved source, copied recipe/runner hashes and the shared log.

## Real session and application results

Both actual LightDM logins reach the new Karyo session. Debian's new shell PID
is 4176; Ubuntu's is 29635. Calculator, Clock and Monitor launch and render real
process data. Their source-level behavior has separate native regressions.

Snip captures the whole virtual screen and editor Copy publishes a 1280x800 PNG
to Wayland clipboard on both VMs. Pointer endpoints (100,150)-(500,380) produce
an inclusive 401x231 region PNG. Escape cancels a new region and the previous
PNG remains byte-identical. Editor, overlay and clipboard evidence is retained
under each VM's `qa-results/wave` and host `results` directory. These checks do
not imply stock-labwc window capture support; that protocol gate remains open.

Archive browses a Python ZIP containing nested UTF-8 files and extracts the
expected 42 bytes on both VMs. An initial Debian attempt failed because the QA
helper inherited inaccessible `/home/qaadmin` as cwd. strace showed EACCES opening
`.` inside libarchive. The corrected helper enters the QA user's home; normal
DE launch already does this. The failed fixture attempt is excluded, and no
program-specific product workaround was added. An original fixed-date external
ZIP fixture was added as a separate regression. All 31 Archive Qt backend cases
then pass as UID 65534 on both bases, with zero skips.

Files starts without opening Home in `--dbus-service` mode. It refuses to replace
a running Thunar (observed on both VMs); after closing only that QA instance it
claims FileManager1 and accepts a real ShowItems request. Both screenshots show
Details open with 42 B, two files and one subfolder for the selected fixture.
No generic FileManager1 activation override is installed into existing desktops.
A later Archive package from DE `f5f6efa1221392a83d643a19eec28091ea3adb7b`
was installed on both VMs to use shared ShowFolders routing. Its extracted files
were correct, but the UI check initially overclaimed folder opening: destinations
such as `sample (2)` never created a Files window. This failed UI attempt is not
counted as acceptance. A real shared-client-to-FilesService regression reproduced
the failure on both bases: PrettyDecoded URLs contained unescaped spaces and
were rejected by the strict FileManager1 parser.

DE `1bf3fbb122005e7f144beadef1abca974d70e56f` uses FullyEncoded URLs. The new
regression opens a spaced directory and selects a Unicode filename containing
`#`; all 43 then-current CTest entries pass on both bases. Native test overlays
of Archive from this clean revision were copied into `~/qa-bin` in each VM;
`/usr/bin/karyo-archive` and its installed DEB were deliberately left unchanged.
Both real extractions then opened a new foreground `sample (3)` Files window,
confirmed with wlrctl and inspected screenshots `archive-uri-fixed.png`.
This accepts the native UI fix, not a rebuilt package; the final DEB wave still
must contain the change. Overlay metadata explicitly identifies it as a test
binary rather than a package:

| Base | Native Archive overlay SHA-256 |
| --- | --- |
| Debian | `2436059c00bf9663d37ca01a07e07506598df5555f44fbeb4d6d5c457473897e` |
| Ubuntu | `1f6355edab847963cfdef157eb3e4b42eee4269ed966b0fc58b23831b774acd9` |

Creating a new folder window is verified. Activating an already-open background
window remains a distinct integration gate.

The VM wave does not establish physical camera/microphone, Bluetooth, Wi-Fi,
audible playback, GPU or multi-user isolation acceptance. Earlier lifecycle
checks are documented separately in VALIDATION_DEBIAN_VM.md and
VALIDATION_UBUNTU_VM.md. Settings, App Center and optional integrations remain
part of the active migration, rather than being waived by this checkpoint.

## Native artifact hashes

These are QA artifacts, not signed release packages. The same package filename
across base rows denotes a different native build; never exchange their binaries.

| Base | Artifact | SHA-256 |
| --- | --- | --- |
| debian | karyo-archive_0.1.0-1_amd64.deb | `11d7ab57db9ab34a50ca69ad9c92803107cf27abb63b25df20a11c94809f2739` |
| debian | karyo-archive-rar_0.1.0-1_amd64.deb | `63b0f2d6dd85cf7f02829e1177fbf8501943f9ed622c5a07df4be0c324958d56` |
| debian | karyo-calculator_0.1.0-1_amd64.deb | `af27a8c3c4c9dee68945a10a39fa2ec3f0d1ee630b3ae074ca23d44b3e7e6fdd` |
| debian | karyo-camera_0.1.0-1_amd64.deb | `2f28f31dc0876616f3a3e06fe3611c412ce2d7cb44b957258456f19b0c502b68` |
| debian | karyo-clock_0.1.0-1_amd64.deb | `ea55dc5afd571cded9f894ab1660b1fafce1f264f02017a89344050ddd40c39f` |
| debian | karyo-editor_0.1.0-1_amd64.deb | `6d1535d0ee7e902360aa179357f5815bf863aa560bd07e0ee852935af236192f` |
| debian | karyo-lock_0.1.0-1_amd64.deb | `afe18cd2b86b65599cc82093eac16a43f4bad5d6f580244a84d98b1cda0ed5e9` |
| debian | karyo-monitor_0.1.0-1_amd64.deb | `74f1cebd0ad90ca182a830f3ac0691c918a9c4c6352326faeda0f5aefdee2bb4` |
| debian | karyo-photos_0.1.0-1_amd64.deb | `8ee54add6aaa33c0952eaf924076780a632ad5ae69910b180496a84b6ea382d9` |
| debian | karyo-player_0.1.0-1_amd64.deb | `144b6f54c284ea8dd4bfcd5b2d30fdf8e86347a6bee0f3fa63f1953c2603740a` |
| debian | karyo-reader_0.1.0-1_amd64.deb | `76eb60736d6104367b7f8ff51479e820da03b371eef22a68cdf398c536e2c75e` |
| debian | karyo-session_0.1.0-1_amd64.deb | `b15b5a39eb8b4e159e3e38e2657d170aa9b19cf8c499934506adc3e590fba5ba` |
| debian | karyo-session-entry_0.1.0-1_amd64.deb | `83767524d7f0f203cf100e393cafcc258d80036be18cec818d36494f8b9e6bb6` |
| debian | karyo-shell_0.1.0-1_amd64.deb | `d8329cdc59336a67bbb8e85d47f7c4fef9c2fac1839acb5ddfb5d1dacf17460f` |
| debian | karyo-snip_0.1.0-1_amd64.deb | `a8463415e61e9910f11f8092edd4fd63e721a30a814a5070b384ef4487713305` |
| debian | karyo-style_0.1.0-1_amd64.deb | `c30a484d99669d0799f2c3f33ffd6df198642ee85de8de810798269a2d8663e1` |
| debian | karyo-terminal_0.1.0-1_amd64.deb | `9caa89f393fc0515a7a1ed13bbbe0fa4972fe43fbc5689af854be959845b57bc` |
| debian | karyo-files_0.1.0-1_amd64.deb | `ff9ab61c7f08e31d239dcf2b2e6c080875dfe9dbe1cd81437a81a5c7440a37c0` |
| debian | karyo-session-entry_0.1.0-1_amd64.deb | `ed1df0d039947ec0b310d75fa831d027e2e7e6348f70b4ce70295de7031c4033` |
| ubuntu | karyo-archive_0.1.0-1_amd64.deb | `e00c742ddce3380a0e27125adaa477e6d0928d1805d1c1d06855c2037186df46` |
| ubuntu | karyo-archive-rar_0.1.0-1_amd64.deb | `a5131b9930ac04f410a6fbdf6b33d1458c8804bedd4a7558b4f06ee9031e2a8c` |
| ubuntu | karyo-calculator_0.1.0-1_amd64.deb | `966fc48fd0e1a0c3b56621035042d23626ba8b4f6a2d57d90360bf679258bfbd` |
| ubuntu | karyo-camera_0.1.0-1_amd64.deb | `2eb3392b4d26a1e8a01ab93f6f2baaf6ece3ba4de0e351240669073d4a53c1b9` |
| ubuntu | karyo-clock_0.1.0-1_amd64.deb | `f4f34505a82e8d5bd0645c73220c6cdcbd4043f6cd9cf277439e30a944f386b3` |
| ubuntu | karyo-editor_0.1.0-1_amd64.deb | `8f5cfdb04405365c8a9f78f7f2c2317dc31a37d9adcee101710149cd4dd44938` |
| ubuntu | karyo-lock_0.1.0-1_amd64.deb | `ea68ca751866f012bd2f7528ba05d86f06d53013bd0a18314ac7141ffa2d5ac4` |
| ubuntu | karyo-monitor_0.1.0-1_amd64.deb | `754d1d0ee5ab4b53381849857cd3ed032faf6ddf55e5ad35c5215c6b3b4c0e9b` |
| ubuntu | karyo-photos_0.1.0-1_amd64.deb | `f051e785e0fbfe5f77b46ad79a93b59d9b29be1bb5e0bd96997833fd3ce2cf14` |
| ubuntu | karyo-player_0.1.0-1_amd64.deb | `2beb63d5fc68ce8bfc27b4aca25ad96bba381552a9b8adb9564ec6c720dce489` |
| ubuntu | karyo-reader_0.1.0-1_amd64.deb | `6c5f36219d66f4d7debba57390594eb37059981bce5dde335915587dcc115488` |
| ubuntu | karyo-session_0.1.0-1_amd64.deb | `7bdebd94ee83264928e92202e85ec8caebef06c7b39771dd4e2543d694a0f843` |
| ubuntu | karyo-session-entry_0.1.0-1_amd64.deb | `1913ff2031b61c78ef944f867e44b3d037fb8a3f8a7004c2806207f058b5f629` |
| ubuntu | karyo-shell_0.1.0-1_amd64.deb | `0fb1834bbf2c8677f9cdd9dd878deb7a2f516a4f484a3a71b29f6904909a218f` |
| ubuntu | karyo-snip_0.1.0-1_amd64.deb | `1691398bd32e3f36993819dcc13a1af48fc9bdeba4c385f5023903f7b699206b` |
| ubuntu | karyo-style_0.1.0-1_amd64.deb | `8fdeb6745ddb9b64f93bc18acd1b7a78964f71cb76c4d5e31ba0ff5bda073161` |
| ubuntu | karyo-terminal_0.1.0-1_amd64.deb | `5df4ed1361cc6db6c30e79d8a15e9acf040aef1634ea7aa528c6d68ec56507ff` |
| ubuntu | karyo-files_0.1.0-1_amd64.deb | `2afc53f71c2a871843b4b4917e48a71090fd58d0fe8e92d3d2ced5f34e637ec3` |
| ubuntu | karyo-session-entry_0.1.0-1_amd64.deb | `fc36f1f77638ce433bc7049a60f8812102be2b85e5fffbeb7950170f167e0285` |
