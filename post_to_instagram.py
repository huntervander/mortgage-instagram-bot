"""
Post an image + caption to the connected Instagram Business account.

Usage:
    python post_to_instagram.py --image-url "https://example.com/image.jpg" --caption "Caption text"

Reads credentials from .env in the same folder (IG_USER_ID, IG_ACCESS_TOKEN).
"""

import argparse
import sys
import time
from pathlib import Path

import requests

API_VERSION = "v21.0"
GRAPH_URL = f"https://graph.instagram.com/{API_VERSION}"


def load_env(env_path: Path) -> dict:
    env = {}
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env


def create_media_container(ig_user_id: str, token: str, media_url: str, caption: str, media_type: str = "IMAGE") -> str:
    data = {"caption": caption, "access_token": token}
    if media_type == "REELS":
        data["media_type"] = "REELS"
        data["video_url"] = media_url
    else:
        data["image_url"] = media_url
    resp = requests.post(f"{GRAPH_URL}/{ig_user_id}/media", data=data)
    resp.raise_for_status()
    return resp.json()["id"]


def wait_until_ready(container_id: str, token: str, timeout: int = 300) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        resp = requests.get(
            f"{GRAPH_URL}/{container_id}",
            params={"fields": "status_code", "access_token": token},
        )
        resp.raise_for_status()
        status = resp.json().get("status_code")
        if status == "FINISHED":
            return
        if status == "ERROR":
            raise RuntimeError(f"Media container {container_id} failed processing")
        time.sleep(5)
    raise TimeoutError(f"Media container {container_id} not ready after {timeout}s")


def publish_media(ig_user_id: str, token: str, container_id: str) -> str:
    resp = requests.post(
        f"{GRAPH_URL}/{ig_user_id}/media_publish",
        data={"creation_id": container_id, "access_token": token},
    )
    resp.raise_for_status()
    return resp.json()["id"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-url", help="Publicly accessible image URL")
    parser.add_argument("--video-url", help="Publicly accessible video URL (for Reels)")
    parser.add_argument("--caption", help="Post caption")
    parser.add_argument("--caption-file", help="Path to a text file containing the caption")
    parser.add_argument("--dry-run", action="store_true", help="Create container but do not publish")
    args = parser.parse_args()

    if args.caption_file:
        caption = Path(args.caption_file).read_text(encoding="utf-8")
    elif args.caption:
        caption = args.caption
    else:
        parser.error("one of --caption or --caption-file is required")

    if args.video_url:
        media_url = args.video_url
        media_type = "REELS"
    elif args.image_url:
        media_url = args.image_url
        media_type = "IMAGE"
    else:
        parser.error("one of --image-url or --video-url is required")

    env_path = Path(__file__).parent / ".env"
    env = load_env(env_path)
    ig_user_id = env["IG_USER_ID"]
    token = env["IG_ACCESS_TOKEN"]

    print("Creating media container...")
    container_id = create_media_container(ig_user_id, token, media_url, caption, media_type)
    print(f"Container created: {container_id}")

    print("Waiting for container to finish processing...")
    wait_until_ready(container_id, token)

    if args.dry_run:
        print("Dry run - not publishing. Container will expire in 24h if unused.")
        return

    print("Publishing...")
    media_id = publish_media(ig_user_id, token, container_id)
    print(f"Published! Media ID: {media_id}")


if __name__ == "__main__":
    main()
