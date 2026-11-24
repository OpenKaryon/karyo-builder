# VMware shutdown and wait diagnostics

The optional shutdown release and session wait diagnostics were built from DE
revision `9e8119cca60c47823a501ace13579e4f92776c98`. Native checks and package
acceptance passed on Debian 13 (trixie) and Ubuntu 26.04 (resolute). The existing
ordinary-user coordinator retains its process-group and channel ownership.

## Source and package checks

Each native base passed five shutdown cases, five wait-diagnostics cases and
six existing ordinary coordinator policy cases. CMake installation and native
`systemd-analyze verify --man=no` also passed. These are selected functional
checks, rather than a claim about the complete repository test suite.

Build the two independently selected components with:

```sh
python3 -m karyo_builder package examples/vmware-shutdown.json \
  --image NATIVE_IMAGE --output OUTPUT --test-regex '^vmware-shutdown$'
python3 -m karyo_builder package examples/vmware-session.json \
  --image NATIVE_IMAGE --output OUTPUT --test-regex '^vmware-wait-diagnostics$'
```

Both recipes resolve the current source HEAD when invoked; the manifest records
the captured revision. The shutdown recipe does not implicitly elevate the
session coordinator or install a different session package.

| Base | Artifact | SHA256 |
| --- | --- | --- |
| Debian | `karyo-vmware-shutdown_0.1.0-1_amd64.deb` | `07e87c8688734539d401ee0c497a2287912ccbea8e944e72d6069812fc1b14d1` |
| Debian | `karyo-vmware-session_0.1.1-1_amd64.deb` | `018c5903151b93ac4576a74d1b9d9a425eaab2044488d9ebe80837bfa485d56f` |
| Ubuntu | `karyo-vmware-shutdown_0.1.0-1_amd64.deb` | `c8c3a6973db070b10fd07ac98fd6cd5c9eff77d8e458b2f74d7994b87cda2e4a` |
| Ubuntu | `karyo-vmware-session_0.1.1-1_amd64.deb` | `7a92903dc945e537d2358ed0522561b0e4e2ecb8a97a23fd5ec50c847d225486` |

Every artifact was rehashed against its successful Builder manifest before
acceptance. All four manifests report selected CTest and `dpkg-deb` success.

## Native kernel and systemd acceptance

On each disposable VMware QA guest, install the native shutdown package and
verify its enabled/active state. Use a minimal native `systemd-nspawn` root
with a private PID/mount namespace, the guest's read-only `/usr`, `/dev/fuse`
and the FUSE control filesystem. The installed guard and session-scope drop-in
are used unchanged. Clear only `ConditionVirtualization` in this nested fixture
because its immediate virtualization identity is a container; the installed
guest unit keeps its VMware condition.

Start the native `vmware-vmblock-fuse` with the ordinary mount parameters
`subtype=vmware-vmblock,fsname=vmware-vmblock,default_permissions,allow_other`.
Open its control file, add a block for an owned temporary transfer path, and
request the matching `blockdir` symlink from a transient `session-*.scope`.
Keep the control descriptor open throughout the blocked request. Check the
native mount's exact filesystem/source metadata before shutdown.

Both bases produced the following observations:

- The real request slept in `request_wait_answer`. Its observed state was `S`,
  so this does not claim reproduction of a vmusr `D`-state incident. The
  sustained `D`-state observer is covered by the separate source cases.
- An ordinary restart of the guard left the request blocked and produced no
  abort. The native scope included the installed drop-in and ordered itself
  before the guard, so the guard stops first during shutdown.
- A normal `systemctl --no-block poweroff` inside the nested PID namespace
  queued shutdown. The installed helper reported releasing exactly the owned
  vmblock connection. The waiting syscall returned `ECONNABORTED` (103), and
  nested systemd completed poweroff successfully.
- The original guest PID 1 and original vmblock mounts were unchanged. The
  temporary package was purged successfully and was absent afterward.

The Ubuntu guest's ordinary unattended download briefly held the package
lock. No lock was removed and no updater was stopped. The final runtime pass
reused the preceding run's installed package after comparing every installed
payload file against the exact native DEB, then purged it after the lock cleared.

Local result JSON receipts have SHA256
`6088f626210a634c1c8724ea617546c25f8ad639a0f963862ce522e09396c4f7`
(Debian) and
`95d8907b55457be3c50ff624afaa83be473ddc222eb612007e6e1becdeae024f`
(Ubuntu). Retain the accompanying native container and guard logs with them.
Preliminary fixture failures were retained separately; they are not counted
as passing runtime observations.

## Bounds of this result

This verifies a real FUSE request and the native shutdown transaction in an
isolated systemd instance, not a reboot of the full desktop VM. It does not
claim new host/guest clipboard, drag-and-drop payload or resize coverage. The
new session package was built and its selected source cases passed on both
bases; an existing interactive coordinator was not replaced during this run.
Wine, Darling and unrelated guest applications were not changed or tested.
