FROM karyo-builder:trixie
# Optional clipboard protocol acceptance; no daemon is started in this image.
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-xlib xvfb xclip wl-clipboard && rm -rf /var/lib/apt/lists/*
