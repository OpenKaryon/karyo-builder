# First native package acceptance

Validated on 2026-11-20. Scope: the UI foundation development package and the
Builder package stage. The full DE session and ISO pipeline are later milestones.

## Inputs

- Donor Karyo prototype: `716d515b765319981b124fb1812a1e3edb9e0ffd`.
- Standalone DE source: `3bf0f5221f66347592286b0a755ff5ead96f07ee`.
- Recipe: `examples/ui-foundation.json`, schema 1, development component.
- Fresh environment built from `environments/debian13/Dockerfile`.
- Resolved Docker image: `sha256:fd5992eeaaed42873d9d8f8da955ae86594d84e72e14d434f26355007f20dc8f`.
- Debian 13 amd64, GCC 14.2.0, CMake 3.31.6, Ninja 1.12.1, Python 3.13.5.
- Host CLI also packaged as a wheel and installed into a disposable Python
  virtual environment. The installed console command performed the final build.

## Reproduction

```sh
python -m unittest discover -s tests -v
docker build -t karyo-builder:trixie environments/debian13
python -m karyo_builder package examples/ui-foundation.json --output out
```

All five host contract tests pass, including malformed metadata, unsupported
paths/schema and missing-recipe failure. The package stage passes CTest
theme/painting checks and dpkg-deb metadata/content inspection.

In a fresh container from the supported build image, with only the result and
DE consumer source mounted read-only:

```sh
dpkg -i /packages/karyo-ui-foundation-dev_0.1.0-1_amd64.deb
cmake -S /de/tests/consumer -B /tmp/consumer -G Ninja
cmake --build /tmp/consumer --parallel 2
QT_QPA_PLATFORM=offscreen /tmp/consumer/foundation-consumer
dpkg -i /packages/karyo-ui-foundation-dev_0.1.0-1_amd64.deb
dpkg --remove karyo-ui-foundation-dev
```

The independent consumer configures, links and renders successfully using
installed headers/CMake metadata. Reinstallation and removal succeed. Headers
and static library are removed, Qt development dependencies remain installed,
and the already linked static consumer still runs.

A real build with an absent install component exits unsuccessfully, retains
its failure log and publishes no successful artifact directory. This check
also uses an output path containing spaces.

## Artifact

- `karyo-ui-foundation-dev_0.1.0-1_amd64.deb`, 43,256 bytes.
- SHA-256: `b01ed71760fe0ca1505c3ebdfe69cbeaf15cad397ad8ec595499304b0cb8a589`.
- Source export SHA-256: `ecb324f61e8e71640dd59cc60e0e75f1054643dc4ea40abaf80c3fb09827ac8b`.

Every build directory contains build.log, manifest.json, environment.json and
SHA256SUMS. The local acceptance run also retains install-check.log.
This verifies a development package in disposable containers. Selectable DE
session, display-manager coexistence, runtime shlibs packaging, APT preparation
and both ISO editions need their own subsequent acceptance.

## Next slice

Extend reviewed shared UI components/resources and define runtime packaging,
then separate shell/session/lock from the optional greeter and OS defaults.
Extend Builder's package stage to compute runtime dependencies before publishing
ELF application packages. Add APT preparation after that contract is tested.
Keep Forge as an external package input under its own agent's ownership.