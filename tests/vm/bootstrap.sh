#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
set -eu
export DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8
install -d /var/lib/karyo-qa /var/log/karyo-qa
exec >>/var/log/karyo-qa/bootstrap.log 2>&1
trap 'echo failed >/var/lib/karyo-qa/bootstrap-state' EXIT
echo starting >/var/lib/karyo-qa/bootstrap-state
apt-get update
apt-get install -y --no-install-recommends open-vm-tools openssh-server
systemctl enable --now open-vm-tools ssh
ip -4 addr
printf '%s\n' 'lightdm shared/default-x-display-manager select lightdm' | debconf-set-selections
apt-get install -y --no-install-recommends xfce4 lightdm lightdm-gtk-greeter xorg dbus-x11 \
    xdotool wmctrl x11-utils x11-xserver-utils wtype grim libnotify-bin zenity mousepad \
    xfce4-terminal network-manager network-manager-gnome mate-polkit pkexec \
    pipewire pipewire-pulse wireplumber pavucontrol chromium python3-websocket python3-gi adwaita-icon-theme librsvg2-common fonts-dejavu-core wl-clipboard wlr-randr
install -d /etc/lightdm/lightdm.conf.d
printf '%s\n' '[Seat:*]' 'user-session=xfce' 'greeter-hide-users=true' >/etc/lightdm/lightdm.conf.d/90-karyo-qa.conf
cp /etc/os-release /var/lib/karyo-qa/os.before
cp /etc/X11/default-display-manager /var/lib/karyo-qa/display-manager.before
find /usr/share/xsessions /usr/share/wayland-sessions -name '*.desktop' -type f -exec sha256sum {} \; >/var/lib/karyo-qa/sessions.before
systemctl set-default graphical.target
systemctl enable lightdm
systemctl restart lightdm
printf '%s\n' 'ready' >/var/lib/karyo-qa/bootstrap-state
trap - EXIT
