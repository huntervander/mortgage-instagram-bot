"""
Refresh the long-lived Instagram access token before it expires.
Long-lived tokens last ~60 days and must be refreshed at least once
every 60 days (and the token must be >24h old to refresh).

Usage:
    python refresh_token.py
"""

from datetime import datetime, timedelta
from pathlib import Path

import requests

ENV_PATH = Path(__file__).parent / ".env"


def load_env(env_path: Path) -> dict:
    env = {}
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env


def save_env(env_path: Path, env: dict) -> None:
    lines = [f"{key}={value}" for key, value in env.items()]
    env_path.write_text("\n".join(lines) + "\n")


def main():
    env = load_env(ENV_PATH)
    token = env["IG_ACCESS_TOKEN"]

    resp = requests.get(
        "https://graph.instagram.com/refresh_access_token",
        params={"grant_type": "ig_refresh_token", "access_token": token},
    )
    resp.raise_for_status()
    data = resp.json()

    new_token = data["access_token"]
    expires_in_seconds = data["expires_in"]
    expires_date = (datetime.now() + timedelta(seconds=expires_in_seconds)).strftime("%Y-%m-%d")

    env["IG_ACCESS_TOKEN"] = new_token
    env["IG_TOKEN_GENERATED"] = datetime.now().strftime("%Y-%m-%d")
    env["IG_TOKEN_EXPIRES_APPROX"] = expires_date
    save_env(ENV_PATH, env)

    print(f"Token refreshed. New expiry approx: {expires_date}")


if __name__ == "__main__":
    main()
