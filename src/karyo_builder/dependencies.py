# SPDX-License-Identifier: GPL-3.0-or-later
"""Discover Debian dependencies from runtime ELF files in the staged payload."""
import subprocess


def discover(payload, build, package_name):
    binaries = []
    for path in sorted(payload.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        with path.open("rb") as stream:
            header = stream.read(20)
        if header[:4] != b"\x7fELF":
            continue
        if len(header) < 20 or header[4:6] != b"\x02\x01" or header[18:20] != b"\x3e\x00":
            raise RuntimeError(f"Unsupported ELF architecture in {path.relative_to(payload)}")
        if int.from_bytes(header[16:18], "little") in (2, 3):
            binaries.append(path)
    if not binaries:
        return []
    # Use Debian's installed symbols/shlibs databases rather than hard-coded ABIs.
    debian = build / "debian"
    debian.mkdir(exist_ok=True)
    (debian / "control").write_text(
        f"Source: karyo-native\n\nPackage: {package_name}\nArchitecture: any\n"
        "Description: native Karyo package\n", encoding="utf-8")
    for binary in binaries:
        subprocess.run(["strip", "--strip-unneeded", str(binary)], check=True)
    result = subprocess.run(
        ["dpkg-shlibdeps", "-O", *[f"-e{path}" for path in binaries]],
        cwd=build, check=True, stdout=subprocess.PIPE, text=True)
    prefix = "shlibs:Depends="
    values = [line[len(prefix):] for line in result.stdout.splitlines()
              if line.startswith(prefix)]
    if len(values) != 1:
        raise RuntimeError("dpkg-shlibdeps did not report its dependency result")
    return [item.strip() for item in values[0].split(",") if item.strip()]
