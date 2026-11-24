# Installed prefix restart and original-app diagnostics on Ubuntu

The complete62 engine was built from immutable DE revision
`85ac99e2206d76318b76a2e82092ef297df40aad` and installed only on the separate
Ubuntu26.04 QA machine. All four artifacts were verified by size and SHA256.
The runtime DEB is92715194 bytes, SHA256
`f4d47de95cace0f533c65eb428c225a570dd18e8b1ad17122938d12ea8ee4875`.
The corresponding Debian62 full build is separate and still running.

## Installed acceptance

All five sequential targeted stages pass: ordinary Cocoa/static Qt, public
hosted buffers, nested painter order, early backing-view presentation and
ordinary prefix restart. The actual red/cyan and blue/blue/yellow frames were
exported, hashed and viewed; the backing-view getter/callback contracts remain
correct. This is bounded rendering acceptance, not all application behavior.

The restart scenario launches a normal echo through karyo-macos, writes a
marker, invokes Darling's normal shutdown API and launches echo again in the
same prefix. The first server really remains in state Z. The second launch
creates a different live server, preserves the prefix inode and retains the
marker exactly. Normal cleanup succeeds. The protected persistent-data and
MUSCLE prefix/server identities are unchanged. No stale PID file was repaired
manually and no crash was intentionally generated. This accepts patch0062's
installed restart contract on Ubuntu; it does not infer the Debian result.

Unchanged upstream TextEditor opens its document with visible text. Its first
keyboard check stops at xdotool mousemove --sync, before typing. That failed
observation remains intact. A separate v2 check uses bounded pointer-coordinate
observation, then the same ordinary click/keyboard input. It saves exactly
45 bytes and the application exits normally with status0. The quit helper
reports BadWindow after the app has already disappeared; that diagnostic is
retained rather than treated as an application failure. Saved SHA256 is
`05786532df55212187f436d1163809d540c98cd0ad30ea1881bfbcbd831bca74`.

The unchanged dynamic Qt client reuses its exact60 binary, original UGENE
Qt5.15.10 frameworks and existing prefix. Its text is visible, its event loop
returns0 and the prefix inode is preserved. The prior recorded server is
absent, so this particular retry does not prove the zombie branch. The separate
ordinary restart above does. Existing NSAppleEventManager/setMask stub-signature
warnings remain limits. Twelve rendering/editor frames were viewed in total.

## Original UGENE and the observed signal path

All12185 regular members of the original Intel UGENE53.1 distribution are
verified unchanged before each launch; its archive is not copied again. The
ordinary application has no accepted GUI and naturally exits with134. With
patch0061 installed, Darling correctly reports child termination by signal6.
This supersedes the earlier misleading launcher0; it is not app compatibility.

A bounded GDB attachment observes the unchanged ordinary launch without
changing the app, its arguments or the ptrace policy. Matching installed
dbgsym Build ID `663511d6bc5f9b9db382988082a543aca17d7062` resolves the observed
mldr return address to __darling_thread_rpc_socket, threads.c:397. The two
preceding Mach-O frames resolve to dserver_rpc_interrupt_enter and
handler_linux_to_bsd_wrapper. The __TEXT vmaddr/fileoff zero mapping is checked
before interpreting those addresses as symbol offsets.

A subsequent breakpoint in that real wrapper records Linux signal17,
SIGCHLD, with code1/CLD_EXITED. Saved interrupted-register/frame-pointer data
maps to Linux libc condition-wait and libvulkan_lvp.so worker frames. The
Darling callback therefore reaches a native Linux worker without a registered
Darling per-thread RPC socket; this explains the immediate abort path. The
GDB warning about PID-namespace thread enumeration is retained. Actual mapped
addresses and saved context, rather than thread names alone, support this
finding. It does not exclude further application limitations after correction.

The initial breakpoint-address attempt used a mapping from before a loader
exec and failed to insert its breakpoint. A second diagnostic collided with
an already-existing QA log filename and stopped. Both failed records remain;
the accepted context observation uses a unique materialized controller, checks
that ugeneui is mapped and resolves its breakpoint after the actual GDB stop.
No signal/thread correction is implemented or accepted yet. Simply suppressing
abort or adding a UGENE-specific setting is not the intended remedy.

Only GDB and its four ordinary dependencies were added to the QA machine.
Existing package versions, accounts, PAM/LightDM configuration and ptrace
policy were checked unchanged. No security/shared unit suite ran.

## Local evidence and remaining scope

The index `out/migration/native62-ubuntu-accepted-slice-evidence-v1.json` has
SHA256 `f49c23f89c6a219ef673c1a22d80435ea992b28cfdbceaf9bdb6596fe167da42`.
It includes all artifact hashes, twelve reviewed frames, restart checks,
saved data, original-app hashes, exact symbolization and retained QA failures.

Two folders containing only public downloaded QA base images were relocated
from Builder out on E to the QA workspace on C. Eight files were independently
hashed before/after copying and through the replacement directory junctions;
all original paths and bytes remain. This gained1296437248 bytes on E.
Running VMware disks, repositories and other agents' output were not moved.

The Debian62 engine/install and old failed Qt-prefix recovery remain separate
gates. Original UGENE GUI, other migration items and hardware behavior remain
open. No user VM, Acer, Forge, donor or distro was changed. Nothing was pushed.
