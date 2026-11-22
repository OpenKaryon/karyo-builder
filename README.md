# Karyo Builder

Karyo Builder is the planned configuration-driven build tool for Karyo Linux
and Karyo Workstation. It will build native packages, prepare a package
repository and produce installation images from versioned configuration.

**Status: first package stage implemented.** The CLI exports a Git revision,
builds/tests native CMake components in isolated Debian 13 or Ubuntu 26.04
containers and produces DEBs with logs, input hashes and a build manifest. Runtime ELF
dependencies are calculated with Debian's dpkg-shlibdeps.
A separate source-package stage builds checksummed distribution DSCs with ordered
quilt patches using native packaging and upstream checks. See
[the source-stage contract](docs/SOURCE_PACKAGE_STAGE.md).
A separate [source-snapshot preparation](docs/SOURCE_SNAPSHOT_STAGE.md) captures
exact recursive public Git trees and explicitly inventories/materializes LFS
inputs before native packaging.
See [the package-stage contract](docs/PACKAGE_STAGE.md) and
[reviewed migration inventory](docs/MIGRATION.md).

The image YAML and full-build commands below remain design examples.
APT repository preparation and ISO stages are subsequent work.

```sh
docker build -t karyo-builder:trixie environments/debian13
# Optional standalone-DE compatibility target:
docker build -t karyo-builder:ubuntu2604 environments/ubuntu2604
python -m venv .venv
# Activate .venv, then install this checkout.
python -m pip install -e .
karyo-builder package examples/ui-foundation.json --output out
# One build/test pass for several components from the same source commit:
karyo-builder package-set examples/shell.json examples/lock.json examples/style.json --output out/session
```

Package builds use the source repository's current `HEAD` by default. A release
tag can be selected later with `--revision`. The manifest records the resolved
commit for each build.

Own executable code is GPL-3.0-or-later. Working prototype code is reused after
review and adapted to the product boundaries described in CONTRIBUTING.md.

## Project boundaries

