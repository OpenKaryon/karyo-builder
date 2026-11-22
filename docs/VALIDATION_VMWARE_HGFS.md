# Installed native VMware shared folders

The separate optional karyo-vmware-shared-folders package restores the
prototype's system HGFS path /mnt/hgfs using native open-vm-tools. It stays
independent of the ordinary GUI session agent and X11/Wayland clipboard bridge.
The helper accepts only fixed-target start/stop, validates private root metadata
and directories, serializes operations and preserves existing/replaced mounts.
The system unit runs only in VMware, skips disabled host sharing, retains
NoNewPrivileges and uses nosuid,nodev,allow_other. Filesystem namespace sandbox
options would hide the intended system mount, so they are deliberately absent.

## Native gates accepted

Both independent native builds use source aa3d70e and declared maintainer hooks;
Builder never executes those scripts during package construction. Thirteen
ownership/protocol regressions and both integrated VMware CTest groups pass on
Debian13 and Ubuntu26.04. The installed gate uses actual6.12/7.0 kernels, native
open-vm-tools programs and real host files, with standard systemd lifecycle:

- A disabled host leaves the new service inactive with exec-condition rather
  than creating a disconnected filesystem.
- A separate vendor mount is recognized and left unchanged, including an EIO
  target. The fixture controller then removes only that test mount while the
  host exposes exclusively the new dummy share, so the package's own mount is
  exercised independently.
- Actual ordinary-user file reads/writes cross the host boundary; a newly cloned
  private mount namespace also inherits working access. This is filesystem
  inheritance, not a claim about a complete Home/Work GUI channel matrix.
- The system-owned FUSE child is UID0 with actual NoNewPrivs1 in its own service
  cgroup. Repeat start preserves the owned mount instead of creating duplicates.
- Foreign tmpfs and replacement HGFS mounts survive service stop unchanged.
- Administrator disable survives reinstall and is not automatically activated.
- After host sharing is disconnected, purge unmounts the owned filesystem,
  removes unit/helper/runtime metadata and keeps the ordinary /mnt/hgfs directory.
  Both original host payloads remain intact.
- Account, PAM, display-manager, fstab, shell and root vmtools daemon identity
  match independently captured before/after state. Temporary host shares and
  the original disabled runtime flag are restored even on failed test phases.

The primary actual replacement control is important: both kernels immediately
reused the old mountinfo number and FUSE device number. The original tuple
could therefore refer to a different filesystem. The helper now binds ownership
to the non-recycled64-bit kernel identity through explicit findmnt/listmount
numeric columns. Unsupported identity queries fail before mounting. No new
persistent Python root monitor, GUI privilege inheritance or private prototype
path is introduced. The optional recipe declares util-linux>=2.40; the backend
also needs kernel support (Linux6.8+, present on both native target guests).

## Exact executed artifacts

- debian: karyo-hgfs-service-546dd8118e; package SHA256 a855c2e1661040026d0ee5a35caf0b4a279cf53f083a1db1ca393a73d6e3e1c1; source aa3d70e3e860650cd22dd4da0ffae985f04994d3.
- ubuntu: karyo-hgfs-service-371fa9d9c0; package SHA256 e36c1316f415e5f828cb2d75673b218c9c30a926eaa0b341073faf2549d2538e; source aa3d70e3e860650cd22dd4da0ffae985f04994d3.

The joined local result is out/migration/vmware-hgfs-evidence.json. Every native
receipt binds package/manifest, source, actor and driver hashes plus all phase
log hashes. The runtime helper/unit/hook bytes have also been compared with the
current source; subsequent acceptance actors and documentation do not relabel
the original package revision. New final full-desktop builds remain separate.

Retained negative controls include the initial target-stat EIO failure, the
old-helper1/new-helper0 paired systemd run against that same inaccessible mount,
and discovery of recycled old IDs in the first installed lifecycle attempt.
The first promotion to a function-based actor caught a Path local-import scope
error before package changes; final source actor and driver pass on both bases.
Ubuntu's systemd-analyze also reports unrelated vendor XFS CPUAccounting
warnings; those files are not changed by this component.

## Repeating the acceptance

Build examples/vmware-shared-folders.json independently in each target SDK. Use
the resulting successful package-output folder with:

```sh
python tests/acceptance/check-vmware-shared-folders.py \
  --base debian --vmx QA_VM.vmx --ssh-host QA_IP \
  --ssh-key QA_KEY --known-hosts QA_KNOWN_HOSTS --vmrun VMRUN \
  --package-output NATIVE_PACKAGE_OUTPUT --de-source ../karyo-de --output out/hgfs
```

Repeat with --base ubuntu and its own native package. The driver checks that
VMware's actual guest IP matches SSH, the selected native distribution matches
the package receipt, and no other host shares are configured before modifying
host settings. The source
actor additionally requires the named disposable QA hostname and ordinary
account; it is not an installer for a user's working machine. Only the newly
created host test folder is exposed. No SSH private key, host clipboard or broad
home directory is copied into the guest or artifacts. Every host mutation has
an independent finally cleanup; no test success is recorded if cleanup fails.

HGFS acceptance does not establish host clipboard payloads, drag/drop, actual
window resize/multi-monitor behavior, another DE's GUI ownership, VPN lifecycle,
Darling compatibility or final current-HEAD desktop deployment. Those broader
migration gates remain open.


The complete Builder suite passes71 cases on each native base and on Windows
(with its two existing native-only skips). Negative controls reject a foreign
base or failed package and prove that a share-removal timeout/nonzero exit still
runs host disable, runtime restoration and final verification. Cleanup failure
prevents an accepted receipt. The final native driver/actor hashes and log
hashes have been checked against both successful phase receipts.
