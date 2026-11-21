# Native package stage, schema 1

This is the first executable Builder stage. It builds CMake install
components from a Git commit into native Debian-family amd64 packages.
Debian 13 and Ubuntu 26.04 environments are validated separately. The edition/image
YAML and full pipeline in the top-level roadmap are still design examples.

The host needs Python 3.12+, Git and access to a running Docker engine.
Build the supported environment explicitly with:

```sh
docker build -t karyo-builder:trixie environments/debian13
python -m venv .venv
# Activate .venv, then install this checkout.
python -m pip install -e .
karyo-builder package examples/ui-foundation.json --output out
```

The example expects sibling checkouts `karyo-builder` and `karyo-de`.
The default input is the source repository's current `HEAD`. The recipe only
needs `source.path`; `source.revision` is optional and defaults to `HEAD`.
Source paths resolve from the recipe directory. Use `--source PATH` to select
another repository. Later, `--revision v0.1.0` or `source.revision` can select
a release tag. Each build records the requested reference and its resolved
commit SHA in the manifest. HEAD means the checked-out Git state, with
working-tree edits excluded from the export.
The initial exporter rejects submodules until a complete pinned-input contract
for them is implemented. Git archive data is extracted with Python's data filter.

Only the declared JSON fields are accepted; the package metadata also supports
the explicit optional maintainer_scripts mapping described below. The package section
declares Debian metadata and dependency relationships. The build section selects
a source-relative CMake directory and install component. Source code is trusted
build input and CMake can execute programs inside the isolated environment.

The CLI resolves the local Docker image to an immutable image ID and runs by
that ID. It does not pull images, install host dependencies, mount credentials
or the Docker socket, or enable build-stage networking. The container receives
read-only source and runner inputs and one writable result directory.
Default limits are two CPUs, 4 GiB memory and 512 processes. Builds require
container-local root for packaging, without privileged mode or Linux capabilities.

CMake configures Release with tests enabled and an install prefix of /usr.
CTest must pass and must discover tests before the selected component is
installed into staging. The recipe declares additional dependencies. Installed native ELF executables
and libraries are checked for the amd64 ABI and stripped; dpkg-shlibdeps adds
runtime dependencies using the container's installed symbols/shlibs metadata.
A missing dependency aborts the build and keeps its diagnostic log.
Static archives and ordinary data do not acquire runtime dependencies.
New shared-library packages still need their own shlibs/symbols policy before
they can serve as dependencies of other packages.

Each successful invocation publishes a new result directory containing the
Debian archive, SHA256SUMS, build.log and manifest.json. The manifest records
the resolved source revision, source archive hash/time, recipe hash and
resolved inputs, runner hashes, resolved dependencies, Docker image ID, installed environment packages
and artifact hash/size. Directory names are unique, allowing concurrent builds
and preserving previous results. Failure retains a hidden .failed directory
with its logs and never publishes a successful result directory.

The environment Dockerfile initially resolves Debian packages from mutable
repositories. The recorded image ID/inventory describes a specific build.
Fresh environment rebuilds and .deb bytes are not claimed to be reproducible.
Pinned snapshots, repository preparation, shared-library metadata,
image recipes, signing and release publication remain subsequent stages.

Run host contract checks with `python -m unittest discover -s tests`.
The UI foundation recipe must also pass a real container package build.
Inspect/install that package in a disposable Debian environment and compile
the separate DE consumer to verify the exported CMake contract.

The runtime acceptance recipe is `tests/fixtures/runtime.json`. It builds a small
Qt Core executable from Builder's own HEAD and verifies automatic dependencies.

## Several components from one source snapshot

```sh
karyo-builder package-set examples/shell.json examples/lock.json examples/style.json examples/session-entry.json examples/session.json --image karyo-builder:trixie --output out/session
```

package-set accepts the same schema-1 recipes. All inputs must use one source
repository, one CMake directory and one resolved commit, with distinct package
names. HEAD is resolved once at the start; different references are accepted if
they identify that same commit. An explicit --source/--revision applies to all
recipes. Mixed commits/directories and duplicate package names fail before build.
Recipe and runner hashes describe their captured bytes, including when a file
changes while a long build is running.

The native runner configures, builds and runs CTest once, then stages each
component separately. Each package retains its own dependency discovery,
conffiles, control metadata, DEB, checksums and manifest. Shared directories are
allowed; colliding file ownership or file/directory prefixes abort the whole set.
The result directory is published only after every component succeeds.

A successful karyo-package-set-* directory contains a shared build.log,
environment/distribution records and a root manifest/checksum list. Named
subdirectories contain the individual package records. Their manifests reference
the shared log by path and hash; the root manifest hashes each package manifest.
Keep that directory together for complete build evidence. A failed set remains
under .failed-* with diagnostics and is never published as a successful set.
The original package command retains its single-package output layout.

Run the real single/set/native-execution/collision acceptance fixture on each base:

```sh
python tests/acceptance/check-package-set.py --image karyo-builder:trixie --output out/check-package-set-debian
python tests/acceptance/check-package-set.py --image karyo-builder:ubuntu2604 --output out/check-package-set-ubuntu
```

The fixture uses a short-lived local Git repository with public test content.
It executes the unpacked native ELF as an unprivileged user in an isolated
matching image, checks per-package conffiles/dependencies and verifies that a
colliding component produces no published result. It does not modify host APT.

## Explicit package lifecycle scripts

A package may opt in with a package.maintainer_scripts object, for example:

```json
"maintainer_scripts": {
  "postinst": "profiles/package/postinst",
  "prerm": "profiles/package/prerm"
}
```

Only preinst, postinst, prerm and postrm roles are accepted. Values are canonical
relative paths inside the captured Git repository, independent of the CMake
build.directory. Absolute/parent/noncanonical paths, inline commands, symlinked
files or parents and hardlinked inputs are rejected. Each input must be a single
regular UTF-8 file of at most 64 KiB, with LF line endings and a literal
#!/bin/sh first line. All inputs are validated before control staging. Scripts
are copied verbatim as executable control files; the build does not run them.
The original ban on a CMake payload supplying its own DEBIAN directory remains.

The native receipt and final manifest include each selected role, source path,
byte count and SHA256 alongside the immutable Git/source archive and complete
DEB hash. Recipes omitting the optional mapping keep their original behavior
and receive an empty script record. Existing data-only/runtime recipes do not
automatically acquire lifecycle behavior.

Maintainer scripts are trusted package source code. dpkg runs them during actual
installation/removal, normally with root privileges. Their authors must implement
idempotent upgrade/failure handling and disable integration references before
removing the referenced executable. Builder validates source/staging provenance;
it does not turn arbitrary script behavior into safe product policy. In
particular, global PAM hook enable/removal still needs its own native acceptance.

Host tests pass 38 cases (one Windows symlink case is explicitly skipped); all
nine maintainer input/staging cases pass on real Debian and Ubuntu filesystems.
A disposable native fixture package then passes installation/removal on both QA
guests. Its four declared scripts execute in order (preinst install, postinst
configure, prerm remove, postrm remove), leave no payload/event file after cleanup
and preserve passwd/shadow/group/common-password bytes. No PAM hook or service is
enabled by that fixture. Evidence is under out/{debian,ubuntu}-vm-qa/results/
maintainer-native.log and out/migration/maintainer-{debian,ubuntu} manifests.
