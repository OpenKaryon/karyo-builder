# SPDX-License-Identifier: GPL-3.0-or-later
FROM ubuntu:26.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates git curl xz-utils build-essential python3 dpkg-dev debhelper fakeroot quilt \
    cmake ninja-build clang llvm-dev bison flex pkg-config libfuse-dev libudev-dev \
    libcap-dev libcap2-bin libcairo2-dev libgl-dev libtiff-dev libfreetype6-dev \
    libelf-dev libxml2-dev libegl-dev libglu1-mesa-dev libfontconfig1-dev libbsd-dev \
    libxrandr-dev libxcursor-dev libgif-dev libavcodec-dev libavformat-dev \
    libswresample-dev libavutil-dev libpulse-dev libdbus-1-dev libxkbfile-dev \
    libssl-dev libvulkan-dev libcurl4-openssl-dev libedit-dev xdg-user-dirs \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /build
