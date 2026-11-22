# Native source-package stage

The source-package command captures a Debian 3.0 (quilt) source and an ordered
list of reviewed patches, then builds the distribution's native binaries.
This is intended for compositor integrations that must follow each base's
labwc/wlroots ABI. It does not replace the CMake package/package-set commands.

Prepare a local Linux amd64 environment with the source's native build
dependencies. The minimal examples are environments/source-debian13 and
environments/source-ubuntu2604; a product-specific image can extend them.
Dependency preparation and downloading sources happen before the isolated
build. Neither host APT nor installed desktop services are changed.

Example schema (paths are relative to this JSON file; fill actual SHA256s):

    {
      "schema": 1,
      "source": {
        "name": "labwc",
        "version": "0.8.3-1",
        "dsc": {"path": "labwc_0.8.3-1.dsc", "sha256": "<64 lowercase hex>"},
        "archives": [
          {"path": "labwc_0.8.3.orig.tar.gz", "sha256": "<64 lowercase hex>"},
          {"path": "labwc_0.8.3-1.debian.tar.xz", "sha256": "<64 lowercase hex>"}
        ]
      },
      "patches": [
        {"path": "layout.patch", "sha256": "<64 lowercase hex>"},
        {"path": "snapshot.patch", "sha256": "<64 lowercase hex>"}
      ],
      "build": {
        "revision": "karyo1",
        "distribution": "trixie",
        "maintainer": "Karyo Developers <developers@openkaryon.invalid>",
        "message": "Add reviewed desktop protocol integrations.",
        "binaries": ["labwc"],
        "source_date_epoch": 1795215210
      }
    }

Only exact fields are accepted. The supported targets are Debian 13/trixie
and Ubuntu 26.04/resolute. Native amd64 remains the default; build.architecture
can explicitly select i386 with a matching Linux386 image. Archives are tar.gz/xz/bz2/zst parts of the
selected DSC; native source and non-quilt formats are outside this stage.
Expected binaries are a required subset: automatically generated debug packages
and other native outputs are retained too. The resulting version appends a plus
and revision to the complete native source version.

Run python -m karyo_builder source-package recipe.json --image IMAGE --output out
with PYTHONPATH=src, or use the installed karyo-builder entry point. Jobs default
to two and are limited to 1 through 8.

## Input and output contract

All source parts and patches are captured before executing Docker. Each captured
SHA256 must match the recipe. DSC identity/format and its complete SHA256/size
table must exactly match the captured archives. Unsafe/duplicate filenames,
symlinks, missing/extra archives, changed inputs and invalid metadata fail.
Clearsigned DSC fields are parsed, but this is not signer authentication.
Obtain inputs and expected hashes through trusted signed APT metadata or another
authenticated source. Source, patches, packaging and the build image are trusted
executable build inputs; Docker is isolation, not a hostile-code security boundary.

The CLI resolves an existing local image to an immutable Linux amd64 ID. It
does not pull images. The runner has no network, capabilities or privileged mode,
a read-only input mount, one writable output mount and bounded CPU/memory/process
resources. It checks the exact native base before extraction. No credentials or
Docker socket are mounted.

dpkg-source extracts with strong checksums enabled. Ordered patches are appended
under unique karyo-* names to the native quilt series and applied with zero fuzz.
Native changelog identity is verified before adding a deterministic downstream
entry. dpkg-buildpackage runs the source's normal binary packaging with fakeroot,
including its configured upstream checks; Builder does not request nocheck or
rewrite native control dependencies/licenses. Actual debhelper rules remain
authoritative: an upstream package may itself have no test target.

Success retains all DEBs/DDEBs, buildinfo/changes records, original/resolved
recipes, environment inventory, log, runner hashes, artifact hashes/sizes and
actual binary metadata. The host checks receipt version, patch order, package
mapping, native base and every artifact before atomically publishing a unique
karyo-source-package-* directory. Failure retains a hidden .failed-source-* with
diagnostics and publishes no successful result. Recipes and runner bytes are
captured even if their live files later change.

Environment preparation uses mutable distribution repositories; its image ID
and package inventory are recorded. Bit-for-bit reproducibility, signer trust,
repository publication, package installation and upgrade/rollback policy are
separate responsibilities.

## Validation

Host unit tests reject corrupted/ambiguous input and inconsistent receipts.
Run python -m unittest discover -s tests.

The acceptance fixture uses a real quilt source with two order-dependent patches.
It builds and executes the native ELF as UID 65534, requires proof that the
upstream check target actually ran, verifies native build records and refuses a
reversed patch sequence or foreign distribution without publishing output:

    python tests/acceptance/check-source-package.py --image karyo-source-builder:trixie --distribution trixie --output out/check-source-debian
    python tests/acceptance/check-source-package.py --image karyo-source-builder:ubuntu2604 --distribution resolute --output out/check-source-ubuntu

Both native fixtures passed on Debian 13 and Ubuntu 26.04. The source-input unit
suite also passed inside both matching Linux images as UID 65534, including
real symlink rejection. These fixtures establish the stage contract; a product's
patched compositor still needs its own native build and session acceptance.


## Native source architecture selection

Existing recipes retain their amd64 meaning and their original captured bytes.
An optional build.architecture accepts amd64 or i386. The host checks the local
immutable Docker image architecture (amd64/386); an image mismatch fails before
creating a native build job. The runner independently checks dpkg's native
architecture before extraction and verifies every binary's architecture/version.
Receipts and manifests record the target; i386 receipts require explicit package
architecture metadata. Architecture-independent all packages remain allowed.
Legacy amd64 receipts retain their previous compatibility behavior.

This selects a native userspace, not a cross compiler, emulated Windows machine
or new target for the CMake/vendor packaging stages. For the Debian native SDK:

    docker build --platform=linux/386 -t karyo-source-builder:trixie-i386 environments/source-debian13-i386
    python tests/acceptance/check-source-package.py --image karyo-source-builder:trixie-i386 --distribution trixie --architecture i386 --output out/check-source-i386

The same real quilt fixture now checks the actual DEB architecture and ELF
class/machine, executes its patched binary as UID65534, proves upstream checks
ran and rejects reversed patches, a foreign base and a foreign image architecture.
Native Debian i386, Debian amd64 and Ubuntu amd64 all pass. These checks establish
the source stage; matching32-bit Wine installation has its own product gate.
Ubuntu's Wine WoW64 runtime uses its native amd64 SDK; no Ubuntu i386 SDK is
claimed by this acceptance.

All50 Builder regressions also pass in ordinary-user Debian/Ubuntu amd64 and
Debian i386 QA containers, including native symlink cases. The first full-suite
runs in minimal SDKs lacked Git and failed four Git-based fixtures; those logs
remain. Separate QA derivatives add Git, and unchanged assertions then pass on
all three targets. Product/host packages and existing source SDK images remain
unchanged; source builds need no Git or network after input capture.