| Repository | Responsibility |
| --- | --- |
| [karyo-de](https://github.com/OpenKaryon/karyo-de) | Desktop shell, applications, Settings, themes, session integration and native desktop packaging |
| [karyo-linux](https://github.com/OpenKaryon/karyo-linux) | Distribution configuration, package selections, usage presets, installer settings and edition recipes |
| [karyo-builder](https://github.com/OpenKaryon/karyo-builder) | Shared build orchestration, isolated build environments, package/repository/image stages, validation and artifacts |

Karyo Linux remains Debian-based. The first supported build target is Debian 13
on amd64. Installing Karyo DE on other distributions is a separate desktop
portability effort; multi-base image generation is not an initial requirement.

Karyo Workstation is an edition recipe using the same builder as the standard
Karyo Linux image. Organization-specific additions can live in a separate
configuration overlay. Both editions must be buildable through the documented
public tool rather than depending on unpublished orchestration scripts.

## Goals

- Build both Karyo installation images through one supported entry point.
- Describe package selections and system configuration in reviewable YAML.
- Build custom packages from explicitly selected source revisions.
- Accept packages from configured repositories and explicit local inputs.
- Prepare an APT repository for the image and release workflow.
- Produce build manifests, checksums, logs and validation results with images.
- Reuse existing distribution tooling and package managers.
- Support local development and CI through the same build interface.

Karyo Builder is a build-time tool. Installed systems continue to use their
normal package manager. A new package manager, custom kernel, runtime switch
between distribution bases and immutable OS update mechanism are outside the
initial scope.

## Intended build workflow

```text
Edition recipe + pinned sources + package inputs
                         |
                         v
               Resolve and validate inputs
                         |
                         v
                 Build custom packages
                         |
                         v
              Prepare package repository
                         |
                         v
          Assemble configured installation image
                         |
                         v
                Validate and export artifacts
```

Use isolated, supported build environments. The initial Debian implementation
should reuse Debian package tooling and live-build. Image construction and
package installation can require privileges inside those environments; do not
silently install build dependencies or change services on the developer's host.

Keep orchestration independent of edition-specific defaults. A Workstation
recipe should select features and configuration without copying the build
pipeline. Existing build tools will be reviewed and moved here incrementally.

## Illustrative configuration

The initial schema will be defined during implementation. The following sketch
shows the desired separation of base, desktop, usage presets and extra inputs:

```yaml
schema: 1
name: karyo-workstation

base:
  distribution: debian
  release: trixie
  architecture: amd64

desktop: karyo

presets:
  - development

packages:
  install:
    - git
    - podman
  local:
    - ./packages/*.deb

desktops:
  - name: Personal
  - name: Work

output:
  format: iso
```

The schema must eventually define source revisions, repository origins,
package versions/checksums, overlay precedence and path resolution. Resolve
recipe-relative paths from the recipe directory. List the selected local files
and their hashes explicitly in the build manifest.

Desktop entries above express desired configuration. Account ownership,
first-boot provisioning and credentials need a separate, explicit contract.
Credentials and signing keys are external inputs, never baked into public
examples, build manifests or installation images.

Usage presets are optional and combinable: Everyday, Development, Science &
data, and ML & AI. Bioinformatics is a Science & data specialization. The
distribution defines the preset catalog; the builder consumes its system
selections. Exact research and ML dependencies belong in project environments
rather than the system Python installation.

## Proposed command interface

```sh
karyo-builder build path/to/karyo-linux.yaml
karyo-builder build path/to/karyo-workstation.yaml
```

The CLI should also expose validation and individual package, repository and
image stages. Stage names and options will be finalized alongside the schema.
Document prerequisites, required privileges, network use, cache locations and
output locations before declaring the tool usable.

## Build records and outputs

Each completed build should export the ISO or selected stage artifact, package
inventory, source revisions, configuration identity, input hashes, logs,
checksums and validation results. Release signing should use an explicit
external signing configuration.

Record mutable upstream inputs and provide a path to pinned repository
snapshots. Fixed Git revisions alone do not make an image reproducible when
package repositories change. Treat bit-for-bit reproducibility as a measured
goal, not a property of the initial implementation.

Cache reuse must account for relevant inputs and toolchain versions. Failed
stages must report errors clearly and must not publish incomplete release
artifacts. Keep local testing separate from deliberate release publication.

## Implementation roadmap

| Stage | Deliverable | Acceptance |
| --- | --- | --- |
| 0 | Architecture, scope and repository boundaries | This planning document; no claim of a working builder |
| 1 | Inventory existing build tools and define configuration/CLI contracts | Every migrated tool has an owner, inputs, outputs and prerequisites; initial schema validation is documented |
| 2 | Reusable build environments and native package stage | Build selected desktop/system packages from pinned revisions without modifying the host system |
| 3 | APT repository preparation and local package ingestion | Validate origins, versions and checksums; reject missing or conflicting inputs; verify repository metadata |
| 4 | Standard Karyo Linux image recipe | Build and boot the standard ISO through the public CLI |
| 5 | Workstation recipe and supported configuration overlays | Build and boot the second ISO through the same pipeline, with edition differences declared in configuration |
| 6 | Local/CI parity, manifests, caching and release checks | Fresh builds and relevant upgrade tests pass; artifacts and provenance are retained |
| 7 | Cut over and retire old orchestration entry points | Both images build using the documented tool without hidden script dependencies |

Package and ISO smoke checks accompany each stage. Validate image boot,
installation and the installed system in isolated test environments. Cover
both edition recipes before replacing the existing production build path.
Additional base distributions and a larger plugin architecture come only after
the initial Debian workflow is reliable.

## Migration and contribution conventions

Bring existing build tools across as focused, reviewable changes, preserving
necessary upstream attribution and checking redistribution terms. Reuse working
implementations where suitable and adapt them to the agreed boundaries.
Do not import private repository history, organizational credentials or
machine-specific build paths.

Use English commit subjects and two substantive English body paragraphs that
explain the problem, resulting behavior and relevant validation. Include an
accurate `Co-authored-by` trailer for assisted changes. Aim for substantive,
focused implementation commits, typically at least 100-200 changed lines, with
an upper budget of 2,000-3,000 hand-maintained code lines. Generated files and
JSON may exceed that budget and should be separated where practical.

The code license is GPL-3.0-or-later (see LICENSE). Preserve each dependency's
own licensing and attribution when adding subsequent components.

## Standalone DE compatibility builds

The native package stage accepts Debian 13 (trixie) and Ubuntu 26.04 LTS
(resolute), verified from the complete os-release identity before configuration.
Use --image karyo-builder:ubuntu2604 for the Ubuntu environment; keep outputs
separate because dependency versions and native ABIs follow the selected base.
The manifest records that identity as well as the immutable Docker image ID.
Karyo Linux ISO recipes remain Debian-based; this does not create an Ubuntu ISO.

The optional `examples/greeter.json` recipe builds the Karyo greetd frontend.
Installing it does not change the current display manager. greetd/cage setup is
an explicit administrator integration; its example and instructions install under
`/usr/share/doc/karyo-greeter`. The session bundle does not depend on this frontend.


The optional examples/profile-host.json recipe packages the root-only systemd
host profile transport separately from account helpers and controlled PAM entry.
It starts/enables nothing on installation. Current public helpers are unchanged;
see docs/VALIDATION_PROFILE_HOST.md for the accepted native peer gate and remaining
persistent runtime/startup integration.


`examples/profile-clipboard.json` builds optional volatile clipboard sharing for
trusted Karyo desktop families. It installs no enabled service; administrators
opt in separately from profile network isolation. Actual Debian/Ubuntu Wayland
Home/Work acceptance and limits are recorded in
[family clipboard validation](docs/VALIDATION_FAMILY_CLIPBOARD.md).


`examples/xclipboard.json` packages the optional ordinary X11/Wayland clipboard
adapter independently of VMware daemons and profile accounts. The extended test
environments are environments/clipboard-debian13 and clipboard-ubuntu2604. See
[X11/Wayland validation](docs/VALIDATION_XCLIPBOARD.md) for installed native results
and the remaining VMware host-channel boundary.


`examples/vmware-session.json` prepares the optional native-session VMware
coordinator and its ordinary worker policy. The separate QA environments under
environments/vmware-* exercise its channel lock and process lifetime without
privileges. See [VMware source/package validation](docs/VALIDATION_VMWARE_SESSION.md)
for accepted source and installed Home/Work coordinator checks and the remaining
host-payload and privileged file-transfer gates. Actual joined GUI lock acceptance
is recorded separately in [VMware lock validation](docs/VALIDATION_VMWARE_LOCK.md).

The optional VMware display worker's installed activation-time acceptance and
remaining host-resize boundaries are documented in
[VALIDATION_VMWARE_DISPLAY.md](docs/VALIDATION_VMWARE_DISPLAY.md).


The generic Win32 hidden-owner palette/minimize compositor slice now has native
Debian/Ubuntu before/after, four-palette and normal/startup-lock protocol evidence.
See [VALIDATION_WIN32_OWNED_WINDOWS.md](docs/VALIDATION_WIN32_OWNED_WINDOWS.md) for exact packages, the retained Ubuntu API/XID
fixture corrections and the still-open real Wine runtime/installed upgrade gates.


Real Wine32/Wine64 owned-palette and focus acceptance is now recorded separately
in [VALIDATION_WIN32_PALETTES.md](docs/VALIDATION_WIN32_PALETTES.md), including
native wlroots lifecycle fixes, unchanged ABI and the remaining toolkit/styling
and installed-upgrade boundaries. The reproducible driver is
`tests/acceptance/check-win32-palettes.py`.


The later [unmapped-owner validation](docs/VALIDATION_WIN32_UNMAPPED_OWNERS.md)
records both framework layouts, exact native compositor/library pairing and
actual refusal/recovery of an unpaired dpkg installation. The optional
`--verify-library-dependency` gate uses the driver's copied native installer.


The installed launcher also preserves existing native prefix architecture;
[the before/after report](docs/VALIDATION_WIN32_EXISTING_PREFIX.md) distinguishes
Debian win32 reuse from Ubuntu PE32-on-WoW64 and from pending legacy import.


The native Wine caption patch now passes real displayed-frame and GDI pixel
checks on both bases; see [the source/runtime report](docs/VALIDATION_WINE_CLOSE_BUTTONS.md).
The optional caption QA script needs Pillow; the Builder CLI remains standard-library-only.
