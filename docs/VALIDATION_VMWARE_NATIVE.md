# Native VMware source-package checkpoint

The DE integration at integrations/vmware/native-tools supplies independently
reviewed transparency patches, source locks and native environments. Builder's
existing source-package stage requires no provider-specific build code.

Both signed native source inputs were rebuilt on their own base with one build
job and no build networking. Native source packaging completed successfully;
all generated binary artifact checksums match their captured SHA256SUMS.

| Base | Required runtime artifact | SHA256 |
| --- | --- | --- |
| debian | open-vm-tools-desktop_12.5.0-2+deb13u1+karyo1_amd64.deb | 10006a75eb8f85c8517d6693f77a1b7abf90ed9957fa28707c1ffa26784c837e |
| debian | open-vm-tools_12.5.0-2+deb13u1+karyo1_amd64.deb | 1822a8de257266eadbb5da8294ccf41425d0ef09df81c9896d65811952bfd24c |
| ubuntu | open-vm-tools-desktop_13.0.10-1ubuntu1.1+karyo1_amd64.deb | cd2bd95719c9266bc433e4998ddb265ae58436ed9da11dda3ed91274800fd7af |
| ubuntu | open-vm-tools_13.0.10-1ubuntu1.1+karyo1_amd64.deb | 6861a21b8ea3b4756b1ca98b39c989ca9262897e2460cf85794e9bae78be6a81 |

Debian uses native open-vm-tools 2:12.5.0-2+deb13u1; Ubuntu uses native
2:13.0.10-1ubuntu1.1. Both append +karyo1. Only the matching core/desktop pair
was installed in each isolated QA guest. The native source build also produces
development/debug/plugin packages; these are not requirements of this feature.
Installation added native GTKmm dependencies, removed no packages and left
dpkg --audit clean. The system vmtoolsd service and LightDM remained active.

Stock/patched observations compile the real upstream DragDetWnd class and GTK
drag callback with each native SDK. On Wayland, the patched mapped detection
surface retains input and has zero painted alpha pixels; the duplicate drag
image is transparent. The ordinary X11 InputOnly window and painted drag image
remain unchanged. All four observations pass before and after each native patch.

Both installed guests completed an ordinary reboot, changed their boot IDs,
returned to LightDM and kept the updated system vmtoolsd active with clean
package audits. No desktop worker or active private profile was running during
this boot-cycle check. It does not establish a populated Home/Work shutdown,
the DE shutdown guard, mounted shared-folder teardown or a new cold install.

Actual Windows host drag-and-drop, clipboard channels, privileged device
handoff, display resize and multimonitor acceptance remain open. The Windows
computer-use runtime failed before acquiring any window on three startup
attempts, including a reset. No real host mouse action or transfer was simulated
through SSH and no drawing observation is counted as a host-channel result.

No user VM, hardware laptop, distro ISO, external application implementation or
frozen compatibility engine was modified by this checkpoint.
