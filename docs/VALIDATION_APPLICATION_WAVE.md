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

## Earlier-wave native artifact hashes

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


## Settings wave: installed native packages and real authorization

Both 20-package native sets use exact DE
`93765d7c6cb8fb1cb77d5d89b3f52a0b382ba4e1`, source archive SHA-256
`edddbe423ec6c7b1e9976b6c57102551297d1afc8013a948d81306704e4854e0`.
Each runs all 53 then-current CTest entries successfully before staging.
Debian installs/reinstalls nineteen packages, omitting only optional RAR;
Ubuntu installs all twenty. The input record verifies each package manifest and
artifact hash before SCP and again inside the VM. dpkg audits are empty.
No APT repository component was enabled on either installation host.

The new real Karyo logins use Debian session 95 (shell PID 7024, idle Files 7020)
and Ubuntu session 243 (shell 34708, Files 34704). Installed Archive from
`/usr/bin/karyo-archive` extracts the public ZIP into `sample (4)`, retains the
24-byte readme and 18-byte UTF-8 CSV, and opens the new foreground Files window
on both bases. wlrctl and inspected `settings-wave-packaged-uri-fixed.png`
confirm that the URI fix is now accepted in real DEBs, superseding the earlier
native-overlay-only gate. Existing background-window activation is still separate.

Installed Settings renders its real pages on both systems. Its new authorized
APT action resolves to `/usr/libexec/karyo/appcenter-apt` and retains admin
polkit policy. A first test launched through SSH inherited the SSH cgroup and
login UID, so its immediate authorization failure is excluded from product
acceptance. Launching Settings through Karyo's own Start footer produced a
process in the actual GUI session, displayed the real Karyo authentication card,
and accepted the fixture administrator password after cancellation/retry.
The real root helper completed `apt-get update`; the UI re-enabled its controls
and displayed the package-list results on both VMs. No package upgrade was run.
Screenshots `settings-wave-real-auth.png` and `settings-wave-auth-result.png`
and the polkit journal retain the observed action and completion.

### Network observation correction

The installed 93765d7 Settings network page failed its first real UI check:
Debian displayed loopback, and Ubuntu reported disconnected despite working SSH.
These cloud QA bases use ifupdown/networkd rather than NetworkManager for their
uplinks. The failure is recorded in `settings-wave-network.png` on each base.

DE `4214e77` fixes observation without replacing the host's network manager.
All 56 then-current native CTests pass on both bases. Explicitly marked native
test overlays, installed only as `~/qa-bin/karyo-settings`, now show `ens160`,
the correct QA IPv4, gateway and resolver on both systems, with a clear
“Managed outside NetworkManager” explanation. They were launched via a disposable
Start entry in the real GUI cgroup; screenshots
`settings-network-observation-fixed.png` were inspected. These overlays do not
replace `/usr/bin/karyo-settings` or its DEB. A final package containing this
newer correction is still required.

| Base | Native Settings observation overlay SHA-256 |
| --- | --- |
| Debian | `7cdcba80a10289facbc99fcf60f8eeb0f4aa796d6a03b1686119d56891ae30b2` |
| Ubuntu | `ef3511f2165d4c2b021d81b767850a57a14b882e9fbfe30abf397aed037ed059` |

### Settings-wave DEB hashes

These filenames retain the QA version; the source revision and base below
identify the new wave unambiguously. They supersede earlier same-name inputs
only in these disposable QA installations.

