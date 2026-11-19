#!/usr/bin/env python3
"""
ClockEE GitHub Auto-Sync & Publisher
Monitors changes in the ClockEE directory and automatically commits and pushes to GitHub.
"""

import os
import sys
import time
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = ROOT_DIR / "sync_config.json"

# Auto-detect git executable
def find_git_binary():
    # 1. System PATH
    found = shutil.which("git")
    if found:
        return found
    # 2. LocalAppData MinGit
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    candidates = [
        os.path.join(local_app_data, "Programs", "MinGit", "cmd", "git.exe"),
        os.path.join(local_app_data, "Programs", "Git", "cmd", "git.exe"),
        r"C:\Program Files\Git\cmd\git.exe",
        r"C:\Program Files (x86)\Git\cmd\git.exe",
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return "git"

GIT_BIN = find_git_binary()

DEFAULT_CONFIG = {
    "repo_url": "",
    "branch": "main",
    "debounce_seconds": 3,
    "user_name": "",
    "user_email": "",
    "auto_push": True
}

# Ignore patterns
IGNORE_NAMES = {
    ".git", ".sync_state.json", "sync_config.json",
    ".vscode", ".idea", "__pycache__"
}
IGNORE_SUFFIXES = {
    ".bak", ".tmp", ".log", ".swp", ".pyc"
}

def load_config():
    if CONFIG_FILE.is_file():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                config = DEFAULT_CONFIG.copy()
                config.update(data)
                return config
        except Exception as e:
            print(f"[!] Warning reading config: {e}")
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def run_git(args, check=False, capture=True):
    cmd = [GIT_BIN] + args
    env = os.environ.copy()
    # Add MinGit directory to PATH if needed
    git_dir = os.path.dirname(GIT_BIN)
    if git_dir and git_dir not in env.get("PATH", ""):
        env["PATH"] = git_dir + os.pathsep + env.get("PATH", "")

    result = subprocess.run(
        cmd,
        cwd=str(ROOT_DIR),
        capture_output=capture,
        text=True,
        env=env
    )
    if check and result.returncode != 0:
        err = result.stderr.strip() if result.stderr else result.stdout.strip()
        raise RuntimeError(f"Git error ({' '.join(args)}): {err}")
    return result

def ensure_git_setup(config):
    # Check if .git exists
    if not (ROOT_DIR / ".git").is_dir():
        print("[*] Initializing local Git repository...")
        run_git(["init", "-b", config.get("branch", "main")], check=True)

    # Check git user.name
    res = run_git(["config", "user.name"])
    if not res.stdout.strip():
        name = config.get("user_name") or "ClockEE AutoSync"
        run_git(["config", "user.name", name], check=True)
        print(f"[*] Configured git user.name: {name}")

    # Check git user.email
    res = run_git(["config", "user.email"])
    if not res.stdout.strip():
        email = config.get("user_email") or "kunal@local"
        run_git(["config", "user.email", email], check=True)
        print(f"[*] Configured git user.email: {email}")

    # Check remote origin
    repo_url = config.get("repo_url", "").strip()
    if repo_url:
        remotes = run_git(["remote", "-v"]).stdout
        if "origin" in remotes:
            run_git(["remote", "set-url", "origin", repo_url], check=True)
        else:
            run_git(["remote", "add", "origin", repo_url], check=True)
        print(f"[*] Remote 'origin' configured to: {repo_url}")

def get_snapshot():
    """Returns a dict of {relative_path: mtime} for tracked project files."""
    snapshot = {}
    for root, dirs, files in os.walk(ROOT_DIR):
        # Filter directories in-place
        dirs[:] = [d for d in dirs if d not in IGNORE_NAMES and not d.startswith(".")]
        for file in files:
            if file in IGNORE_NAMES:
                continue
            ext = os.path.splitext(file)[1].lower()
            if ext in IGNORE_SUFFIXES:
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, ROOT_DIR).replace("\\", "/")
            try:
                snapshot[rel_path] = os.path.getmtime(full_path)
            except OSError:
                pass
    return snapshot

def git_has_changes():
    res = run_git(["status", "--porcelain"])
    return res.stdout.strip()

