# Optional profile account helpers: native acceptance

The low-level account runtime is optional. It does not install a production PAM
profile, enable a service, create users on installation or replace the display
manager. Full protected desktop sessions and network/clipboard isolation remain
separate migration gates. Forge and owner machines are not part of this QA.

## Source and tests

Creation/polkit runtime source: 37da8de7603ea97eda68d26c6f10d676858b4017.
Cache-free launcher source: 348ae18a1db81fe085436f7f603da94af0da4849.
Both native Qt bases pass all 68 full DE CTests. The independent profiles CMake
project runs the same Python suite without compiling Qt applications. Its final
85 cases pass on Debian 13 and Ubuntu 26.04 as root (three role-specific skips)
and UID 65534 (42 root-fixture skips). A real isolated Python interpreter ignores
hostile cwd, PYTHONPATH and PYTHONHOME and writes no bytecode.

The independent and complete DE CMake projects stage identical account payloads
on both bases. An earlier whole-project package attempt was deliberately stopped
before publication when that unnecessary Qt rebuild was identified; the final
account recipe uses build.directory=profiles.

## Exact native artifacts

### Debian

- Source: 37da8de7603ea97eda68d26c6f10d676858b4017.
- Output: out/migration/profile-accounts-debian/karyo-profile-accounts-20261121T090604Z-aa6f5089.
- DEB SHA256: f329f81077263c8b1dd30ded18b8a0239439c4941fef99117a50a53550902811.
- Source archive SHA256: 65570810d9db88824df254d5938612e48d8a0a53ab908230f342d7986a0e33b6.
- Source: 348ae18a1db81fe085436f7f603da94af0da4849.
- Output: out/migration/profile-accounts-final-debian/karyo-profile-accounts-20261121T090858Z-54790827.
- DEB SHA256: 7c45695fb10ba6a45cb802fca3dbff06e6c424c1c654927b61ea0a3359723cf3.
- Source archive SHA256: c0eddc137853b47a38382a7b3733573f150d33f0c0dd1fba0864bab07e004b1d.

### Ubuntu

- Source: 37da8de7603ea97eda68d26c6f10d676858b4017.
- Output: out/migration/profile-accounts-ubuntu/karyo-profile-accounts-20261121T090607Z-4f90344c.
- DEB SHA256: 7d46a1b5da0bb5d7582fadbd1ec89d48da1b425ef184a1eb1ad66a8d700d204f.
- Source archive SHA256: 65570810d9db88824df254d5938612e48d8a0a53ab908230f342d7986a0e33b6.
- Source: 348ae18a1db81fe085436f7f603da94af0da4849.
- Output: out/migration/profile-accounts-final-ubuntu/karyo-profile-accounts-20261121T090854Z-2b1e189e.
- DEB SHA256: fef13336f81127f20b4c030567fa6c461f0339fa8c39c12461509e2e1bb9b4fa.
- Source archive SHA256: c0eddc137853b47a38382a7b3733573f150d33f0c0dd1fba0864bab07e004b1d.

## Installed behavior

Both disposable VMware guests install the exact base-specific DEB after verifying
the receipt and artifact checksums. The production org.karyo.desktops.add policy
is invoked through actual pkexec from Terminal launched by the real Karyo shell.
It creates two preflighted fixture children: a shared-password account and a
separate native YESCRYPT account. Root checks verify ownership, active expiry
state and password behavior, then remove only the newly captured test identities,
homes and unchanged metadata. The main account password hash stays unchanged.

A separate actual pkexec read-only identity probe accepts the active graphical
user on both hosts while root SSH with forged GUI variables is refused. Temporary
QA-only policy and launcher files are removed afterward. The installed account
helper also refuses direct root SSH without an authenticated PKEXEC_UID.

The final cache-free package then passes native upgrade, removal and reinstallation
on both guests. No package module/cache remains after removal. Checksums of
/etc/passwd, /etc/shadow, /etc/group and common-password remain identical through
that lifecycle, as does the configured display-manager link. dpkg verification
and audit stay clean; original LightDM remains active.

Local ignored evidence per out/{debian,ubuntu}-vm-qa/results:

- logind-native-stage.log and logind-native-gui.log;
- profile-accounts-install.log and profile-accounts-native.log;
- profile-accounts-upgrade-remove.log.

Input receipt/hash records are under the matching *-input QA directories. Native
source-overlay provisioning separately covers a child adding a sibling, safe
pre-activation rollback, already-active retention and untouched main credentials.
The global PAM hook, protected entry on every switch, network namespaces, DNS/VPN
and cross-session clipboard still require installed acceptance.

## Actual private PAM stack

The installed final helpers also pass a separate native PAM password-update
fixture on both guests. A small C client calls pam_chauthtok against a temporary
fixed-name service with native pam_unix.so yescrypt followed by pam_exec.so
seteuid and the installed desktop-password-changed executable. No plaintext
PAM token is exported to the synchronization helper.

All three fixture accounts, including the main account, are newly allocated.
Main-account changes propagate only to the shared child; a shared-child change
propagates back; a separate child remains independent. The installed desktop-sync
command passes too. Teardown restores original passwd/shadow/group/common-password
bytes exactly and removes the private PAM service, fixture users/homes/metadata
and QA binaries. Main QA login credentials are never changed. Both logs are
out/{debian,ubuntu}-vm-qa/results/profile-pam-native.log, with captured native ELF
and source hashes in the corresponding pam-input/record.json and SHA256SUMS.

The extended probe also sets an ordinary fixture real UID while retaining root
effective identity, matching a setuid password client. Both native PAM stacks
reject a wrong current password with every family hash unchanged, then accept
the correct current password and update only shared accounts. This executes
native pam_unix conversation/checking rather than a mock; it does not claim to
run the distro passwd binary or establish global pam-auth-update enable/removal.
A production enabled hook needs a maintainer lifecycle that disables the PAM
reference before removing its executable. No such global hook is enabled by
the optional low-level package in these tests.
