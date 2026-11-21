# Installed public desktop profile command

Exact DE source: bf831b069749654aaad232dbc7ea24ae2141c24b.

The native profile-accounts build is independent of Qt and does not rebuild
or change shell/session-entry. It installs the public karyo-desktops frontend
alongside the existing fixed polkit helpers. No stopped session is implicitly
started; switch retains exit 3 for that case.

## Exact inputs

### Debian

- Output: out/migration/profile-frontend-debian/karyo-profile-accounts-20261121T121653Z-770e5b67.
- Source archive SHA256: 1e257724205aca8d0068ff1e28252d697018de697ae95e63bf628e49f0bca041.
- DEB SHA256: 505d01f6f5f7a4bd8dca61847f03ac545eb5442bcd3d808f284d738863100626.

### Ubuntu

- Output: out/migration/profile-frontend-ubuntu/karyo-profile-accounts-20261121T121654Z-1872dea8.
- Source archive SHA256: 1e257724205aca8d0068ff1e28252d697018de697ae95e63bf628e49f0bca041.
- DEB SHA256: d9f20b6d53ab4ced0cae13fe600b13cab0e48ab4f676ee56f46527d3c545509f.

## Acceptance

All 129 profile cases pass natively on Debian 13 and Ubuntu 26.04 as root
(three role-specific skips) and UID 65534 (42 skips). Regression coverage
rejects arbitrary commands/owners/paths, inappropriate stdin modes and option
abbreviation. A real isolated launcher ignores hostile cwd, PYTHONPATH and
PYTHONHOME and writes no bytecode. Independent CMake staging installs it in
the public binary directory and passes the same accounts suite.

Both native DEBs install with no-remove, after SHA verification. Original
passwd/shadow/group/common-PAM bytes and the default manager are unchanged;
dpkg verification and audit are clean. Native policy binds only the fixed
root helpers. A forged SSH caller remains denied independently of environment.

The positive check uses real LightDM GUI sessions and actual Terminal windows
launched by the real shell panel. In those terminals, installed karyo-desktops
list --json returns exactly the current karyoqa family at VT8, and switch
karyoqa returns changed=false. Native pkexec is reached by exec, preserving
the caller cgroup/login session and exact helper JSON/exit result. SSH graphical
rendering helpers do not substitute for this caller proof.

Known QA script and output JSON files are removed after assertions; QA users
are signed out and LightDM remains active. No product account is added or
password changed. Logs: out/{debian,ubuntu}-vm-qa/results/profile-frontend-
install.log and profile-frontend-positive.log; exact inputs are in the
profile-frontend-input stages.

This closes installed public-CLI and current-desktop noop acceptance only.
Two different live profiles, shell menu wiring, owned stopped-session startup,
network/DNS/VPN isolation and family clipboard remain separate required gates.
Nothing is pushed; private donor, Forge and owner systems remain untouched.
