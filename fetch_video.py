#!/usr/bin/env python3
"""
ClockEE Media Ingestion Helper
Downloads public video links (YouTube Shorts, YouTube, Instagram public reels, etc.)
for AI multimodal analysis and feature implementation.
"""

import os
import sys
import json
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
MEDIA_DIR = ROOT_DIR / "temp_media"
MEDIA_DIR.mkdir(exist_ok=True)

def cleanup_old_media(max_age_hours=24):
    """Remove media older than max_age_hours to save disk space."""
    now = time.time()
    for item in MEDIA_DIR.iterdir():
        if item.is_file():
            try:
                if now - item.stat().st_mtime > (max_age_hours * 3600):
                    item.unlink()
            except Exception:
                pass

def download_video(url: str):
    cleanup_old_media()
    
    timestamp = int(time.time())
    output_template = str(MEDIA_DIR / f"video_{timestamp}_%(id)s.%(ext)s")
    
    # Configure yt_dlp
    ydl_opts = {
        'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
        'outtmpl': output_template,
        'quiet': False,
        'no_warnings': True,
        'retries': 3,
        'merge_output_format': 'mp4'
    }
    
    try:
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # Ensure mp4 extension if merged
            base, _ = os.path.splitext(filename)
            if os.path.isfile(base + ".mp4"):
                filename = base + ".mp4"
                
            res = {
                "success": True,
                "title": info.get("title", "Video"),
                "duration": info.get("duration", 0),
                "filepath": os.path.abspath(filename),
                "url": url
            }
            print(json.dumps(res, indent=2))
            return res
    except Exception as e:
        err_res = {
            "success": False,
            "error": str(e),
            "url": url
        }
        print(json.dumps(err_res, indent=2), file=sys.stderr)
        return err_res

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_video.py <URL>")
        sys.exit(1)
        
    target_url = sys.argv[1].strip()
    result = download_video(target_url)
    if not result.get("success"):
        sys.exit(1)