| Base | Artifact | SHA-256 |
| --- | --- | --- |
| debian | karyo-style_0.1.0-1_amd64.deb | `be2b553a18dc6fd2038244d0c95a4b9be90abc271881c34a17736f466c45cb3c` |
| debian | karyo-shell_0.1.0-1_amd64.deb | `c40c4e66f19f21809a0641a291e6c799ca8041af04404718aed172bd18eee0f8` |
| debian | karyo-lock_0.1.0-1_amd64.deb | `321229037b83ce591c3a3a46040598e57371477ee165b71f88fdf8ce8e2a3b02` |
| debian | karyo-session-entry_0.1.0-1_amd64.deb | `eca9d9fccd33229022ebc7195fffdd54f84312a2a87aa8d13f940204b0360bb1` |
| debian | karyo-session_0.1.0-1_amd64.deb | `6a00b8abbac1742f647b789619460c62e1068b3dd5a9adf8f16faa1a921e7aa4` |
| debian | karyo-terminal_0.1.0-1_amd64.deb | `2e26393a1b001ed71d8bd94a57f8090509a23c56444a994092aa77a7f98b2b8b` |
| debian | karyo-camera_0.1.0-1_amd64.deb | `ebba526dabba8d91ad0a2a6281ccd38a293eebddd7130c2deb9afac4a904efa0` |
| debian | karyo-photos_0.1.0-1_amd64.deb | `8169c0d5095d10c15d9258705d08e1d138680937969e1e2a749f290fd55bcf27` |
| debian | karyo-calculator_0.1.0-1_amd64.deb | `ab779cb2814c427e6b9d6a5db89242d373a4b40a785c5248d00c1d1713c31ee6` |
| debian | karyo-clock_0.1.0-1_amd64.deb | `26fa6e34ce80552d4c47b757e59cdf7374838c0bc5016f7b8f02479d7f82b070` |
| debian | karyo-editor_0.1.0-1_amd64.deb | `e682c7893f8eae1b2a46c7c4ddac0c9fdd4ac5fad3448d047c93a6f99444618d` |
| debian | karyo-reader_0.1.0-1_amd64.deb | `7f73668e72c13f803ebd2bd4deae95dcb2fe1683411f9c3235043ff37c9b8bb7` |
| debian | karyo-player_0.1.0-1_amd64.deb | `496af4f569fca9b805c03e0ec913548c2ee71110b6d32cfbd6ab83faac1f00b2` |
| debian | karyo-monitor_0.1.0-1_amd64.deb | `43c254792769b682a7763b7c5e32dacaab23625f6c71bc4f276de5d1fd58ca00` |
| debian | karyo-snip_0.1.0-1_amd64.deb | `6b54ed51d79178ff3b564a63e7a5826e880839403ee2eed0269c999e6b124895` |
| debian | karyo-archive_0.1.0-1_amd64.deb | `e58bc5faa3b9fe1807e7f6d6d0615aba923c7eb84a8ac14fee572f1eef2cf792` |
| debian | karyo-archive-rar_0.1.0-1_amd64.deb | `31c5cbab9be244cd740d6907c62cb42100728680015c386ecc1d6fc4a2b7cf22` |
| debian | karyo-files_0.1.0-1_amd64.deb | `4cff282f01fd0f04ec5c8c393ee3f460724f0975d14a3fe787eaee148410a274` |
| debian | karyo-software_0.1.0-1_amd64.deb | `7ebd9bc548fb4655f1790e036be4677b816c88b9762203da488882960022ba00` |
| debian | karyo-settings_0.1.0-1_amd64.deb | `e407a6a5224542907899a916346f0c58f7c991de64b990aec2c03578924aeb7e` |
| ubuntu | karyo-style_0.1.0-1_amd64.deb | `d25413d801ed66aed2fea3e11f7505405122f202a0fce6455fff319e804536e7` |
| ubuntu | karyo-shell_0.1.0-1_amd64.deb | `c9eb29d22a4f31db0454c131d8308f6804d95cab4d474ed45e2f7e840486df6b` |
| ubuntu | karyo-lock_0.1.0-1_amd64.deb | `53f2e9bf294fc711379af4aa18adc254e023f9aad10dc29c8a198f636cb3ca47` |
| ubuntu | karyo-session-entry_0.1.0-1_amd64.deb | `a33b4fe68555e57f7b154e5330d9d0d7af6a398d2ffab924da1b4a7cc6e6ddfa` |
| ubuntu | karyo-session_0.1.0-1_amd64.deb | `c40ad1f48598a724202628d27370284d9d8acee66020ec73ef9debf670a3a98d` |
| ubuntu | karyo-terminal_0.1.0-1_amd64.deb | `2d4572298646c93f8148e90d429bb8b47b63e73a8115e13331a5bbff009cf319` |
| ubuntu | karyo-camera_0.1.0-1_amd64.deb | `ef4da72f573f4bf58736ceebb9614550b7d7c87c4110282a73493a09851ef8a9` |
| ubuntu | karyo-photos_0.1.0-1_amd64.deb | `1b412c7a22ceacc99ea68569b54c6612b669c58006f8e30c774dece5baf1c4de` |
| ubuntu | karyo-calculator_0.1.0-1_amd64.deb | `536b26770d9132255727869c21148250a8cccad7577e9aaf9d2fa3697f5e79a2` |
| ubuntu | karyo-clock_0.1.0-1_amd64.deb | `a004007f7958c6127bb687a4d35a00fa1cf58a557513b77bf3c5eebc5839a105` |
| ubuntu | karyo-editor_0.1.0-1_amd64.deb | `965bb1ce2500aefa866afae0de8781652eb297788a19310af2ec20fe21c68074` |
| ubuntu | karyo-reader_0.1.0-1_amd64.deb | `7fe2b9d78693bd9e1a486cdd841354b1f5be7d401f3583fc8f4b279af38e991e` |
| ubuntu | karyo-player_0.1.0-1_amd64.deb | `126f4dfcbca8ebdbe36b036431fe828e672c23c6f40dec012fa44d014fc8bec7` |
| ubuntu | karyo-monitor_0.1.0-1_amd64.deb | `b3185152e1ffaf11f5612b21ff5c5cf4a22cd5650e3f87edbc2fa3b25aeb1741` |
| ubuntu | karyo-snip_0.1.0-1_amd64.deb | `04f42c1010c5c00fab74feaa5950bec6ad4856903eba9813e82798fe629a41a3` |
| ubuntu | karyo-archive_0.1.0-1_amd64.deb | `d94d36a7700ccebdc9e76d632f6599563442f615e1991f97ee4e18968f2381c9` |
| ubuntu | karyo-archive-rar_0.1.0-1_amd64.deb | `5757386946fdd6e09e06d974777048538f81e4741e36b81dcaae72012ea23f9f` |
| ubuntu | karyo-files_0.1.0-1_amd64.deb | `1a58a7ca9933c2dcb2f6bb736ebacf7d4398b297eda7a5a1babd6df3b61775d5` |
| ubuntu | karyo-software_0.1.0-1_amd64.deb | `b1551a100e0717a36a928bfd970df886ae54d25668daa1b59f20baa8a51a5658` |
| ubuntu | karyo-settings_0.1.0-1_amd64.deb | `3c74adb45f0283424729d272e23a10ccf03da8b6b3b0e35dc1c63a90e6d4d0f8` |