def perform_sync(config):
    status_output = git_has_changes()
    if not status_output:
        return False

    # Collect changed files for commit message
    lines = status_output.splitlines()
    changed_files = []
    for line in lines[:5]:
        parts = line.strip().split(maxsplit=1)
        if len(parts) > 1:
            changed_files.append(parts[1])
        elif len(parts) == 1:
            changed_files.append(parts[0])

    if len(lines) > 5:
        summary_str = ", ".join(changed_files) + f" (+{len(lines) - 5} more)"
    else:
        summary_str = ", ".join(changed_files)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Auto-sync [{timestamp}]: {summary_str}"

    print(f"\n[+] Changes detected in {len(lines)} file(s):")
    for line in lines[:6]:
        print(f"    {line}")
    if len(lines) > 6:
        print(f"    ... and {len(lines) - 6} more")

    # Git stage
    print("[*] Staging files (git add -A)...")
    run_git(["add", "-A"], check=True)

    # Git commit
    print(f"[*] Committing: \"{commit_msg}\"...")
    run_git(["commit", "-m", commit_msg], check=True)

    # Git push
    if config.get("auto_push", True):
        repo_url = config.get("repo_url", "").strip()
        if not repo_url:
            print("[!] Notice: No remote GitHub repository URL configured yet.")
            print("    Run 'python auto_sync.py --setup' or edit 'sync_config.json' to set repo_url.")
            print("[*] Changes committed locally.")
            return True

        branch = config.get("branch", "main")
        print(f"[*] Pushing to GitHub (origin {branch})...")
        push_res = run_git(["push", "-u", "origin", branch])
        if push_res.returncode == 0:
            print(f"[OK] Successfully pushed and published to GitHub at {timestamp}!")
        else:
            err = push_res.stderr.strip() or push_res.stdout.strip()
            print(f"[!] Push failed: {err}")
            print("    Check your network, repository permissions, or Personal Access Token.")
    else:
        print("[*] Local commit created (auto_push disabled).")

    return True

def interactive_setup():
    print("=" * 60)
    print("      ClockEE GitHub Auto-Sync & Publisher Setup")
    print("=" * 60)
    config = load_config()

    current_repo = config.get("repo_url", "")
    print(f"\nCurrent GitHub Repository URL: {current_repo or '(Not configured yet)'}")
    print("Example: https://github.com/YourUsername/ClockEE.git")
    print("Or with Token: https://YOUR_TOKEN@github.com/YourUsername/ClockEE.git")
    new_repo = input(f"Enter GitHub Repo URL [{current_repo}]: ").strip()
    if new_repo:
        config["repo_url"] = new_repo

    current_branch = config.get("branch", "main")
    new_branch = input(f"Target Branch [{current_branch}]: ").strip()
    if new_branch:
        config["branch"] = new_branch

    current_name = config.get("user_name", "")
    new_name = input(f"Git Commit Author Name [{current_name or 'ClockEE User'}]: ").strip()
    if new_name:
        config["user_name"] = new_name

    current_email = config.get("user_email", "")
    new_email = input(f"Git Commit Author Email [{current_email or 'kunal@local'}]: ").strip()
    if new_email:
        config["user_email"] = new_email

    save_config(config)
    print("\n[*] Initializing Git configuration...")
    ensure_git_setup(config)
    print("[OK] Setup completed successfully!\n")

def run_watcher():
    config = load_config()
    ensure_git_setup(config)

    repo_url = config.get("repo_url", "")
    branch = config.get("branch", "main")
    debounce_sec = max(1, int(config.get("debounce_seconds", 3)))

    print("=" * 60)
    print("      ClockEE Live GitHub Auto-Sync is Running")
    print("=" * 60)
    print(f"Directory   : {ROOT_DIR}")
    print(f"Git Binary  : {GIT_BIN}")
    print(f"Branch      : {branch}")
    print(f"Remote URL  : {repo_url or '(No remote URL yet - committing locally)'}")
    print(f"Debounce    : {debounce_sec}s delay after last edit")
    print("Status      : Watching for changes... (Press Ctrl+C to stop)")
    print("=" * 60)

    # Initial check
    if git_has_changes():
        print("\n[*] Initial uncommitted changes detected. Syncing now...")
        perform_sync(config)

    last_snapshot = get_snapshot()
    pending_sync = False
    last_change_time = 0

    try:
        while True:
            time.sleep(1)
            current_snapshot = get_snapshot()

            # Compare snapshots
            changed = False
            if set(current_snapshot.keys()) != set(last_snapshot.keys()):
                changed = True
            else:
                for path, mtime in current_snapshot.items():
                    if last_snapshot.get(path) != mtime:
                        changed = True
                        break

            if changed:
                last_change_time = time.time()
                last_snapshot = current_snapshot
                if not pending_sync:
                    print(f"\n[*] Change detected at {datetime.now().strftime('%H:%M:%S')}. Waiting {debounce_sec}s for editing to settle...")
                    pending_sync = True

            # If pending and debounce period has passed
            if pending_sync and (time.time() - last_change_time >= debounce_sec):
                pending_sync = False
                perform_sync(config)
                print(f"[*] Resumed watching for changes...")

    except KeyboardInterrupt:
        print("\n\n[*] Auto-sync stopped by user. Goodbye!")
        sys.exit(0)

def main():
    if "--setup" in sys.argv:
        interactive_setup()
        return

    if "--once" in sys.argv:
        config = load_config()
        ensure_git_setup(config)
        print("[*] Running one-time sync...")
        performed = perform_sync(config)
        if not performed:
            print("[OK] Everything is up to date, nothing to sync.")
        return

    # Check if config is brand new without repo_url
    config = load_config()
    if not config.get("repo_url"):
        # Still run watcher, but warn that commits are local until remote is added
        print("[!] Note: No 'repo_url' is set in 'sync_config.json'.")
        print("    Auto-sync will commit changes locally.")
        print("    Run 'python auto_sync.py --setup' anytime to connect your GitHub repo.\n")

    run_watcher()

if __name__ == "__main__":
    main()
