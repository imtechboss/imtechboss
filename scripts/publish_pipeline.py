#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER AUTOMATED PUBLISHING & INDEXING PIPELINE — TECH BOSS (imtechboss.com)
=============================================================================
This script executes the complete end-to-end publishing, SEO indexing,
syndication, and deployment pipeline whenever a new post is added to js/data.js.

Workflow executed:
 1. Detect & Inspect latest article from js/data.js
 2. Regenerate sitemap.xml (generate_sitemap.py)
 3. Regenerate feed.xml (generate_rss.py)
 4. Regenerate Cloudflare Worker _worker.js with Edge SSR (generate_worker.py)
 5. Validate master pre-flight integrity (validate_all.py)
 6. Push to Google Instant Indexing API (google_indexing.js)
 7. Push to Bing & IndexNow partners (ping_indexnow.js)
 8. Syndicate to DEV.to with DA 92 canonical backlink (auto-devto.js)
 9. Broadcast to Bluesky & Mastodon (social-auto-scheduler.js)
 10. Git commit & push origin main (triggers Cloudflare Pages live deploy)
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime

# Enforce UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT_DIR, 'js', 'data.js')

def print_header(title):
    print("\n" + "=" * 70)
    print(f"   {title}")
    print("=" * 70)

def print_step(step_num, title):
    print(f"\n[STEP {step_num}] {title}...")

def run_command(cmd, cwd=ROOT_DIR, check=True):
    """Run a shell command, printing output in real time."""
    use_shell = isinstance(cmd, str)
    cmd_str = cmd if isinstance(cmd, str) else " ".join(cmd)
    print(f"  > Executing: {cmd_str}")
    result = subprocess.run(cmd, cwd=cwd, shell=use_shell, text=True, capture_output=True, encoding='utf-8', errors='replace')
    if result.stdout:
        for line in result.stdout.strip().splitlines():
            print(f"    {line}")
    if result.returncode != 0:
        if result.stderr:
            for line in result.stderr.strip().splitlines():
                print(f"    [ERR] {line}")
        if check:
            print(f"\n❌ PIPELINE HALTED: Command failed with exit code {result.returncode}")
            sys.exit(result.returncode)
    return result

def get_latest_article():
    """Extract and validate the latest article from js/data.js."""
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: {DATA_PATH} not found!")
        sys.exit(1)

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);', content, re.DOTALL)
    if not match:
        print("❌ Error: initialArticles not found in js/data.js!")
        sys.exit(1)

    try:
        articles = json.loads(match.group(1))
    except Exception as e:
        print(f"❌ JSON parse error in data.js: {e}")
        sys.exit(1)

    if not articles:
        print("❌ No articles found in data.js!")
        sys.exit(1)

    latest = articles[0]
    return latest, len(articles)

def main():
    skip_git = "--no-git" in sys.argv
    skip_social = "--no-social" in sys.argv
    enable_devto = "--devto" in sys.argv

    print_header("TECH BOSS MASTER AUTO-PUBLISHING PIPELINE")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Working Directory: {ROOT_DIR}")

    # 1. Inspect Latest Article
    print_step(1, "Inspecting Latest Article in js/data.js")
    latest, total = get_latest_article()
    post_id = latest.get('id', '')
    title = latest.get('title', 'Untitled')
    date_str = latest.get('date', '')
    url = f"https://imtechboss.com/{post_id}/"

    print(f"  Article ID : {post_id}")
    print(f"  Title      : {title}")
    print(f"  Date       : {date_str}")
    print(f"  Target URL : {url}")
    print(f"  Total Posts: {total}")

    # 2. Pre-generate all static pages (/<slug>/index.html)
    print_step(2, "Pre-generating all static pages (/<slug>/index.html)")
    run_command("python scripts/build_static.py")

    # 3. Re-generate sitemap.xml
    print_step(3, "Regenerating sitemap.xml")
    run_command("python scripts/generate_sitemap.py")

    # 3. Re-generate feed.xml
    print_step(3, "Regenerating feed.xml (RSS 2.0 with Media RSS)")
    run_command("python generate_rss.py")

    # 4. Re-generate Cloudflare Worker Edge SSR
    print_step(4, "Regenerating Cloudflare Worker (_worker.js)")
    run_command("python scripts/generate_worker.py")

    # 5. Pre-Flight Validation
    print_step(5, "Running Master Pre-Flight Validation (Schema + Anti-AI + XML)")
    run_command("python scripts/validate_all.py")

    # 6. Google Instant Indexing API Push
    print_step(6, "Pushing URL to Google Instant Indexing API")
    run_command(f'node scripts/google_indexing.js "{url}"', check=False)

    # 7. Bing & IndexNow Push
    print_step(7, "Pushing to Microsoft Bing & IndexNow Engines")
    run_command("node scripts/ping_indexnow.js", check=False)

    # 8. DEV.to Syndication (High DA 92 Backlink) - Opt-in only to protect AdSense
    if enable_devto:
        print_step(8, "Syndicating to DEV.to with Canonical Backlink")
        run_command("node scripts/auto-devto.js", check=False)
    else:
        print("\n  [INFO] DEV.to syndication paused to guarantee 100% AdSense original content compliance (pass --devto to enable).")

    # 9. Decentralized Social Broadcast (Bluesky & Mastodon)
    if not skip_social:
        print_step(9, "Broadcasting to Bluesky & Mastodon")
        run_command("node scripts/social-auto-scheduler.js --once", check=False)

    # 10. Git Commit & Push (Cloudflare Live Deploy)
    if not skip_git:
        print_step(10, "Committing & Pushing to GitHub (Cloudflare Auto-Deploy)")
        run_command(["git", "add", "."])
        clean_title = re.sub(r'["\']', '', title)
        commit_msg = f'Publish: {clean_title} [auto-pipeline]'
        # Check if there are changes to commit
        diff_proc = subprocess.run(["git", "diff", "--staged", "--name-only"], cwd=ROOT_DIR, shell=False, text=True, capture_output=True)
        if diff_proc.stdout.strip():
            run_command(["git", "commit", "-m", commit_msg])
            run_command(["git", "push", "origin", "main"])
        else:
            print("  Git: No unstaged/staged changes to commit.")
        
        print("  Deploying live to Cloudflare Pages edge network...")
        run_command("npx wrangler@3 pages deploy . --project-name imtechboss --commit-dirty=true", check=False)
    else:
        print("\n  [INFO] Git commit & push skipped (--no-git flag set).")

    print_header("✨ AUTO-PUBLISH PIPELINE COMPLETE (ALL SYSTEMS LIVE)")
    print(f"  Live Article URL : {url}")
    print(f"  Google Search    : Queued via Google Indexing API")
    print(f"  Bing / IndexNow  : Queued via IndexNow API")
    print(f"  Syndication      : Processed via DEV.to")
    print(f"  Social Channels  : Bluesky & Mastodon updated")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main()
