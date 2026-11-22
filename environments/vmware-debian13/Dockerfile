FROM karyo-xclipboard-qa:debian
# Disposable metadata for ordinary flock/parent-death worker acceptance only.
RUN install -d -o root -g root -m 0755 /run/karyo-vmware \
    && install -o root -g root -m 0644 /dev/null /run/karyo-vmware/channel
