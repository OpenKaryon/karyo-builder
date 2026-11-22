# Optional native family clipboard

The standalone DE now provides a separately packaged, opt-in family clipboard.
This is a product migration from the prototype's desktop clipboard integration,
with a rewritten bounded protocol, peer authorization and ordinary Wayland client.
It does not require the prototype registry, private user data or Forge.

## Package and policy

`examples/profile-clipboard.json` builds only `profile-clipboard-runtime` from
DE's standalone profiles CMake entry. It depends on the common accounts package,
Python, systemd and wl-clipboard. The two new clipboard modules are excluded from
the accounts install component and owned only by the optional package. There are
no maintainer scripts and installation starts/enables nothing. Administrator
activation is explicit: `systemctl enable --now karyo-profile-clipboard.socket`.
The session starts the ordinary adapter only after its startup PAM gate.

The Unix-socket broker uses DynamicUser with an empty capability bound,
NoNewPrivileges and its own network namespace. It has no home access and no
network transport. SO_PEERCRED authorizes real ordinary UIDs against trusted
account/family metadata. Spoofed USER/LOGNAME values confer no access. Account
and family generations invalidate cached values. UTF-8 text and PNG are capped
at8MiB each; volatile caches are bounded to32MiB/16 families and four concurrent
requests. Selection bytes are not written to disk or diagnostic logs.

Sensitive password-manager hints and unsupported/rich/file selections stay
local and are protected from an incoming remote value. Absence of a selection
does not mean explicit clear. Startup seeds an empty broker without overwriting
a newer value. New copies win over older in-flight replies and pending seeds
following a broker restart. Failed local writes do not acknowledge revisions.
Opting in deliberately shares marked-family clipboard data, including between
background sessions; this is separate from protected session-entry policy.

## Exact native inputs

Clipboard and session-entry packages for each base were built from DE
`4d013607fef64af518c0971d7f3dd94eb9c6950a`. Native tests use installed .deb files,
not a source overlay. Accounts and the other runtime packages are unchanged.

| Base | Package | SHA256 |
| --- | --- | --- |
| debian | karyo-profile-clipboard_0.1.0-1_amd64.deb | 4d4c3ec7d004d79ca5828dbbb3cf35225f781bf89c039023da7cdd2257fa26c9 |
| debian | karyo-session-entry_0.1.0-1_amd64.deb | 16c81e8430ae36ea8ce60dc8540168a25818e74a752e357344a0b14f1886bd41 |
| ubuntu | karyo-profile-clipboard_0.1.0-1_amd64.deb | 03be3830db47c93193f2f0c2b37340c3e2af3c10ea6f38c43c2ca3053d085243 |
| ubuntu | karyo-session-entry_0.1.0-1_amd64.deb | fb569b619691711fd879bc365e98387c5989feb7e98574f8b35ef94e6d195bf1 |

The fixed-host actor is `profiles/tests/installed-family-clipboard.py`, SHA256
`b9417683c5c4440e618975b59212ef35a91f5bdaa64a8e482d086fd048f455ec`. Full manifests, artifact/log hashes and paths are
retained in `out/migration/family-clipboard-evidence.json`.

## Acceptance and retained failures

Debian13 and Ubuntu26.04 each pass actual text copies in both directions,
byte-exact PNG, sensitive-local preservation under remote copies, outsider
spoof denial, broker capabilities/NoNewPrivileges/private-network checks,
sharing after an actual broker restart and reuse of the running sessions.
Home is the existing native session; Work starts cold through the installed
public runtime, and its bridge is launched by real session autostart.

The original Home session remains active. Captured Work/account/manager/network
resources, Home bridge/source units, singleton lock and clipboard socket are
removed. The broker is disabled/inactive and volatile state is gone. Final
postchecks pass on both bases: original Home shell/session/VT, empty schema7
journal, forwarding0, no child/provider/DNS/NAT fixtures, unchanged account/PAM
and display-manager settings, clean package verification/audit. Root0600 QA
receipts remain as evidence and require review before reusing the gate.

Initial native failures are retained rather than presented as passing tests.
The first test source used wl-copy's default fork in a one-shot transient unit;
systemd then killed the clipboard owner on unit exit. The corrected fixture uses
foreground owners that live until the selection is replaced or cleanup completes.
A process counter also initially counted the wl-paste watcher as a second bridge;
it now selects only the actual ordinary Python client. Captured recovery checks
required a completed cleanup receipt and empty runtime before removing only the
fixture's owned optional-runtime activation.

Source regression tests separately caught two genuine client races: a new local
copy while an older reply is in flight, and a fresh copy while restart seeding
is pending. Both have focused fixes and regression coverage. The failing seed
regression log is retained. The ordinary-user container invocation originally
used setpriv inside a capability-dropped container and was denied; the accepted
run uses docker exec's ordinary UID without adding capabilities.

Current source suites pass22 clipboard tests and469 profile tests on each base;
ordinary runs skip115 root-only cases. Native component ctest/dpkg-deb checks,
component ownership checks and13 session contracts also pass. Builder's47 tests
skip2 environment-dependent cases. No ISO, owner VM, Acer, private donor or Forge
is modified by this acceptance.

## Remaining boundaries

This does not establish X11/VMware host clipboard interoperability, multi-MIME
rich/file transfer, automatic detection of unmarked secrets or physical hardware
clipboard behavior. No VMware feature is claimed by transferring between two
native guest Wayland sessions. The full DE migration remains active, including
external ExternalProvider integration, remaining VPN lifecycle/vendor GUI cases and
Wine/Darling/VMware work. See the migration inventory for independent gates.
