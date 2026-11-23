# Native launcher streams and focused functional package builds

The installed macOS launcher now preserves application stdout separately from
Darling diagnostics. Previously it merged the two pipes: Ubuntu's prefix setup
and EGL warnings appeared in the output of real upstream uname and echo. The
fix reads both pipes concurrently, keeps both in the launch log and retains the
bounded post-exit drain when a persistent daemon inherits either pipe. It does
not suppress renderer warnings or alter application output.

DE32a8f99 contains the stream fix and five ordinary subprocess scenarios.
DE65c36f7 exposes those scenarios as the independent macos-process-streams CTest
entry. Builder3ab3450 adds --test-regex to package/package-set, retains the full
suite default and records selected versus all scope in artifact manifests.

Both native packages use committed DE65c36f763ca224dde33366ff14ccf3e8dd92721d,
source HEAD, archive SHA256
d70777d04a92060567dfc1f9c9fc94fa369d619b831117cd22c543a4d337eb2d.
The package version remains the development version0.1.0-2 and each QA machine
uses an explicit reinstall. Debian package SHA256 is
22ffc09a667a748bad3a5cb93bdfac5038376bf63ecb0dde91bcb403f733463c;
Ubuntu is59c53588f222fdfdd1f742f1e710fa43c0dc7f00e7b339510d8f74ce03a7de81.

Only ^macos-process-streams$ runs during these builds: one CTest entry containing
five ordinary subprocess checks, on each native SDK. The manifests explicitly
record ctest_scope:selected and the expression. The shared launcher/source-input
suites and security cases do not run. These package checks are not a complete
suite or Mach-O compatibility pass.

Both packages are installed in the dedicated native QA VMs. Actual packaged
Mach-O uname, echo, defaults write and defaults read all pass with exact stdout,
including newly initialized prefixes. The Ubuntu EGL diagnostics remain visible
on stderr. Accounts, PAM, display manager configuration and all installed package
versions are preserved; dpkg audit and verification of both launcher and engine
are clean. Candidate-only runs before installation also preserve installed files
and pass first and repeated launches on both systems.

To free E: space, only our Ubuntu QA VM was relocated to C:. Nine powered-off VM
files were copied and compared by SHA256, the original source was rechecked,
and its E: path was preserved as a junction. The native session restarted;
temporary auto-login configuration was removed. Existing package/configuration
hashes and the same Mac prefix inode were preserved. A real Mac executable read
the previous53-byte persistent data file after reboot. The user VM is untouched.

Exact build/install/relocation receipts are joined in the ignored local
out/migration/macos-native-streams-evidence.json. This result concerns the new
launcher on installed35-patch engines. Full43-patch graphics engine builds and
unchanged Cocoa/Qt/TextEditor acceptance remain separate pending gates; it does
not establish general GUI compatibility or resolve glyph quality.
