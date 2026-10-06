---
name: release
description: Run the test cycle of an Ente app release. Post a Discord testing thread for a release candidate with what to test, check tester feedback when Aman asks, and after the release make sure the help changelog PR and help docs are updated. Use for /release, /release check and /release done.
disable-model-invocation: true
---

# Release

This chat is the release's thread; keep the whole cycle in it. Aman runs the
`app-release.yml` workflow himself (`start`, then `promote`). This skill never
triggers workflows, moves tags or merges anything.

Discord is read and written through the browser where the agent Discord account
is logged in (Codex: its browser or computer-use plugin; Claude Code: Claude in
Chrome). Show Aman every message before posting and post only after his OK.

## `/release`: start testing a release candidate

1. **Ask which app** (Photos, Auth, Locker, …) and the release candidate
   version, unless Aman already said. Confirm the tag exists:
   `git ls-remote --tags origin "<app>-v<version>-rc"`. Find the previous
   final release tag (`git tag --sort=-creatordate | grep "^<app>-v[0-9.]*$" | head -1`).
2. **What changed:** the `changes/` entries added since the previous release,
   `git diff --name-only --diff-filter=A <previous tag> <rc tag> -- mobile/apps/<app>/changes/`,
   and read each one at the RC tag. For context, also read
   `git log --oneline <previous tag>..<rc tag> -- mobile/apps/<app> mobile/packages`.
   Note risky changes that have no changes entry (shared packages, sync,
   encryption, upload, app lock).
3. **Tester brief**, plain and short. For each change: where it is in the app,
   the steps, the expected result, and the edge cases worth trying (Android
   and iOS, offline, large files, light and dark). Then a short "also check"
   list for the risky areas, and how to report: device, OS, app version and
   build, steps, and a screenshot or recording.
4. **Post to Discord:** in the testing channel, a new thread named
   `<App> <version> RC (build <n>)` whose first message is the brief. Show
   Aman the thread name and text, post after his OK, and give him the link.

## `/release check`: read tester feedback

1. Read the release's Discord thread since the last check (the chat shows when
   that was).
2. Classify each report: **critical** (crash, data loss, broken sync, upload,
   encryption, login or app lock, or anything that blocks the release),
   **real but minor**, **needs info**, or **false positive** (expected
   behavior, not in this build, already fixed, a device or network issue).
   Check each against the code at the RC tag, the `changes/` entries and
   Sentry if connected. Reproduce only when it's cheap.
3. **Report only.** A table of report, verdict, evidence and suggested next
   step. Offer `/todo` for real bugs, and draft a reply to the tester when it
   helps (post only after Aman's OK). Never start a fix unless Aman asks.

## `/release done`: after Aman promotes the release

1. Confirm the release exists: `gh release view <app>-v<version> --repo ente/ente`.
2. **Help changelog:** the promote step opens a PR titled
   `Update <app> help changelog for v<version>`. Find it
   (`gh pr list --repo ente/ente --search "help changelog for v<version>" --state all`),
   check it matches the release notes, and tell Aman whether it's ready to merge.
3. **Help docs:** for each user-facing change, check `docs/docs/<app>/`
   (features, FAQ, troubleshooting). List the pages that are missing or out of
   date, with the edit you'd make. Make the edits only after Aman approves,
   as a normal task (`/pickup-task`, then `/openpr`).
4. Offer a closing message for the Discord thread; post after his OK.
