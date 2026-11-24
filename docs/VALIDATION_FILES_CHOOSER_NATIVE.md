# Actual Files chooser and native desktop coexistence

The visible Files Open with menu is exercised on both separate Debian 13 and
Ubuntu 26.04 joined QA systems. This follows the removal acceptance recorded
in VALIDATION_STANDALONE_SESSION_REMOVAL.md; the later running-state information
here supersedes that document's historical final-state paragraph.

## Reinstall and normal login

Only the same 22 newly installed QA base packages are restored from their
recorded, SHA256-verified native artifacts. The seven scoped-association package
updates and the actual standalone Builder session package retain their own
provenance. APT simulation and installation introduce exactly those 22 packages;
all other package versions, foreign configuration, data and the running Xfce
process are preserved. Ordinary logout, selection of Karyo in LightDM and the
correct fixture password start the real Karyo session on each base.

## Real menus and actual selected applications

Files opens a new window on an ordinary directory containing a plain text
fixture and a ZIP with one text member. Selecting the text file shows Text
Editor in Details. Clicking the actual Open with button displays Text Editor,
Mousepad and Vim. Selecting Text Editor opens the exact fixture with its text
visible in Karyo Editor. Reopening the menu and choosing Mousepad opens that
same document in the distribution's installed Mousepad. No MIME preference is
changed by these one-off selections.

Selecting the ZIP changes Details to Archive Manager. Its actual Open with
menu offers Archive Manager; choosing it opens Karyo Archive with the expected
note.txt member and its 40-byte size visible. All five menu/application frames
per base are captured, hashed and viewed. Independent ordinary process
observations confirm /usr/bin/karyo-editor, /usr/bin/mousepad and
/usr/bin/karyo-archive with the exact selected fixture path in their arguments.
Both original fixture hashes remain unchanged.

The native DesktopEntry client still returns all six Karyo-scoped defaults
and matching declared candidates. A genuinely activated user D-Bus fixture
receives the same API results and real Karyo environment. This complements,
rather than substitutes for, the visible menu and application observations.

## Normal return and boundaries

After normal compositor exit and a correct-password LightDM login to Xfce,
a new Xfce process runs on each system. The direct and genuinely activated
API clients resolve folders to Thunar and inherit Xfce's original directories,
without Karyo's association/configuration scopes or Qt platform/style overrides.
No compositor is left running. Accounts, PAM/display-manager configuration,
fixture data and the pre-existing MIME preference file remain unchanged;
dpkg audit is clean. Final Xfce frames are captured, hashed and viewed.

The joined QA systems now run Xfce with the 22 Karyo packages installed again.
Root receipts remain under /var/lib/karyo-qa/chooser449 and the complete local
hashed index is out/migration/chooser449-both-evidence-v1.json. The older
Darling QA pair is separate and unaffected.

This accepts the tested text/ZIP menu choices and ordinary session roundtrip,
not every MIME type or installed application, persistence/default-changing UI,
concurrent same-user sessions, profiles, full privilege prompts, VMware channels
or the complete DE migration. An attempted Shift+F10 gesture did not open a
menu in this run; the accepted scenario uses the visible Details button.
No security/shared unit suite ran, no authentication policy changed, and
no user VM, Acer, Forge or distro was modified. Nothing was pushed.
