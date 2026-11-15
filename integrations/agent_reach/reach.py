#!/usr/bin/env python3
"""
ClockEE Package: Agent Reach Data Bridge
Allows AI agents to search, scrape, and ingest discussions, syllabus updates,
and reference materials across web sources and educational forums (e.g., Reddit, StackExchange).
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
    def handle_data(self, data):
        cleaned = data.strip()
        if cleaned:
            self.texts.append(cleaned)
    def get_text(self):
        return " ".join(self.texts)

class AgentReach:
    def __init__(self, user_agent=None):
        self.headers = {
            "User-Agent": user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ClockEE-AgentReach/1.0"
        }

    def fetch_reddit_thread(self, subreddit: str, query: str = "", limit: int = 5):
        """Fetch top public educational threads from Reddit without API keys."""
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
        req = urllib.request.Request(url, headers=self.headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                posts = []
                for child in data.get("data", {}).get("children", []):
                    d = child.get("data", {})
                    posts.append({
                        "title": d.get("title"),
                        "score": d.get("score"),
                        "author": d.get("author"),
                        "num_comments": d.get("num_comments"),
                        "url": f"https://reddit.com{d.get('permalink')}"
                    })
                return {"success": True, "subreddit": subreddit, "posts": posts}
        except Exception as e:
            return {"success": False, "error": str(e), "subreddit": subreddit}

    def fetch_webpage_summary(self, url: str):
        """Fetch and extract clean plain text from a public web document."""
        req = urllib.request.Request(url, headers=self.headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
                parser = TextExtractor()
                parser.feed(html)
                text = parser.get_text()
                return {
                    "success": True,
                    "url": url,
                    "summary_text": text[:1500] + "..." if len(text) > 1500 else text
                }
        except Exception as e:
            return {"success": False, "error": str(e), "url": url}

if __name__ == "__main__":
    reach = AgentReach()
    res = reach.fetch_reddit_thread("JEENEETards", limit=3)
    print(json.dumps(res, indent=2))
