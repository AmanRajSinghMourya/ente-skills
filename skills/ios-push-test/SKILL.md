---
name: ios-push-test
description: Send a real APNs push to the Photos iOS debug build on a physical iPhone through Apple's Push Notifications Console (no .p8 key) and prove the encrypted Notification Service Extension ran. Use for /ios-push-test, "test the NSE", "send a push to the phone", or any iOS notification regression run.
---

# iOS push test without a .p8

Proves server payload → APNs → OS-launched NSE → alert on a phone. Nobody on
the team shares the APNs `.p8`, so the push is sent from Apple's Push
Notifications Console with Aman's developer login. What it cannot prove: the
FCM hop (the server sends through Firebase) and the production APNs
environment (non-admins may only send to Development, which matches a debug
build's sandbox token). A simulator never launches an NSE; `simctl push` with
`mutable-content` just displays the raw alert.

Known phone: iPhone 11 Pro, UDID `00008030-000934AE2282802E`, iOS 26.5.2,
debug bundle `io.ente.frame.debug`, logged into the test account. Debug NSE
bundle `io.ente.frame.debug.NotificationServiceExtension`; release
`io.ente.frame.NotificationServiceExtension`. Team `6Z68YJY9Q2`.

## One-time setup

- Aman logs into https://icloud.developer.apple.com/dashboard/notifications in
  the Claude built-in browser (Claude never types passwords). The login
  persists in that browser.
- `brew install libimobiledevice` for `idevicesyslog` (installed 2026-10-28).
- Go 1.26+ on the Mac (`crypto/hpke` with X-Wing is in the standard library).
- The Dart MCP plugin (`dart-flutter`) for `dtd` / `vm_service`.

## 1. Run the debug app on the phone from `flutter run`

Debug builds launched from the home screen do not start Dart on iOS 14+, so
`flutter attach` finds no VM service. Start it from a Terminal tab and leave it
running:

```bash
cd <checkout>/mobile/apps/photos && flutter run -d 00008030-000934AE2282802E --debug
```

Prerequisites in a fresh worktree: `flutter pub get`, `cargo codegen frb` in
`rust/`, `flutter gen-l10n` in `mobile/packages/strings`. Reinstalling the same
bundle many times puts the phone in a state where the NSE never launches (see
Troubleshooting). Prefer hot restart over reinstall.

## 2. Read the APNs token and the HPKE public key

1. `dtd listDtdUris` → `dtd connect <uri>`.
2. `vm_service callMethod getVM` → take the main isolate id → `getIsolate` → pick
   the `libraries/@…` id of `package:photos/main.dart` (any library importing
   `firebase_messaging` and `notification_key_service.dart` works).
3. `vm_service callMethod evaluate` on that library, output lands in the
   `flutter run` terminal (read it with `read_terminal`):

```dart
FirebaseMessaging.instance.getAPNSToken().then((t) => print('PUSHCONSOLE_APNS=' + (t ?? 'null')))
```

```dart
NotificationKeyService.generateNotificationKey().then((k) { print('PKLEN=' + k.length.toString()); for (var i = 0; i < k.length; i += 200) { print('PK' + (i ~/ 200).toString().padLeft(2, '0') + '=' + k.substring(i, (i + 200) > k.length ? k.length : i + 200)); } })
```

The terminal truncates long lines, hence the 200-char chunks; join them and
check: 1624 base64 chars → 1216 bytes. The APNs token is 64 hex chars.
`generateNotificationKey` reuses the stored seed, so this is the key the server
has, if registration succeeded (`PushDiagnostics: registration.response` in the
log). The key is per install and per account; redo this after reinstall or
re-login.

## 3. Build the payloads from the real server code

```bash
~/Development/ente-skills/skills/ios-push-test/scripts/build_payloads.sh "<public key>" <out-dir>
```

`scripts/payloads/main.go` is a standalone copy of the server's
`sendAlbumShare` encryption (HPKE X-Wing, HKDF-SHA256, ChaCha20Poly1305,
info `ente-push`, plaintext `{"eventType":"album_shared"}`), with FCM's
`data` keys placed next to `aps` as FCM does. Before a run, diff it against
`server/pkg/controller/push.go` in the branch under test and update the
plaintext or headers if the server changed. A valid ciphertext is 1164 bytes
(1552 base64 chars). It writes:

| file | expected on the phone |
| --- | --- |
| `payload-valid.json` | "An album was shared with you" (NSE decrypted) |
| `payload-garbage.json` | "Ente / New activity" (NSE fallback) |
| `payload-plain.json` | "RAW-APNS / NSE did not run" (no ciphertext → passthrough, correct) |

Every payload's visible `aps.alert` is the marker `RAW-APNS / NSE did not run`.
If the phone shows it for `valid` or `garbage`, the NSE did not run. Keep
`"mutable-content": 1` and the alert; a background push plus mutable-content
never invokes an NSE.

## 4. Send from the console

Open in the built-in browser:
`https://icloud.developer.apple.com/dashboard/notifications/teams/6Z68YJY9Q2/app/io.ente.frame.debug/notifications/create`

Fields (`read_page` gives refs): name textbox, Environment combobox
(`Development`, leave it), `DEVICE` radio, `device-token` textbox, `apns-topic`
(leave empty; Apple fills the bundle id), push type `alert`, priority
`High (10)`, expiration default. `form_input` works for name and token.

The payload editor is a `react-simple-code-editor` textarea. `form_input` stores
`[object Object]`, and `type` drops characters at this length. Instead click
`JSON View`, then run `scripts/set_payload.js` through `javascript_tool` with
`__PAYLOAD__` replaced by the payload object, then `type` a space and press
`Backspace` so the editor re-validates. Confirm with `javascript_tool`:

```js
(() => { const ta = document.querySelector('textarea.npm__react-simple-code-editor__textarea'); let ok; try { ok = JSON.parse(ta.value).aps.alert.title; } catch (e) { ok = e.message; } return { ok, valid: /Payload is valid/.test(document.body.innerText) }; })()
```

Then click `Send`. The row appears under the `Send` tab with a `Resend`
button; use that for repeat runs, no re-entry needed. The sent size shown
(about 1.7 KB) is the minified JSON; a missing comma in the console's viewer is
cosmetic. `Get cURL Command` needs a `.p8`, ignore it. Ask Aman what app state
he wants (killed, background, foreground, locked) before each send; one push
per case, he dislikes notification spam on the phone.

## 5. Verify on the device log

Start the stream before sending (no sudo, survives Ctrl-C):

```bash
idevicesyslog -u 00008030-000934AE2282802E > <out-dir>/idevicesyslog.txt 2>&1 &
```

Grep after the send:

```bash
grep -E 'can be modified|Request replacement content|Received replacement content|NotificationServiceExtension' <out-dir>/idevicesyslog.txt | tail -20
```

Healthy run (killed app): SpringBoard `Remote notification request … can be
modified: 1` → `Request replacement content` → `NotificationServiceExtension`
process launches → `Received replacement content` within about 1–3 s. The
replacement content line is the proof the OS, not Flutter, produced the alert.
Then Aman reads the banner text aloud, or `read_terminal` the Flutter log when
the app is open: the main app also decrypts the same push on open
(`Received encrypted album-share push`), which is the known duplicate until
step 6 of the Notion plan.

Do not use `/usr/bin/log collect --device-udid`: it needs sudo and the archive
corrupts if interrupted (two archives lost that way on 2026-10-28).

## Troubleshooting

- `can be modified: 0` with `hasMutableContent: 1`: device-state bug after
  about five reinstalls of the same bundle. Not a build, signing, payload or
  naming problem. Fix: `xcrun devicectl device reboot --device <udid>`, wait
  for `devicectl list devices` to show it connected, resend. The
  `ENABLE_DEBUG_DYLIB=NO` xcodebuild tried on 2026-10-28 was not the fix.
- Console says delivered but nothing shows: token is from the release bundle,
  or the app was reinstalled since the token was read. Re-read step 2.
- `Payload is valid` never appears: the input event did not fire; retype the
  space/backspace with the textarea focused.
- Release app on the phone: non-admins cannot send to Production, and a release
  build has no VM service for the token. Needs an admin or the `.p8`.
- Foreground: AppDelegate's `willPresent` may suppress the encrypted remote
  alert and hand the payload to Flutter (step 5 work in PR 153's worktree);
  judge by the Flutter log, not the banner.

## Cleanup

`pkill idevicesyslog`. If a scratch xcodebuild was installed, run step 1 again
to restore the normal `flutter run` build. Record the phone's current token
and key in the session scratchpad only, never in the repo.
