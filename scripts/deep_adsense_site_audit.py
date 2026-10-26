# -*- coding: utf-8 -*-
"""
deep_adsense_site_audit.py
Exhaustive, rigorous, multi-point Google AdSense Readiness Audit across EVERY post on imtechboss.com.
"""

import os
import sys
import json
import re
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_JSON_PATH = os.path.join(ROOT_DIR, 'posts.json')
DATA_JS_PATH = os.path.join(ROOT_DIR, 'js', 'data.js')

# 1. Anti-AI Banned Clichés
BANNED_AI_WORDS = [
    "delve", "landscape", "pivotal", "testament",
    "game-changer", "in conclusion", "tapestries",
    "realm", "beacon", "seamlessly"
]

# 2. Strict AdSense Policy Triggers (piracy, warez, unverified downloads)
POLICY_RISK_TERMS = [
    r'\bwarez\b', r'\bkeygen\b', r'\btorrent download\b',
    r'\bcracked software\b', r'\bpirated\b', r'\bnull script\b',
    r'\bbypass paywall\b'
]

# 3. Known Boilerplate Leak Phrases
LEAK_PHRASES = [
    "modify protected kernel modules",
    "operate within standard operating system guidelines and do not modify",
    "Yes. All diagnostic tools, hardware versus comparison engines",
    "Action completed",
    "<!--",
    "-->"
]

def clean_html(raw_html):
    return re.sub(r'<[^>]+>', ' ', raw_html)

def word_count(raw_html):
    text = clean_html(raw_html)
    return len(text.split())

