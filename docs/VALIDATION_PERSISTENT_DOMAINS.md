# Persistent Foundation domains and ordinary upstream applications

Both installed32 engines execute real Mach-O CLI code and preserve application
data across an actual engine update/restart in the same prefix. Both Cocoa GUI
checks remain failed. Ubuntu's independent Qt case also fails, with a distinct
unrecognized `-[QNSWindow setRestorable:]` selector. The native longjmp repair
alone cannot establish Qt compatibility; the general NSWindow API still needs
that follow-up.

## Actual persistent-domain defect

On Debian32, the packaged OPENSTEP defaults utility uses its documented plain
write syntax, returns0, then the next read returns2 with no saved value. Its
NSUserDefaults setPersistentDomain implementation clears a suite but uses
registerDefaults for the replacement values. Those are transient registration
defaults. DEd4ae809 adds patch0034: use the suite setter for each supplied value
before the existing synchronization. Other domain methods, lifecycle and
compiler options remain unchanged. No application-specific configuration exists.

The exact proposed method body was compiled as an isolated Mac subclass, leaving
the installed framework unchanged. Separate real Mach-O processes successfully
write/read the UTF-8 preference on both kernels: Debian with32 patches and Ubuntu
with31 at the time of this prototype. This is actual Mac method/body evidence,
not an installed Foundation or whole34 acceptance claim. Archive SHA256:
05dc23df71e02f6e5ea64057fae3845f4b87de133c385a4b1f6b1d52a78e35c3.
Binary SHA256: de42b56980462672af158cba449ebc91da7a98cb9fa3c6351422b964cce225f8.

The Ubuntu32 utility checker initially stops on engine-setup or native DRI3
diagnostics mixed with expected stdout. Those logs are preserved; they do not
establish a failed program computation or a clean stdout contract. The actual
stock defaults round-trip after the framework update still needs acceptance.

## Unchanged upstream TextEditor

The pinned Cocotron TextEditor example is compiled with the existing immutable
Mac SDK, unchanged main/document sources and nib resources. Only the two normal
CMake bundle-name placeholders are resolved. Original sources and LICENSE are
included in the QA bundle. The first producer rejected tar's root directory;
the corrected v2 accepts that directory and validates the genuine executable.

Source revision: c8d38d16a9f613d300157bebbab2b9501bc0c274.
Bundle archive SHA256: f5ea815eb3f24a25ccb55430942003add268941da7ad9d9313dfd5eec38735e0.
TextEditor executable9992B SHA256:
3b117e7521357e1c395c6efaa091d7b06098a4213e6c94346a37c58abb12b804.

Ordinary dedicated-profile launches on both32 kernels reproduce the same native
longjmp termination and capture no working window. A zero launcher status is
not graphical acceptance. The process exits itself; no user application is
closed. These runs show the shared failure on an upstream application as well
as the purpose-built Cocoa probe.

## New inputs and remaining native gates

Source-only preparation v11 passes on both SDKs:44 fixed Swift inputs,34 Git and
zero-fuzz quilt forward/reverse patches,76 pristine files restored, and explicitly
unit_tests_executed:false. The source bundle recorded in
`darling-persistent-domain-inputs.json` uses clean DEd4ae809. The Debian34 full
engine is running; it combines the independently checked stack-return and
persistent-domain corrections. The queued Ubuntu34 full build is deliberately
replaced by the next shared NSWindow API follow-up, avoiding another known
Qt-incomplete build. There is no completed33 or34 native GUI acceptance yet.

`out/migration/darling-persistent-domain-evidence.json` retains both native/data
and prototype-method receipts, upstream app failures, exact Qt selector and
source34 preparation. The Debian QA VM was relocated from E to C while off:
all20 files were checked before removing the old copy, and a junction preserves
its original path. UUID is retained. Its native session and same Mac file work
after boot; temporary autologin is removed and protected guest hashes match.
This frees about19GB on E for continued QA. User VMs are outside this operation.

Only ordinary functional/source checks run, without the shared unit/security
suites or denied-operation scenarios. All commits remain local. Full actual
Cocoa, Qt and upstream editor windows on both current installed engines remain
required; source/compile/prototype success does not substitute for them.
