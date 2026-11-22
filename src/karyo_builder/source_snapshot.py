# SPDX-License-Identifier: GPL-3.0-or-later
"""Export exact recursive Git trees without checking out upstream code."""
from contextlib import contextmanager
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import posixpath
import re
import subprocess
import tarfile
from urllib.parse import urljoin, urlsplit
import uuid

from . import __version__

PIN = re.compile(r"[0-9a-f]{40}")
LFS = re.compile(rb"version https://git-lfs.github.com/spec/v1\noid sha256:([0-9a-f]{64})\nsize (0|[1-9][0-9]*)\n?")


def public_url(value):
    if not isinstance(value, str) or any(ord(c) <= 32 or ord(c) == 127 for c in value):
        raise ValueError("Source URLs must be public HTTPS URLs without whitespace")
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username is not None
            or parsed.password is not None or parsed.query or parsed.fragment
            or "\\" in value or not parsed.path.startswith("/")):
        raise ValueError("Only public HTTPS Git URLs without credentials/query/fragment are supported")
    return value


def capture_recipe(path):
    def distinct(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate snapshot recipe field: " + key)
            result[key] = value
        return result
    data = Path(path).read_bytes()
    recipe = json.loads(data, object_pairs_hook=distinct)
    if not isinstance(recipe, dict) or not {"schema", "source"} <= recipe.keys() or not recipe.keys() <= {"schema", "source", "external_symlinks"} or type(recipe["schema"]) is not int or recipe["schema"] != 1:
        raise ValueError("Expected snapshot schema 1 and source only")
    source = recipe["source"]
    if not isinstance(source, dict) or set(source) != {"url", "revision"}:
        raise ValueError("Source requires exactly url and revision")
    public_url(source["url"])
    if not isinstance(source["revision"], str) or not PIN.fullmatch(source["revision"]):
        raise ValueError("Source revision must be an exact lowercase 40-digit Git commit")
    external = recipe.get("external_symlinks", {})
    if not isinstance(external, dict):
        raise ValueError("external_symlinks must be an exact path-to-target table")
    for name, target in external.items():
        source_path(name)
        if (not isinstance(target, str) or not target or "\\" in target
                or any(ord(c) < 32 or ord(c) == 127 for c in target)
                or any(p.casefold() == ".git" for p in target.split("/"))):
            raise ValueError("Invalid declared external symlink target")
    return recipe, hashlib.sha256(data).hexdigest()


def source_path(value):
    if (not value or value.startswith("/") or "\\" in value
            or any(ord(c) < 32 or ord(c) == 127 for c in value)
            or any(p in ("", ".", "..") or p.casefold() == ".git" for p in value.split("/"))):
        raise ValueError("Unsafe source path: " + repr(value))
    return value


def environment():
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_SYSTEM=os.devnull,
               GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0",
               GIT_NO_REPLACE_OBJECTS="1", GIT_LFS_SKIP_SMUDGE="1")
    return env


def invocation(cache, *args):
    # No project/user configuration, credential helpers, executable protocols,
    # checkout filters, hooks or submodule update commands are used.
    return ["git", "-c", "credential.helper=", "-c", "core.hooksPath=" + os.devnull,
            "-c", "protocol.allow=never", "-c", "protocol.https.allow=always",
            "-c", "http.extraHeader=", "-c", "fetch.fsckObjects=true",
            "--git-dir=" + str(cache), *args]


def git(cache, *args, timeout=300, check=True):
    result = subprocess.run(invocation(cache, *args), env=environment(),
                            capture_output=True, timeout=timeout)
    if check and result.returncode:
        detail = result.stderr.decode("utf-8", "replace")[-3000:].strip()
        raise RuntimeError("Source Git operation failed: " + detail)
    return result