def run_deep_audit():
    print("=" * 75)
    print("   DEEP GOOGLE ADSENSE READINESS AUDIT — EVERY SINGLE POST AUDITED")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Root Directory: {ROOT_DIR}")
    print("=" * 75)

    if not os.path.exists(POSTS_JSON_PATH):
        print("❌ Error: posts.json not found!")
        sys.exit(1)

    with open(POSTS_JSON_PATH, 'r', encoding='utf-8') as f:
        posts = json.load(f)

    total_posts = len(posts)
    print(f"\nTotal Posts to Audit: {total_posts}\n")

    issues_found = []
    thin_content = []
    ai_cliches = []
    policy_risks = []
    boilerplate_leaks = []
    ad_placeholder_leaks = []
    missing_images = []
    invalid_images = []
    missing_static_dir = []
    schema_issues = []

    seen_ids = set()
    seen_titles = set()
    faq_hashes = {}

    for idx, p in enumerate(posts, 1):
        pid = p.get('id', f'unknown-{idx}')
        title = p.get('title', '')
        category = p.get('category', '')
        author = p.get('author', '')
        date = p.get('date', '')
        image = p.get('image', '')
        content = p.get('content', '')
        excerpt = p.get('excerpt', '')

        # Check A: Unique ID & Title
        if pid in seen_ids:
            issues_found.append(f"[{pid}] Duplicate ID found!")
        seen_ids.add(pid)

        title_lower = title.strip().lower()
        if title_lower in seen_titles:
            issues_found.append(f"[{pid}] Duplicate Title found: '{title}'")
        seen_titles.add(title_lower)

        # Check B: Word Count (Thin Content check)
        wc = word_count(content)
        if wc < 600:
            thin_content.append((pid, title, wc))

        # Check C: Anti-AI Banned Words
        full_text = f"{title} {excerpt} {clean_html(content)}".lower()
        for bw in BANNED_AI_WORDS:
            pattern = r'\b' + re.escape(bw) + r'\b'
            if re.search(pattern, full_text):
                ai_cliches.append((pid, title, bw))

        # Check D: AdSense Policy Risk Words
        for pr in POLICY_RISK_TERMS:
            if re.search(pr, full_text):
                policy_risks.append((pid, title, pr))

        # Check E: Boilerplate Leaks
        for lp in LEAK_PHRASES:
            if lp.lower() in content.lower():
                boilerplate_leaks.append((pid, title, lp))

        # Check F: Empty Ad / Sponsor Placeholders
        if re.search(r'Sponsored\s*/\s*Advertisement', content, re.IGNORECASE) or '<ins class="adsbygoogle"' in content:
            ad_placeholder_leaks.append((pid, title))

        # Check G: Image Standards
        if not image:
            missing_images.append((pid, title))
        elif 'images.unsplash.com' in image:
            if 'w=1200' not in image and 'w=1600' not in image:
                invalid_images.append((pid, title, image))

        # Check H: Author & Metadata
        raw_author = author if isinstance(author, str) else (author.get('name', '') if isinstance(author, dict) else '')
        if raw_author != 'Tech Boss':
            schema_issues.append((pid, f"Author name is '{raw_author}', expected 'Tech Boss'"))

        # Check I: Static Folder & index.html Existence
        static_dir = os.path.join(ROOT_DIR, pid)
        static_file = os.path.join(static_dir, 'index.html')
        if not os.path.exists(static_file):
            missing_static_dir.append((pid, static_file))
        else:
            file_size = os.path.getsize(static_file)
            if file_size < 1000:
                schema_issues.append((pid, f"Static index.html too small ({file_size} bytes)"))

    # Print Summary Report
    print("-" * 75)
    print("AUDIT RESULTS SUMMARY:")
    print("-" * 75)

    print(f"1. Total Posts Audited          : {total_posts}")
    print(f"2. Duplicate Post IDs/Titles    : {len(issues_found)}")
    print(f"3. Thin Content (<600 words)    : {len(thin_content)}")
    print(f"4. Anti-AI Banned Clichés       : {len(ai_cliches)}")
    print(f"5. AdSense Policy Risk Terms    : {len(policy_risks)}")
    print(f"6. Boilerplate / FAQ Leaks      : {len(boilerplate_leaks)}")
    print(f"7. In-Content Ad Placeholders   : {len(ad_placeholder_leaks)}")
    print(f"8. Missing Images               : {len(missing_images)}")
    print(f"9. Non-1200px Unsplash Images   : {len(invalid_images)}")
    print(f"10. Missing Static Directories  : {len(missing_static_dir)}")
    print(f"11. Schema / Metadata Issues    : {len(schema_issues)}")

    # Detailed Findings
    if thin_content:
        print("\n⚠️ THIN CONTENT ARTICLES (<600 words):")
        for pid, t, wc in thin_content:
            print(f"  - [{wc} words] {pid}: {t[:60]}...")

    if ai_cliches:
        print("\n⚠️ ANTI-AI CLICHÉS DETECTED:")
        for pid, t, bw in ai_cliches:
            print(f"  - [{bw}] in {pid}")

    if policy_risks:
        print("\n⚠️ ADSENSE POLICY RISK TERMS:")
        for pid, t, pr in policy_risks:
            print(f"  - [{pr}] in {pid}")

    if boilerplate_leaks:
        print("\n⚠️ BOILERPLATE LEAKS DETECTED:")
        for pid, t, lp in boilerplate_leaks:
            print(f"  - [{lp}] in {pid}")

    if ad_placeholder_leaks:
        print("\n⚠️ AD PLACEHOLDERS IN CONTENT:")
        for pid, t in ad_placeholder_leaks:
            print(f"  - {pid}")

    if invalid_images:
        print("\n⚠️ NON-1200px IMAGES:")
        for pid, t, img in invalid_images[:5]:
            print(f"  - {pid}: {img}")

    if missing_static_dir:
        print("\n❌ MISSING STATIC DIRECTORIES:")
        for pid, f in missing_static_dir:
            print(f"  - {pid}")

    if schema_issues:
        print("\n⚠️ SCHEMA / METADATA ISSUES:")
        for pid, msg in schema_issues:
            print(f"  - {pid}: {msg}")

    # Final Verdict
    total_critical = (
        len(issues_found) + len(thin_content) + len(ai_cliches) +
        len(policy_risks) + len(boilerplate_leaks) + len(ad_placeholder_leaks) +
        len(missing_images) + len(invalid_images) + len(missing_static_dir) +
        len(schema_issues)
    )

    print("\n" + "=" * 75)
    if total_critical == 0:
        print("🎉 PERFECT SCORE: 100% OF ALL 146 ARTICLES ARE FULLY ADSENSE READY!")
        print("   Zero thin content, zero AI buzzwords, zero policy violations, zero leaks!")
    else:
        print(f"⚠️ TOTAL ATTENTION POINTS IDENTIFIED: {total_critical}")
    print("=" * 75)

    return total_critical

if __name__ == '__main__':
    run_deep_audit()
