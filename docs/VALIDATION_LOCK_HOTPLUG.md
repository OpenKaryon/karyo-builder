# Lock output-lifecycle regression acceptance

The old installed 156d1aa lock reproduces the Ubuntu wallpaper-only VT-return
defect. DE correction 283cce4 separates lock ownership and PAM from output views.
This file records the source-overlay gate; final native DEB acceptance follows.

## Source overlays

### Debian

- Native binary SHA256: d78516dfe8c52ae177ffa4d5564523b065ea98107321f59ba27631ab6db46087.
- Temporary wrapper SHA256: 0b446d4de8d9ba430a1b80c253745ddd9d8303e12446c41392ddbf9e1dba69c7.
- Per-file source hashes: out/debian-vm-qa/lock-hotplug-input/record.json.

### Ubuntu

- Native binary SHA256: f40ee3202c6bd362d59d327985b8d31d940fc1a470465995cd94048538319829.
- Temporary wrapper SHA256: 0b446d4de8d9ba430a1b80c253745ddd9d8303e12446c41392ddbf9e1dba69c7.
- Per-file source hashes: out/ubuntu-vm-qa/lock-hotplug-input/record.json.

The fixture wrapper is installed only under /usr/local/bin on the disposable
VMs and executes a separately named /usr/local/libexec QA binary. It never
replaces the packaged /usr/bin/karyo-lock, and dpkg verification remains clean.
The ordinary installed-policy fixture identifies the product binary by name,
so its initial-lock check deliberately does not accept this differently named
overlay. A separate exact-argv/UID/LockedHint/no-client probe verifies that stage.

## Before and after

Old Ubuntu source stays locked but loses the password form after vmwgfx removes
all outputs during VT deactivation. Its screenAdded path creates only decoration
views. The replacement source keeps a hidden display connection for the lock,
ignores Qt placeholders without wl_output and gives every real output a password
form. One shared PAM operation survives screen replacement and disables all forms.
Deferred role creation rechecks its guarded screen/output; unlock flushes through
the original display instead of a potentially removed toplevel.

Native Qt 6.8 and Qt 6.10 builds pass lock layout/PAM, session launcher and account
reader checks. Actual QA initial PAM still works with the corrected source.
Both VMs then leave the active graphical VT, confirm LockedHint while inactive
and return to an interactive password form. Wrong passwords fail; correct ones
return to the same shell: Debian PID 27850 and Ubuntu PID 78374. A second Ubuntu
output replacement during the wrong-password PAM delay retains an interactive
error/retry form and subsequently accepts the correct password.

Ubuntu captures lock-hotplug-return.png and lock-hotplug-wrong.png show the
restored form/error where startup-return-current.png showed wallpaper alone.
Debian has corresponding initial/return/wrong captures. Each guest has
lock-hotplug-native.log, overlay-install and overlay-cleanup logs under results.

Only known unchanged root metadata is removed after original account/PAM hash
checks. Cleanup verifies exact overlay hashes before removing its wrapper and
binary, terminates QA graphical sessions and preserves original LightDM. Both
dpkg verification and audit are clean. Source credentials, personal endpoints
and owner systems are not modified. The original fixed-host QA fixture binary
and previous root-only PAM recovery snapshots remain for the final package run.

This establishes one virtual display with real VT-driven output replacement,
not a physical multi-monitor/GPU matrix. It also does not complete privileged
two-profile switching. Clean lock package builds from exact 283cce4 are running;
their installed final acceptance is a separate required gate.