@contextmanager
def cache_repository(root, url, revision, fetch):
    key = hashlib.sha256(url.encode()).hexdigest()
    cache = root / (key + ".git")
    lock = root / (key + ".lock")
    # Simultaneous builders must not change the same bare object store. A lock
    # left by a killed process needs explicit operator review; never steal it.
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        with os.fdopen(descriptor, "w") as stream:
            stream.write(str(os.getpid()) + "\n")
        if cache.is_symlink() or (cache.exists() and not cache.is_dir()):
            raise ValueError("Source cache must be an ordinary directory")
        if not cache.exists():
            if not fetch:
                raise ValueError("Pinned source is not cached; explicitly use --fetch to download dependencies")
            git(cache, "init", "--bare", "--object-format=sha1", str(cache))
            (cache / "karyo-source-url").write_text(url + "\n", encoding="utf-8")
        marker = cache / "karyo-source-url"
        if marker.is_symlink() or marker.read_text(encoding="utf-8") != url + "\n":
            raise ValueError("Source cache identity does not match the recipe URL")
        exists = git(cache, "cat-file", "-e", revision + "^{commit}", check=False).returncode == 0
        if not exists:
            if not fetch:
                raise ValueError("Pinned revision is absent from the offline source cache")
            git(cache, "fetch", "--depth=1", "--no-tags", "--no-recurse-submodules", url, revision)
        actual = git(cache, "rev-parse", "--verify", revision + "^{commit}").stdout.decode().strip()
        if actual != revision:
            raise ValueError("Source identity is not the requested commit")
        git(cache, "fsck", "--full", "--no-reflogs", "--no-dangling", revision)
        yield cache
    finally:
        lock.unlink()