## App Center package contract

The optional appcenter-runtime recipe supplies the standalone GUI, public
appcenter launcher and Russian catalog. It depends on the shared authorized
software helper and Karyo Terminal. Curated public application descriptions are
a separate appcenter-catalog-runtime package; the GUI still supports repository
search and environments if that optional catalog is absent. The source recipe
continues to resolve HEAD at build start and the manifest records the exact SHA.
Flatpak stays optional and per-user when installed; conda is set up only by an
explicit user action with a checked upstream installer. Neither private profiles
nor a downloaded conda environment is included in these package components.


## Font runtime contract

The separate fonts-runtime recipe packages the 16 original complete IBM Plex
Sans/Mono files with their OFL notices. The session bundle depends on this
runtime; installing an individual app still permits its ordinary font fallback.
Distribution Noto fonts supply additional scripts and emoji. No package installs
global fontconfig family aliases. Native Qt hash/family/Cyrillic checks and
isolated staged fontconfig resolution pass on both supported bases, including
UID 65534 payload checks. Native DEB and real VM font installation acceptance
remain pending; the running App Center wave resolves an earlier source revision
that predates this component.


## Installed App Center wave

Exact DE source 2e33ed69ce101883780c29e075057528f57512db builds a native set
of 22 components on each base. All 59 then-current CTest entries pass before
packaging, duplicate file ownership is rejected and every staged artifact hash
is verified again before installation. Debian installs 21 components, keeping
the optional RAR addon omitted; Ubuntu installs all 22. No repository sources or
owner VM/laptop are changed. Both dpkg audits and installed package verification
are clean. Local records are under out/migration/appcenter-wave-{debian,ubuntu}
and out/{base}-vm-qa/appcenter-wave-input.

Fresh actual LightDM Karyo logins succeed after installation (Debian GUI session
119, shell 8555; Ubuntu GUI session 262, shell 37070). App Center starts from the
Karyo menu as /usr/bin/karyo-appcenter in those GUI scopes. Discovery, the public
catalog, system repository search and details render on both bases. Sources
correctly identify Debian 13 and Ubuntu 26.04.1; update counts come from native
APT simulation, with no unsolicited system upgrade.

