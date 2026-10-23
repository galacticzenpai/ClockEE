# ClockEE GitHub Auto-Sync & Publishing System

This system continuously monitors your ClockEE folder for any file additions, edits, or deletions, automatically creates clean Git commits, and pushes them directly to GitHub to keep your project published online.

---

## Quick Start (1-Minute Setup)

### Step 1: Create a GitHub Repository
1. Go to [GitHub - New Repository](https://github.com/new).
2. Repository name: `ClockEE` (or any name you prefer).
3. Set visibility to **Public** (recommended for free GitHub Pages hosting) or **Private**.
4. Leave "Add a README file" **unchecked** (we already have files).
5. Click **Create repository**.
6. Copy the repository URL (e.g., `https://github.com/YOUR_USERNAME/ClockEE.git`).

---

### Step 2: Connect Your Repository
You can connect in one of two ways:

#### Option A: Double-Click Setup (Easiest)
- Double-click **`setup_github.bat`** in this folder.
- Paste your GitHub repository URL and follow the prompts.

#### Option B: Edit `sync_config.json` Directly
Open [`sync_config.json`](file:///d:/Desktop/ClockEE/sync_config.json) and enter your repo URL:
```json
{
    "repo_url": "https://github.com/YOUR_USERNAME/ClockEE.git",
    "branch": "main",
    "debounce_seconds": 3,
    "user_name": "Your Name",
    "user_email": "your_email@example.com",
    "auto_push": true
}
```
> **Tip for Authentication:**  
> If GitHub asks for a password during push, GitHub requires a **Personal Access Token (PAT)** instead of your account password:
> 1. Go to [GitHub Settings -> Developer Settings -> Personal access tokens -> Tokens (classic)](https://github.com/settings/tokens).
> 2. Generate a token with the `repo` scope.
> 3. You can put it directly in the URL: `https://ghp_YOUR_TOKEN@github.com/YOUR_USERNAME/ClockEE.git`

---

### Step 3: Run the Auto-Sync Watcher
- **Double-click `start_sync.bat`** to start the continuous watcher.
- It will watch your files. Whenever you edit or save any HTML, JS, or CSS file:
  - It waits 3 seconds (debounce) for you to finish saving.
  - Automatically stages and commits changed files.
  - Pushes directly to GitHub!
- To manually sync anytime, double-click **`push_now.bat`**.

---

### Step 4: Publish with GitHub Pages (Live Website)
ClockEE is already configured with an automated deployment workflow [`.github/workflows/deploy.yml`](file:///d:/Desktop/ClockEE/.github/workflows/deploy.yml).

To activate GitHub Pages for your repo:
1. In your GitHub repo, go to **Settings** -> **Pages**.
2. Under **Build and deployment** -> **Source**, select:
   - **GitHub Actions** (it will use the included workflow automatically!)
3. After the first push, your live site will be accessible at:  
   `https://<your-username>.github.io/<repo-name>/`
