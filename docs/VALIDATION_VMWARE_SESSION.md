# Optional VMware session coordinator: installed handover accepted

DE now owns an independent native-session VMware coordinator, packaged by
examples/vmware-session.json. Source policy, ordinary
worker lifecycle, native packaging and actual installed Home/Work coordinator
handover now pass on Debian13/Ubuntu26.04. Actual initial/manual GUI lock is additionally accepted in
[VALIDATION_VMWARE_LOCK.md](VALIDATION_VMWARE_LOCK.md). Host clipboard payload
exchange and privileged file transfer remain separate pending gates.

## Product boundary

The standalone integrations/vmware CMake entry installs vmware-session-runtime.
It requires the native open-vm-tools-desktop, libsystemd and the separately
packaged karyo-xclipboard. Its own payload has no enabled service, account/PAM
change, default display-manager replacement or vendor autostart diversion.
A tmpfiles declaration provides only a root-owned runtime directory/channel lock.
For a running machine the documented administrator tmpfiles command creates that
metadata; the package never elevates its ordinary session agent to create it.

The Karyo session calls the optional agent only after startup PAM and valid
application-role setup. A Karyo-local XDG_CONFIG_DIRS mask suppresses the vendor
vmware-user desktop entry before normal autostart. The vendor file and other
DEs are unchanged; an already running external vmusr is respected, never killed.
New Karyo sessions restore normal resolution after removing this optional package.
This does not yet coordinate a non-cooperating other DE's stock vmusr process.

Actual identity comes from sd_pid_get_session and native logind UID/type/class/
seat/VT/remote/active state. Missing identity is rejected; USER or XDG_SESSION_ID
cannot select another desktop. A finite-time native system-bus LockedHint check
keeps locked/background sessions from owning the channel. No loginctl process
is spawned in the normal polling loop. Foreground workers use vmtoolsd -n vmusr
and the ordinary clipboard bridge without a SUID wrapper.

The agent drops current/permitted/inheritable/ambient capabilities and enables
NoNewPrivileges. A root-owned0644 file is opened read-only with no-follow checks
and flock coordinates cooperating agents across UIDs. Child workers retain the
reservation, verify their parent and request parent-death termination. Foreground
child leaders are not reaped until their captured process group is stopped,
preventing PID/group reuse during cleanup. Failed helpers stop their sibling
before a bounded retry; active-seat handover also waits before a fresh claim.

Rootless vmusr is not assumed to replace privileged vmblock/uinput handling for
file transfer. Native desktop dependencies have their own distribution
maintainer scripts. The matching native desktop tools are now installed on both
QA guests and intentionally enable/mount their standard vmblock FUSE unit. No
unrelated package is upgraded or removed; the existing root vmtoolsd process
keeps its PID and invocation. This vendor mount remains as installed functionality.

## Evidence

The source/package revision is
`d74a8a882d0fc583c3f0329b0a479685af1bce21`.

| Base | Package | SHA256 |
| --- | --- | --- |
| debian | karyo-vmware-session_0.1.0-1_amd64.deb | bfa7f6d7b220b25ccc98c74e269699fc44e0d7643e2f46cafbe41cf5fe96b134 |
| debian | karyo-session-entry_0.1.0-1_amd64.deb | b11f32c8bc93b64b96082b1fb6766e226b8bf8b4391793232be428f8a1eec60f |
| ubuntu | karyo-vmware-session_0.1.0-1_amd64.deb | 5de08c1fe8f7d9d93c7d1b1eb54258cc3d0778704c6663e2d94a2b940f51ccf6 |
| ubuntu | karyo-session-entry_0.1.0-1_amd64.deb | cc53742a3c13a0274667a66183daafafcb2e4e15f3e181243e653eb7c0dc7495 |

Both native package manifests report successful ctest/dpkg-deb validation.
Exact manifests and source/log/artifact hashes are retained in
out/migration/vmware-session-evidence.json. These exact packages are now installed
on both guests. Later DE c0240a2 adds only the native QA controller/documentation;
production coordinator and session-entry bytes are unchanged from the revision above.

Both isolated ordinary UID1001 source environments pass11 agent cases, including
actual capability-free foreground workers, inherited channel reservation, exited
leader/descendant cleanup and actual parent-death termination observed through a
pidfd. Network is disabled, all container capabilities are dropped and root/source
filesystems are read-only. Eight policy cases cover background/lock state,
external ownership, retry/backoff and missing/faked native identity. Three real
worker cases require the isolated root-owned metadata fixture. Root component
ctest skips those three cases; the ordinary runs execute them without skips.
Both bases also pass14 session-launch contracts and all71 full DE CTest groups.

The first worker run rejected PID1, which is a valid parent inside an isolated
process namespace. Diagnostic evidence identified that constraint and it was
corrected to the native positive pid_t range. Initial failing logs are preserved.
There was no restart of a live operation or relaxation of capabilities to make
the tests pass. On the existing Debian native guest, the actual libsystemd path
encoder and LockedHint property ABI were additionally checked read-only; this
is an ABI probe, not evidence of native session/channel handover.

