# Installed private DNS journal reattachment and recovery

This gate extends ownership to the private DNS layer and observers. Full live
user-manager/GUI/forwarding/VPN supervision and the overall migration remain
unfinished. All commits are local; no owner machine or Forge is modified.

## Exact runtime inputs

Final source: DE 357a0e16f4277429ce8c816c85f292e65fc53fd6.
Source archive SHA256:
264d31acf5539d39635c003b7a07ff427ee2e0fa5f64875db1cac30df8d2a37e.

- debian accounts: out/migration/profile-dns-journal-final-debian-accounts/karyo-profile-accounts-20261121T184107Z-a84825b2; 73344 bytes; SHA256 ec3439ae8e547b0727c865dffd117cc85da7e4175e2e9dd893a5eeac23f28558.
- debian host: out/migration/profile-dns-journal-final-debian-host/karyo-profile-host-20261121T184122Z-9f8556c6; 32632 bytes; SHA256 2529c88bd989c4d3d288fade01c3a0299dba3c604dff81cbc2fcb39996654222.
- ubuntu accounts: out/migration/profile-dns-journal-final-ubuntu-accounts/karyo-profile-accounts-20261121T184108Z-7d0fb6a1; 74448 bytes; SHA256 76819e222b1ee2d3a6becbb548e6bbc5223a3ca2a45833701f3c2e849bf68a9a.
- ubuntu host: out/migration/profile-dns-journal-final-ubuntu-host/karyo-profile-host-20261121T184123Z-53cddce0; 33008 bytes; SHA256 0efc5c90f062617f1be02abc231153ee3fe89cc2cbcd8a5e50a5fb78fc317618.

The installed public DE profiles/tests/installed-journal-dns.py has SHA256:
51616ca2da4f724c5dcff08afc133cb4035efdf490e580c948b8e1d9f1917a5d.
Both guests execute those exact root-owned bytes with installed packages and no
Python source overlay. Earlier a029976 package acceptance is preserved separately
in profile-dns-journal-a029976-native.log under each QA results directory.

## Typed ownership and ordering

Journal schema 2 supports fixed private DNS receipts while schema-1 network
records remain readable/recoverable. Paths, filenames, unit names and cgroups
are derived from the captured profile token. The record carries a validated
physical seed, native resolver/profile identities, configuration directory/file
inodes, service InvocationID/PID/start/executable/namespace and runtime-directory
inodes. Configuration bytes come from the fixed ResolverPlan, not recorded
arbitrary commands or file contents.

Internal ResolverServices before/after hooks publish start/stop intent before
native operations and capture proof afterwards. JournalDNS restores new observer
FDs for the same live resources; it does not restart a matching resolver or bus.
The ordinary-user GUI retains the host system bus contract. Offline host startup
reconciles resolver, private bus and configuration before deleting its network.
Interrupted recorded stop and partial/full configuration removal can finish;
unknown creation, replaced identities and extra consumers retain resources.
The network-only cleanup path refuses a record that still owns DNS.

New allocation also stops behind unresolved current-controller network or DNS
intent. A token created by the current controller is not automatically a complete
lease. Fully acknowledged current leases can still coexist across profiles.

The transport package does not install or switch the host DNS backend. These
private DNS tests consume the already configured native systemd-resolved backend,
root resolver symlink, dbus-daemon and service account accepted in the earlier DNS
gate. An explicit dependency/setup integration remains part of later runtime
packaging; native acceptance does not imply automatic backend conversion.

## Source regressions and fixture corrections

All 300 profile tests pass on Debian 13 and Ubuntu 26.04 as root (skip3) and
ordinary UID65534 (skip89). New cases cover DNS schema/file/unit identities,
no-restart observer restoration, dependency/retention and current-intent interlock.
Existing ResolverServices callers without hooks keep their behavior.

An initial file fixture attempted chown in capability-dropped containers. It now
checks the actual current group plus wrong-group/mode rejection without adding
capabilities. After introducing the current-intent gate, the duplicate-account
fixture needed to capture its first network receipt before exercising duplicate
identity validation. Its earlier failure was not accepted as a passing result;
the local interlock commit was amended after both complete root runs passed.
Final ordinary-role runs pass as well.

Builder implementation/recipes are unchanged in this wave; the existing 38-test
Builder result remains recorded, and new native package builds provide recipe/
artifact validation. C++ code is unchanged, so the earlier full CTest suite is
not rerun for this Python-only integration.

## Real installed acceptance

The fixed-host root probe prepares an otherwise absent UID1002 QA family child.
A fresh captured Popen controller creates a real journaled network and private
DNS resources. For crash cases the parent verifies its receipt/PID and SIGKILLs
only that child; systemd DNS services and named resources remain. Both native
kernels pass all six cases on final packages:

- Normal start and complete close.
- Controller crash and reattachment to identical private bus/resolver PIDs,
  InvocationIDs, namespace/executable/runtime identities and configuration inodes.
  A private D-Bus GetConnectionUnixProcessID confirms the captured resolver still
  owns org.freedesktop.resolve1. No unit is restarted during reattachment.
- Resolver already stopped under its persisted stop intent before acknowledgement.
- Both services closed, then one captured configuration file removed before crash.
- Whole configuration directory removed under recorded file removal intent.
- Actual socket-activated installed host startup reconciles a complete captured
  private DNS/network graph before serving requests.

The fixed service/socket identities are verified before stopping only those QA
units. Every case restores original links/routes/rules/nft/netns, host resolver
symlink/hash, forwarding and main login. Final fixture cleanup restores exact
account/common PAM bytes. Temporary DNS configuration/runtime paths disappear;
the journal is empty, private and still bound to its original lock inode.

The previous network-only SIGKILL probe and host/private-net/mount transport
probe pass again on the final runtime. Main GUI shell PIDs36901 and 97122 remain
active/unlocked on VT8. Host units stay disabled/inactive, no socket or QA child
remains, and dpkg verification/audit are clean.

Final logs under out/BASE-vm-qa/results:

- profile-dns-journal-final-install.log
- profile-dns-journal-native.log
- profile-journal-native.log (network-only compatibility)
- profile-host-native.log (private-context transport compatibility)

The stop reminder about a still-active triggering socket is followed immediately
by verified removal of that captured socket, as in earlier host acceptance.

## Remaining complete-profile integration

JournalDNS.restore currently accepts only its known resolver as a namespace
consumer. Full GUI/user-manager/VPN reattachment must supply separately proven
consumer/scope ownership, rather than relaxing that check to arbitrary PIDs.
Typed user-manager/logind/graphical/VT/forwarding/VPN receipts and a long-lived
profile supervisor remain required before public stopped-profile startup.

Still pending: source return after logout/crash, primary Home restart, physical
DHCP/DNS reconciliation and dependency/forwarding setup, actual NetBird private
state/socket/callback/browser and DNS control, profile catalogs, family clipboard,
and remaining Wine/macOS/VMware integrations. These DNS checks do not claim
Internet/VPN forwarding or recovery of a live complete graphical profile.


The later living manager/GUI gate is recorded separately in
VALIDATION_PROFILE_SESSION_JOURNAL.md, including preserved unsaved editor content.
It does not complete interrupted session cleanup or public runtime integration.
