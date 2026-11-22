#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Inspect native build prerequisites; this does not build or run Darling."""
import hashlib
import json
import os
from pathlib import Path
import platform
import struct
import subprocess
import tempfile


def run(args, **kwargs):
    return subprocess.run(args, check=True, capture_output=True, text=True, **kwargs).stdout.strip()


def main():
    if os.getuid() == 0 or len(set(os.getresuid())) != 1 or len(set(os.getresgid())) != 1:
        raise ValueError("SDK checks require ordinary, unmixed credentials")
    status = dict(line.split(":", 1) for line in Path("/proc/self/status").read_text().splitlines() if ":" in line)
    for field in ("CapInh", "CapPrm", "CapEff", "CapAmb"):
        if int(status[field], 16) != 0:
            raise ValueError("SDK checks must not retain capabilities")
    if status["NoNewPrivs"].strip() != "1":
        raise ValueError("SDK checks require no-new-privileges")
    distribution = platform.freedesktop_os_release()
    if (distribution["ID"], distribution["VERSION_ID"]) not in (("debian", "13"), ("ubuntu", "26.04")):
        raise ValueError("Unexpected native base")
    packages = run(["dpkg-query", "-W", "-f=${binary:Package}\t${Version}\t${Architecture}\n"])
    modules = ("fuse", "libudev", "libcap", "cairo", "gl", "libtiff-4", "freetype2", "libelf",
               "libxml-2.0", "egl", "glu", "fontconfig", "libbsd", "xrandr", "xcursor",
               "libavcodec", "libavformat", "libswresample", "libavutil", "libpulse",
               "dbus-1", "xkbfile", "openssl", "vulkan", "libcurl", "libedit")
    pkgconfig = {module: run(["pkg-config", "--modversion", module]) for module in modules}
    tools = {tool: run([tool, "--version"]).splitlines()[0]
             for tool in ("cc", "c++", "clang", "cmake", "ninja", "git", "llvm-config", "bison", "flex")}
    with tempfile.TemporaryDirectory(prefix="karyo-darling-sdk-") as temporary:
        folder = Path(temporary)
        source = folder / "check.c"
        source.write_text("int main(void) { return 0; }\n")
        executable = folder / "native"
        run(["cc", str(source), "-o", str(executable)])
        header = executable.read_bytes()
        if header[:5] != b"\x7fELF\x02" or struct.unpack_from("<H", header, 18)[0] != 62:
            raise ValueError("Native compiler did not emit Linux amd64 ELF")
        run([str(executable)])
        foreign = folder / "macos.o"
        run(["clang", "-target", "x86_64-apple-macosx10.13", "-c", str(source), "-o", str(foreign)])
        header = foreign.read_bytes()
        if header[:4] != b"\xcf\xfa\xed\xfe" or struct.unpack_from("<I", header, 4)[0] != 0x01000007 or struct.unpack_from("<I", header, 12)[0] != 1:
            raise ValueError("Clang did not emit an Intel Mach-O object")
    record = {"schema": 1, "kind": "darling-sdk", "status": "verified", "distribution": distribution,
              "uid": os.getresuid(), "gid": os.getresgid(), "capabilities": "zero", "no_new_privileges": True,
              "tools": tools, "pkg_config": pkgconfig, "packages": packages.splitlines(),
              "native_elf_compile_and_execute": True, "macho_object_compile": True,
              "darling_compiled": False, "mac_application_executed": False,
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
