# Real desktop lock with the installed VMware coordinator

Debian13 and Ubuntu26.04 now pass a joined real PAM/Wayland GUI lock and native
VMware ownership gate. This closes the earlier modeled-LockedHint limitation for
these scenarios using a separate temporary Work password. It does not accept
Windows host payload exchange, privileged file transfer or other-DE handover.

## Inputs and credential boundary

Production packages remain the exact d74a8a882d0fc583c3f0329b0a479685af1bce21
coordinator/session artifacts recorded in VALIDATION_VMWARE_SESSION.md. This step
adds QA and documentation only; source11/session14/full71 suites from checkpoint
264 are not claimed to have been rerun for this QA-only change.

The fixed-host integrations/vmware/tests/installed-lock.py actor creates only the
known absent-before Work account using the accepted account fixture. It assigns
that temporary child a new separate YESCRYPT password and separate-entry policy,
retaining its inherited credential/policy for verified restoration. Home's own
password, common PAM and display-manager settings are never modified. After
logout the child credential/policy are restored before captured user teardown.

The driver generates random24-hex-character correct and wrong credentials in
memory. Plaintext travels only through SSH/Python stdin and VM-only RFB keys;
not argv, environment, files or exported logs. Stored Linux password hashes are
normal native authentication data and remain protected. QA receipts contain only
fingerprints/ownership/outcome metadata; exported summaries omit credentials and
password fingerprints. No user's private profile or token is read.

The public switch uses the earlier fixed root-only selected-context helper to
exercise installed authorization/IPC. That fixture is distinct from an interactive
polkit gate. The real Work compositor, locker, PAM authentication, logind state,
shell, coordinator and worker processes are the installed native components.
No synthetic LockedHint setter or fake unlocked state drives this test.

## Actual acceptance

Each native guest passes all six observations:

1. Protected cold Work enters its actual initial locker. Coordinator, shell,
   vmusr and bridge are absent before startup PAM completes; the channel is free.
2. An actual wrong initial password displays denial and leaves every tool closed.
3. Correct initial authentication unlocks and starts ordinary UID1002 coordinator,
   vmusr and bridge with empty current capabilities, NoNewPrivileges and inherited
   channel FDs in the native Work login scope.
4. The real Super+L binding opens the manual Wayland locker. The existing
   coordinator survives while its workers stop and the channel becomes available.
5. A wrong manual password displays denial and keeps those workers stopped.
6. Correct manual authentication restores new workers with the same coordinator,
   shell, logind session and captured graphical lease.

Initial and manual denial frames from both bases were captured and inspected;
the real password-failure message is visible. GUI input occurs only in the fixed
disposable VMware RFB consoles, without grabbing Windows input or clipboard.
Both native gates exit0. Finally the captured Work compositor/runtime/user,
protection/credential transition, channel metadata and driver acknowledgement are
removed. Original Home shell/session/VT and account/PAM/display-manager hashes
survive; full final postchecks pass on both guests with empty schema7 journal,
forward0, disabled/inactive optional runtime, no temporary child/DNS/NET/NAT/user
tools and clean package verification/audit. The intended vendor mount remains.

## Retained observation race and exact actors

Ubuntu's first manual-lock observation saw no named vmusr/bridge process but
attempted flock before the coordinator had finished releasing its reservation.
That test failed. Its native log and root receipt were preserved; cleanup had
completed, and account/runtime restoration was verified before another attempt.
The corrected observer waits at most10 seconds for actual exclusive-lock access,
while continuing to require the real locked state and preserved coordinator.
It does not declare a held lock released or relax product privileges. The final
Ubuntu run passes; all observed acquisition waits are below1ms. No production
change was required. Debian passed the earlier immediate observer.

| Base | Actually executed accepted actor SHA256 |
| --- | --- |
| debian | 65de52ca8a3dd78b75bf5d5e56fc23492e30ff786615a5cba9e5fe7d9cce0aeb |
| ubuntu | b89a7ba268b5371d04b14ddf1d89189ff03b45e6d8b8cad4961e978cac153022 |

Both executed actor versions are retained. The committed actor contains the
bounded observation correction, accepted on Ubuntu; the Debian pass is not
rewritten as having executed a later file. Exact receipt summaries, source/log
and frame hashes are in out/migration/vmware-lock-evidence.json. Native logs are
out/{base}-vm-qa/results/vmware-lock-native.log. The first Ubuntu race/recovery
logs and root receipt retain their separate names.

These guests still disable host copy/paste/HGFS in VMX. This gate proves actual
GUI authentication and release/resume of the coordinator's local reservation and
processes; it cannot establish Windows clipboard payload, vmblock/uinput file
transfer, drag/drop, HGFS or display following. The remaining full migration stays
active, including external VPN clients and Wine/Darling integrations.
