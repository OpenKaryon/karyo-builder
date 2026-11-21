# Native protected-startup compositor acceptance

DE integration source: 5abf930 (plus the immutable recipe patch hashes below).
Only disposable native containers are used for this gate.
Installed PAM/session-entry acceptance is recorded separately after its wave finishes.

## Artifacts

### Debian

- Native output: out/compositor/debian/startup-final-packages/karyo-source-package-20261121T104047Z-a36ab96a.
- Native version: 0.8.3-1+karyo2.
- labwc DEB SHA256: e28aa21e27bc188a574655839122b46ca9add0deaff2e2a382af545fdd1dd7e2.
- Startup patch SHA256: 33aa92d755a9a98087379cac1fc3320a2d121960e3b2b5f36c60141ece0a4964.
- Immutable image: sha256:7cc96448ba880bf63c7c670905a09400451d7bdc190554dcc791bbca604318c5.

### Ubuntu

- Native output: out/compositor/ubuntu/startup-final-packages/karyo-source-package-20261121T104044Z-817950a7.
- Native version: 0.9.3-1+karyo2.
- labwc DEB SHA256: 8b8a5cfdd44ff63871ebf5b97b9f43457567a8e280535c65c30c46410ddc1764.
- Startup patch SHA256: 1e09cea422b1e487a7bf4dbb7f72cabe2ec426bb10f98bf13b01f83c33169dbc.
- Immutable image: sha256:2b6171bfacf5f8d34424c582232e0fffc15c5fafd2b0d732955e29af57cc1c09.

## Actual protocol checks

Both packages build from their checksum-locked native DSC, keeping wlroots ABI,
hardening and upstream license/test rules. The startup flag uses the existing
abandoned-lock state before server_start; Ubuntu explicitly includes the manager
definition because its labwc.h only declares that type. Unflagged startup is
unchanged. The first Ubuntu attempt exposed that header difference and failed
compilation; the final package outputs above include the corrected explicit header.

The actual packaged compositors run as UID 65534 with no network or capabilities,
read-only root and disposable tmpfs. Normal acceptance passes; startup acceptance
adds these actual client operations before repeating the normal protocol suite:

1. Connect before any locker and map an ordinary toplevel; snapshot data stays
   unavailable, as it does throughout the startup lock.
2. A first ext-session-lock client adopts the state and receives locked.
3. Disconnect that client without unlock; the session remains private.
4. A replacement client adopts it and explicitly unlocks; only then does the
   mapped normal window appear in snapshots.
5. Repeat stacking, minimize, sandbox-global filtering and normal lock/unlock.

Evidence: DE out/compositor/{debian,ubuntu}/startup-acceptance-{normal,startup}.
Each directory has compositor.log, probe.log, protocol-probe and acceptance.json.
The physical-input and pixel-output checks are not established by snapshot
privacy alone. Installed initial PAM and VT switching remain separate gates.
