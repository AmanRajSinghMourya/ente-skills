---
name: release
description: Run an Ente app release cycle. Test main's changes on the iOS simulator and then Android before the release candidate, give Aman the release commands to run, check the RC and post the Discord testing thread, check tester feedback when asked, and after the release check the help changelog and help docs. Use for /release, /release check and /release done.
disable-model-invocation: true
---

# Release

This chat is the release's thread; keep the whole cycle in it.

**Never run release commands.** `.github/docs/app-release.md` in `ente/ente`
has the commands for starting, fixing and promoting a release (the
`app-release.yml` workflow, cherry-picks, build bumps). Read it, fill in the
app and version, and give Aman the exact commands to run himself, with
`--repo ente/ente` on every `gh` command so they work from any folder. Never
run them, trigger workflows, move tags or merge anything.

This skill covers the mobile apps Photos, Auth and Locker. For Ensu, Cast or
Photos desktop, give the commands from `app-release.md` and stop there.

**Test without stopping.** Log in with the stored test account (Codex keeps it
in memory) and never ask first. On simulators, emulators and test devices,
handle the app's own prompts yourself: permission requests (photos, camera,
notifications, files), onboarding screens, "allow" and "OK" dialogs, and
install prompts (unknown sources, Play Protect). Claude Code doesn't type
passwords or accept legal terms, so there ask Aman once, at the start.

Discord is read and written through the browser where the agent Discord account
is logged in (Codex: its browser or computer-use plugin; Claude Code: Claude in
Chrome). Show Aman a message before posting it.

## `/release`: test, then start the release

Test before the RC exists, so a failure is fixed on `main` instead of
cherry-picked.

1. **App and version.** Ask which app (Photos, Auth or Locker) and version,
   unless Aman said.
2. **Pin the commit.** `git ls-remote origin refs/heads/main` (in `ente/ente`).
   Say the hash in the chat; every result belongs to it. Make a worktree
   detached at that hash (`R-<app>-<version>`; Codex: `create_worktree`,
   Claude Code: `git fetch origin <hash> && git worktree add --detach .worktrees/R-<app>-<version> <hash>`).
3. **What's in it.** The release notes are the entries in
   `mobile/apps/<app>/changes/` at that hash. Also read
   `git log --oneline <previous final tag>..<hash> -- mobile/apps/<app> mobile/packages rust`
   (previous final tag: `git tag --sort=-creatordate | grep "^<app>-v[0-9.]*$" | head -1`)
   and note risky changes no entry mentions (shared packages, sync,
   encryption, upload, app lock).
4. **Test plan.** For each entry: how you'll test it and where: iOS
   simulator, Android emulator, or "needs a real device" (camera and scanner,
   biometrics, sharing from other apps). Post it in the chat and start
   testing; Aman can redirect.
5. **Build and test.** In the worktree, run `flutter pub get --enforce-lockfile`
   under `mobile/`, then for Photos or Locker `cargo codegen frb <app>` from
   `rust/`. Then from `mobile/apps/<app>`:
   - iOS first: `flutter run -d <simulator>`.
   - Then Android: `flutter run --flavor independent -d <emulator>`. Prefer
     an emulator (`emulator -list-avds`, then `emulator -avd <name>`). Use a
     connected phone (`adb devices`) only if Aman has said it's a test device:
     installing over an existing app keeps its data, so a phone signed in to
     his real account would test with it. If neither exists, mark Android
     "not tested" and carry on.

   Screenshot each result.
6. **Report.** A table: change, iOS result, Android result (pass, fail, or
   not testable here), with screenshots and what failed. A failure is a normal
   task, then `/openpr`; after it merges, test again from step 2.
7. **Commands to start.** When everything passes, give Aman the `start`
   command from `app-release.md`, and remind him to merge the PR it opens to
   move `main` to the next beta.
8. **Check the RC** once the build finishes: the `<app>-v<version>-rc`
   pre-release on `ente/nightly` (the Discord release channel also announces
   "<App> release candidate"). Read its commit with
   `git ls-remote origin refs/tags/<app>-v<version>-rc`. Apart from the
   version change, it must hold only the commits you tested; test any others
   now. Then smoke-test the real APK on the emulator (open, log in, one
   sync): `gh release download <app>-v<version>-rc --repo ente/nightly --pattern '*.apk' --pattern SHA256SUMS`,
   `shasum -a 256 -c SHA256SUMS --ignore-missing`, then `adb install -r <apk>`.
   If the signature differs from the installed app, uninstall it on an
   emulator; on a real phone, ask first.
9. **Discord testing thread.** In the testing channel, a new thread named
   `<App> <version> RC (build <n>)`: what's new (from the RC's changelog,
   `gh release view <app>-v<version>-rc --repo ente/nightly --json body`), and
   how to report (device, OS, app version and build, steps, screenshot or
   recording).
10. **Notion draft.** The app's "<App> Releases" item for this version: `Stage`
    to "Release candidate", with the RC link. Write it after Aman's OK.
11. Remove the RC worktree with `/cleanup`. If a tester finds a fix is needed
    later, give Aman the cherry-pick and build-bump commands from
    `app-release.md`.

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
   Draft the "<App> Releases" item's `Stage` change to "Current production
   release" (and the previous one's to historical), with the
   release link, and write it after Aman's OK.
3. **Help changelog:** promote opens a PR titled
   `Update <app> help changelog for v<version>`. Find it
   (`gh pr list --repo ente/ente --search "help changelog for v<version>" --state all`),
   check it matches the release notes, and tell Aman whether it's ready to merge.
4. **Help docs:** for each user-facing change, check `docs/docs/<app>/`
   (features, FAQ, troubleshooting). List the pages that are missing or out of
   date, with the edit you'd make. Make the edits only after Aman approves,
   as a normal task, then `/openpr`.
5. Offer a closing message for the Discord thread.
