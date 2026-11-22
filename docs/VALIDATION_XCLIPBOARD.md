# Optional X11 / Wayland clipboard protocol component

The reviewed prototype clipboard bridge and timestamped X11 owner now belong to
DE's `integrations/clipboard`, independently of the profile account runtime and
VMware policy. Builder supplies the native package recipe and test environments.
This completes the protocol-component migration and its installed native gate;
it does not mark VMware host clipboard, session handover or drag/drop accepted.

## Ownership and behavior

The standalone CMake entry `integrations/clipboard` and `xclipboard-runtime`
component install `karyo-xclipboard` and its private Python modules. The recipe
has Python/Xlib, wl-clipboard, xclip and X11/XFixes runtime dependencies, no
maintainer scripts, services or autostart entries. Installation starts nothing,
changes no accounts/PAM/default display manager and runs no VMware user daemon.
The wrapper accepts an ordinary account and both display environments; root and
missing-display invocations are rejected in native acceptance.

The donor at26bad17cef413d26c36c117f2f1123dca4edded7 was read only. The reviewed own
Python implementation is adapted under GPL-3.0-or-later with public names and
standalone packaging. Runtime library/tool licenses remain their own. No private
configuration, profiles or clipboard data are imported. This does not modify or
consume Forge.

The adapter preserves UTF-8 text, PNG and local file-copy URL lists without
opening lazy VMware vmblock paths. Text/file URLs are bounded to1MiB, PNG32MiB.
File copy semantics are retained and cut becomes copy. The X11 owner provides
TARGETS/TIMESTAMP/MULTIPLE/INCR while leaving PRIMARY unchanged, including the
case where re-copying an identical image must get a newer timestamp than a later
PRIMARY selection. MIME type participates in loop deduplication.

Compared with the donor, MULTIPLE metadata reads and simultaneous INCR transfers
are bounded; no more than32 transfers and4 owner processes are retained. Notifier
drains have time/byte limits, X11 connections close and termination runs owned
process cleanup. Marked password-manager selections are not exported or replaced
by remote X11 data. Clipboard payload is never written to disk or diagnostic
logs; metadata hints do not identify unmarked secrets.

## Native inputs

Both actual .deb files were built from DE
`46fc3f124f0948187a34bfafc4ed63d775ac4554`; dc13a9e adds only QA/documentation.
No source overlay replaces installed production modules in the native gate.

| Base | Package | SHA256 |
| --- | --- | --- |
| debian | karyo-xclipboard_0.1.0-1_amd64.deb | b02b9b3f19a355c1c4d8315f66d19de2187889d1f2a10318b7008231f79d81f1 |
| ubuntu | karyo-xclipboard_0.1.0-1_amd64.deb | 7ab25788591a268eb8671e579237fab87702c4be76a41e431a10ec13a1d79883 |

The fixed-host native actor is
`integrations/clipboard/tests/installed-acceptance.py`, SHA256
`3c897ce10cec65c8513bb7b20ba93ff86932e0886bd68bbf78d5ea96f364a974`.
Exact manifests, build environment IDs and artifact/test/log hashes are retained
in `out/migration/xclipboard-evidence.json`.

## Acceptance

Both extended native test images pass all21 source protocol cases as UID65534,
with network disabled, all capabilities dropped, NoNewPrivileges and a read-only
source/root filesystem. Xvfb listens only locally; a separate headless labwc
provides Wayland. The suite covers real multi-megabyte repeated INCR, MULTIPLE,
request bounds, malformed oversized property rejection, original PRIMARY,
identical-image recopy, PNG/files in both directions and sensitive-local behavior.

The final native packages are installed on the disposable Debian13 and Ubuntu
26.04 VMware QA guests. Both run the same21 tests against installed modules as
the ordinary qaadmin UID1000 with all capabilities removed and NoNewPrivileges.
There are no skipped tests. Each gate uses its own Xvfb/headless compositor and
does not take over the existing Home display or the Windows host clipboard.
Package integrity/audit, root/missing-display rejection, account/PAM/LightDM hash
snapshots and the unchanged original Home shell/session/VT are required.

Native apt adds only karyo-xclipboard, python3-xlib, xclip and QA-only xvfb, with
zero upgrades/removals. Debian uses python3-xlib0.33-3/xclip0.13-4; Ubuntu0.33-5/
0.13-4build1. The QA test directory and all selection/bridge/compositor processes
are removed. Root0600 accepted receipts remain for review and cannot be silently
overwritten by a repeated gate. Current final postchecks pass on both guests:
original Home, empty schema7 profile journal, disabled/inactive optional runtimes,
forwarding0, no temporary child/DNS/NET/NAT/provider and clean dpkg state.

Both complete DE builds also pass all70 CTest groups. The source root invocation
skips9 display-protocol owner cases, which are separately exercised without any
skip by the ordinary source and installed native gates. Builder native package
manifests report ctest and dpkg-deb passed. No full VMware integration is inferred
from these protocol checks.

## Reproduce the component

Build the base Builder images first, then the optional test images:

    docker build -t karyo-xclipboard-qa:debian environments/clipboard-debian13
    docker build -t karyo-xclipboard-qa:ubuntu environments/clipboard-ubuntu2604
    karyo-builder package examples/xclipboard.json --image karyo-xclipboard-qa:debian --output out/xclipboard/debian
    karyo-builder package examples/xclipboard.json --image karyo-xclipboard-qa:ubuntu --output out/xclipboard/ubuntu

The package recipe uses the repository HEAD selected by the ordinary Builder
workflow; acceptance artifacts above retain the exact source revision. Keep
outputs for different bases separate. The fixed-host controller is QA-specific,
not an installer for an owner's machine.

Remaining integration includes active-seat vmusr handover, actual VMware host
text/image/file exchange, native drag/drop and duplicate prevention, HGFS and
display following. Simultaneous family sharing and host exchange also need their
own joined gate. Wine/Darling, external VPN/vendor GUI and the full migration
remain active independent work.
