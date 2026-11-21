# Installed account metadata policy acceptance

Runtime source: 2f263df059fd00dce52d3af72effb5d3c94b7b3b.
Only disposable Debian 13 and Ubuntu 26.04 VMware guests are changed.
All work stays local; Forge, donor and owner machines remain untouched.

## Native artifacts

### Debian

- Output: out/migration/accounts-policy-wave-debian/karyo-package-set-20261121T100651Z-cc6c645e.
- Source archive SHA256: eb68aa761026232278c9fc1bbab1c4c540d243c982da19e602ac976ee65dab6f.
- karyo-greeter 0.1.0-1 SHA256: 7a8e261e9a671aa75ec91757a1b083256798e3d808f10b38805dcbeaef397c79.
- karyo-settings 0.1.0-1 SHA256: 16f7c14f7a1cf7fb350972a1d44b2cfeb40f840d8b52de4e1a1e97e4bf6f71ac.
- Metadata fixture SHA256: 792a6db283555d0763b6e0fe7686462b8e1be1a557a28a8058a39d9180549a8e.

### Ubuntu

- Output: out/migration/accounts-policy-wave-ubuntu/karyo-package-set-20261121T100650Z-01cf32b8.
- Source archive SHA256: eb68aa761026232278c9fc1bbab1c4c540d243c982da19e602ac976ee65dab6f.
- karyo-greeter 0.1.0-1 SHA256: b9df635451eecbe495043047e5f0795951739e31a27ed48db58ebf43fafd1336.
- karyo-settings 0.1.0-1 SHA256: 6dc72aad55aafe96833c7313dc7d0ff144b14aebd1a4b923486b35d7c6291eae.
- Metadata fixture SHA256: 792a6db283555d0763b6e0fe7686462b8e1be1a557a28a8058a39d9180549a8e.

## Native and installed checks

Clean native package builds run all 68 CTests on each base. Independent profile
discovery passes 95 Python cases; real root and UID 65534 fixtures check trusted
regular metadata, foreign ownership, malformed UTF-8, size bounds and strict
canonical-versus-legacy fallback. The Qt/Python corpus is shared input rather
than an implementation-derived expected result.

Installation verifies manifests and DEB hashes, reinstalls only Settings and
Greeter with --no-remove, and preserves account databases, every common PAM
stack and the default display-manager link. dpkg verification and audits pass.

The fixed-host metadata-only fixture is profiles/tests/installed-policy-ui.py
in DE. It never changes the existing QA password. Actual installed Settings,
running as UID 1001 with an explicitly empty OPENKARYON_DESKTOP_PASSWORD, shows
root-mandated separate protection enabled and disabled for editing. Clicking
the control cannot turn it off. The fixture then removes only its own unchanged
settings and checks original account/PAM hashes.

A root-owned dangling canonical desktops.conf plus a valid legacy map exercises
the old fallback bypass. A real isolated greetd/cage session displays a metadata
error with no user inventory; submit/Enter do not start a user session. After
controlled metadata removal, the same installed Greeter rejects a wrong password
and accepts the original QA password, starting actual karyo-shell in seat0/tty7
on both systems. A timed watchdog protects each temporary display-manager run.

Original LightDM is restored afterward; no policy fixture maps, settings or state
remain, and account/password/PAM hashes and dpkg verification are clean. Root-only
global PAM recovery snapshots from earlier acceptance remain intentionally kept.

Evidence under out/{debian,ubuntu}-vm-qa/results: accounts-policy-install.log,
accounts-policy-ui.log, accounts-policy-cleanup.log, and screenshots named
accounts-policy-settings[-clicked].png, accounts-policy-greeter-invalid.png,
accounts-policy-greeter-valid.png, accounts-policy-greeter-wrong.png and
accounts-policy-greeter-login.png. Build logs live with the package-set receipts.

This closes installed policy readers, not protected child startup/switching,
network/VPN/DNS isolation, family clipboard or remaining compatibility runtimes.
