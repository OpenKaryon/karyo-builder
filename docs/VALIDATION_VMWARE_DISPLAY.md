# Installed VMware preferred-mode following

The standalone VMware integration now contains its own ordinary-user display
worker. Debian 13 and Ubuntu 26.04 pass a native activation-time acceptance gate.
The gate observes real kernel metadata and compositor modes; it does not claim
that an actual VMware host window resize or monitor hotplug has been tested.

## Production and packaging

Runtime packages were built from DE source
`13c1bb7` (the full revision is retained in the local evidence). The later
`3299f2a` commit adds the executed QA actor and documentation only. Builder's
optional VMware recipe explicitly requires `wlr-randr`; ordinary sessions gain
no new system daemon. Both QA guests already had that dependency, so APT changed
only the coordinator/session payloads. No unrelated package was upgraded or
removed; account/PAM/display-manager hashes and the original root vmtoolsd
PID/invocation were preserved. The vendor autostart remains unchanged. Its
previously installed vmblock mount remains enabled and mounted.

The observer reads connected vmwgfx connector sizes every half-second. It avoids
relying on a global udev subscription inside private desktop network namespaces;
this is a design boundary, not a claim that every private namespace loses udev
events. It debounces changing metadata and performs one later correction.
Unchanged metadata does not continuously override a manually selected mode.
Non-VMware, disabled, unknown or ambiguous outputs are not modified. The new
KARYO_VMWARE_DISPLAY_SYNC opt-out has precedence over its legacy fallback.

The display worker belongs to the foreground coordinator's captured groups.
Every bounded output-management request retains the channel reservation and its
own parent-death notification. Native active/unlocked state is checked before
querying and before writes. Delayed display work does not block the coordinator's
state loop. The source policy suite covers locked/unknown states and retries;
the new display child has not yet been tested through the real GUI lock gate.
The earlier joined-lock report remains evidence for its earlier runtime revision.

## Native before and after

The old installed runtime used d74a8a8. In a cold disposable Work session the QA
actor selected 1152x720 while the kernel preferred 1280x800, then switched to the
original Home and back. Debian retained the off-preferred size; Ubuntu's existing
compositor path already restored its preferred size on reactivation. Thus the
missing behavior was reproduced on Debian, not asserted on both bases.

With the new installed runtime, both native guests pass:

- The display child has UID1002, the actual Work logind session, zero effective,
  permitted, inheritable and ambient capabilities, NoNewPrivileges and an open
  FD for the captured channel inode.
- After initial settling, a manually selected 1152x720 remains for four seconds
  while kernel metadata stays 1280x800. No repeated override occurs.
- Switching to the original Home removes the display child. Returning to the
  same Work session creates a new owned child and restores 1280x800.
- The original Home session, geometry and shell remain. Captured Work/account,
  network, DNS, forwarding and channel resources are removed; the empty schema7
  journal, disabled socket, inactive service and clean dpkg state are verified.

The first implementation failed this Debian gate. Its wlr-randr reports a custom
mode as `1152x720 px (current)`, omitting the refresh rate. The original parser
accepted only the standard rate-bearing form. A separate production correction
accepts both, with an actual-format regression; the same corrected source was
rebuilt, installed and accepted on both bases. The first failed actor/log/receipt
and the diagnostic repetition are retained rather than relabeled as successes.

## Validation and exact evidence

Both full DE CTest runs passed 71/71 after the initial implementation. After the
parser correction, the affected CTest group was rerun on each base, and all 25
VMware cases passed under UID1001 in isolated Debian/Ubuntu images, including real
worker lifetime, inherited-lock and parent-death tests, with no skips. Builder's
47 host tests pass with its two expected native-symlink skips on Windows.

The final native actor is integrations/vmware/tests/installed-display.py, SHA256
`f670138e8d1f1aa545559008814b5d676b14d54aa09e86d5f03009bcce9e4dd8`
on both guests. Root-owned 0600 receipts are /var/lib/karyo-qa/vmware-display.json,
phase accepted and cleanup_complete true. Root upgrade receipts are under
/var/lib/karyo-qa-vmware-display-custom-mode-upgrade. Local evidence joins actor,
module, artifact, receipt and log hashes in out/migration/vmware-display-evidence.json;
filtered native summaries and exact actor copies are in each QA results folder.

| Base | Coordinator artifact SHA256 | Session artifact SHA256 |
| --- | --- | --- |
| Debian | ff4a4958387cba4d042906fab6d8d7a7382d18a697703c1a17c41ae894c73a38 | c046b4865ca7ca59823cbe188f7795b25fd31ccf577484e2e150ce222f68934a |
| Ubuntu | 7b3b0a5944cf8af9d38150469c79a7638f0771c65149c3cbfe1cad9baab3f05c | ba7144fe9a8abe64b68d7579af31ff6dc77be7025f9a8d3178eb17a02a9eb6ef |

## Excluded topology probe and recovery

Before the accepted scenario, a synthetic vmwgfxctrl topology request worked in
a quiet Home but did not publish the requested preferred mode reliably with Work
running. No cause or successful host-resize result is inferred from that. A
follow-up paused only the captured Work vmusr, still failed to produce the mode,
and complicated teardown. That probe is excluded from acceptance and is not a
recommended resize procedure.

During its teardown networkd restarted and removed some captured private static
routes/rules. Supervisor correctly retained the unproven graph rather than
removing changed resources. The original networkd was already running before
the probe; an early recovery hypothesis that it was newly introduced was wrong.
A recovery attempt briefly stopped it, its socket reactivated it, and the same
DHCP address/default route returned. Captured backups and recovery logs remain.
After proving that only the exact recorded peer route and original nft graph
remained, the missing recorded routes/rules were restored and strict normal
recovery removed the profile. No journal ownership proof was weakened or bypassed.
The original Home/root vmtoolsd remained; networkd's original PID was not retained.
Robust reconciliation of external networkd route removal is still a separate
network lifecycle gate, not fixed by this display change.

## Remaining boundaries

Actual host-window resize, host-driven monitor layout changes and multi-monitor
placement remain open. The guest-only activation gate does not substitute for
those. The QA VMX copy/paste/HGFS isolation flags remain TRUE; Windows payload
exchange, privileged vmblock/uinput transfer, duplicate-safe drag/drop, HGFS and
another DE's ownership handover are likewise separate gates. Full VPN, Wine and
Darling migration continues. No push/fetch, Forge, donor, owner VM or Acer change
was made in this checkpoint.