class Blobs:
    """One sequential cat-file process per repository, without smudge filters."""
    def __init__(self, cache):
        self.process = subprocess.Popen(invocation(cache, "cat-file", "--batch"),
                                        env=environment(), stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.remaining = 0

    def begin(self, oid):
        if self.remaining:
            raise RuntimeError("Previous source blob was not fully consumed")
        self.process.stdin.write(oid.encode() + b"\n")
        self.process.stdin.flush()
        fields = self.process.stdout.readline().split()
        if len(fields) != 3 or fields[0] != oid.encode() or fields[1] != b"blob":
            raise ValueError("Missing or non-blob source object")
        self.remaining = int(fields[2])
        self.digest = hashlib.sha1(b"blob " + fields[2] + b"\0")
        self.oid = oid
        return self.remaining

    def read(self, size=-1):
        count = self.remaining if size < 0 else min(size, self.remaining)
        data = self.process.stdout.read(count)
        if len(data) != count:
            raise ValueError("Truncated source blob")
        self.remaining -= count
        self.digest.update(data)
        return data

    def finish(self):
        if self.remaining or self.process.stdout.read(1) != b"\n" or self.digest.hexdigest() != self.oid:
            raise ValueError("Source blob integrity check failed")

    def close(self):
        self.process.stdin.close()
        self.process.stdout.close()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()


def submodules(cache, revision, entries):
    links = {path for mode, _, path in entries if mode == "160000"}
    if not links:
        return {}
    if not any(path == ".gitmodules" and mode in ("100644", "100755") for mode, _, path in entries):
        raise ValueError("Gitlinks require a tracked regular .gitmodules file")
    raw = git(cache, "config", "--no-includes", "--null", "--blob", revision + ":.gitmodules",
              "--get-regexp", r"^submodule\..*\.(path|url)$").stdout
    sections = {}
    for record in raw.rstrip(b"\0").split(b"\0"):
        key, separator, value = record.partition(b"\n")
        if not separator:
            raise ValueError("Malformed .gitmodules configuration")
        name, _, field = key.decode("utf-8").rpartition(".")
        fields = sections.setdefault(name, {})
        if field in fields:
            raise ValueError("Duplicate submodule field")
        fields[field] = value.decode("utf-8")
    mapping = {}
    for fields in sections.values():
        if set(fields) != {"path", "url"}:
            raise ValueError("Submodule requires exactly one path and URL")
        path = source_path(fields["path"])
        if path in mapping:
            raise ValueError("Duplicate submodule path")
        mapping[path] = fields["url"]
    if not links <= mapping.keys():
        raise ValueError("Gitlink has no matching .gitmodules entry")
    return mapping


class Snapshot:
    def __init__(self, cache, fetch=False, objects=None, external_symlinks=None):
        self.cache = Path(cache).resolve()
        self.cache.mkdir(parents=True, exist_ok=True)
        self.fetch = fetch
        self.objects = Path(objects).resolve(strict=True) if objects is not None else None
        self.modules = []
        self.lfs = []
        self.members = 0
        self.links = {}
        self.external = dict(external_symlinks or {})
        self.paths = []
        self.active = set()

    def validate_links(self):
        # Check actual component-by-component resolution, including links in a
        # target's ancestors. Lexical normalization alone misses a/../ escapes
        # when a itself points somewhere shallower in the snapshot.
        if not self.external.keys() <= self.links.keys():
            raise ValueError("Declared external symlink is absent from the source")
        for name in self.paths:
            pending, resolved, followed = name.split("/"), [], 0
            while pending:
                part = pending.pop(0)
                if part in ("", "."):
                    continue
                if part == "..":
                    if not resolved:
                        raise ValueError("Source symlink chain escapes snapshot: " + name)
                    resolved.pop()
                    continue
                resolved.append(part)
                current = "/".join(resolved)
                if current in self.external:
                    if pending:
                        raise ValueError("Source path traverses an external symlink: " + name)
                    break
                if current in self.links:
                    followed += 1
                    if followed > 40:
                        raise ValueError("Source symlink cycle/depth exceeded: " + name)
                    resolved.pop()
                    pending = self.links[current].split("/") + pending

    def export(self, url, revision, tar, epoch, prefix="", depth=0):
        if depth > 32 or (url, revision) in self.active:
            raise ValueError("Recursive source dependency cycle/depth exceeded")
        self.active.add((url, revision))
        print(f"Source module {prefix or '.'}: {url}@{revision}", flush=True)
        try:
            with cache_repository(self.cache, url, revision, self.fetch) as cache:
                entries = []
                for record in git(cache, "ls-tree", "-r", "-z", revision).stdout.split(b"\0"):
                    if not record:
                        continue
                    metadata, separator, name = record.partition(b"\t")
                    mode, kind, oid = metadata.decode("ascii").split()
                    if not separator or mode not in ("100644", "100755", "120000", "160000"):
                        raise ValueError("Unsupported source tree entry")
                    if kind != ("commit" if mode == "160000" else "blob") or not PIN.fullmatch(oid):
                        raise ValueError("Invalid source object identity")
                    entries.append((mode, oid, source_path(name.decode("utf-8"))))
                mapping = submodules(cache, revision, entries)
                self.modules.append({"path": prefix or ".", "url": url, "revision": revision,
                                     "tree": git(cache, "rev-parse", revision + "^{tree}").stdout.decode().strip()})
                blobs = Blobs(cache)
                try:
                    for mode, oid, path in entries:
                        name = source_path(prefix + path)
                        if mode == "160000":
                            child = mapping[path]
                            if child.startswith(("./", "../")):
                                child = urljoin(url.rstrip("/") + "/", child)
                            self.export(public_url(child), oid, tar, epoch, name + "/", depth + 1)
                            continue
                        self.paths.append(name)
                        size = blobs.begin(oid)
                        member = tarfile.TarInfo(name)
                        member.uid = member.gid = 0
                        member.uname = member.gname = ""
                        member.mtime = epoch
                        member.mode = 0o755 if mode == "100755" else 0o644
                        if mode == "120000":
                            if size > 4096:
                                raise ValueError("Oversized source symlink")
                            target = blobs.read().decode("utf-8")
                            blobs.finish()
                            normalized = posixpath.normpath(posixpath.join(posixpath.dirname(name), target))
                            if (not target or "\\" in target
                                    or any(ord(c) < 32 or ord(c) == 127 for c in target)
                                    or any(p.casefold() == ".git" for p in target.split("/"))):
                                raise ValueError("Invalid source symlink target: " + name)
                            if name in self.external:
                                if self.external[name] != target:
                                    raise ValueError("Declared external symlink target changed: " + name)
                            elif target.startswith("/") or normalized == ".." or normalized.startswith("../"):
                                raise ValueError("Source symlink escapes snapshot: " + name)
                            self.links[name] = target
                            member.type = tarfile.SYMTYPE
                            member.linkname = target
                            tar.addfile(member)
                        elif size <= 1024:
                            data = blobs.read()
                            blobs.finish()
                            pointer = LFS.fullmatch(data.replace(b"\r\n", b"\n"))
                            if data.startswith(b"version https://git-lfs.github.com/spec/") and not pointer:
                                raise ValueError("Malformed LFS pointer: " + name)
                            if pointer:
                                digest, length = pointer[1].decode(), int(pointer[2])
                                item = {"path": name, "sha256": digest, "bytes": length,
                                        "pointer_blob": oid, "materialized": False}
                                if self.objects is not None:
                                    source = self.objects / digest
                                    if source.is_symlink() or not source.is_file():
                                        raise ValueError("Missing regular LFS object: " + digest)
                                    with source.open("rb") as stream:
                                        if source.stat().st_size != length or hashlib.file_digest(stream, "sha256").hexdigest() != digest:
                                            raise ValueError("LFS object checksum/size mismatch: " + name)
                                        stream.seek(0)
                                        member.size = length
                                        tar.addfile(member, stream)
                                    item["materialized"] = True
                                else:
                                    member.size = len(data)
                                    tar.addfile(member, io.BytesIO(data))
                                self.lfs.append(item)
                            else:
                                member.size = len(data)
                                tar.addfile(member, io.BytesIO(data))
                        else:
                            member.size = size
                            tar.addfile(member, blobs)
                            blobs.finish()
                        self.members += 1
                finally:
                    blobs.close()
        finally:
            self.active.remove((url, revision))


def prepare_snapshot(args):
    recipe, recipe_hash = capture_recipe(args.recipe)
    source = recipe["source"]
    snapshot = Snapshot(args.cache, args.fetch, args.lfs_objects, recipe.get("external_symlinks"))
    # Resolve root metadata before opening the archive. The same exact commit
    # is checked again during export; a cached floating branch is never used.
    with cache_repository(snapshot.cache, source["url"], source["revision"], args.fetch) as cache:
        epoch = int(git(cache, "show", "-s", "--format=%ct", source["revision"]).stdout)
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    job = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    stage = output / (".partial-snapshot-" + job)
    stage.mkdir()
    try:
        archive = stage / "source.tar.gz"
        with archive.open("wb") as raw:
            with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as zipped:
                with tarfile.open(fileobj=zipped, mode="w|", format=tarfile.PAX_FORMAT) as tar:
                    snapshot.export(source["url"], source["revision"], tar, epoch)
                    snapshot.validate_links()
        with archive.open("rb") as stream:
            archive_hash = hashlib.file_digest(stream, "sha256").hexdigest()
        manifest = {"schema": 1, "kind": "source-snapshot", "builder_version": __version__,
                    "source": source, "external_symlinks": snapshot.external, "recipe_sha256": recipe_hash, "source_date_epoch": epoch,
                    "git_version": git(snapshot.cache, "--version").stdout.decode().strip(),
                    "modules": snapshot.modules, "members": snapshot.members, "lfs": snapshot.lfs,
                    "build_ready": all(item["materialized"] for item in snapshot.lfs),
                    "archive": {"file": archive.name, "sha256": archive_hash, "bytes": archive.stat().st_size},
                    "exporter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        (stage / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        (stage / "SHA256SUMS").write_text(archive_hash + "  source.tar.gz\n", encoding="utf-8")
        final = output / ("karyo-source-snapshot-" + job)
        if final.parent != output or stage.parent != output:
            raise ValueError("Snapshot results must remain inside the selected output directory")
        stage.rename(final)
    except BaseException:
        failed = output / (".failed-snapshot-" + job)
        if stage.parent != output or failed.parent != output:
            raise ValueError("Failed snapshot must remain inside the selected output directory")
        stage.rename(failed)
        raise
    print("Source snapshot: " + str(final))
    if not manifest["build_ready"]:
        print("LFS objects remain unresolved; this snapshot is an inventory, not build-ready source")
    return final, manifest


def source_snapshot(args):
    prepare_snapshot(args)
    return 0
