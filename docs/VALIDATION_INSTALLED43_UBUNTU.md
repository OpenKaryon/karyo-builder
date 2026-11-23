# Installed43 engine: Ubuntu applications and document editing

The complete43-patch Darling engine builds successfully on Ubuntu26.04 and is
installed in the dedicated QA VM. Runtime package SHA256 is
2db5e47d3633f3c0b5517e9e70698fa10aa4c7f3e880b237a5579c4682aaf366,
92674430bytes. Protected session/account/display-manager configuration and
existing package versions remain unchanged. The exact runtime patch provenance
is verified separately from its unchanged development package version.

The original clean-source Mach-O loader, Cocoa bundle and Qt5.15.19 bundle all
pass on the installed libraries, without executable prototype categories or
replacement functions. Real Cocoa and Qt frames were exported and viewed.
Both actual window titles now contain their intended UTF-8 Cyrillic text.
The original Qt application saves its nonempty widget PNG; its SHA256 is
a043c436661c41667bf846c902634e4fe52841306c83a161ca8f87ad207b4325.
The actual Qt raster still has visible glyph/spacing defects, so this is not
a visual-quality or arbitrary-application compatibility pass.

The unchanged upstream Cocotron TextEditor opens an ordinary ASCII fixture via
the standard NSOpen option. The actual named document window and file text were
viewed. A separate run uses xdotool to send ordinary X11 mouse/keyboard events
to this QA application: select all, type replacement text, Save and Quit.
The file contains exactly45bytes of the intended replacement text and the
application exits normally with status0. The post-save frame was also viewed.
The final quit helper itself reports status1; that diagnostic is retained,
alongside the independently observed application exit0 and exact saved data.
This demonstrates synthetic ordinary-session input, not a physical-keyboard or
general menu-navigation acceptance result. No TextEditor source was changed.

All four packaged upstream utilities also pass: uname, UTF-8 echo, defaults
write and defaults read. Diagnostics remain on stderr with the installed stream
fix. These are ordinary functional checks; no shared or security suites run.

An independent remaining delay is now reproducible on both installed35 bases:
Foundation timers complete a250ms interval in roughly253ms, while a Cocoa
50ms event wait sometimes takes29-30seconds. Instrumented Ubuntu tracing places
the delay inside NSRunLoop runMode, not X11 processPendingEvents. A plain
CoreFoundation50ms wait without a window takes about52ms on both bases.
After creating a window, a direct CF wait also takes29.6seconds on Debian;
Foundation and CF default-mode names are identical. These are diagnostics,
not a fixed timeout contract. No speculative runtime patch was added for them.

The full Debian43 build has started after verified Ubuntu artifacts. Its normal
applications, utilities, unchanged editor and keyboard/save check remain queued.
Do not label both installed43 systems accepted yet. The normal Mac actor stays
untracked until both required native GUI gates are reviewed. Full graphical
compatibility, Qt glyph quality, event deadlines, multioutput and broad DE
migration remain open. Exact receipts and reviewed file hashes are joined in
out/migration/darling-native43-ubuntu-evidence.json.
