FROM debian:trixie
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake ninja-build python3 dpkg-dev \
    qt6-base-dev qt6-base-dev-tools \
    && rm -rf /var/lib/apt/lists/*

# SVG is needed by the separately packaged desktop icon integration.
RUN apt-get update && apt-get install -y --no-install-recommends qt6-svg-dev \
    && rm -rf /var/lib/apt/lists/*