## Installed native coordinator gate

The fixed-host actor is DE integrations/vmware/tests/installed-handover.py. Both
normal user accounts and the original Home display remain real native sessions;
no agent is launched using a fake XDG_SESSION_ID or root attachment into its
login cgroup, and no production source overlay is used. The privileged public
switch itself reuses the earlier root-only selected-context/authorization fixture;
this is separate from an interactive polkit/password authorization gate.
Home starts from a newly opened GUI Terminal launched by its original shell.
Work starts cold through the installed public profile runtime and its real
post-PAM session autostart. RFB controls only these disposable VMware consoles,
without grabbing the Windows desktop mouse or keyboard.

Both bases pass all six observations:

1. Home coordinator/vmusr/bridge share the original native login scope, UID1001,
   empty current/permitted/inheritable/ambient capabilities, NoNewPrivileges and
   inherited root-owned channel FDs.
2. Cold Work autostart claims the single worker set as UID1002. Home retains its
   coordinator while releasing background workers. The actual Work XDG mask is
   present; the packaged vendor desktop file keeps its hash and is not diverted.
3. A real SIGKILL of foreground vmusr stops/replaces its sibling pair with new
   PIDs while the same coordinator recovers.
4. Returning to existing Home restores its workers and releases Work's pair
   without replacing either coordinator or graphical profile lease.
5. Killing the Home coordinator clears both workers through parent-death handling
   and leaves a newly opened exclusive flock reservation available.
6. Existing Work then reclaims the channel using its original coordinator and
   graphical lease. Logout removes its captured user/runtime/network resources.

Captured Home agent, QA Terminal and channel metadata are removed; original Home
shell/session/VT, account/PAM/LightDM hashes, default display manager and root
vmtoolsd remain unchanged. Final complete postchecks pass on both bases: empty
schema7 journal, forward0, optional runtime disabled/inactive, no temporary
child/provider/DNS/NET/NAT/coordinator/bridge/vmusr and clean dpkg verification.
The intended vendor desktop package and enabled/mounted vmblock unit remain.
Root0600 accepted receipts and downloaded public package artifacts are retained.

The initial installer fixture had a nested-string escaping SyntaxError; Python
rejected it before any root mutation. After correction both native installations
passed. The first Debian coordinator actor omitted closing its newly created
Terminal after the child exited. That exact Terminal PID/start/UID/command was
captured and closed separately without touching any original terminal. The
corrected actor captures/removes that GUI fixture itself on Ubuntu. Both executed
actor versions and the additional Debian cleanup log are preserved, rather than
claiming the first actor already performed the corrected cleanup.

| Base | Executed actor SHA256 |
| --- | --- |
| debian | da82879a2c291223c10fb6ef3252f14fe5870801017fb2f391b1659444aea8b4 |
| ubuntu | 0744ebe633fad253baeb0e1648ebb569b0b0a4a87ef1ba778160224925220654 |

Exact accepted receipt summaries, actor/log/frame hashes and native installation
records are retained in out/migration/vmware-handover-evidence.json. Final native
frames are out/{base}-vm-qa/results/vmware-home-final.png and were inspected.
No user clipboard payload or private profile is captured in this evidence.

## Remaining joined VMware gates

The actual QA VMX files explicitly set isolation.tools.copy.disable,
isolation.tools.paste.disable and isolation.tools.hgfs.disable to TRUE. They were
not changed by this test. The native evidence therefore proves coordinator,
process and channel-reservation handover; it cannot prove Windows host clipboard
payload exchange or HGFS. A controlled, enabled host-channel fixture is required
for text/PNG/files; generic guest X11/Wayland tests do not replace it.

Actual initial/manual GUI lock/unlock is now accepted by the separate joined
gate linked above. Privileged vmblock/uinput authority, native drag/drop and
duplicate prevention, HGFS, display following and other-DE handover also retain
their own remaining gates. The separate joined-lock report records real denied/correct PAM attempts and
coordinator release/resume, superseding the earlier modeled-only LockedHint limit. The full
VPN/Wine/Darling migration remains active.

A separate focused source correction now reopens a broken system-bus connection.
The failed read first removes foreground eligibility, so a later reconnect must
return a valid unlocked state before the channel can be claimed again. Its
additional policy regression passes on both bases. Native artifacts above include
this correction; actual host-bus restart is not claimed by that focused test.


## Installed preferred-mode following accepted on activation

The new optional worker now passes real Work activation, manual-mode retention,
background release and preferred-size restoration on Debian and Ubuntu. A
Debian-only custom-mode output format exposed and fixed a parser defect before
acceptance. See [VALIDATION_VMWARE_DISPLAY.md](VALIDATION_VMWARE_DISPLAY.md) for
exact source/artifacts, the preserved initial failures and networkd recovery,
and limits: actual host resize/multi-monitor events and real GUI lock of the new
display child remain separate gates. Earlier lock/handover evidence keeps its
original runtime revision; it is not silently relabeled as a new joined pass.
