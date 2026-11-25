# Native desktop-worker package checkpoint

This checkpoint covers the optional desktop-worker producer at DE revision
`3998870ab7ca5d9097e1a16ab24f9b6cefeff6cc`. Builder exports repository HEAD
through its existing package-set pipeline. No provider-specific build path is
introduced. Native Debian 13 and Ubuntu 26.04 environments built the Python
profile payload with one job. All installed artifacts matched their recorded
SHA256 checksums.

## Installed upgrade and native activation

The matching accounts, host and runtime packages were installed into each
disposable running native VM. Both package audits and payload verification
passed. Restarting the owner preserved the existing Home account, lifetime
token and network-namespace identity. The bus name became available after
ordinary service initialization; a fixed one-second readiness assumption was
too short and was replaced by observing the actual registered owner.

An ordinary application then called the installed producer directly. Native
process-specific polkit text authentication used the temporary QA account's
password, with no permissive authorization rule. The checks observed:

- A sealed final activation descriptor and an actual root worker socket peer.
- Exact raw prepared-descriptor bytes whose SHA256 matches the final record.
- Fresh activation of the same committed worker for the same application.
- Cancellation of a pending request without retiring its existing worker.
- Cancellation after native unit acknowledgement and before delayed readiness,
  without publishing a completed activation.
- Scoped retirement, removal of the registered unit and owned journal cleanup.

These checks pass on both bases. They exercise the native system bus, installed
entry point and real private service views. The additional application
observations below cover the graphical authorization and packet-engine paths.

## Clean package installation and purge

Separate disposable containers started with each native base and no installed
Karyo package. Native dependencies were installed with service startup blocked.
The complete tested closure was:

| Package group | Source revision |
| --- | --- |
| profile-accounts, profile-host, profile-session, profile-runtime | `3998870ab7ca5d9097e1a16ab24f9b6cefeff6cc` |
| style, session-entry prerequisites | `9abeb50648b6f57bd5156c290a0d9f971d3a2487` |

The prerequisites are previously captured native builds, checked against their
own manifests. They are not described as newly built from the worker revision.
Omitting them first exposed the profile-session dependency on session-entry,
and session-entry's dependency on style. The complete six-package closure
installs and purges successfully on Debian and Ubuntu.

Package payload verification and `dpkg --audit` pass. Installing and purging
these packages creates no account and changes no enabled-unit link relative
to the dependency baseline. Ubuntu's slim SDK deliberately excludes packaged
documentation; the installation test explicitly includes `/usr/share/doc/*`
so license and README payloads are verified rather than silently skipped.

This is a container package-lifecycle result. It is not a cold graphical
installation, desktop login, boot or populated multi-desktop shutdown result.
Native package manifests, container logs and VM activation records are retained
in local QA diagnostics; no temporary credentials are part of the repository.

## Independently maintained application observations

Both native guests also exercised a separately maintained application's real
helper, adapter and production packet engine through the same installed API.
The application remains an external package input; its implementation and
provider-specific identifiers are outside this repository.

An actual graphical Karyo authorization card appeared for the temporary Home
account on each base. Entering the account's password through ordinary Wayland
input authorized the worker. Password input stayed in driver memory and stdin,
outside arguments, environment variables, screenshots and exported logs.

Home then exchanged random 512-byte TCP and UDP payloads through a pinned TLS
endpoint with a fresh temporary token. A separate Home application scope sent
the payloads, keeping the worker's carrier bypass from producing a false
positive. The remote receiver checked their digests and observed the endpoint's
source address; the production engine also reported both downlink types.

Work retained its independent stock NetBird connection, peer DNS and private
TCP/UDP payloads. Selecting a Work exit node changed Work's source address at
its remote receiver while Home's tunneled payload retained its own source.
Deselecting restored Work's original path. These observations pass on both
native bases.

Normal closure and Release while the application still held a TUN descriptor
both completed through scoped retirement. Independent native inventories found
no declared interface, route-table/rule-table, IPv4/IPv6 route-protocol or nft
resources afterward, and no registered worker unit or journal item remained.
Home and Work retained their captured namespace, resolver and session identities.

