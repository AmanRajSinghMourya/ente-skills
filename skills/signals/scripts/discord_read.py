#!/usr/bin/env python3
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request

DISCORD_EPOCH_MS = 1420070400000
KEYCHAIN_SERVICE = "ente-discord-bot"


def usage():
    print("usage: discord_read.py <channel_id> [hours=24]", file=sys.stderr)
    sys.exit(2)


def bot_token():
    result = subprocess.run(
        ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-w"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        print(f"no bot token in Keychain (service {KEYCHAIN_SERVICE})", file=sys.stderr)
        sys.exit(3)
    return result.stdout.strip()


def snowflake_at(epoch_seconds):
    return (int(epoch_seconds * 1000) - DISCORD_EPOCH_MS) << 22


def get(path, token):
    request = urllib.request.Request(
        f"https://discord.com/api/v10{path}",
        headers={"Authorization": f"Bot {token}", "User-Agent": "ente-skills-signals (1.0)"},
    )
    while True:
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code == 429:
                time.sleep(float(json.load(error).get("retry_after", 1)))
                continue
            print(f"Discord API error {error.code} for {path}", file=sys.stderr)
            sys.exit(1)


def main():
    if len(sys.argv) not in (2, 3) or not sys.argv[1].isdigit():
        usage()
    channel = sys.argv[1]
    hours = float(sys.argv[2]) if len(sys.argv) == 3 else 24.0
    token = bot_token()
    guild = get(f"/channels/{channel}", token).get("guild_id", "@me")
    after = snowflake_at(time.time() - hours * 3600)
    messages = []
    while True:
        batch = get(f"/channels/{channel}/messages?limit=100&after={after}", token)
        if not batch:
            break
        messages.extend(batch)
        after = max(int(message["id"]) for message in batch)
        if len(batch) < 100:
            break
    for message in sorted(messages, key=lambda m: int(m["id"])):
        author = message.get("author", {})
        who = "bot" if author.get("bot") else author.get("username", "?")
        text = " ".join(message.get("content", "").split())
        if text:
            link = f"https://discord.com/channels/{guild}/{channel}/{message['id']}"
            print(f"{message['timestamp'][:16]} {who}: {text} <{link}>")


if __name__ == "__main__":
    main()
