# Native console reservation primitive

Exact account runtime source: afdcbbd793072d94bd3f5435471434cd13df3a90.
The public switch helper remains existing-session-only; this primitive does not
yet launch or terminate complete desktop units or configure any network.

## Exact native inputs

### Debian

- Output: out/migration/profile-consoles-debian/karyo-profile-accounts-20261121T132840Z-7dd3f0c2.
- Source archive SHA256: a05bdb40bc6e9671ec349f8f1b4aae94207998c778a2e6aae68512f1f92359b5.
- DEB SHA256: 08b5ee263a295e9030406668865c9e9f04a619fbae6d98d0a49d654e1a3da167.
- Final native probe SHA256: b874e527ff49161efff5955af8a367f7fea50cdc996621dfd68fa5e08b0274f9.

### Ubuntu

- Output: out/migration/profile-consoles-ubuntu/karyo-profile-accounts-20261121T132839Z-a49d8139.
- Source archive SHA256: a05bdb40bc6e9671ec349f8f1b4aae94207998c778a2e6aae68512f1f92359b5.
- DEB SHA256: 9b8b63f3931ad69042acae8265ecc4ceb37c49f5875dd109e6cc56d7a83c48e8.
- Final native probe SHA256: b874e527ff49161efff5955af8a367f7fea50cdc996621dfd68fa5e08b0274f9.

## Behavior and evidence

All 143 profile regressions pass on native Debian/Ubuntu, as root with three
role-specific skips and UID 65534 with 42 skips. Cases cover all-session/closing
console owners, malformed inventory, the total deadline, kernel state parsing,
full/partially occupied pools, a new owner after open, active/lost reservations,
caller failure cleanup, released-lock/lease rejection and fixed native devices.

Exact independent account packages install no-remove without changing accounts,
common PAM or default manager; dpkg checks are clean and forged SSH callers
remain denied. The fixed installed probe opens native TTYs under ConfigStore
lock while main VT8 stays active. Logind owns VT8; kernel initially marks 1/6/8
busy. First lease holds VT9, the nested allocator chooses VT10, both descriptors
are close-on-exec and verify against live logind/kernel state. After closing
them the busy set returns to 1/6/8, the same graphical session remains active,
and original passwd/shadow/group/common-PAM bytes are unchanged. Released lease
verification is refused. No VT activation, mode change, reset or deallocation
is performed. Probe and production code use only the reviewed Linux UAPI.

The first Ubuntu probe failed an assertion that expected the busy bit to clear
synchronously after close. A subsequent read found the original mask restored
and zero open descriptors for VT9/10. The corrected fixture polls for at most
two seconds without changing any console. Both kernels then report about 5 ms
settling for the inner release (Debian 5.138 ms, Ubuntu 5.079 ms), and immediate
final restoration. This is an acceptance-fixture correction, not weakening the
allocator: production continues treating any reported busy console as occupied.
The original failure is preserved as profile-consoles-first-native.log.

The complete native probe is public as DE profiles/tests/installed-consoles.py.
Logs: out/{debian,ubuntu}-vm-qa/results/profile-consoles-*. The Ubuntu diagnostic
after-failure log records kernel 7.0.0-43-generic, unchanged active VT8, owners
[8], original busy set and zero relevant descriptors. Source UAPI reference and
its read-only downloaded copy are retained in local migration evidence.

The lease is cooperative allocation, not a barrier against another privileged
administrator selecting a fixed console. The forthcoming unit controller must
revalidate before handoff and prove its own resulting unit/session. Complete
owned startup/teardown and isolated profile networking remain required. All
changes are local; no push, owner-system, donor or Forge mutation is performed.
