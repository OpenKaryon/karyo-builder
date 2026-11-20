# Package stage and UI integration validation

Validated on 2026-11-20. This record covers the two DE development packages,
the installed Python CLI and automatic dependencies for native executables.
Full session/greeter integration and ISO stages remain later milestones.

## Sources and build environment

- DE source: `cef9c92`, including public `karyo/ui` headers and `Karyo::Ui`.
- Builder uses the `src/karyo_builder` layout and its installed console command.
- Recipes follow their source repository HEAD and record the resolved commit.
- Debian 13 amd64, Qt 6.8.2, GCC 14.2.0, CMake 3.31.6, Ninja 1.12.1.
- Environment: `environments/debian13/Dockerfile`, including Qt SVG.
- Docker image ID:
  `sha256:53b1763dffbae6dee245978bf42b55733f2d482a4bc056e56c57e7778b25b410`.

Install Builder into a virtual environment before these commands. The
acceptance run checks both editable development installation and a normal
wheel installation. Unit tests import the installed package, with no root-level
import directory masking packaging mistakes.

## Commands and results

```sh
python -m pip install .
python -m unittest discover -s tests -v
docker build -t karyo-builder:trixie environments/debian13
karyo-builder package examples/ui-foundation.json --output out/desktop-acceptance
karyo-builder package examples/desktop-integration.json --output out/desktop-acceptance
karyo-builder package tests/fixtures/runtime.json --output out/runtime-acceptance
```

All seven host tests pass. They cover recipe/path validation, default HEAD and
explicit tag selection, absent input, unsupported ELF ABI and ordinary
data/static objects. Both Qt test targets pass: theme/painting and desktop
entries/icons. The latter preserves qualified/profile application-ID behavior
and covers current-desktop MIME defaults and embedded icon rendering.

Install both development DEBs into a disposable container, compile
`tests/desktop-consumer` through the installed CMake packages and run it
offscreen. The consumer locates static resources and renders the Files icon.
Only `/usr/include/karyo/ui` is installed. Removing the integration package
leaves the foundation headers/archive usable by its separate consumer.
Then removing the foundation package succeeds.

The native Qt Core fixture starts with an empty explicit dependency list.
dpkg-shlibdeps derives libc6, libgcc-s1, libqt6core6t64 and libstdc++6.
A clean `debian:trixie` container installs the DEB through APT, resolves those
dependencies, runs the executable (reporting Qt 6.8.2) and removes the package.
Staging follows Debian's package-directory convention before symbol analysis.

An empty install component was also tested end to end. It retains a failure log
without publishing a successful result directory, including an output path
containing spaces.

## Captured artifacts

These hashes describe the acceptance runs. Subsequent HEAD changes produce
their own source/export identity, timestamps and manifests.

| Package | Bytes | SHA-256 |
| --- | --- | --- |
| karyo-ui-foundation-dev_0.1.0-1_amd64.deb | 43220 | bdf8cf1d869c7db611ab3af8d6e213bbf04ff8f63aedab018ec60afbe601352c |
| karyo-desktop-integration-dev_0.1.0-1_amd64.deb | 77260 | ffd9fa8bc794e0657bb8869123be8be5979f53cb5a5d7d8c291484267c995812 |
| karyo-builder-runtime-check_0.1.0-1_amd64.deb | 2936 | bbe0594e46a4b08aacfc58e96f8f2b7ca213e19fdec06533a7a233466b046ccf |

Build directories contain build.log, manifest.json, environment.json,
dependencies.json and SHA256SUMS. The clean-runtime acceptance also retains
runtime-install.log. Installed-consumer checks run in isolated containers.

One measured initial foundation build took 8.414 seconds: external host
commands accounted for 8.355 seconds and host Python work between commands
for 0.058 seconds. This measures the small current component and supports
retaining Python for orchestration. Broader scale needs separate measurements.

## Next slice

Shared widgets, Qt style and session entry preparation have since passed the
checks recorded in [VALIDATION_WIDGETS_SESSION.md](VALIDATION_WIDGETS_SESSION.md).
Continue the shell/lock and platform/session boundaries. Newly
introduced shared-library packages need their own symbols/shlibs policy.
APT repository preparation, selectable Debian session, existing display-manager
coexistence and the two ISO editions need subsequent acceptance.
Forge remains an external package input maintained by its separate agent.

## Standalone session follow-up

The shell, PAM/Wayland lock and runtime bundle are now implemented and tested.
See [VALIDATION_SESSION.md](VALIDATION_SESSION.md) for package, clean runtime,
configuration upgrade and actual headless compositor acceptance, plus retained
hardware/display-manager gates.
