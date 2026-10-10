#!/usr/bin/env python3
"""Publish selected screenshots without changing the product checkout."""

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import quote


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="public owner/fork")
    parser.add_argument("--slug", required=True, help="lowercase task slug")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--publish", action="store_true", help="upload; default is preview")
    args = parser.parse_args()
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", args.repo):
        parser.error("--repo must be owner/repository")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        parser.error("--slug must contain lowercase words separated by hyphens")
    try:
        rows, assets = read_manifest(args.manifest, args.slug)
        result = {"repository": args.repo, "branch": f"pr-assets/{args.slug}",
                  "files": [str(path) for path, _ in assets.values()]}
        if args.publish:
            result.update(publish(args.repo, result["branch"], assets))
        result["preview"] = not args.publish
        key = "markdown" if args.publish else "preview_markdown"
        result[key] = render(rows, args.repo, result.get("commit", "COMMIT_SHA"))
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


def read_manifest(manifest, slug):
    rows = json.loads(manifest.read_text())
    if not isinstance(rows, list) or not rows:
        raise ValueError("manifest must be a non-empty list of screenshot rows")
    assets = {}
    for row in rows:
        if not isinstance(row, dict) or not all(isinstance(row.get(k), str) and row[k].strip()
                                               for k in ("platform", "step")):
            raise ValueError("each row needs a platform and step")
        if not row.get("before") and not row.get("after"):
            raise ValueError("each row needs a before or after image")
        for side in ("before", "after"):
            if not row.get(side):
                continue
            path = (manifest.parent / row[side]).resolve()
            data = path.read_bytes()
            suffix = path.suffix.lower()
            signatures = {".png": data.startswith(b"\x89PNG\r\n\x1a\n"),
                          ".jpg": data.startswith(b"\xff\xd8\xff"),
                          ".jpeg": data.startswith(b"\xff\xd8\xff"),
                          ".gif": data[:6] in (b"GIF87a", b"GIF89a"),
                          ".webp": data[:4] == b"RIFF" and data[8:12] == b"WEBP"}
            if not signatures.get(suffix):
                raise ValueError(f"not a supported image: {path}")
            name = re.sub(r"[^a-zA-Z0-9_.-]", "-", path.name)
            target = f"{slug}/{hashlib.sha256(data).hexdigest()[:12]}-{name}"
            assets[target] = (path, data)
            row[side] = target
    return rows, assets


def publish(repo, branch, assets):
    account = gh("GET", "user")["login"]
    info = gh("GET", f"repos/{repo}")
    if info["full_name"].lower() != repo.lower() or info["private"] or not info["fork"]:
        raise ValueError("screenshots must target the selected public fork")
    if not info["permissions"]["push"]:
        raise ValueError(f"{account} cannot push to {repo}")
    ref = f"refs/heads/{branch}"
    matches = gh("GET", f"repos/{repo}/git/matching-refs/heads/{branch}")
    previous = next((r["object"]["sha"] for r in matches if r["ref"] == ref), None)

    def upload(item):
        path, (_, data) = item
        blob = gh("POST", f"repos/{repo}/git/blobs",
                  {"content": base64.b64encode(data).decode(), "encoding": "base64"})
        return {"path": path, "mode": "100644", "type": "blob", "sha": blob["sha"]}

    with ThreadPoolExecutor(max_workers=4) as pool:
        entries = list(pool.map(upload, assets.items()))
    tree = gh("POST", f"repos/{repo}/git/trees", {"tree": entries})
    identity = {"name": "AmanRajSinghMourya", "email": "amanrajmourya7@gmail.com"}
    commit = gh("POST", f"repos/{repo}/git/commits",
                {"message": f"Add PR screenshots for {branch.removeprefix('pr-assets/')}",
                 "tree": tree["sha"], "parents": [previous] if previous else [],
                 "author": identity, "committer": identity})
    print(json.dumps({"repository": repo, "branch": branch, "asset_commit": commit["sha"]}),
          file=sys.stderr)
    if previous:
        gh("PATCH", f"repos/{repo}/git/refs/heads/{branch}",
           {"sha": commit["sha"], "force": False})
    else:
        gh("POST", f"repos/{repo}/git/refs", {"ref": ref, "sha": commit["sha"]})
    published = gh("GET", f"repos/{repo}/git/ref/heads/{branch}")
    if published["object"]["sha"] != commit["sha"]:
        raise ValueError(f"asset branch changed during publication; inspect {repo}:{branch}")
    return {"account": account, "commit": commit["sha"]}


def render(rows, repo, commit):
    lines = []
    for platform in dict.fromkeys(row["platform"] for row in rows):
        lines.extend([f"**{html.escape(platform)}**", "",
                      "| Step | Before | After |", "| --- | --- | --- |"])
        for row in rows:
            if row["platform"] != platform:
                continue
            cells = [html.escape(row["step"]).replace("|", "\\|").replace("\n", " ")]
            for side in ("before", "after"):
                if not row.get(side):
                    cells.append("—")
                    continue
                url = f"https://raw.githubusercontent.com/{repo}/{commit}/{quote(row[side])}"
                alt = html.escape(f"{platform}: {row['step']} ({side})", quote=True)
                cells.append(f'<img src="{url}" width="230" alt="{alt}">')
            lines.append("| " + " | ".join(cells) + " |")
        lines.append("")
    return "\n".join(lines)


def gh(method, endpoint, data=None):
    command = ["gh", "api", endpoint, "--method", method]
    if data is not None:
        command.extend(["--input", "-"])
    result = subprocess.run(command, input=json.dumps(data) if data is not None else None,
                            capture_output=True, text=True, timeout=60)
    if result.returncode:
        raise ValueError(f"{method} {endpoint}: {result.stderr.strip()}")
    return json.loads(result.stdout)


if __name__ == "__main__":
    sys.exit(main())
