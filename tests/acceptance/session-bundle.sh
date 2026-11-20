#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Run only in disposable debian:trixie, with runtime DEBs at /packages and
# karyo-de/tests at /checks. All users and passwords below are test fixtures.
set -eu
if [ ! -f /.dockerenv ] || [ "$(id -u)" != 0 ] || [ ! -r /checks/wayland-session-smoke.sh ]; then
    echo "This acceptance test requires its disposable Debian container and test mounts." >&2
    exit 2
fi
export DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8
mkdir -p /tmp/qa /etc/X11 /usr/share/wayland-sessions
printf '%s\n' /usr/sbin/existing-display-manager >/etc/X11/default-display-manager
printf '%s\n' '[Desktop Entry]' 'Name=Existing desktop' >/usr/share/wayland-sessions/existing.desktop
cp /etc/X11/default-display-manager /tmp/qa/display-manager.before
cp /usr/share/wayland-sessions/existing.desktop /tmp/qa/session.before
cp /etc/os-release /tmp/qa/os.before
apt-get update -qq
apt-get install -y --no-install-recommends /packages/*.deb wtype grim >/tmp/qa/apt-install.log 2>&1
karyo-session --check
! command -v cmake
QT_QPA_PLATFORM=offscreen QT_STYLE_OVERRIDE=Karyo /packages/style-runtime-consumer
! test -d /usr/include/karyo
! test -e /usr/etc/pam.d/karyo-lock
dpkg-query -W -f '${Conffiles}\n' karyo-lock | grep '/etc/pam.d/karyo-lock'
printf '\n# Local lock policy comment retained on reinstall\n' >>/etc/pam.d/karyo-lock
cp /etc/pam.d/karyo-lock /tmp/qa/pam.local
dpkg --force-confold -i /packages/karyo-lock_*.deb >/tmp/qa/lock-reinstall.log
cmp /tmp/qa/pam.local /etc/pam.d/karyo-lock
printf '\nvalue=local-fixture\n' >>/etc/karyo-builder-runtime-check/example.conf
cp /etc/karyo-builder-runtime-check/example.conf /tmp/qa/fixture.local
dpkg-deb -R /packages/karyo-builder-runtime-check_*.deb /tmp/fixture-upgrade
sed -i 's/^Version:.*/Version: 0.1.0-2/' /tmp/fixture-upgrade/DEBIAN/control
printf '\nvalue=new-shipped-fixture\n' >>/tmp/fixture-upgrade/etc/karyo-builder-runtime-check/example.conf
dpkg-deb --build --root-owner-group /tmp/fixture-upgrade /tmp/fixture-upgrade.deb >/dev/null
dpkg --force-confold -i /tmp/fixture-upgrade.deb >/tmp/qa/config-upgrade.log 2>&1
cmp /tmp/qa/fixture.local /etc/karyo-builder-runtime-check/example.conf
grep -q 'new-shipped-fixture' /etc/karyo-builder-runtime-check/example.conf.dpkg-dist
useradd -m -s /bin/sh karyo-test
printf '%s\n' 'karyo-test:KaryoTest42' | chpasswd
install -d -m 700 -o karyo-test -g karyo-test /tmp/karyo-runtime
install -d -m 777 /tmp/qa/wayland
install -d -m 755 -o karyo-test -g karyo-test /home/karyo-test/.config/autostart
printf '%s\n' '#!/bin/sh' 'echo run >> /tmp/qa/wayland/autostart-runs' >/home/karyo-test/autostart-probe.sh
chmod 755 /home/karyo-test/autostart-probe.sh
printf '%s\n' '[Desktop Entry]' 'Type=Application' 'Name=Autostart fixture' 'OnlyShowIn=Karyo;' 'Exec=/home/karyo-test/autostart-probe.sh' >/home/karyo-test/.config/autostart/fixture.desktop
runuser -u karyo-test -- env XDG_RUNTIME_DIR=/tmp/karyo-runtime KARYO_TEST_PASSWORD=KaryoTest42 KARYO_TEST_ARTIFACTS=/tmp/qa/wayland KARYO_TEST_PIPEWIRE=1 dbus-run-session -- sh /checks/wayland-session-smoke.sh
[ "$(wc -l </tmp/qa/wayland/autostart-runs)" -eq 1 ]
cmp /tmp/qa/display-manager.before /etc/X11/default-display-manager
cmp /tmp/qa/session.before /usr/share/wayland-sessions/existing.desktop
cmp /tmp/qa/os.before /etc/os-release
dpkg --remove karyo-session karyo-session-entry karyo-shell karyo-lock karyo-style karyo-builder-runtime-check >/tmp/qa/remove.log
! test -e /usr/bin/karyo-session
! test -e /usr/bin/karyo-shell
! test -e /usr/bin/karyo-lock
! test -e /usr/share/xdg-desktop-portal/karyo-portals.conf
cmp /tmp/qa/pam.local /etc/pam.d/karyo-lock
dpkg --purge karyo-lock karyo-builder-runtime-check >>/tmp/qa/remove.log
! test -e /etc/pam.d/karyo-lock
cmp /tmp/qa/display-manager.before /etc/X11/default-display-manager
cmp /tmp/qa/session.before /usr/share/wayland-sessions/existing.desktop
cmp /tmp/qa/os.before /etc/os-release
echo 'PASS clean Debian bundle installation, runtime-only session, autostart, PAM lock/unlock, conffile upgrade and removal'
