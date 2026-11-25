# Final joined DE and Builder acceptance

This checkpoint closes the selected DE/Builder migration tails on native Debian
13 and Ubuntu 26.04 QA systems. It uses DE
`3d7b5f4ade8bccbe6b510972ae666a7a9e1e14c4` and Builder
`6e210edc1c5102b59af36407229bd8357be87216`. Subsequent changes in this checkpoint
are acceptance documentation. Existing compatibility engines are frozen;
distribution policy, ISO assembly and Forge remain outside this scope.

## Joined package cohort

The joined root graph produces 42 packages per base, including the optional
main-login, LightDM and physical-network integration packages. All 84 DEBs,
their component manifests and shared build logs are hash-verified. The
[artifact matrix](VALIDATION_FINAL_JOINED_PACKAGES.json) records versions,
sizes, hashes, immutable SDK image identities and actual selected test names.
Recipes use the captured public source revision and the joined build directory.
This does not claim that every standalone component entry was rebuilt.

Each build runs one job, without build-time networking, using Builder's standard
4 GiB container limit. Eighteen selected CTest groups pass per base, including
the PAM module ABI. The requested optional name `desktop-entry` matches no test;
the actual `desktop-entry-icons` group is subsequently run once against each
same build and reports 29 Qt cases, all passing. This is selected ordinary
validation, not an all-tests assertion.

Forty-one packages install and purge on each clean native SDK container. The
optional RAR codec addon is built and hash-verified but excluded from this
installation slice. Service startup is inhibited in these containers. Package
payload verification and `dpkg --audit` are clean. Original accounts, PAM/DM
files, enabled-unit baseline and an owned data fixture's identity, permissions
and content are restored or preserved after purge. Installed launcher and
worker payloads are then absent. No graphical or boot behavior is inferred
from this container check.

Two effects of explicitly selected optional packages are intentional during
installation: the password-sync PAM hook and the two VMware service enablement
links. Purge restores their original baseline. The first Debian observer
incorrectly expected those links to remain unchanged; a read-only observation
and normal purge establish the retained baseline before the corrected complete
cycle passes. This is not a package workaround or a hidden system edit.

## Native core desktop coexistence

On separate native desktop QA guests, ordinary APT reinstallation of the current
22 core packages preserves the running Xfce PID, accounts/groups, existing
PAM/LightDM configuration, package versions and original user data. Exact
installed regular files and symlinks match the new DEBs.

Both systems then complete real Xfce logout, select Karyo in LightDM and enter
with the unchanged fixture credential. The actual session uses Karyo-scoped
configuration and association views. Terminal launches from the panel. A
harmless `pkexec /usr/bin/true` request displays the native authentication card,
normal authentication succeeds, and the recorded command exit is zero.

Files' visible Open With menu opens the original text fixture in the installed
Text Editor. The exact argument and unchanged data digest are independently
verified, and the real editor frame is viewed. Application windows close
normally; Start -> Sign out returns to LightDM. Ordinary selection and login
to Xfce starts a fresh native Xfce process. Karyo session processes, activation
views and Qt overrides are gone, the original authentication agent runs again,
and accounts/PAM/DM/data checks and package audit remain clean.

## Three desktops and current native runtime packages

The profile QA guests install the matching reviewed native compositor pairs:
Debian labwc `0.8.3-1+karyo12` with wlroots `0.18.2-3+karyo4`, and Ubuntu
labwc `0.9.3-1+karyo9` with wlroots `0.19.2-1+karyo3`. Their existing desktops
first log out normally. The exact temporary autologin configuration is saved,
then restored after installation; a fresh ordinary Home entry follows.

Home, Work and Experiments have three independent network namespaces and three
owned resolver views. Actual Start-menu dispatch switches Home/Work without a
password. The first Experiments entry presents the native protected login
before its shell starts. The unchanged Home password unlocks it. Returning
Home and entering the same Experiments lifetime again asks for that password
again. Independent receipts establish unchanged neighboring contexts and live
TCP/UDP payloads, including Work's private peer DNS.

Thirty-six current runtime packages upgrade while all three profiles exist;
owner restart preserves their exact captured records. Development packages,
the optional greeter and RAR addon are excluded from this live-runtime slice.
The explicitly installed password-sync component adds its one ordinary PAM
hook. Ubuntu verifies the exact pre/post delta; Debian's initial observer stops
at the expected changed file and retains that limitation, followed by account
timestamp/configuration, hook/payload checks and actual unchanged-password
authentication. No claim of a missing original Debian full-file PAM hash is
substituted. Both native package audits and payload verification are clean.

## Ordinary external GUI and populated reboot

A separately maintained external client uses the general launcher and public
managed-worker boundary without DE code depending on its package identity.
An explicitly supplied dedicated test account enables real GUI file import,
registration/bootstrap, ordinary native connection and native authorization
on both systems. The supplied secret is not typed into an import text field,
shown in a log, committed or included in build inputs.

Both actual GUIs reach Connected. An independent ordinary Home process verifies
external HTTPS and UDP DNS, TUN route selection and increasing receive/transmit
counters. Work simultaneously preserves private peer DNS and TCP/UDP nonce
exchange; Experiments preserves direct payloads. Clicking the GUI's normal
disconnect returns it to Ready. Independent selectors show no owned TUN,
routes/rules/firewall resources, worker journal entries or worker units. Ordinary
GUI reconnect then repeats the successful traffic and neighboring isolation.
This closes the previously separate account/enrollment GUI gate for this tested
client input, without asserting compatibility with every external application.

Each VM performs a real kernel reboot with all three desktops, Work's upstream
VPN and the Home GUI worker live. The captured reboot interval has no Karyo
service stop failure or stop timeout; worker, resolver, bus and network services
have actual stopped records. The new boot ID differs, old lifetime paths and
workers are absent, accounts/PAM/autologin bytes remain unchanged, and Home
enters a fresh lifetime. A first post-reboot Experiments entry again presents
the locked native login before shell startup and accepts the same Home password.

The first controller attempted a subsequent action before the asynchronously
starting Work shell owned its bus name. It performed no fallback launch;
observed shell readiness precedes the successful ordinary switches. Those
controller attempts are retained separately from product acceptance.

## Evidence, cleanup and remaining boundary

Native root receipts, private GUI frames, component manifests and controller
logs are joined by an ignored local evidence index. Public artifacts contain
only neutral acceptance facts and build metadata, not account/profile names,
external client declarations, endpoints or credentials.

After acceptance, all three QA profiles log out normally and their owned
namespaces/processes retire. The inactive test client package, imported profile,
cache and temporary credential copies are removed. The operator's source file
is untouched; server-side test device registrations remain for operator
revocation. Exact captured temporary TLS and peer-lab services, credentials,
binaries and the one test route are retired; clean-install containers are
removed after their purge evidence is saved. Existing desktop-only QA guests
remain in Xfce with original data intact.

[Actual VMware Windows-host channels](VALIDATION_VMWARE_NATIVE.md) remain open:
Windows Computer Use fails during initialization before a window can be
acquired. Native Linux GUI/RFB observations do not prove host clipboard, DnD or
host-driven display resize. Physical Wi-Fi, a different physical interface or
gateway, untested monitor layouts and IPv6 are not covered here; IPv6 remains
disabled. Those retained boundaries must stay explicit when the distribution
and ISO stage is planned.
