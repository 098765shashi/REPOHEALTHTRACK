#!/usr/bin/env python3
"""Single-command launcher: starts DB + backend + frontend, opens browser."""
import os, shutil, subprocess, sys, time, webbrowser
from pathlib import Path

ROOT = Path(__file__).parent

def have(cmd): return shutil.which(cmd) is not None

def main():
    env_file = ROOT / ".env"
    if not env_file.exists():
        shutil.copy(ROOT / ".env.example", env_file)
        print("[demo] Created .env from .env.example — set OPENAI_API_KEY for AI insights.")
    if not (have("docker") and (have("docker-compose") or True)):
        print("[demo] Docker is required. Install Docker Desktop and retry.")
        sys.exit(1)
    print("[demo] Building & starting containers (this takes a minute the first time)...")
    subprocess.run(["docker", "compose", "up", "--build", "-d"], cwd=ROOT, check=True)
    print("[demo] Waiting for services...")
    time.sleep(8)
    url = "http://localhost:3000"
    print(f"[demo] Opening {url}")
    try: webbrowser.open(url)
    except Exception: pass
    print("[demo] Backend docs at http://localhost:8000/docs")
    print("[demo] Tail logs: docker compose logs -f   |   Stop: docker compose down")

if __name__ == "__main__":
    main()
