# Debian VM acceptance

Completed on 2026-11-20 UTC (2026-11-21 in Moscow). This extends the container
checks in VALIDATION_SESSION.md with a real display manager and logind guest.
Forge and the existing Karyo workstation VM were not modified.

## Clean baseline

A new VMware Workstation VM uses UEFI, two vCPUs, 4096 MiB RAM, a 24 GiB sparse
disk, NAT e1000e and virtual SVGA with 3D disabled. The verified official Debian
13 generic amd64 cloud image was provisioned with cloud-init, Xfce and LightDM.
The image was not copied from a developer workstation or a Karyo image.

Base URL: https://cloud.debian.org/images/cloud/trixie/latest/debian-13-generic-amd64.qcow2

Downloaded size: 434831360 bytes. SHA-512, checked against Debian SHA512SUMS:

```text
e53a93ef33f828ceed0e7278c2cc2753bdc7d5098fbfae15bd64b6d878db350ea3744247763a1c8ecb6b4019a0f623c38caf6038ad6f9c357fb4e01493ddf1a3
```

The guest kernel is 6.12.117+deb13-amd64. A disposable password-protected
`karyoqa` user exercises graphical PAM and polkit; SSH administration uses a
separate fixture account and generated key. Neither account is included in
product packages. No personal browser/VPN data was imported.

Before Karyo installation, a real LightDM password login reached Xfce and
opened Mousepad. Hashes of /etc/os-release, /etc/X11/default-display-manager
and the Xfce desktop entry were saved, together with the Xfce process ID.

## Observed results

| Check | Result and evidence |
| --- | --- |
| Install alongside Xfce | Runtime DEBs installed with APT --no-install-recommends. Existing Xfce PID survived and all three host-file hashes matched. Karyo did not start itself. |
| Login/session selection | LightDM's real session picker offered Karyo alongside Xfce. Password login started an active seat0 session with Desktop=karyo and Type=wayland. A later logout and second Karyo login passed too. |
| Application launch | Start search launched Mousepad, the authorization fixture, tray fixture and Chromium. Mousepad opened the selected sample file and copied its exact 33-byte contents through the Wayland clipboard. |
| Lock/PAM | loginctl lock-session set LockedHint=yes and created karyo-lock. A wrong password kept it locked; the correct fixture password removed the lock and cleared LockedHint. |
| Suspend/resume | logind delay inhibitor was present. A clean systemctl suspend cycle logged s2idle entry at 21:51:10 and exit at 21:51:16 UTC. A virtual hardware Shift key woke it; LockedHint stayed yes and shell/Mousepad PIDs were unchanged. Correct password unlocked normally. |
| Polkit | A real Start-launched pkexec action displayed Karyo's agent, accepted the fixture user's password and wrote uid=0. polkitd recorded successful one-shot authorization through karyo-shell. |
| Status notifier | A real Qt QSystemTrayIcon registered in the overflow. Left click recorded activated-3 and showed its window. Right click displayed its two-item menu; Open fixture recorded menu-open. |
| File portal | A persistent Gio FileChooser.OpenFile caller displayed the GTK chooser and received Response=0 with file:///home/karyoqa/qa-data/sample.txt. The sender stayed connected until the response. |
| Screen sharing | Chromium getDisplayMedia used the normal Entire Screen picker. A live monitor stream reached the video/canvas at 1280x800, 30 fps settings, with 498 sampled colors. A PNG frame was saved and visually inspected; tracks were then stopped. No fake media or chooser bypass was used. |
| Upgrade | All six fixture runtime packages upgraded from 0.1.0-1 to 0.1.0-2 while shell/Mousepad remained running. The edited lock PAM file stayed byte-identical and the changed shipped default became .dpkg-dist. Host-file hashes still matched. |
| Removal/purge | Back in Xfce, removing the Karyo packages removed their binaries, session entry and portal choice while preserving local PAM. Xfce PID survived. A further LightDM login reached Xfce successfully. Purging lock removed its owned PAM file; host-file hashes still matched. |

## Defect found and fixed

Start used QProcess::startDetached for desktop applications. Its double fork
left pkexec with PID 1 as parent, so polkit rejected the request with
`Refusing to render service to dead parents` before showing the agent.

DE commit 7c1cd7d keeps a live direct caller using an observed QProcess, while
allowing ordinary applications to outlive the launcher. Regression tests failed
on the original implementation and pass with the change. All eleven CTest
targets passed in the package build. The VM then proved the actual polkit path,
not only a mocked prompt. This is a general launcher fix, with no app-name rules.

The actual fixed karyo-shell_0.1.0-2_amd64.deb has SHA-256:

```text
b892daa6bfb31eccbcc105a4ca4bac9fc9b7c4f931656af14129bd268c0b59c1
```

The other 0.1.0-2 packages are acceptance-only version/default-change fixtures,
not new software releases. Their executable payloads match the initial packages.
The bundle's exact internal dependencies were advanced together. The real shell
build replaced the shell's version-only fixture; its separate build manifest
records source 7c1cd7d4dde4671ddfa2aef9d36d1eef104696a6. These artifacts must
not be mistaken for a published distribution release.

## Reproduction and artifacts

Reusable guest fixtures are in tests/vm; the package-upgrade fixture generator
is tests/acceptance/make-upgrade-fixtures.py. They supplement interactive VM
acceptance, not an automated substitute for selecting sessions and verifying
pixels. No VM image, private key, password, browser profile or screenshot is
committed.

Local ignored output root: out/debian-vm-qa. It contains the VM, seed, official
image/checksums, generated upgrade fixtures and the actual shell build manifest.
The results directory contains LightDM, Xfce, Karyo, PAM, tray and portal PNGs.
results/evidence retains install/upgrade/remove/purge logs, sleep kernel logs,
polkit authorization, the FileChooser JSON and captured PipeWire frame.

## Scope and diagnostic limits

This establishes coexistence and the above user flows on Debian with VMware
software rendering (WLR_RENDERER=pixman), not physical GPU/multimonitor support.
A guest RTC wake attempt did not wake this VMware configuration; a virtual
hardware key did. The final clean sleep cycle used no host suspend/checkpoint.
An earlier recovery also preserved RAM using VMware hard suspend/resume.

The minimal --no-install-recommends fixture logs missing RealtimeKit and
accessibility services, discarded audio nodes during logout, and a virtual HDA
resume warning. The test-only ydotool user service lacked uinput permission;
input used a separately scoped root fixture and localhost-only authenticated
VNC. Those are fixture diagnostics, not evidence that physical audio or input
hardware has been accepted. No global host input permissions were changed.

Stock labwc still lacks Karyo's optional layout-cycle protocol. Physical GPU,
multiple displays, physical sleep devices and the reviewed compositor extension
remain separate gates. Files/Settings, distro/ISO stages and optional privileged
integrations remain subsequent migration work.
