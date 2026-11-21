# Installed file-manager activation acceptance

DE source 82f9d4b0de338cf8339eb539aa2232c25055b495 fixes common FileManager1
activation handoff. Native fixtures first reproduced the existing-window failure
on Debian and Ubuntu: a real button click in a separate GUI reused the folder
but left Files behind the caller. This was independent of the earlier URI fix.

The fixed helper asynchronously requests one standard activation token per call,
using the focused caller's real serial/seat/surface. It forwards that token as
the startup ID, bounds waiting and cancels with its context. No forced-focus
compositor exception or process-wide token mutation was added to the caller.

## Clean native package sets

Both sets export the exact source commit above, pass all 67 CTests and stage only
the eight affected caller runtimes. Each runtime includes the unmodified MIT
xdg-activation XML under its own documentation path, avoiding file ownership
collisions between independently installed applications.

### Debian

Source archive SHA256: 4a6655c8e05904e78cded91f3280c6185ae0bc50eb027f8fb3d95410f5df9edf.

Immutable image: sha256:f5abf68140a71f3abffbdeac454e883bd9d71fa71bc10f42da648ae3f190dd20.

| Runtime | DEB SHA256 |
| --- | --- |
| karyo-archive | c862118a9abd82c1df25cf68dc106a50b0df276308f7210fae89438c72ddac7e |
| karyo-photos | 9669bf26a5300b829e5b9bee48d66dd8e7c947eebba9887798447140c6cd623d |
| karyo-monitor | a41b9b7645859f18060a486f771f2bb4347d4df1e644a5714eda6d8166a01d50 |
| karyo-appcenter | a5e67c414892f1c928e957edec087251fbbaa83ef0d1deaaa748c1544d8394de |
| karyo-reader | c146b22a930b92b81f93dc1437af24a146767cdac6cefa0565e1b509fd2c9606 |
| karyo-snip | 9701a5d8d198755f5264cf953537a483eef07effc0d8c0f1b752f5af2ddc30af |
| karyo-player | 9106d91e44786281916a56db5071543fa42e3f6051afb2db9ad874acabc377b9 |
| karyo-settings | 6590fb223274951a58e1e49930242e38bbf20b3002998d6bd11111eb7110acc6 |

### Ubuntu

Source archive SHA256: 4a6655c8e05904e78cded91f3280c6185ae0bc50eb027f8fb3d95410f5df9edf.

Immutable image: sha256:241fbca9fd2091251c6e54232817874551e75792f7ef459cc36e73ac2fdadbf3.

| Runtime | DEB SHA256 |
| --- | --- |
| karyo-archive | 5db74796836eb02ac63399ad32302024ad5a00e3b325784011411b2428fbb2a2 |
| karyo-photos | f8ffb776536330af6702ccc42c462d84bd305c7d478f08bd66638066eb4b6e1b |
| karyo-monitor | 398beea12ab496d8d497596ce3149f12803d281754dc0d03b96f14ca7bd6f604 |
| karyo-appcenter | 91bd3b85e10b65a68a3fdf3b034f5b72d2d3c28b9d65d21c61a1101625662f5a |
| karyo-reader | c0eb814de333f6948048723ef874671b668b00e27bec5cbde1f3080c5f712d8b |
| karyo-snip | b3947097b2087d8575e86c67af8ca027363080e150319de062ea3da7b7f34718 |
| karyo-player | cfd376e03bf95f2452cefdb942a424be1ae331908ce9de86df179b4c4c94cadb |
| karyo-settings | 0bb29af125f9e49ed11e0759959a76c9a7d4e0bf3561c39374df49afb44f9f82 |

## Live checks

A native before/after GUI fixture using a real Wayland compositor and the same
installed Files process confirmed the old failure and corrected activation on
both VMs. A private-bus fixture then issued two simultaneous user-triggered
requests and destroyed a third request's owner. Both tokens were nonempty and
different, their paths matched, no cancelled request was sent, and no duplicate
arrived after the request timeout interval. Token contents were not logged.

All sixteen final artifacts and their package manifests were verified before
SCP/install. Both disposable VMs reinstalled their eight native runtimes without
removing packages, restarting Files or changing the existing display manager.
The original Files PIDs survived: Debian 17999 and Ubuntu 59240. Every installed
MIT protocol copy matched the source; dpkg integrity checks and audits were clean.

The final installed application check used /usr/bin/karyo-photos and a generated
public 256x160 PNG. The target folder was already open in Files. A real menu click
on Show in Files raised the same window and selected photo.png on both bases,
with the Details pane showing that file. No second Files window was created.
This checks an installed caller's real menu action, beyond a standalone fixture.

Both fixture sessions were terminated after checks; original LightDM remained
active with its original display-manager symlink. Native labwc extension packages
from the previous acceptance wave remain installed with their native wlroots ABI.
No owner VM, laptop, Forge, installed profile helper or APT source changed.

## Evidence and limits

Ignored local outputs:
- out/migration/activation-wave-{debian,ubuntu}/karyo-package-set-* retain manifests,
  checksums, native dependencies, full source/test logs and eight package records.
- out/{base}-vm-qa/results/activation-wave-install.log and activation-final.log
  retain installation, PID survival, integrity and native fixture results.
- files-activation-before-source/before-clicked/after-clicked.png show fixture
  behavior before and after; files-activation-photos/menu/revealed.png show the
  final installed menu action and selected item.
- Native fixture binary hashes are under activation-fixture-before/after.

The test-only Ubuntu fixture has no installed desktop entry, so its isolated
portal registration logs report that missing fixture AppInfo. The installed
Photos run logs no corresponding error. This does not weaken token checks or
establish a separate portal product regression.

This closes the existing-background Files activation gate on both bases. Other
prototype compositor changes and optional account/PAM/network/DNS/clipboard
helpers remain part of the active migration goal. Those helpers are not implied
to be installed by this application package wave. No commit or package was pushed.