The small public ncdu package is initially absent on both guests. Cancelling
its authorization leaves the app responsive and permits retry. A second request
with the disposable account's administrator authorization installs ncdu through
the fixed root helper on each base; package versions are 1.22-1 and 1.22-1build1.
The UI changes to Open/Remove. Open shows ncdu --help in Karyo Terminal; Remove
uninstalls the same test package and installed-state checks confirm its absence.
The corresponding pkexec journal confirms the GUI user and explicit install/
remove verbs. Existing htop/jq on Ubuntu are retained. No broad upgrade occurs.

Real Environments without conda shows the explanatory setup state and does not
download anything until explicitly requested. A per-user QA desktop entry
selecting ru_RU.UTF-8 confirms the Russian chrome, navigation and environment
page on both bases. No real Miniforge installation or Flatpak transaction is
claimed; their isolated source regressions use substituted tools.

The updated Settings network page is now accepted from its installed DEB rather
than the earlier native overlay. Both GUI processes resolve to /usr/bin/karyo-
settings and correctly show ens160, the guest IPv4/gateway/DNS and management
outside NetworkManager. This closes the earlier loopback/disconnected package
gate. Screenshots appcenter-wave-*.png and installation/verification logs remain
local. Packaged Archive additionally contains the deterministic ZipCrypto fix;
its native root/unprivileged tests establish the decoder/password behavior.

Installed acceptance found one small App Center issue: the prior cancelled
authorization notice remains after a later successful install. DE 8505b39 clears
it on retry and passes the native/unprivileged window regressions on both bases;
this later fix is not yet in the recorded installed DEB. Ubuntu's Terminal title-
bar close clicks did not finish that fixture; exit was used and button behavior
remains a separate follow-up, rather than an accepted result.

Later font and greetd-transport work is intentionally outside this captured wave.
The current native suite includes 61 tests, while the wave's exact revision has
59. Neither the font DEB/VM installation, greeter UI/real login, optional
compositor protocols, profile integrations nor physical-device acceptance is
established by these application results. No commits are pushed.

### Native App Center artifact hashes

