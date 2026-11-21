# Native package-set acceptance

Observed on 2026-11-21 UTC with tests/acceptance/check-package-set.py. These
small sources are public acceptance fixtures, not a DE or distribution image.
The fixture creates a short-lived Git repository from tests/fixtures/runtime.
Actual DE multi-package VM acceptance remains a separate gate.

| Base | Fixture source commit | Immutable native image |
| --- | --- | --- |
| debian | ad0315fb6b6670010bafe42cecf7ccc0045cca96 | sha256:f5abf68140a71f3abffbdeac454e883bd9d71fa71bc10f42da648ae3f190dd20 |
| ubuntu | ee26e0f82e762dd72eaaabe8c98286a6cf188a49 | sha256:241fbca9fd2091251c6e54232817874551e75792f7ef459cc36e73ac2fdadbf3 |

Both native bases passed:

- Legacy package invocation and its existing artifact/manifest layout.
- package-set with one Git snapshot, one CMake build and one CTest invocation.
- Independent runtime and documentation DEBs, manifests and checksum records.
- Native Qt Core dependency discovery for the executable; no ELF dependencies
  for the data-only component.
- Runtime conffiles registered while documentation remains outside conffiles.
- Actual unpacked ELF execution as uid 65534 in the matching native image.
- A deliberately colliding component rejected without a published package set;
  diagnostics and partial artifacts stay in the hidden failed directory.
- Parent and child manifest hashes, artifact hashes and shared build-log hashes.

The first inspector used Docker's default noexec temporary mount and could not
execute its unpacked fixture. That attempt is not acceptance. The corrected
inspector explicitly permits execution only in its disposable tmpfs, while
remaining unprivileged, capability-free, read-only and without networking.

The host suite has seventeen passing tests, including a moving-HEAD simulation,
real local Git references, immutable captured recipe bytes, incompatible input
sets and file/directory ownership conflicts. The fixtures do not need credentials,
remote repositories or changes to host APT. Source/image/package records and
logs are retained locally under ignored out/migration/package-set-*.
