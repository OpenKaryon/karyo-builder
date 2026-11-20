FROM debian:trixie
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake ninja-build python3 dpkg-dev \
    qt6-base-dev qt6-base-dev-tools \
    && rm -rf /var/lib/apt/lists/*

# SVG is needed by the separately packaged desktop icon integration.
RUN apt-get update && apt-get install -y --no-install-recommends qt6-svg-dev \
    && rm -rf /var/lib/apt/lists/*

# Standalone session development and isolated headless acceptance tools.
RUN apt-get update && apt-get install -y --no-install-recommends \
    qt6-wayland qt6-wayland-dev qt6-wayland-private-dev qt6-base-private-dev \
    libpam0g-dev liblayershellqtinterface-dev libpolkit-qt6-1-dev \
    labwc dbus-daemon wayland-utils wtype grim procps \
    && rm -rf /var/lib/apt/lists/*
