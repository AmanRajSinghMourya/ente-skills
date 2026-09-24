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
4. **Login** with the test account in
   `~/.config/ente-workflow/mobile-test-account.json` (`email`, `password`).
   Aman allows it for verification. Never print or copy the password anywhere.
   If the file is missing, ask him.
5. **Locks.** Tell the simulator's device lock apart from Ente's app lock. Use
   the simulator controls, a known test PIN or simulated biometrics. The account
   password is not a PIN. If an unknown app PIN blocks you, use a separate
   throwaway simulator. Never erase Aman's simulator or reset the account.
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
