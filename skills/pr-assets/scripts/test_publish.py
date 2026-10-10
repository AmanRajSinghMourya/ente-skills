import base64
import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import publish


PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jS1sAAAAASUVORK5CYII=")
REPO = "AmanRajSinghMourya/ente"
BRANCH = "pr-assets/test-flow"
SHA = "a" * 40


class AssetTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.image = self.root / "screen.png"
        self.image.write_bytes(PNG)
        self.manifest = self.root / "manifest.json"
        self.manifest.write_text(json.dumps([
            {"platform": "iOS", "step": "Denied | access", "before": "screen.png",
             "after": "screen.png"},
            {"platform": "Android", "step": "Resume", "after": "screen.png"}]))

    def test_preview_does_not_call_github_or_change_files(self):
        original = self.manifest.read_bytes()
        output = io.StringIO()
        with patch.object(publish, "gh", side_effect=AssertionError("network in preview")), \
             patch("sys.argv", ["publish.py", "--repo", REPO, "--slug", "test-flow",
                                "--manifest", str(self.manifest)]), \
             contextlib.redirect_stdout(output):
            self.assertEqual(publish.main(), 0)
        preview = json.loads(output.getvalue())
        self.assertTrue(preview["preview"])
        self.assertNotIn("markdown", preview)
        self.assertIn("COMMIT_SHA", preview["preview_markdown"])
        self.assertEqual(preview["files"], [str(self.image.resolve())])
        self.assertEqual(self.manifest.read_bytes(), original)
        self.assertEqual(self.image.read_bytes(), PNG)

    def fake_github(self, previous=None, private=False, conflict=False):
        calls = []

        def api(method, endpoint, data=None):
            calls.append((method, endpoint, data))
            if endpoint == "user":
                return {"login": "aman-pilot"}
            if endpoint == f"repos/{REPO}":
                return {"full_name": REPO, "private": private, "fork": True,
                        "permissions": {"push": True}}
            if "/matching-refs/" in endpoint:
                return [{"ref": f"refs/heads/{BRANCH}", "object": {"sha": previous}}] if previous else []
            if endpoint.endswith("/git/blobs"):
                self.assertEqual(base64.b64decode(data["content"]), PNG)
                return {"sha": "blob"}
            if endpoint.endswith("/git/trees"):
                self.assertEqual(len(data["tree"]), 1)
                self.assertTrue(data["tree"][0]["path"].startswith("test-flow/"))
                return {"sha": "tree"}
            if endpoint.endswith("/git/commits"):
                return {"sha": SHA}
            if method == "PATCH" and conflict:
                raise ValueError("update is not a fast-forward")
            return {"object": {"sha": SHA}}

        return api, calls

    def test_new_branch_is_root_assets_commit_with_immutable_urls(self):
        rows, assets = publish.read_manifest(self.manifest, "test-flow")
        api, calls = self.fake_github()
        with patch.object(publish, "gh", api):
            result = publish.publish(REPO, BRANCH, assets)
        commit = next(data for _, endpoint, data in calls if endpoint.endswith("/git/commits"))
        self.assertEqual(commit["parents"], [])
        markdown = publish.render(rows, REPO, result["commit"])
        self.assertIn(f"/{SHA}/test-flow/", markdown)
        self.assertNotIn(BRANCH, markdown)
        self.assertIn("Denied \\| access", markdown)
        self.assertIn("| Resume | — |", markdown)

    def test_update_preserves_old_commit_without_force(self):
        _, assets = publish.read_manifest(self.manifest, "test-flow")
        api, calls = self.fake_github(previous="old-commit")
        with patch.object(publish, "gh", api):
            publish.publish(REPO, BRANCH, assets)
        commit = next(data for _, endpoint, data in calls if endpoint.endswith("/git/commits"))
        self.assertEqual(commit["parents"], ["old-commit"])
        update = next(data for method, _, data in calls if method == "PATCH")
        self.assertEqual(update, {"sha": SHA, "force": False})

    def test_concurrent_update_is_reported_without_retry(self):
        _, assets = publish.read_manifest(self.manifest, "test-flow")
        api, calls = self.fake_github(previous="old-commit", conflict=True)
        with patch.object(publish, "gh", api), self.assertRaisesRegex(ValueError, "fast-forward"):
            publish.publish(REPO, BRANCH, assets)
        self.assertEqual(sum(method == "PATCH" for method, _, _ in calls), 1)

    def test_private_repo_rejected_before_upload(self):
        _, assets = publish.read_manifest(self.manifest, "test-flow")
        api, calls = self.fake_github(private=True)
        with patch.object(publish, "gh", api), self.assertRaisesRegex(ValueError, "public fork"):
            publish.publish(REPO, BRANCH, assets)
        self.assertTrue(all(method == "GET" for method, _, _ in calls))

    def test_publish_main_returns_ready_markdown(self):
        api, _ = self.fake_github()
        output = io.StringIO()
        with patch.object(publish, "gh", api), \
             patch("sys.argv", ["publish.py", "--repo", REPO, "--slug", "test-flow",
                                "--manifest", str(self.manifest), "--publish"]), \
             contextlib.redirect_stdout(output):
            self.assertEqual(publish.main(), 0)
        result = json.loads(output.getvalue())
        self.assertFalse(result["preview"])
        self.assertEqual(result["account"], "aman-pilot")
        self.assertNotIn("COMMIT_SHA", result["markdown"])

    def test_uncertain_ref_write_keeps_commit_receipt(self):
        api, calls = self.fake_github()

        def timeout_api(method, endpoint, data=None):
            if method == "POST" and endpoint.endswith("/git/refs"):
                raise subprocess.TimeoutExpired("gh api", 60)
            return api(method, endpoint, data)

        output, errors = io.StringIO(), io.StringIO()
        with patch.object(publish, "gh", timeout_api), \
             patch("sys.argv", ["publish.py", "--repo", REPO, "--slug", "test-flow",
                                "--manifest", str(self.manifest), "--publish"]), \
             contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            self.assertEqual(publish.main(), 1)
        self.assertEqual(output.getvalue(), "")
        receipt = json.loads(errors.getvalue().splitlines()[0])
        self.assertEqual(receipt["asset_commit"], SHA)
        self.assertEqual(receipt["branch"], BRANCH)

    def test_non_image_rejected_before_publication(self):
        self.image.write_text("private log disguised as an image")
        with self.assertRaisesRegex(ValueError, "supported image"):
            publish.read_manifest(self.manifest, "test-flow")


if __name__ == "__main__":
    unittest.main()
