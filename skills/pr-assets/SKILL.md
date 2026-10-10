---
name: pr-assets
description: Publish selected PR screenshots on a separate asset branch in Aman's public Ente fork and generate commit-pinned Before/After tables. Use for PR screenshots or from openpr for a visual change.
---

# PR screenshots

Use the format in [ente/ente#13540](https://github.com/ente/ente/pull/13540):
short PR bullets, then tables of relevant screenshots with 230px-wide images.
Assets stay on `pr-assets/<task-slug>` in `AmanRajSinghMourya/ente`; never merge
that branch into the product branch. Links use the asset commit SHA, so later
uploads don't change an existing PR's evidence.

1. Select screenshots already captured for this task. Compare the same device,
   app state and theme; label platform and step. Use synthetic/test data and
   inspect the selected images before publishing. Don't publish customer files,
   credentials or unrelated screenshots. No UI change means no screenshot work.
2. Write a manifest outside the repo. Paths are relative to the manifest or
   absolute; omit `before` or `after` when that view doesn't exist:

   ```json
   [{"platform":"iOS","step":"After denying access",
     "before":"ios-before.png","after":"ios-after.png"}]
   ```

3. Preview with the helper in this skill's real directory:

   ```sh
   python3 <skill-dir>/scripts/publish.py --repo AmanRajSinghMourya/ente \
     --slug <task-slug> --manifest <file>
   ```

   It prints the exact files, branch and draft table without network calls or
   Git changes. `/openpr` authorizes publishing selected screenshots for that
   PR. Outside it, publish only when Aman asked to upload them; a preview alone
   needs no approval. Add `--publish` to upload through the authenticated `gh`
   CLI. The helper checks the account and public fork's write permission, makes
   a root commit for a new asset branch, and only fast-forwards existing ones.
   It does not change the local checkout, index, product branch or PR.
   If publication fails, inspect that branch before retrying. A printed asset
   commit receipt proves the commit exists, not that the branch update succeeded;
   compare its SHA with `gh api repos/<repo>/git/ref/heads/<branch>`. If they match,
   reuse that commit and check its URLs instead of uploading again.
4. Read the returned account, repository, branch and commit. Check each raw URL
   is publicly reachable as an image before using its table. If it isn't ready,
   retry the reads once and report the remaining gap; don't repeat the upload.
   Add the published result's `markdown` after the PR bullets, with one brief line of
   device/build/state context. Missing comparisons stay blank; don't fabricate
   a before image or recapture unchanged screens just for the table.
5. Pass the finished body file to `gh pr create --body-file <file>`, or
   `gh pr edit --body-file <file>` when editing was requested. Keep asset
   branches after cleanup so PR images remain available.
