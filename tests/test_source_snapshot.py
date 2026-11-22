# SPDX-License-Identifier: GPL-3.0-or-later
"""Real Git trees exercise recursive exports and fail-closed source handling."""
from argparse import Namespace
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest
from unittest.mock import patch

from karyo_builder.source_snapshot import (Snapshot, capture_recipe, environment,
    git, invocation, prepare_snapshot, public_url, source_path)

URL = "https://sources.example.invalid/team/upstream.git"
CHILD = "https://sources.example.invalid/team/library.git"
EPOCH = 1700000000


class SnapshotTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cache = self.root / "cache"
        self.cache.mkdir()
        self.repo = self.repository(URL)
        self.child = self.repository(CHILD)

    def repository(self, url):
        repo = self.cache / (hashlib.sha256(url.encode()).hexdigest() + ".git")
        git(repo, "init", "--bare", "--object-format=sha1", str(repo))
        (repo / "karyo-source-url").write_text(url + "\n", encoding="utf-8")
        return repo

    def blob(self, repo, data):
        return subprocess.run(invocation(repo, "hash-object", "-w", "--stdin"),
            input=data, capture_output=True, check=True, env=environment()).stdout.decode().strip()

    def tree(self, repo, files):
        # Dict children become trees. Tuples carry exact Git mode/object IDs.
        records = []
        for name, value in sorted(files.items()):
            if isinstance(value, dict):
                mode, kind, oid = "040000", "tree", self.tree(repo, value)
            else:
                mode, oid = value if isinstance(value, tuple) else ("100644", self.blob(repo, value))
                kind = "commit" if mode == "160000" else "blob"
            records.append(f"{mode} {kind} {oid}\t{name}".encode() + b"\0")
        return subprocess.run(invocation(repo, "mktree", "-z", "--missing"),
            input=b"".join(records), capture_output=True, check=True, env=environment()).stdout.decode().strip()

    def commit(self, repo, files):
        tree = self.tree(repo, files)
        env = environment()
        for role in ("AUTHOR", "COMMITTER"):
            env[f"GIT_{role}_NAME"] = "Karyo snapshot fixture"
            env[f"GIT_{role}_EMAIL"] = "fixture@openkaryon.invalid"
            env[f"GIT_{role}_DATE"] = f"{EPOCH} +0000"
        message = ("Create a fixed source fixture\n\n"
                   "Keep object metadata stable for recursive export regression checks.\n\n"
                   "Use plumbing only so links and executable modes work on Windows.\n\n"
                   "Co-Authored-By: Codex <noreply@openai.com>\n")
        return subprocess.run(invocation(repo, "commit-tree", tree), input=message.encode(),
            capture_output=True, check=True, env=env).stdout.decode().strip()

    def recipe(self, revision):
        path = self.root / "recipe.json"
        path.write_text(json.dumps({"schema": 1, "source": {"url": URL, "revision": revision}}), encoding="utf-8")
        return path

    def prepare(self, revision, **kwargs):
        recipe = self.recipe(revision)
        if "external" in kwargs:
            value = json.loads(recipe.read_text(encoding="utf-8"))
            value["external_symlinks"] = kwargs["external"]
            recipe.write_text(json.dumps(value), encoding="utf-8")
        args = Namespace(recipe=recipe, cache=self.cache, output=self.root / "out",
                         fetch=False, lfs_objects=kwargs.get("objects"))
        return prepare_snapshot(args)

    def test_recursive_exact_export_preserves_modes_not_export_ignore_and_is_deterministic(self):
        child = self.commit(self.child, {"library.c": b"child source", "LICENSE": b"library license"})
        root = self.commit(self.repo, {
            ".gitattributes": b"LICENSE export-ignore\nmain.c export-subst\n",
            ".gitmodules": b'[submodule "library"]\n path = vendor/library\n url = ../library.git\n branch = ignored-floating-branch\n',
            "LICENSE": b"root license", "main.c": b"$Format:%H$ literal bytes",
            "run": ("100755", self.blob(self.repo, b"#!/bin/sh\n")),
            "alias": ("120000", self.blob(self.repo, b"vendor/library/library.c")),
            "vendor": {"library": ("160000", child)}})
        first, manifest = self.prepare(root)
        second, repeated = self.prepare(root)
        self.assertEqual(manifest["archive"], repeated["archive"])
        self.assertTrue(manifest["build_ready"])
        self.assertEqual([m["revision"] for m in manifest["modules"]], [root, child])
        self.assertEqual(manifest["source_date_epoch"], EPOCH)
        with tarfile.open(first / "source.tar.gz") as tar:
            self.assertEqual(tar.extractfile("LICENSE").read(), b"root license")
            self.assertEqual(tar.extractfile("main.c").read(), b"$Format:%H$ literal bytes")
            self.assertEqual(tar.extractfile("vendor/library/library.c").read(), b"child source")
            self.assertEqual(tar.getmember("run").mode, 0o755)
            self.assertEqual(tar.getmember("alias").linkname, "vendor/library/library.c")
            self.assertTrue(all(m.uid == 0 and m.gid == 0 and m.mtime == EPOCH for m in tar))
            self.assertFalse(any(".git/" in m.name for m in tar))
        self.assertFalse((self.repo / "refs/heads/main").exists())
        self.assertEqual(git(self.repo, "remote").stdout, b"")
        self.assertEqual((first / "source.tar.gz").read_bytes(), (second / "source.tar.gz").read_bytes())

    def test_lfs_inventory_then_exact_local_materialization(self):
        data = b"an upstream binary object" * 100
        digest = hashlib.sha256(data).hexdigest()
        pointer = f"version https://git-lfs.github.com/spec/v1\noid sha256:{digest}\nsize {len(data)}\n".encode()
        revision = self.commit(self.repo, {"runtime.dylib": pointer})
        inventory, manifest = self.prepare(revision)
        self.assertFalse(manifest["build_ready"])
        self.assertEqual(manifest["lfs"][0]["sha256"], digest)
        with tarfile.open(inventory / "source.tar.gz") as tar:
            self.assertEqual(tar.extractfile("runtime.dylib").read(), pointer)
        objects = self.root / "lfs"
        objects.mkdir()
        (objects / digest).write_bytes(data)
        final, materialized = self.prepare(revision, objects=objects)
        self.assertTrue(materialized["build_ready"])
        self.assertTrue(materialized["lfs"][0]["materialized"])
        with tarfile.open(final / "source.tar.gz") as tar:
            self.assertEqual(tar.extractfile("runtime.dylib").read(), data)
        (objects / digest).write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "checksum/size"):
            self.prepare(revision, objects=objects)
        self.assertEqual(len(list((self.root / "out").glob("karyo-source-snapshot-*"))), 2)
        self.assertEqual(len(list((self.root / "out").glob(".failed-snapshot-*"))), 1)

    def test_offline_never_fetches_missing_revision(self):
        self.commit(self.repo, {"present": b"yes"})
        with patch("karyo_builder.source_snapshot.subprocess.run", wraps=subprocess.run) as runner:
            with self.assertRaisesRegex(ValueError, "offline"):
                self.prepare("a" * 40)
            self.assertFalse(any("fetch" in call.args[0] for call in runner.call_args_list))
        self.assertFalse(list(self.cache.glob("*.lock")))

    def test_submodule_file_url_is_rejected_without_running_update(self):
        child = self.commit(self.child, {"code": b"child"})
        revision = self.commit(self.repo, {"module": ("160000", child),
            ".gitmodules": b'[submodule "module"]\n path = module\n url = file:///private/source\n'})
        with self.assertRaisesRegex(ValueError, "HTTPS"):
            self.prepare(revision)
        self.assertFalse(list((self.root / "out").glob("karyo-source-snapshot-*")))

    def test_missing_and_duplicate_gitmodule_mapping_fail(self):
        child = self.commit(self.child, {"code": b"child"})
        for content in (b'', b'[submodule "a"]\n path = module\n path = other\n url = ../library.git\n',
                        b'[submodule "a"]\n path = other\n url = ../library.git\n'):
            revision = self.commit(self.repo, {"module": ("160000", child), ".gitmodules": content})
            with self.assertRaises((ValueError, RuntimeError)):
                self.prepare(revision)

    def test_symlink_escape_and_chain_escape_fail_without_publishing(self):
        for files in ({"link": ("120000", self.blob(self.repo, b"../outside"))},
                      {"link": ("120000", self.blob(self.repo, b"/etc/passwd"))},
                      {"a": ("120000", self.blob(self.repo, b".")),
                       "dir": {"b": ("120000", self.blob(self.repo, b"../a/../outside"))}},
                      {"a": ("120000", self.blob(self.repo, b"b")),
                       "b": ("120000", self.blob(self.repo, b"a"))}):
            with self.assertRaisesRegex(ValueError, "symlink"):
                self.prepare(self.commit(self.repo, files))
        self.assertFalse(list((self.root / "out").glob("karyo-source-snapshot-*")))

    def test_exact_reviewed_external_link_is_preserved_and_reported(self):
        revision = self.commit(self.repo, {"Developer": {"git": ("120000", self.blob(self.repo, b"/usr/bin/git"))}})
        output, manifest = self.prepare(revision, external={"Developer/git": "/usr/bin/git"})
        self.assertEqual(manifest["external_symlinks"], {"Developer/git": "/usr/bin/git"})
        with tarfile.open(output / "source.tar.gz") as tar:
            self.assertEqual(tar.getmember("Developer/git").linkname, "/usr/bin/git")
        with self.assertRaisesRegex(ValueError, "target changed"):
            self.prepare(revision, external={"Developer/git": "/other/git"})
        with self.assertRaisesRegex(ValueError, "absent"):
            self.prepare(revision, external={"Developer/git": "/usr/bin/git", "unused": "/outside"})

    def test_declared_external_link_cannot_be_traversed_by_another_entry(self):
        revision = self.commit(self.repo, {
            "external": ("120000", self.blob(self.repo, b"/outside")),
            "alias": ("120000", self.blob(self.repo, b"external/file"))})
        with self.assertRaisesRegex(ValueError, "traverses an external"):
            self.prepare(revision, external={"external": "/outside"})

    def test_binary_blob_is_streamed_and_verified(self):
        data = bytes(range(256)) * 9000
        result, _ = self.prepare(self.commit(self.repo, {"large": data, "empty": b""}))
        with tarfile.open(result / "source.tar.gz") as tar:
            self.assertEqual(tar.extractfile("large").read(), data)
            self.assertEqual(tar.extractfile("empty").read(), b"")

    def test_malformed_pointer_is_not_labeled_build_ready(self):
        revision = self.commit(self.repo, {"bad": b"version https://git-lfs.github.com/spec/v1\nnot-an-object\n"})
        with self.assertRaisesRegex(ValueError, "Malformed LFS"):
            self.prepare(revision)

    def test_concurrent_cache_use_does_not_steal_lock(self):
        revision = self.commit(self.repo, {"code": b"source"})
        lock = self.cache / (hashlib.sha256(URL.encode()).hexdigest() + ".lock")
        lock.write_text("another-builder\n")
        with self.assertRaises(FileExistsError):
            self.prepare(revision)
        self.assertEqual(lock.read_text(), "another-builder\n")

    def test_rejects_cache_identity_mismatch(self):
        revision = self.commit(self.repo, {"code": b"source"})
        (self.repo / "karyo-source-url").write_text(CHILD + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "identity"):
            self.prepare(revision)

    def test_rejects_floating_credentials_extra_and_duplicate_fields(self):
        valid = {"schema": 1, "source": {"url": URL, "revision": "1" * 40}}
        cases = [dict(valid, unknown=True), dict(valid, schema=True),
                 dict(valid, source={"url": URL, "revision": "main"}),
                 dict(valid, source={"url": "https://user:password@example.invalid/repo", "revision": "1" * 40})]
        for value in cases:
            path = self.root / "bad.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaises(ValueError):
                capture_recipe(path)
        path.write_text('{"schema":1,"schema":1,"source":{}}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            capture_recipe(path)

    def test_git_environment_cannot_inherit_project_config_or_helpers(self):
        with patch.dict(os.environ, {"GIT_DIR": "private-project", "GIT_CONFIG_COUNT": "1",
                                    "GIT_CONFIG_KEY_0": "url.file:///private.insteadof",
                                    "GIT_CONFIG_VALUE_0": "https://"}):
            clean = environment()
        self.assertNotIn("GIT_DIR", clean)
        self.assertNotIn("GIT_CONFIG_COUNT", clean)
        self.assertEqual(clean["GIT_TERMINAL_PROMPT"], "0")
        command = invocation(self.repo, "fetch", "--depth=1", URL, "1" * 40)
        self.assertIn("credential.helper=", command)
        self.assertIn("protocol.allow=never", command)
        self.assertIn("fetch.fsckObjects=true", command)

    def test_rejects_unsafe_urls_and_paths(self):
        for value in ("ssh://example/repo", "https://example/repo?token=secret", "https://example/repo#ref",
                      "https://example/repo\n", "file:///repo", "ext::touch file"):
            with self.assertRaises(ValueError):
                public_url(value)
        for value in ("../x", "/x", "a/../x", "a\\x", ".git/config", "a/.GIT/config", "a//b", "a\x00b"):
            with self.assertRaises(ValueError):
                source_path(value)


if __name__ == "__main__":
    unittest.main()
