# Data-only vendor package stage

`vendor-package` creates an optional native DEB from an explicit selection of
checksummed third-party DEB files and separate license resources. It never runs
upstream install/remove scripts and never copies their control metadata, service
units, launchers, polkit rules or autostart entries. Product launchers and service
ownership belong to the consuming DE integration.

```sh
python -m karyo_builder vendor-package examples/netbird-provider.json \
  --image karyo-builder:trixie --output out/vendor
```

Use a pre-existing local Debian13/trixie or Ubuntu26.04/resolute amd64 build image.
The build resolves its immutable image ID, runs offline with no capabilities and
no new privileges, mounts captured inputs read-only, and publishes a unique
result directory only after receipt/artifact validation. Failed jobs are retained
under a distinct `.failed-vendor-*` directory. Source CMake/quilt stages keep their
existing contracts; this command consumes external data rather than a Git HEAD.

The version1 recipe declares package metadata, exact input package/version/arch/
SHA256 and file lists, mandatory license input SHA/destination, and an explicit
source epoch. The NetBird example expects public0.82.1 CLI/UI DEBs and the exact
upstream root LICENSE under `out/vendor-inputs/netbird/`; obtain and verify those
inputs separately. The root source archive used for that notice is pinned in
VALIDATION_PROFILE_NETBIRD_CONNECTED.md. No binary or credentials are committed.

Selected input files may only reside under `usr/bin`, `usr/libexec`,
`usr/share/pixmaps` or `usr/share/icons/hicolor`. License destinations are confined
to the output package's own `usr/share/doc/<name>/` directory. Every file must be
an ordinary unique non-writable archive member without special permission bits.
Directories and links are not extracted from upstream. Missing/duplicate selected
members, traversal, active-system paths, symlink/hardlink/FIFO selections, changing
input files and digest mismatches reject publication. Host input copies also
reject symlink/junction paths and multi-link/non-regular or oversized files.

The resulting control archive contains only generated `control` and `md5sums`.
`Depends`, optional `Provides` and `Conflicts` come from the reviewed recipe;
dynamic runtime dependencies are not guessed by executing vendor binaries.
The NetBird example uses the upstream GUI's GTK4/WebKitGTK6 dependency family,
requires the separate Karyo scoped client wrappers, and conflicts with raw
upstream netbird/netbird-ui packages. It does not silently replace an existing
system daemon or import its credentials/state.

The manifest captures original recipe hash, private input-copy hashes/sizes,
resolved selections, immutable native image identity, distribution and installed
build-environment hash, exact runner hashes, omitted upstream control inventory,
selected payload hashes/modes/sizes, and final artifact hash. License resources
are copied byte-for-byte at0644. Payload/control timestamps follow the explicit
epoch. Native compression/tool versions may differ between Debian and Ubuntu;
equal input binary hashes do not imply identical DEB bytes across bases.

This stage verifies data identity and inert packaging, not upstream signature/
APT metadata chains, comprehensive third-party license clearance or the behavior
of arbitrary binaries after launch. Runtime/service/GUI and distribution catalog
acceptance remain separate gates. See the provider validation documents for the
actual fixed inputs and native checks used by this migration.
