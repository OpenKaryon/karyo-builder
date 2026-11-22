# Exact recursive upstream source snapshots

`source-snapshot` prepares source inputs before the isolated native package
build. It does not execute upstream configure/build scripts, initialize working
checkouts, update project remotes, install dependencies or produce a package.
The product owning a runtime owns its source recipe, patches and packaging.

```json
{
  "schema": 1,
  "source": {
    "url": "https://example.org/team/project.git",
    "revision": "0123456789abcdef0123456789abcdef01234567"
  }
}
```

These fields and the optional exact `external_symlinks` table are accepted. Revisions are complete lowercase SHA-1 commit
IDs, including every recursive gitlink. Floating branches and submodule branch
settings are not used. Public HTTPS URLs may be absolute or use Git's `../`
sibling-relative syntax inside `.gitmodules`. Authenticated repositories, local
paths, SSH, executable protocols, URL credentials and query strings are outside
this stage. Fetches require normal authenticated TLS; a commit ID is an identity
pin, not evidence that a publisher signed or endorsed the source.

```sh
karyo-builder source-snapshot upstream.json --cache /separate/upstream-cache \
  --output out/sources --fetch
# The same operation defaults to offline, using only already cached objects:
karyo-builder source-snapshot upstream.json --cache /separate/upstream-cache \
  --output out/sources
```

Missing objects are downloaded only with explicit `--fetch`, using shallow,
no-tag fetches of exact commits into URL-keyed bare repositories. There is no
working checkout, configured origin or recursive `git submodule update`.
System/user Git configuration and inherited `GIT_*` variables are excluded;
credential helpers, hooks, filters, replacement objects and unsafe protocols
are not used. Cache locks serialize each repository. A lock surviving a killed
process requires operator review; another builder does not steal it.

`git fsck` checks the object store. Export walks the pinned tree, verifies each
streamed blob's Git object hash and preserves exact bytes, executable bits and
relative symlinks. It deliberately ignores export-ignore/export-subst, so a
license cannot disappear and source strings cannot be silently rewritten.
Git administrative directories are excluded. Unsafe paths, duplicate submodule
mappings, missing gitlinks, dependency cycles and escaping/cyclic symlink chains
fail before publishing a result. Upstream code and source caches remain trusted
build inputs; this preparation is not a sandbox for hostile Git installations.

The result is `source.tar.gz`, `SHA256SUMS` and `manifest.json` in a unique output
directory. Archive order follows Git tree order; uid/gid are zero, timestamps
use the root commit time and gzip metadata is fixed. The manifest records every
module's resolved URL, commit/tree, recipe/exporter hashes, archive SHA256/size,
source date epoch, member count and LFS inventory. Identical inputs produce an
identical archive. Failed exports retain a `.failed-snapshot-*` directory rather
than publishing success or deleting source caches.

## Reviewed external symlinks

A source may deliberately stage links into a guest filesystem, such as a runtime
shipping `Developer/usr/bin/git -> /usr/bin/git`. Such links fail by default.
The product recipe can explicitly declare `"external_symlinks": {"PATH": "TARGET"}`.
Every declaration must match an existing tracked symlink and its exact target;
unknown, unused or changed declarations fail. Another entry cannot traverse one
of these links. The manifest repeats the complete table. This permits preserving
reviewed upstream bytes, not silently rewriting or broadly allowing unsafe links.
Consumers must inspect this policy and materialize source only in their isolated
build environment. Never extract an archive with external links on the host.

## LFS is explicit

Unresolved Git LFS pointer blobs are preserved and enumerated by snapshot path,
original pointer blob, SHA256 and byte size. Their result is **build_ready:false**:
it is an inventory, not usable native-build source. The command does not guess
LFS endpoints, fetch account credentials or install Git LFS globally.

A runtime's reviewed preparation may obtain its binary inputs separately, with
license and origin records. Supply the resulting SHA256-named regular files
through `--lfs-objects DIRECTORY`. Every listed object must exist and match both
size and SHA256; mismatches fail. The exporter substitutes verified bytes and
marks each entry materialized. Only a snapshot with no unresolved pointers is
`build_ready:true`. Consumers must check that field and verify the archive hash.
This status concerns source completeness, not compilation or runtime success.
Externally supplied binaries remain binaries; this command does not claim that
they were compiled from source. Their retrieval/license provenance belongs to
the product-specific source preparation alongside this manifest.

The existing `source-package` stage still accepts ordinary checksummed Debian
quilt source packages. Converting a complete snapshot and product packaging to
that input is a separate, explicit step; incomplete snapshots must not enter it.

## Validation

The host/native regression suite has65 cases. Windows Python3.14 passes with
its two existing native-symlink skips; ordinary UID1001 Debian13/Python3.13 and
Ubuntu26.04/Python3.14 pass all65 without skips. The native runner uses a
read-only source/tests/examples mount, no network, no capabilities and
no-new-privileges. `tests/environments/source-snapshot.Dockerfile` extends the
chosen QA base with Git; production CMake images do not need that dependency.

The15 snapshot-specific cases create actual bare Git fixtures with plumbing:
recursive pins/relative URLs, exact binary/mode/license preservation despite
export attributes, repeatable archives, offline behavior, LFS verification and
failure retention, duplicate/missing module metadata, external-link allowlists,
symlink chain escapes, cache identity/locks and isolated Git configuration.
These source preparation checks do not establish that an upstream runtime
compiles or runs on either base.
