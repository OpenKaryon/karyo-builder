# Native compositor protocol acceptance

DE revision 8cdd77e carries separate native labwc layout/snapshot patches and
recipes. Builder revision 7e349ba supplies the generic source-package stage.
These results close those two optional protocol gates; they do not establish
the remaining Wine/VMware compositor or profile/account/network helper migration.

## Native builds and source trust

Both source DSCs and their archive parts were obtained through signed native APT
metadata and matched the DE recipes. The public fetch script was exercised for
both bases and preserved existing verified inputs. Downstream patches were
captured in order, applied with zero fuzz, and built offline with native
dpkg-buildpackage rules and strong source checksums. CMake DE package-set behavior
was not changed by this source-package stage.

### Debian

Native package version: 0.8.3-1+karyo1.

Build/runtime QA image: sha256:7cc96448ba880bf63c7c670905a09400451d7bdc190554dcc791bbca604318c5.

Source recipe SHA256: a787ee4b30bd3eb4fc2a54d5da2321af89af1fdcf33363be185083b32ce9dc42.

Native upstream test suites: 2/2 passed.

| Artifact | SHA256 |
| --- | --- |
| labwc-dbgsym_0.8.3-1+karyo1_amd64.deb | fde58605d72c575cb13cd983b4f6b265d86d824770ad98183a09e3b578940dd9 |
| labwc_0.8.3-1+karyo1_amd64.buildinfo | 966e5ee461d70c55580b4c555672b03f7b54dc2622e0476f836317e96c32b5dc |
| labwc_0.8.3-1+karyo1_amd64.changes | 96bc891027797efce6c3a23ca59c49525e273678c578828cf9603e1c77285f13 |
| labwc_0.8.3-1+karyo1_amd64.deb | 9a62cdbb3401dc344edd43793d7c303740219c94526a410a8ff8764e5353a21e |

### Ubuntu

Native package version: 0.9.3-1+karyo1.

Build/runtime QA image: sha256:2b6171bfacf5f8d34424c582232e0fffc15c5fafd2b0d732955e29af57cc1c09.

Source recipe SHA256: dfcae8f07a98c9e99313909a5bdee9f5b66ecf6def93c5eb437ab9cab8183e14.

Native upstream test suites: 3/3 passed.

| Artifact | SHA256 |
| --- | --- |
| labwc-dbgsym_0.9.3-1+karyo1_amd64.ddeb | 85bb89e02604a7ec42c16aee9ef645bd5f979e0abc52535f814f14db0cd023cf |
| labwc_0.9.3-1+karyo1_amd64.buildinfo | 03362abf4239fcffc831b87506ab2f327bf4fa4ae548850239a70a0683bb651f |
| labwc_0.9.3-1+karyo1_amd64.changes | 48479245dc5b06e95f7d514e6a9af06612df2fb032d697f7d51840c2f3529934 |
| labwc_0.9.3-1+karyo1_amd64.deb | d3ae0e6a94add680dc6778f451593a0542a99051a030dd6f28212aaf25f17551 |

## Real server/client acceptance

Both exact image IDs above ran the packaged labwc with headless outputs and
pixman as UID 65534, read-only root, no capabilities, no new privileges and no
network. A compiled Wayland client made actual requests to the packaged server:
mapped SHM-backed toplevels appeared in front-to-back order; minimization removed
one; a real security-context client could not discover privileged globals; session
lock hid windows and rejected layout cycling; unlock restored snapshots.
The no-physical-keyboard case remained safe. No fake compositor was substituted.

## Installed VMware sessions

Both disposable guests installed the verified native labwc package and retained
their original libwlroots ABI (Debian 0.18.2-3 / Ubuntu 0.19.2-1). Package integrity
and dpkg audits passed. Real LightDM Karyo logins used a temporary us,ru fixture.
The compiled probe observed physical keyboard modifier events changing groups
through the protocol, including no group change while locked.

Actual installed shell clicks changed RU to EN. The installed Snipping Tool
opened its window picker and clicking the terminal delivered that complete
window, including its titlebar, to the editor on both bases. This establishes
interoperation with the migrated clients, beyond the standalone probe.

The original keyboard file was restored, fixture sessions ended, and LightDM
remained active with the original display-manager symlink. After sessions ended,
each native stock labwc was restored from a checksummed saved APT package, then
the downstream package reinstalled. Integrity/dpkg audits remained clean. No
wlroots upgrade/downgrade, owner VM, laptop, Forge or APT source changes occurred.

QA output lives in DE's ignored out/compositor/{base}/final-packages and
final-acceptance; Builder's ignored out/{base}-vm-qa/results retains transport
logs and compositor-session/layout-click/snip-picker/snip-editor screenshots.
Guests retain /var/log/karyo-qa/compositor-physical.log and package lifecycle
logs, plus stock rollback archives in /var/cache/karyo-qa/stock-labwc.
Source-stage fixtures and host input/receipt regressions are separate: 29 host
tests pass, real fixture packaging/native execution passes on both bases, and
the eight source-input cases also pass as UID 65534 on both native Linux images.

Ubuntu labwc's own security filter logs rejection of an additional unknown
upstream xdg_wm_dialog_v1 during the sandbox check. The two Karyo globals are
correctly hidden; the unrelated upstream allowlist was not broadened.

## Limits

Snapshots describe visible-screen bounds and retain occluding pixels. The tests
do not establish isolated unoccluded-window capture, physical GPU acceleration,
multiple physical monitors, Wine decorations/owned-window behavior or network
namespace/profile isolation. Those remain active migration/acceptance gates.
No package, commit or image has been pushed or published.
