# Native package stage, schema 1

This is the first executable Builder stage. It builds one CMake install
component from a Git commit into a Debian 13 amd64 package. The edition/image
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
The default input is the source repository\'s current `HEAD`. The recipe only
needs `source.path`; `source.revision` is optional and defaults to `HEAD`.
Source paths resolve from the recipe directory. Use `--source PATH` to select
another repository. Later, `--revision v0.1.0` or `source.revision` can select
a release tag. Each build records the requested reference and its resolved
commit SHA in the manifest. HEAD means the checked-out Git state, with
working-tree edits excluded from the export.
The initial exporter rejects submodules until a complete pinned-input contract
for them is implemented. Git archive data is extracted with Python's data filter.

Only the exact JSON fields in the example are accepted. The package section
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
installed into staging. Metadata declared in the recipe is used directly;
this first stage targets development files with explicit dependencies.
Runtime ELF packages still require shlibs/substvars integration.

Each successful invocation publishes a new result directory containing the
Debian archive, SHA256SUMS, build.log and manifest.json. The manifest records
the resolved source revision, source archive hash/time, recipe hash and
resolved inputs, runner hash, Docker image ID, installed environment packages
and artifact hash/size. Directory names are unique, allowing concurrent builds
and preserving previous results. Failure retains a hidden .failed directory
with its logs and never publishes a successful result directory.

The environment Dockerfile initially resolves Debian packages from mutable
repositories. The recorded image ID/inventory describes a specific build.
Fresh environment rebuilds and .deb bytes are not claimed to be reproducible.
Pinned snapshots, repository preparation, runtime dependency discovery,
image recipes, signing and release publication remain subsequent stages.

Run host contract checks with `python -m unittest discover -s tests`.
The UI foundation recipe must also pass a real container package build.
Inspect/install that package in a disposable Debian environment and compile
the separate DE consumer to verify the exported CMake contract.
