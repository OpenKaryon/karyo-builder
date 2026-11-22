# Optional Intel macOS launcher core

The independently packaged karyo-macos-core0.1.0-1 now passes native Debian13
and Ubuntu26.04 wrapper and installed-CLI gates. The package contains reviewed
own-code Python policy/process helpers and the isolated public karyo-macos entry.
It does not supply an engine, change MIME defaults, activate a service or install
another desktop. Shared Qt picker/MIME and actual Darling runtime are subsequent
migration pieces, not claims made by this report.

## Exact native inputs

Both regular examples/macos-core.json builds use committed DE
022644ed3de6dafd10bc1d5e3a5bafccbfd6e289, source archive
7c15a2ac8d9437d70095d65ddffa9b47d6529f2ac4624b65036a568f1992bb66. The source reference remains HEAD;
actual resolved Git revision and archive hashes are recorded for reproducibility.

| Base | Native DEB SHA256 | Installed image SHA256 |
| --- | --- | --- |
| debian | f98fd96450741f1879fa6c2733af02fb7b3b3811404ac23d5f60e30aebfbf6c1 | 7d24967927aea23254d4ed29115a1d4c4d0c3299e030e2b5a85d83f72d904350 |
| ubuntu | 84d4f793729b97ab3a8f662931fd017ebc092250e02b8efd35db65c7e1589579 | db5ff783bdc70b686faf513b259403c5e85c74b59cbe4899ccf877e41d7d9bc6 |

Regular native outputs are out/migration/macos-core-<base>-v2; final installed
receipts are out/migration/macos-core-installed-<base>-v3. The joined machine
record is out/migration/macos-core-evidence.json. Parent images are the accepted
actual-shell runtime images, not shared foreign-native binaries. The source and
native identities, DEB digest/size, install script, actor, driver and receipt
hashes are all captured and checked. Documentation is explicitly included when
a minimal container base filters it; dpkg -V must emit no diagnostic.

## Source-level contract

All33 cases pass without skips as ordinary UID1001 on each native base. The
CMake component separately passes in both normal native package environments,
where root refusal is tested rather than treating root as an application user.
Tests establish thin/fat32/fat64 Intel Mach-O and XML/binary .app metadata,
bundle containment, unsupported formats, bounded/nonregular plist refusal,
FIFO handling, safe literal arguments and unchanged file data.

Actual Unix accounts replace the prototype's fixed two-slot authority. Spoofed
HOME/USER/LOGNAME and old slot variables cannot select another profile. Display
pairs select persistent-server state under that account's short storage path;
79/80-byte UTF-8 socket boundaries fail before writes. An overlay home requires
owned private tmpfs runtime storage, explicitly marked nonpersistent. Prefix
and metadata ancestors reject symlinks/foreign ownership; saved data survives
refreshes. Logs are exclusive0600; profile directories are0700.

The fixed graphical script forwards all application paths/arguments positionally,
sets scoped10.13.6 metadata and Fusion/native selection, and never embeds caller
text into shell code. Real Linux/bash fixtures prove literal forwarding, atomic
replacement preserving the lower file, absent-source rollback and refusal to
follow or remove a pre-existing temporary alias. Linux Qt/QML/loader variables
are scrubbed and X display/auth survive; headless mode removes the X11 IPC opt-in.

Real Linux process fixtures preserve exit23, signal status143 and binary output;
a quiet live child has no artificial timeout. A completed direct child returns
while its own explicitly synthetic persistent daemon still holds the output
pipe. This is process-wrapper evidence, not simulated Darling compatibility.
Credential checks include effective/saved UID/GID; a subprocess proves inherited
capabilities are cleared while existing NoNewPrivs stays unchanged. The wrapper
does not install a privileged helper or disable the engine's separate policy.

## Installed public entry

Each native DEB installs through real dpkg followed by silent verification and
apt-get check. Root invocation of --inspect is rejected before profile creation.
The ordinary account executes the installed /usr/bin/karyo-macos shebang; no
checkout import or alternate interpreter substitutes for that public path.

Ten installed checks pass on both bases: missing-engine status; noncreating
inspection; account/slot authority; missing-engine failure without state;
foreign-format refusal; isolated Python entry despite spoofed PYTHONHOME/PYTHONPATH;
literal arguments and exit23; scrubbed environment/capabilities; exclusive
private logs; and preservation of an existing data file including its inode.
The installed test uses a clearly named Linux engine fixture in a private PATH,
with network disabled, read-only root/source, private home/tmp, no capabilities
and NoNewPrivs. Actor and final receipts explicitly say fixture_only=true and
darling_runtime_proven=false. No Mach-O application is executed by these checks.

## Reproduce and retained QA corrections

Run tests/acceptance/check-macos-core.py with --source <DE checkout>,
--runtime-acceptance <accepted native image receipt>, --package <regular native
package folder> and a fresh --output folder. A separate native receipt is kept;
the final acceptance file appears only after install/user checks and version
comparison pass. The host Builder suite still passes50 tests, with its two
pre-existing native-only skips on Windows.

The first preparation attempted packaging before the new component was committed
because a Git whitespace guard rejected trailing blank lines; those failed
outputs are retained, and the accepted packages come only from committed
022644e. Installed v1 passed; v2 separated native/final receipts and caught
a driver metadata-variable collision in the added version assertion. Final v3
fixes that QA naming error and reruns every installed check on both bases.
No runtime behavior was changed to obtain those installed passes.

## Remaining acceptance

The Qt6/C++17 picker and Karyo-scoped MIME association are not in this backend
package yet. Darling's pinned native sources,21 prototype patches, stock build,
Swift/license provenance, native bridge and Vulkan/LLVM dependencies and engine
privilege bootstrap still need their own standalone component and acceptance
on both bases. Actual Intel CLI/Cocoa/Qt GUI operation, application credentials,
ordinary/native style, two-account isolation and installed engine upgrades are
not established by Linux fixtures or engine presence. The wider DE migration
also retains VMware/VPN lifecycle and final joined current-HEAD session gates.
