# Actual connected controller loss and native host recovery

Debian13 and Ubuntu26.04 now pass actual root controller SIGKILL while the
captured graphical profile has a connected NetBird0.82.1 provider. A new installed
socket-activated host reattaches the living owner graph and then supervises its
natural logout or compositor crash. This extends the prior same-PID fresh-journal
gate; it is not the end of the provider or complete DE migration.

## Exact inputs

Production packages remain the eight artifacts from DE revision
`25273daa8aac34426787a7c78be1cd2b55867ea9`, archive SHA256
`b9731d0501e744c1d833ac44375b518c44939d16630650bf476e6e73975ed438`.
See VALIDATION_PROFILE_NETBIRD_CONNECTED.md for individual Debian/Ubuntu DEB
hashes, schema6 ownership boundaries and public external CLI/server inputs.
No product code or native package changed in this QA-only extension.

QA-only DE revision: `8cfeaf29eaac18e52e7bae2f5d58805e1b41b250`.
Extended `karyo-de/profiles/tests/installed-supervision-netbird.py` SHA256:
`3e9f3b92898d14e1b1750d1b9fc90cb1ffb5f9c498aafb5b2b93b71e55e0c108`.
The explicit `--connected` flavor requires a fresh fixed disposable-host fixture
and the root0600 temporary lab admission key described in the preceding gate.
The original no-argument six-mode pre-login matrix remains available and was
repeated successfully on both bases with this same exact driver.

## Observed transitions

For each connected lease, the driver starts the normal journaled network,
forwarding, resolver, provider and graphical/user-manager owners. An ordinary
manager-launched CLI inherits its endpoint, uses the lab key-file API and returns
Connected. Persistent provider state is reused across the leases. The initial
protected case retains its real lock and has no shell; the test does not bypass
password entry into that desktop.

The parent captures the live receipt and forcibly kills only its own direct
root controller child using the captured process handle. It verifies a SIGKILL
exit and leaves all native owner processes running. A request from the captured
Work context starts the installed root host through its real socket. Recovery
must preserve the entire typed native receipt, and an ordinary CLI must still
return Connected. The provider PID/start time is checked against that receipt.

| Connected mode | Native recovery and result |
| --- | --- |
| logout | New socket host reattaches the connected graph; actual labwc logout returns to the original Home and closes provider/DNS/forwarding/network. |
| crash | Same connected reattachment, followed by pidfd-SIGKILL of the captured compositor; automatic Home return and cleanup complete without later client traffic. |
| background | Activate the original Home before the captured Work compositor exits; the host records exactly one seat-unchanged decision instead of activating over it. |
| locked-crash | Protected Work begins with a real lock and no shell. The connected graph survives controller loss; compositor crash returns Home and cleans up. |
| closed | Kill the controller after captured GUI closure and natural user-manager exit but before policy removal. A new installed SessionRegistry completes only the recorded closing transition and the connected lower-layer teardown. |

The four living modes exercise the real installed host unit and socket. The
closed case uses a fresh installed registry directly. Each living host records
exactly one return decision. The driver never sends provider `down`; shutdown
follows owned graph/manager/provider/resolver/forwarding/namespace order.

## Evidence and final state

Each base's `out/<base>-vm-qa/results/netbird-connected-recovery-native.log`
records all five connected modes and successful admission/vendor fixture cleanup.
The `connected_after_controller_sigkill` and `same_native_receipts` observations
precede compositor termination in every living mode. The exact log digests are
listed below after the completed runs.

| Base | Connected native log SHA256 |
| --- | --- |
| debian | `1a0640283db9c3b275a82d7e6877a54eea2883d9b1acff688da751109decb408` |
| ubuntu | `c3d7779df9064ba7091b60a73da01d0f55cb176d38e82117a2ddf5985a6b3aaa` |

The original six-mode regression is retained separately as
`profile-supervision-netbird-native.log` on each base. Source discovery remains
425 profile cases on both bases (root4skip, ordinary109skip); those source runs
are documented in the preceding production gate. This extension only changes
the explicit native QA driver and does not broaden privilege or product policy.

After both connected and legacy matrices, captured lab cleanup removes the
server, temporary owner/PAT/key, data directory and matching binary. Final
`profile-supervision-netbird-postchecks.log` verifies original Home shell/login
active/unlocked, empty schema6 journal, forwarding0, disabled/inactive host
socket, inactive host/runtime units, clean package verification/audit and no
child1002/home, manager/provider policy/state, vendor binary, private namespace,
veth/NAT, admission, server or connected-recovery fixtures.

## Limits still open

This checks SIGKILL of the direct journal-owning controller followed by startup
of the real installed systemd host. It does not kill an already-running systemd
host a second time, simulate kernel/system power loss, or establish all partial
mutation boundaries while connected. No peer payload, private-domain DNS,
exit-node routing, userspace TUN native fallback or real browser PKCE completion
is inferred from Connected status alone. Final GUI/tray and inert vendor/catalog
packaging and public VPN startup remain open; configured VPN still refuses
before allocation. Other full migration work remains active.
