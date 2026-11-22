# SPDX-License-Identifier: GPL-3.0-or-later
ARG BASE=karyo-builder:trixie
FROM ${BASE}
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
