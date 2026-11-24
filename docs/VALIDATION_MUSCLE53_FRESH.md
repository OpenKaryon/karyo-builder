# Original MUSCLE53 in a fresh installed63 prefix

An independent real scientific command-line application now passes on installed
Ubuntu63, source `8513964d0c00d6eb5ef1a7e925795c14884a7d98`. This precedes the
Ubuntu64 installation and does not establish UGENE GUI compatibility.

The unchanged official Intel macOS MUSCLE5.3 executable is1,859,392 bytes, SHA256
`0cfd18b7f7a95b5101ba8e86b4c50fce654247fce26deb6522eb4bb03744d70e`.
Its source is the upstream release asset
`https://github.com/rcedgar/muscle/releases/download/v5.3/muscle-osx-x86.v5.3`.
Both version reporting and a normal three-sequence alignment return0 in a new
QA prefix. No thread-count argument is supplied: the real application reports
two available cores and runs two threads.

The synthetic FASTA input and actual output are exported and SHA256 checked.
All three identifiers remain present, every ungapped output sequence exactly
matches its original input and all aligned rows have width21 with actual gaps.
This confirms the bounded format/sequence result, not broad algorithm validation
or any biological or clinical conclusion. Input SHA256:
`6446a6539a2f6ccfaa12377e55fb09ac1acb3b873d9960996e6adf735c6b5408`.
Output SHA256:
`8ba71ff96a428a5db26f92776020c939c1c67c827fd1f8d123a3b7d9325fe657`.

Three original GCC11 macOS libraries and their three license texts are copied
unchanged from the previously verified official Homebrew bottle into this fresh
QA prefix at their expected paths. No binary dependency names or app bytes are
rewritten. Bottle SHA256 is
`af5d635ec43e4fc786abafe5f963ea26ac147ac10880d3ab4e2eea49948051cc`.
These are QA-only dependencies, not payloads of a distributed Karyo package.
The license is GPL-3.0-or-later WITH GCC-exception-3.1; original texts are retained.

Normal shutdown of the new prefix succeeds with status0 and no forced cleanup.
The existing saved-data and earlier MUSCLE prefix process identities are checked
before and after and remain unchanged. No older prefix is stopped or modified.

Two earlier QA-controller mistakes remain separate: a private-module import
failure, then a bootstrap attempt using absent /bin/true and a pipe held by a
persistent server. Neither executes the scientific binary. The final ordinary
bootstrap uses /bin/bash and a regular log file, then performs the real alignment.
These corrections are not runtime or scientific-application patches.

Evidence is `out/migration/muscle-macos53/ubuntu-installed63-fresh-v3.json` and
`native63-muscle-fresh-evidence-v1.json`. The latter has SHA256
`4c14f4929636e0f99886738e5636ac506d71fc71ece40533d8e06bdc2b50ac97`.
No shared/security suite, deliberate fault, app compatibility override or push
is used. Debian64 and original UGENE GUI acceptance remain separate gates.

The same original executable now passes independently on installed Ubuntu64,
source `a261c3710a1c063c0574efb7e2ad2112f1342545`, in another fresh prefix.
Both commands return0 with default two threads, the three-sequence output is
byte-identical, normal shutdown succeeds and protected prefix identities remain
unchanged. Its separate `native64-muscle-fresh-evidence-v1.json` SHA256 is
`bb726a0f425573ab6f9f192a3aa860c4e1be8ee3708ada7d79c6e43a664f4a7a`.
The63 controller failures linked there remain historical63 observations; there
is no imported64 failure or inferred Debian runtime acceptance.