Work was also logged out and started cold through the ordinary graphical
frontend after Home's packet engine became ready. Each new Work acquired a new
namespace and resolver while Home retained its original context and payload.
The same DNS, payload and Work exit-node observations passed. The native
application quiesced and exited, and independent inventories confirmed cleanup.
The test launcher's runuser/systemd-run wait pipe timed out after the foreground
desktop changed, so its process return code is not counted as an accepted result.

A single restart of the actual profile owner on each base replaced its native
PID and bus generation while Home's packet engine was live. The application
reported interruption and quiesced with fixture exit status 3. DE recovery
retired the worker and its resources. The exact Home/Work contexts survived and
Work's DNS and TCP/UDP still worked after the restart. This is an interruption
and recovery observation; the fixture's ordinary disconnect cases return zero.

## Remaining acceptance

The subsequent reconnect/cancellation and explicit Repair observations pass on
both bases. During cancelled reacquisition the same registered worker, native
unit and prepared files remain, and an independent inventory still sees its
guard. A fresh handoff restores the packet engine and separate-scope TCP/UDP;
Work retains DNS and payload. After scoped retirement, the observer first sees
an empty worker journal and no declared resources, then observes a distinct new
worker for explicit authenticated Repair. Both corrected observers complete
with exit zero and independently confirm final cleanup. The first Repair
observer stopped on a missing Python import; its actor completed afterward,
and its disappearance was checked before the corrected attempts began.

The final external application package also installs over its inactive earlier
payload on both native VMs with clean package audits and preserved Home/Work
contexts. Its declaration's LF bytes differ from the Windows snapshot's CRLF
bytes; parsed content is identical and the helper bytes are unchanged.

## General application launcher

DE revision `729448d14db053264d45234ffc4b766bc6ed0a10` closes the observed
menu-to-application-scope gap. Common desktop-entry, file-handler and Start
command paths use the optional runtime's `karyo-launch` helper inside an
isolated desktop. Its user scope inherits the actual network and mount
namespaces, resolver/service view, arguments, working directory and input.
It does not substitute the user manager's different mount namespace. The small
resident parent stays attached to its original graphical login independently
of the panel. Native administrative helpers pin and recheck their actual
ancestry back to that active login; worker-origin authorization is unchanged.

On both native bases, the real menu launches the packaged external GUI into
an independent application scope. Restarting the captured panel preserves the
GUI PID, start time and scope. The same menu launches the frozen production
worker/packet-engine participant with ordinary native authorization. A separate
Home scope exchanges digest-checked TCP/UDP through the pinned TLS endpoint,
with the remote receiver observing the endpoint's source address. Work retains
its stock provider, private peer DNS, TCP/UDP and exact captured context.
Normal completion returns zero and quiesces; independent selectors find no
owned interface, routes/rules, nft resources, worker unit or journal item.

The first Debian observer checked PTY echo before the authorization agent had
finished disabling it. It stopped before entering a password, and the actual
participant refused activation and exited without a worker. The corrected
observer waits for echo to be disabled; that complete attempt is accepted.
No test authorization bypass or package-specific public dispatch rule is used.

The rebuilt native Files application opens a selected file whose name contains
spaces. Its editor receives the complete filename in a separate scope with the
same private network and resolver. The ordinary desktop frontend still lists
all family members from a menu-started scoped terminal after panel restart.
Native desktop-entry tests pass on both bases: 29 passed, zero failed.

Builder also produces the account, host and runtime package set from the
committed revision above with one build job on each native base. Installing
those packages over the live own QA guests preserves Home/Work and gives clean
`dpkg --audit` and package-payload verification. The runtime contains the new
executable helper and the account component contains native login-lineage
support. These packages do not replace the external client or enable a new
provider. Shell and Files additionally receive native CMake build and installed
GUI checks; this observation does not claim a rebuilt full distribution image.

Full external application enrollment is outside these packet-engine fixtures.
The new protected Experiments account also correctly refuses startup on the
QA VM's stock compositor, which lacks the required startup-lock capability.
The previously accepted matching native compositor/library inputs are staged
for deployment after desktop teardown. Final protected-session and populated
shutdown acceptance and application package removal remain separate open gates.

VMware host clipboard, drag-and-drop, privileged device handoff and display
acceptance retain the limits recorded in `VALIDATION_VMWARE_NATIVE.md`.
No user VM, physical laptop, distro image or frozen compatibility engine was
changed for this checkpoint.
