---
name: release
description: Run an Ente app release cycle. Give Aman the release commands to run, post the Discord testing thread when the release candidate exists, test its changelog on the iOS simulator and then Android, check tester feedback when asked, and after the release check the help changelog and help docs. Use for /release, /release check and /release done.
disable-model-invocation: true
---

# Release

This chat is the release's thread; keep the whole cycle in it.

**Never run release commands.** `.github/docs/app-release.md` in `ente/ente`
has the commands for starting, fixing and promoting a release (the
`app-release.yml` workflow, cherry-picks, build bumps). Read it, fill in the
app and version, and give Aman the exact commands to run himself. Never run
them, trigger workflows, move tags or merge anything.

**Test without stopping.** Log in with the stored test account (Codex keeps it
in memory) and never ask first. On simulators, emulators and test devices,
handle the app's own prompts yourself: permission requests (photos, camera,
notifications, files), onboarding screens, "allow" and "OK" dialogs, and
install prompts (unknown sources, Play Protect). Claude Code doesn't type
passwords or accept legal terms, so there ask Aman once, at the start.

Discord is read and written through the browser where the agent Discord account
is logged in (Codex: its browser or computer-use plugin; Claude Code: Claude in
Chrome). Show Aman a message before posting it.

## `/release`: start a release and test the RC

1. **Commands to start.** Ask which app and version, unless Aman said. From
   `app-release.md`, give him the `start` command (and remind him to merge the
   PR it opens to move `main` to the next beta).
2. **Find the RC** once his build finishes: the `<app>-v<version>-rc`
   pre-release on `ente/nightly` (the Discord release channel also announces
   "<App> release candidate"):
   `gh release view <app>-v<version>-rc --repo ente/nightly --json name,body,assets`.
   Its body is the changelog; its assets hold the Android APK and `SHA256SUMS`.
3. **Discord testing thread, right away.** In the testing channel, a new thread
   named `<App> <version> RC (build <n>)`. First message: what's new (from the
   changelog), risky areas, what testers should focus on, and how to report
   (device, OS, app version and build, steps, screenshot or recording). Post
   it now; don't wait for your own testing.
4. **Context.** In `ente/ente`, read
   `git log --oneline <previous final tag>..<app>-v<version>-rc -- mobile/apps/<app> mobile/packages`
   (previous final tag: `git tag --sort=-creatordate | grep "^<app>-v[0-9.]*$" | head -1`).
   Note risky changes the changelog doesn't mention (shared packages, sync,
   encryption, upload, app lock).
5. **Test plan.** For each changelog line: how you'll test it and where: iOS
   simulator, Android, or "needs a real device" (camera and scanner,
   biometrics, sharing from other apps). Post it in the chat and start
   testing; Aman can redirect.
6. **iOS simulator first.** Simulators can't run the TestFlight build, so
   build the same tag from source in a worktree detached at the RC tag
   (`R-<app>-<version>`; Codex: `create_worktree`, Claude Code:
   `git worktree add --detach .worktrees/R-<app>-<version> <app>-v<version>-rc`),
   then `flutter run -d <simulator>` from `mobile/apps/<app>`. Drive each test
   (Claude Code: the iOS simulator tool or Maestro; Codex: computer use),
   with a screenshot per result.
7. **Then Android.** `adb devices`: use a connected device if there is one,
   otherwise boot an emulator (`emulator -list-avds`, then
   `emulator -avd <name>`). If neither exists, mark Android "not tested" and
   carry on. Install the RC's real APK:
   `gh release download <app>-v<version>-rc --repo ente/nightly --pattern '*.apk' --pattern SHA256SUMS`,
   `shasum -a 256 -c SHA256SUMS --ignore-missing`, then `adb install -r <apk>`.
   If the signature differs from the installed app, uninstall it on an
   emulator; on a real phone, ask first. Run the same tests, with screenshots.
8. **Report.** A table: change, iOS result, Android result (pass, fail, or
   not testable here), with screenshots and what failed. If a fix is needed,
   give Aman the cherry-pick and build-bump commands from `app-release.md`.
   Remove the RC worktree with `/cleanup`.

## `/release check`: read tester feedback

1. Read the release's Discord thread since the last check.
2. Classify each report: **critical** (crash, data loss, broken sync, upload,
   encryption, login or app lock, or anything that blocks the release),
   **real but minor**, **needs info**, or **false positive** (expected
   behavior, not in this build, already fixed, a device or network issue).
   Check each against the code at the RC tag and Sentry if connected, and
   reproduce on a simulator when it's cheap.
3. **Report only.** A table of report, verdict, evidence and suggested next
   step. Draft replies to testers when they help. Never start a fix unless
   Aman asks.

## `/release done`: promote and wrap up

1. **Before promoting:** remind Aman to edit the `<app>-v<version>-rc` draft
   release notes in `ente/ente` into the final user-facing changelog, then
   give him the `promote` command from `app-release.md`.
2. After he runs it, confirm the release:
   `gh release view <app>-v<version> --repo ente/ente`.
3. **Help changelog:** promote opens a PR titled
   `Update <app> help changelog for v<version>`. Find it
   (`gh pr list --repo ente/ente --search "help changelog for v<version>" --state all`),
   check it matches the release notes, and tell Aman whether it's ready to merge.
4. **Help docs:** for each user-facing change, check `docs/docs/<app>/`
   (features, FAQ, troubleshooting). List the pages that are missing or out of
   date, with the edit you'd make. Make the edits only after Aman approves,
   as a normal task (`/pickup-task`, then `/openpr`).
5. Offer a closing message for the Discord thread.