| Base | Package | SHA-256 |
| --- | --- | --- |
| debian | karyo-style | bfa527c54fe13b0675eeecbf33cad27304eb2034c889b8191a3bfc0556ab7d41 |
| debian | karyo-shell | 3d51358f1c9a5b1fee5c29789e0c3f0fd69cf9d74ac56ad41c89dbcf12774468 |
| debian | karyo-lock | 0a188f0b4ce72d3c930ab4c7dba7e758cb4d6f75bd44c9041209c0ed44c07239 |
| debian | karyo-session-entry | 8e3fbff0454b076446d9ad75e7836dfe3f41d48e652f7abd876ac7dbd247269a |
| debian | karyo-session | 02088134d76096debee0d845e8310a1c357fefe23e19882ceceeadaee420db09 |
| debian | karyo-terminal | fe8f308dab7137e666ba01f7b45af42ae91607c6c14f0b96b68bc0239d28d3b6 |
| debian | karyo-camera | 5077590e251b237822033e9865d219c29809592ebb6ad242358cd1c6cb4044fd |
| debian | karyo-photos | ec0f59e4b8cbacbfe7685acb9c8191ebce78ecfb39933955c0c9c41357e219a5 |
| debian | karyo-calculator | 948e6669d0341ca5bc0cc7fca35ba871d07d865cf4df54efb035638cd84ada72 |
| debian | karyo-clock | 5dae6cd3fa9618c82d5845c0eaa790fd4e50baf27193d5ca9f2086ff30ccbe3a |
| debian | karyo-editor | 06c8c3f5a65065208629adb12ddf7a2b0790b1b00ef29005ce141b8f537cda1d |
| debian | karyo-reader | 9911dce2d0158e989a3e6e9e702ec35a1c3aaaba1e11b1bdda5a300bbff924f0 |
| debian | karyo-player | c06b1a0dc78cd4084fa395e9ce53e9fb68d882f592a36bad3b737be73f7b15f6 |
| debian | karyo-monitor | 18deb09a92d2cf59483d3a53f1edaccdcb333deac997b247a71b40d048677109 |
| debian | karyo-snip | 5e4234b24529cf808a287592c828f9e083a14f1b490c53124bf104bcd7ed1789 |
| debian | karyo-archive | 446708bc569a7d3bf888c1d5493eaaefb317ad146a86683d7d1a597f74d05293 |
| debian | karyo-archive-rar | 14f431f64eed917828be660fe916ae89c6a8097968a680ae9fb02fc57e3b6c0f |
| debian | karyo-files | ad603b437e13d9c82a1535bea5f876c3749839bfed1be74a2b3efe3ac21844aa |
| debian | karyo-software | ad3d0dcddcca8c168f6defb9431bc5009f1f68da9954c9f29ee72388f411fb5e |
| debian | karyo-settings | ccfb55a285d03de1d4de738abb0bf7ac0e7e03bb834538f4fec6570431f1c321 |
| debian | karyo-appcenter | 9a4c824c9d384c24e6d4a0cb9481fb42dad78cfe35885121f76b2d4ec561f3d4 |
| debian | karyo-appcenter-catalog | 901398e862177ba165a4c01678d97d58fd4bc76d27834ee621f6dbc7d7b03caa |
| ubuntu | karyo-style | a21fe7b7f7a6f77c09b07a26a4c002ffe5e150906da3926dfd43cfed36a6de47 |
| ubuntu | karyo-shell | a81aee402960be96ecc54997f591440f345bc5d8975d621d1cc30d6f20947295 |
| ubuntu | karyo-lock | 75fef59d5270aaaa44c6469e0f47d2a5c35073a0196aa9dd1b5b5616faeee00e |
| ubuntu | karyo-session-entry | 733a120b1d9438f8d3c86b459039784237252a183a7be1e54c89c850dfd3b3f8 |
| ubuntu | karyo-session | e8aa12d3c1831f1ff461b88395a008371746c2d9d779e2548923a3fe836eca54 |
| ubuntu | karyo-terminal | 2650fa9ccfacbc0b76d3ef2d30357f7c61ef9d49c6cb102b2f047f573930f6dc |
| ubuntu | karyo-camera | f1a013392757d8a7faadf3c3d8ac7dbfb76829297afcc5ef5d475861f47cff29 |
| ubuntu | karyo-photos | 4cfb0a23bf249392593edec268499226e3fe6ddd33de59cf3875703c11ba585e |
| ubuntu | karyo-calculator | b7720339a677479291bbab29e55249e2ff16b5f8a3efedec460ab2570841e1c7 |
| ubuntu | karyo-clock | 3304368546d7eb9776e46e3897419c1d8a12b19623e666bc815fddd735cd20bc |
| ubuntu | karyo-editor | fa4ac9963ea0f96d9583f2018ff40a66908eedaf1ed463dad9c8ba3a6e4bb359 |
| ubuntu | karyo-reader | bc59321c51d97caffbcc8fd3c4ce8b7705ecaa6e6da7ae6f8b7dcc245d2c22fe |
| ubuntu | karyo-player | 5940491acc272efd135fd70b10d7a1d2401658ce5b3653b1066d2a35b4b53452 |
| ubuntu | karyo-monitor | b198a2eeb5613f7c170ef787c5f02600243f9aed73ce7a36ab9144c5218eacb9 |
| ubuntu | karyo-snip | 4592e2e339eb69761e7bf153fc3ec5ec96e534a8e3a5c6d93311fd62e13e95f4 |
| ubuntu | karyo-archive | e6387b883209477a1fb660bc11484a95e6ba16dbf4ca0387899416a26404aaa1 |
| ubuntu | karyo-archive-rar | ca3ea849b68c4365533d2bb926fb5ec83277fcc63ca72184c0f564fbf08ec6c1 |
| ubuntu | karyo-files | 782f64a8ce594900019a1f18edf47d23cb747e8158fb7a2b2bc0a19eec8e1d08 |
| ubuntu | karyo-software | 311cdb48b349b90433ae38120c5eee45cca55222de95ac3032912f764d4f8bba |
| ubuntu | karyo-settings | 7801431dbb45de2cb460938c3cefad7acc1ed461be8b1253ba33359ca99340ec |
| ubuntu | karyo-appcenter | 116a3cf9cea74e9fbc77c8af8da1d2a2ab7b206fdaae61b5904303b2639fc845 |
| ubuntu | karyo-appcenter-catalog | ecbfcc7b040b2993257c864856bec46c140de9ec496242dc27cadd9a2ae81f4c |
