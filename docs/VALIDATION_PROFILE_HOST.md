# Native root host profile transport

This gate accepts only the optional host transport and native peer identity.
The complete profile runtime and overall migration remain unfinished. All
commits and evidence are local; there is no push or owner-machine update.

## Inputs and package ownership

Runtime source: DE 70fe92c972a7762625c68a57f9078039e6d67dd1.
Source archive SHA256:
58fd456b9be853f73517f098ff03bc3d5ac93416b27cf1796827a7cedda0cc05.

The accounts package owns the Python libraries. The separate optional
examples/profile-host.json payload owns only its fixed root entry, socket,
service and documentation. Installation enables no unit, changes no common
PAM/account data and does not replace the display manager. System units install
under /usr/lib/systemd/system, without the multiarch library directory.

- debian accounts: out/migration/profile-host-final-debian-accounts/karyo-profile-accounts-20261121T175044Z-115a9fc1; 65000 bytes; SHA256 b72009f86203a0ecac918ace503cfb686f69186886beca4b6d3c2587fc7d28f4.
- debian host: out/migration/profile-host-final-debian-host/karyo-profile-host-20261121T175053Z-45ed1537; 30692 bytes; SHA256 e9e958f6ad1c41ee87c59336ec831c1f891596178b33518666a052365af01874.
- ubuntu accounts: out/migration/profile-host-final-ubuntu-accounts/karyo-profile-accounts-20261121T175041Z-c8669612; 66074 bytes; SHA256 da7d666771a16c23f5b3393570ff8130a6a79a044e3d3195d7746cc16628efa0.
- ubuntu host: out/migration/profile-host-final-ubuntu-host/karyo-profile-host-20261121T175050Z-a76aaa0a; 31102 bytes; SHA256 ad9c975e161dc236d2d7594ed81d6e858762497aa49ca0a515d52d47f58d9142.

Native QA hosts are disposable Debian 13 and Ubuntu 26.04 VMware guests. Existing
main GUI shell PIDs remain 36901 and 97122, respectively, active/unlocked on VT8.
Previously accepted profile-session, lock, shell, manager and compositor packages
remain unchanged except for the accounts library update. Host packages remain
installed but disabled/inactive after the test, with no socket path left.

## Peer and transport contract

The root filesystem Unix socket uses mode 0600 beneath a trusted root parent.
The host captures SO_PEERCRED and a pidfd before parsing input. It derives the
ordinary caller account from sd_pid_get_session(peer PID), the active native
logind session and exact session cgroup, then revalidates PID/start/exe/all UID
credentials, user namespace, account and active VT identity. A helper may inherit
private network/mount namespaces; the host controller stays in PID 1's
user/network/mount namespaces. Forwarded environment or caller IDs are ignored.

The bounded versioned protocol exposes family listing and existing-session
switching only. Repeated JSON keys, unknown fields, invalid UTF-8, truncated,
oversized/trailing frames and slow/unclosed requests are refused. Errors are
sanitized and typed. A lost reply never retries an operation. Switching rechecks
the original peer under the configuration lock and immediately before activation
or a no-op response, preventing replacement by a later session of the same UID.

## Source and installed acceptance

All 266 profile tests pass in both native build bases as root (skip3) and
ordinary UID65534 (skip63). Staged installation contains only the intended
/usr/libexec entry, /usr/lib/systemd/system units and documentation.
All 38 Builder tests pass (one platform-specific skip).

The published DE profiles/tests/installed-dispatcher.py has SHA256:
66530d678683afeb01f6f1385cffffb6bdc7a967b90e6058c0a5955652e70c81.
Both guests execute those exact installed root-owned bytes without a Python
source overlay. It accepts no arguments and only the two fixed QA hostnames.
It contains no credentials or private configuration.

Only the probe's own root child PIDs enter the captured existing GUI cgroup.
This proves native kernel peer identity; it does not claim interactive polkit
or PAM UI acceptance. The fixture demonstrates on both installed bases:

- Socket creation alone leaves the service inactive; a root connection activates it.
- Ordinary UID1001 cannot open the root-only filesystem socket and cannot trigger activation.
- A root SSH/service process is rejected as a graphical caller.
- A captured active GUI caller succeeds despite forged PKEXEC_UID, XDG_SESSION_ID and USER.
- Unknown owner fields are rejected without an operation.
- Family listing and same-session switching work from host context.
- The same operations work after setns to a new owned network namespace and
  unshare of the caller's mount namespace; the server remains in host namespaces.
- The captured service InvocationID/MainPID remains stable across requests.
- Only the captured fresh socket inode and service are stopped; no global enable is added.
- Accounts/common PAM, network links/routes/rules/nft/netns, resolver target/hash,
  forwarding and original active login match their initial snapshots; dpkg checks are clean.

Final logs under out/BASE-vm-qa/results:

- profile-host-final-install.log
- profile-host-native.log

Earlier accepted 3f79895 evidence is profile-host-3f79895-native.log. Debian's
profile-host-first-native.log preserves the first failure, before an operation:
the client incorrectly rejected root PID1 as the socket creator. Systemd socket
activation deliberately retains those listener credentials. DE 3f79895 accepts
root PID1 on the client side, while retaining the host's strict live helper PID
and graphical session checks. Source regressions cover both sides. The first
fresh socket/service were inactive after cleanup; no graphical state changed.

Unit stop prints systemd's ordinary reminder that its triggering socket is still
active; the immediately following captured socket stop removes that trigger.
This is not a failed cleanup or an enabled production service.

## Next integration gates

Current public polkit helpers do not call this optional transport yet. Stopped
profiles still return DesktopStopped. No persistent resource graph, journaled
restart recovery, automatic logout return or primary-session restart is claimed.
The service has no restart policy while that ownership/recovery work is pending.

Next combine accepted graphical/session-manager, private DNS and physical
forwarding leases under a long-lived controller, preserving identities across
requests and recovering only proven owned objects. Add physical DHCP/DNS
reconciliation and dependency/forwarding activation, then verify stopped-profile
public GUI startup and logout on both bases. Actual NetBird lifecycle/callback,
profile catalogs, family clipboard and remaining platform/VMware integrations
remain open. Forge, distribution images, donor and owner machines are untouched.
