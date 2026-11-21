# Global desktop password synchronization acceptance

Exact PAM runtime source: 6b9093391bde39bd4cf1b2a4d1ce2c7cc50dca1a.
Installed account helpers: 348ae18a1db81fe085436f7f603da94af0da4849.
Only the two disposable VMware acceptance guests are changed. Forge, prototype
source, owner VM and physical laptop remain untouched. All commits stay local.

## Native artifacts

### Debian

- Output: out/migration/profile-password-sync-debian/karyo-profile-password-sync-20261121T092942Z-6a5252ed.
- Package: 0.1.0-1.
- DEB SHA256: 80b87540d96d58cd1e518cd80945fd0071d514dd0d2ad0361fc7a8dd9212a920.
- Source archive SHA256: d3031fc4287e8a8700f31b92f88c51ffe4efdd4e9f95383e0446c9d72daa2827.
  postinst source SHA256: 853a8dc71307e815633662b79354cdf3d6b4570bc2ec824f33a13f5aa50a78e9.
  postrm source SHA256: c940b53ad785b87eb4b333c00a31e2242d86ddf919bdd07511c8266567d253f8.
  prerm source SHA256: 889d0c440fb2e4af9af264d3f8bc67759507ffd2af4e9cf3232bd26bb026672a.
- Output: out/migration/profile-password-sync-upgrade-debian/karyo-profile-password-sync-20261121T093318Z-85f93137.
- Package: 0.1.0-2.
- DEB SHA256: ff7db93c0c0bdc775fee95b2f4897ee128c51a5aa426624f36af46c1b73121cd.
- Source archive SHA256: d3031fc4287e8a8700f31b92f88c51ffe4efdd4e9f95383e0446c9d72daa2827.
  postinst source SHA256: 853a8dc71307e815633662b79354cdf3d6b4570bc2ec824f33a13f5aa50a78e9.
  postrm source SHA256: c940b53ad785b87eb4b333c00a31e2242d86ddf919bdd07511c8266567d253f8.
  prerm source SHA256: 889d0c440fb2e4af9af264d3f8bc67759507ffd2af4e9cf3232bd26bb026672a.

### Ubuntu

- Output: out/migration/profile-password-sync-ubuntu/karyo-profile-password-sync-20261121T092944Z-848d00a9.
- Package: 0.1.0-1.
- DEB SHA256: 9402918bcdc1c9f3cf96d51cdb5cba51f5e708192dd54b76de41b24df6a4ffc8.
- Source archive SHA256: d3031fc4287e8a8700f31b92f88c51ffe4efdd4e9f95383e0446c9d72daa2827.
  postinst source SHA256: 853a8dc71307e815633662b79354cdf3d6b4570bc2ec824f33a13f5aa50a78e9.
  postrm source SHA256: c940b53ad785b87eb4b333c00a31e2242d86ddf919bdd07511c8266567d253f8.
  prerm source SHA256: 889d0c440fb2e4af9af264d3f8bc67759507ffd2af4e9cf3232bd26bb026672a.
- Output: out/migration/profile-password-sync-upgrade-ubuntu/karyo-profile-password-sync-20261121T093325Z-5c370ded.
- Package: 0.1.0-2.
- DEB SHA256: e969cd5f5a70dd97467a5d877bb5546ccb54054dd9ca5c83d2e8e8940f8dc3a0.
- Source archive SHA256: d3031fc4287e8a8700f31b92f88c51ffe4efdd4e9f95383e0446c9d72daa2827.
  postinst source SHA256: 853a8dc71307e815633662b79354cdf3d6b4570bc2ec824f33a13f5aa50a78e9.
  postrm source SHA256: c940b53ad785b87eb4b333c00a31e2242d86ddf919bdd07511c8266567d253f8.
  prerm source SHA256: 889d0c440fb2e4af9af264d3f8bc67759507ffd2af4e9cf3232bd26bb026672a.

## Installed evidence

The independent profile build passes all 94 Python cases under native Debian and
Ubuntu. Ordinary UID runs pass too, with 42 root-only fixtures skipped; root runs
skip three ordinary-role tests. Existing full graphical DE regression is 68/68
on each base; this component adds no Qt source.

Actual installation registers exactly one helper in common-password. The other
common PAM stacks and account bytes do not change. Recovery snapshots of PAM and
native tool state stay root-only under /var/lib/karyo-qa on the disposable guests.

Fresh fixture families exercise native PAM including common-password and actual
/usr/bin/passwd. Root changes propagate main to shared child. runuser launches
the actual setuid passwd for an ordinary shared child: wrong current passwords
fail with unchanged hashes; correct passwords update only the shared family.
Separate children remain independent. No plaintext token is exported to the
synchronization hook. Original QA login credentials never change, and fixture
users/homes/metadata/temporary PAM services and binaries are removed afterward.

Native lifecycle also verifies these operations:

1. Explicit administrator disable survives same-version reinstall.
2. Explicit re-enable and a -1 to -2 upgrade retain exactly one enabled hook.
3. A harmless extra module in the managed block reproduces local PAM edits.
   Native removal refuses the stale active helper reference, preserves that
   stack byte-for-byte and retains the profile/helper.
4. After restoring only the controlled QA edit and its captured tool state,
   removal restores original common PAM/account bytes exactly.
5. Reinstall and purge again restore those bytes and the display-manager link.
6. The ordinary -1 package is finally reinstalled/enabled for further session QA.
   Both guests finish with original LightDM active and clean dpkg verification/audit.

The -2 package is a generated QA-only version bump of the same source. The normal
recipe remains 0.1.0-1. No maintainer uses --force or rewrites common-* itself.

Local ignored logs per out/{debian,ubuntu}-vm-qa/results: pam-global-install.log,
profile-pam-global-passwords.log and pam-global-lifecycle.log. Corresponding
root logs preserve each install/reinstall/upgrade/blocked-remove/remove/purge
operation under /var/log/karyo-qa. Native source/binary fixture hashes are in
pam-input/record.json and SHA256SUMS; package manifests record every script hash.

This closes shared password/PAM package acceptance. Full logind/VT profile
startup/switching, password-protected entry on every visit, isolated VPN/DNS
and family clipboard remain separate required migration gates.
