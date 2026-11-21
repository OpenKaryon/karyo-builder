# Installed private profile DNS

Accepted runtime source: 8b091285853dea695af7157dbe9ed3c3106c7518.
This accepts the private DNS library, not a complete enabled profile supervisor.

## Exact native inputs

### Debian

- Output: out/migration/profile-dns-accepted-debian/karyo-profile-accounts-20261121T152306Z-ba13ca89.
- Source archive SHA256: a8cc37accb3690798ef51bbc3617348572995e27695ac1b890e130affdafed06.
- DEB SHA256: 1c948a8520490825cdee41d0dc7c5b2d9b946dc3b4d209892746daadcc63e0d5.

### Ubuntu

- Output: out/migration/profile-dns-accepted-ubuntu/karyo-profile-accounts-20261121T152308Z-469ab279.
- Source archive SHA256: a8cc37accb3690798ef51bbc3617348572995e27695ac1b890e130affdafed06.
- DEB SHA256: 1df7b3e2542f02e3abf3c93a4441dfbd00c4d3dc95b0acbb9f9308e1ce325761.

- Final probe SHA256 on both bases: 443a5cae71a6af6daadc081f19017b6504d19fa8dcc98451c383df85e6b1230d.
- Published probe: Karyo DE profiles/tests/installed-dns.py (6047af9).
- Final logs: out/BASE-vm-qa/results/profile-dns-accepted-native.log.

## Native discovery and library regressions

The complete profile suite passes 195 cases on Debian 13 and Ubuntu 26.04,
as root (three role-specific skips) and ordinary UID 65534 (52 skips).
A root test actually parses the generated policy with native dbus-daemon and
completes a real bus handshake, alongside the isolated parser/lifecycle tests.

Discovery reads typed resolve1 properties of the selected physical IPv4 link,
not global resolv.conf or a VPN default. Before/after physical snapshots must
match. DNSEx and DNS values must agree. IPv6-only seeds, nonstandard ports,
authenticated server names and effective encrypted DNS transport are explicitly
refused rather than downgraded to plain public fallback DNS. A root-owned
canonical resolved symlink is required before resource creation. This does not
claim support for all DNSSEC/advanced resolver policies or backend layouts.

The private resolver has its own D-Bus, runtime aliases and varlink directory.
Only root/service control and the profile user's bounded read/query operations
are admitted. The desktop client retains the host system bus for logind/polkit.
Client mounts bind the whole private resolved runtime directory; the generic
client plan adds neither NoNewPrivileges nor a restrictive capability bounding
set. Resolver-specific capabilities/sandboxing stay on the service.

## Installed native acceptance

The fixture runs only as root on the two disposable QA hostnames. It creates
an owned network/forwarding graph, captured transient private bus and resolver,
then an ordinary UID 1000 client. It proves the bus name owner equals the
captured resolver MainPID before private per-link bootstrap. Services are
identified by invocation, PID descriptor, executable, UID, cgroup and namespace.
No account, existing user manager, graphical session or personal VPN is changed.

Debian's hosts line uses nss-resolve before dns; Ubuntu's uses files dns. The
same live Python client performs actual getaddrinfo in both implementations,
first for public example.org, later example.net and a synthetic .test name.

Both bases pass:

- Public name resolution through the seeded private physical DNS.
- Host logind bus access, private resolver query and denial of client mutation.
- Existing QA sudo rule still elevates; NoNewPrivs is zero. This verifies the
  setuid path, not a newly tested interactive password prompt.
- Atomic replacement of the host stub with a deliberately unreachable test
  server does not change that client's private resolver hash or successful DNS.
- Atomic host symlink retargeting to the other supported resolved alias still
  selects the private runtime directory.
- A root private-bus update with NetBird-style SetDNS, SetDomains and
  SetDefaultRoute changes the same client's answer to 192.0.2.123 from a local
  test responder. Private alias inodes change and remain visible through mounts.
- Original global file/symlink inodes, host link DNS API values and full
  network/forwarding/resolver snapshots are restored.
- Original accounts, common PAM bytes and shell PIDs stay unchanged.
  dpkg verification/audit is clean.

The final Debian client/resolver PIDs were 47508/47491; Ubuntu used
113497/113480. The active main shells remained 36901 and 97122 on VT8, unlocked.
Readonly postchecks confirm no private namespace/runtime directories or fixture
backups, original stub symlink, and global forwarding restored to zero.

## Failed attempts preserved

The first generated bus policy put global connection rules inside a user policy,
then omitted receive permissions needed for the native handshake. The native
parser/connection tests caught both; 07737e5 fixes and regresses those cases.

The first installed private-name phase failed using a synthetic .invalid suffix;
the public lookup, host bus and sudo had passed and owned cleanup completed.
The .test fixture passes. No unproven explanation of the suffix failure is used
as a product workaround. Logs remain profile-dns-first-native.log and the
earlier corrected pass profile-dns-corrected-native.log.

The later transport preflight expected a method-output array for a string
property. Actual busctl returns scalar data. It refused before mutation;
profile-dns-final-native.log preserves this failure. Revision 8b09128 corrects
scalar handling, effective manager inheritance and regression coverage. Only
profile-dns-accepted-native.log is the final extended acceptance.

## Primary-source review and remaining work

Upstream [NetBird v0.82.1 DNS code](https://github.com/netbirdio/netbird/tree/v0.82.1/client/internal/dns)
selects systemd-resolved with nss-resolve or the native stub and controls link
DNS through the system bus. Its go.mod selects godbus v5.2.2. No undocumented
resolver-file environment override is assumed and no upstream implementation is
copied. [resolve1](https://www.freedesktop.org/software/systemd/man/latest/org.freedesktop.resolve1.html),
[execution properties](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html)
and [bus policy](https://dbus.freedesktop.org/doc/dbus-daemon.1.html)
inform the separately tested own implementation.

Installation enables no network/resolver service. Production owned-unit
supervision, stopped-profile launch, user-manager scope, forwarding dependency
setup, physical-change reconciliation/persistence and actual NetBird
daemon/config/socket/authentication/GUI remain required. Arbitrary global
resolver symlink destinations need controller policy and tests beyond these
two canonical aliases. The fixture is not an authenticated Home/Work VPN test.
