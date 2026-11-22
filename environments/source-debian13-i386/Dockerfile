# Build with --platform=linux/386; this is a native userspace, not a cross build.
FROM debian:trixie
RUN test "$(dpkg --print-architecture)" = i386 \
    && apt-get update && apt-get install -y --no-install-recommends \
       build-essential python3 dpkg-dev debhelper fakeroot quilt ca-certificates pkgconf \
    && rm -rf /var/lib/apt/lists/*
