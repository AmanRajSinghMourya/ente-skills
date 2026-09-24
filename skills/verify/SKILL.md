---
name: verify
description: Prove an Ente change works on the real app or server. Drive the mobile app on a simulator with before and after screenshots, or run the server locally. Use for UI or runtime changes during a task, or /verify.
---

# Verify on the real thing

These are the Ente-specific facts. The driving itself is built in: Claude Code's
`run` skill looks for a project skill like this one, and Codex uses its
`computer-use` and `browser` plugins.

Skip this if Aman said he'll test it himself. Only one agent drives a simulator
at a time; if another chat is using it, wait or ask.

## Mobile

1. **Before and after.** Run the unchanged build (the main checkout or the base
   commit) through the user journey and take screenshots. Then run the same
   journey on the task worktree. If you can't capture the before state, say so.
2. **Run** from the app folder: iOS `flutter run -d <simulator>`, Android
   `flutter run --flavor independent -d <device>`, Auth on macOS
   `flutter run -d macos`. Flutter may need permission to use its SDK cache
   outside the workspace.
3. **Drive** it with the simulator control tool, Maestro or computer use. Prefer
   accessibility labels to coordinates.
4. **No logging in.** Never type a password or one-time code. Aman keeps a
   simulator named `Ente Test` that's already logged in to the test account in
   Photos and Locker, with no Ente app lock. Work on a copy of it, never on
   `Ente Test` itself:
   ```sh
   xcrun simctl shutdown "Ente Test" 2>/dev/null
   xcrun simctl clone "Ente Test" "Ente Test <task>"
   xcrun simctl boot "Ente Test <task>"
   ```
   Run both builds on the copy. The apps keep their IDs (`io.ente.frame`,
   `io.ente.locker`), so installing over them keeps the login. Delete the copy
   when you're done: `xcrun simctl delete "Ente Test <task>"`. If `Ente Test` is
   missing or logged out, tell Aman once (setup is in the README) and carry on
   with anything that doesn't need a logged-in app. On Android, do the same with
   the emulator snapshot `ente-test`:
   `emulator -avd <avd> -snapshot ente-test -no-snapshot-save`.
5. **Locks.** Tell the simulator's device lock apart from Ente's app lock. Use
   the simulator controls or simulated biometrics. If a lock the task didn't
   cause blocks you, delete the copy and clone a fresh one. Never erase or reset
   `Ente Test`.
6. Screenshots show layout, not persistence, permissions or races. Check those
   another way: reopen the app, use a second device, or read logs.
7. **Report** the journey, device and OS, before and after, and anything odd you
   saw on the way. Offer `/todo` for problems unrelated to the task.

## Server

1. **Logic:** Go tests from `server/` with `./scripts/test-with-postgres.sh
   host`. If that fails on Postgres auth, use a throwaway test database over the
   socket:
   `TESTDB="ente_test_$(date +%s)"; createdb "$TESTDB" && { ENV=test PGHOST=/tmp PGDATABASE="$TESTDB" go test -p 1 -count=1 ./...; rc=$?; dropdb "$TESTDB"; echo "go test exit $rc"; }`.
   The result is the `go test` exit code it prints, not the exit code of the
   whole line.
2. **Behavior:** run `go run cmd/museum/main.go` from `server/` (port 8080),
   then `curl` the endpoint and check the rows with `psql`. A crashed museum can
   leave a stale process on port 8080: `lsof -nP -iTCP:8080 -sTCP:LISTEN`.
3. Museum only checks the length of encrypted fields, so dummy base64 of the
   right size works for API tests.
