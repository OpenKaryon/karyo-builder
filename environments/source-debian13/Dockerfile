FROM debian:trixie
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3 dpkg-dev debhelper fakeroot quilt ca-certificates pkgconf \
    && rm -rf /var/lib/apt/lists/*
