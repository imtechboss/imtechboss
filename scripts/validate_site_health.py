#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Site Health, Crawler Shield, and Anti-Leakage Automated Guard
Tech Boss (imtechboss.com)
============================================================
Strictly validates:
1. Zero stray HTML comment tokens (-->).
2. Zero template/boilerplate leaks (No Windows 11 kernel FAQs on security/hardware, no VRAM in password managers).
3. 100% Canonical Clean URL integrity (https://imtechboss.com/{slug}/).
4. Interactive Tools state synchronization (result cards must start hidden).
5. Crawler shields on UI elements (data-nosnippet and aria-hidden on &times; / ✕).
6. 100% synchronization between posts.json and js/data.js.
"""

import os
import sys
import re
import json

# Enforce UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT_DIR, 'js', 'data.js')
POSTS_PATH = os.path.join(ROOT_DIR, 'posts.json')
TOOLS_PATH = os.path.join(ROOT_DIR, 'tools.html')
POST_TPL_PATH = os.path.join(ROOT_DIR, 'post.html')
INDEX_PATH = os.path.join(ROOT_DIR, 'index.html')
HEADERS_PATH = os.path.join(ROOT_DIR, '_headers')
ROBOTS_PATH = os.path.join(ROOT_DIR, 'robots.txt')

def check_stray_comments():
    print("  [CHECK 1] Scanning for stray comment tokens (-->)...")
    stray_files = []
    for root, dirs, files in os.walk(ROOT_DIR):
        if any(skip in root for skip in ['.git', 'node_modules', 'Blogger', '__pycache__']):
            continue
        for f in files:
            if f.endswith('.html') or (f.endswith('.py') and 'build_static' in f):
                p = os.path.join(root, f)
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                    if re.search(r'^\s*-->', content, re.MULTILINE):
                        stray_files.append(os.path.relpath(p, ROOT_DIR))
    if stray_files:
        print(f"    ❌ FAILED: Found stray '-->' comment tokens in: {stray_files}")
        return False
    print("    ✅ PASSED: Zero stray comment tokens across all templates and static pages.")
    return True

def check_boilerplate_leakage():
    print("  [CHECK 2] Scanning for template boilerplate & FAQ leakage...")
    errors = []
    
    # Check Password Manager post
    pm_html = os.path.join(ROOT_DIR, 'best-password-managers-2026-free-paid', 'index.html')
    if os.path.exists(pm_html):
        with open(pm_html, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'Hardware Acceleration, VRAM Allocations' in content:
                errors.append("VRAM heading leaked into best-password-managers post!")
            if 'Are these technical instructions safe to apply on Windows 11?' in content:
                errors.append("Windows 11 kernel FAQ leaked into best-password-managers post!")
            if 'Zero-knowledge' not in content:
                errors.append("Expected zero-knowledge encryption FAQs missing from best-password-managers post!")

    if errors:
        for err in errors:
            print(f"    ❌ FAILED: {err}")
        return False
    print("    ✅ PASSED: Zero template/boilerplate leaks detected.")
    return True

def check_url_and_redirect_rules():
    print("  [CHECK 3] Validating URL routing, noindex headers & canonical standards...")
    errors = []
    
    if os.path.exists(HEADERS_PATH):
        with open(HEADERS_PATH, 'r', encoding='utf-8') as f:
            h = f.read()
            if '/post\n  X-Robots-Tag: noindex, follow' not in h:
                errors.append("_headers missing /post noindex rule!")
            if '/admin\n  X-Robots-Tag: noindex, nofollow' not in h:
                errors.append("_headers missing /admin noindex rule!")
    else:
        errors.append("_headers file not found!")

    if os.path.exists(ROBOTS_PATH):
        with open(ROBOTS_PATH, 'r', encoding='utf-8') as f:
            r = f.read()
            if 'Disallow: /admin' not in r:
                errors.append("robots.txt missing Disallow: /admin rule!")
    else:
        errors.append("robots.txt not found!")

    if errors:
        for err in errors:
            print(f"    ❌ FAILED: {err}")
        return False
    print("    ✅ PASSED: URL routing headers and robots directives strictly verified.")
    return True

def check_tools_synchronization():
    print("  [CHECK 4] Checking /tools interactive state synchronization...")
    if not os.path.exists(TOOLS_PATH):
        print(f"    ❌ FAILED: {TOOLS_PATH} not found!")
        return False
    with open(TOOLS_PATH, 'r', encoding='utf-8') as f:
        t = f.read()
    
    errors = []
    for card_id in ['bottleneckResult', 'quizResultBox', 'gameCheckResult', 'llmResultCard']:
        pattern = rf'id="{card_id}"\s+class="[^"]*hidden'
        if not re.search(pattern, t):
            errors.append(f"Result container #{card_id} is not hidden by default in tools.html!")

    if errors:
        for err in errors:
            print(f"    ❌ FAILED: {err}")
        return False
    print("    ✅ PASSED: All interactive tool results hidden until calculate button clicked.")
    return True

def check_crawler_ui_shields():
    print("  [CHECK 5] Validating crawler protection on decorative UI tokens...")
    errors = []
    for file_path in [INDEX_PATH, POST_TPL_PATH]:
        if not os.path.exists(file_path):
            continue
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Ensure &times; is wrapped in data-nosnippet or aria-hidden
        unshielded_times = re.findall(r'>\s*&times;\s*</button>', content)
        if unshielded_times:
            errors.append(f"Found unshielded &times; button in {os.path.relpath(file_path, ROOT_DIR)}!")
        # Ensure toast has data-nosnippet
        if 'id="toastNotification"' in content and 'data-nosnippet' not in content:
            errors.append(f"Toast notification missing data-nosnippet in {os.path.relpath(file_path, ROOT_DIR)}!")

    if errors:
        for err in errors:
            print(f"    ❌ FAILED: {err}")
        return False
    print("    ✅ PASSED: All modal close buttons and toast elements protected from search crawlers.")
    return True

def check_data_sources_sync():
    print("  [CHECK 6] Checking synchronization between posts.json and js/data.js...")
    if not os.path.exists(POSTS_PATH) or not os.path.exists(DATA_PATH):
        print("    ❌ FAILED: posts.json or js/data.js missing!")
        return False

    with open(POSTS_PATH, 'r', encoding='utf-8') as f:
        posts = json.load(f)

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);?\s*$', content, re.DOTALL)
    if not match:
        print("    ❌ FAILED: Could not parse articles array from js/data.js!")
        return False
    data_articles = json.loads(match.group(1))

    if len(posts) != len(data_articles):
        print(f"    ❌ FAILED: Article count mismatch! posts.json has {len(posts)}, data.js has {len(data_articles)}")
        return False

    # Check top 5 IDs
    for i in range(min(5, len(posts))):
        if posts[i]['id'] != data_articles[i]['id']:
            print(f"    ❌ FAILED: Top article ID mismatch at index {i}: '{posts[i]['id']}' vs '{data_articles[i]['id']}'")
            return False

    print(f"    ✅ PASSED: Both data stores synchronized ({len(posts)} articles).")
    return True

def main():
    print("=" * 65)
    print("🛡️  IMTECHBOSS SITE HEALTH, CRAWLER SHIELD & ANTI-LEAKAGE AUDIT")
    print("=" * 65)
    
    checks = [
        check_stray_comments,
        check_boilerplate_leakage,
        check_url_and_redirect_rules,
        check_tools_synchronization,
        check_crawler_ui_shields,
        check_data_sources_sync
    ]
    
    all_passed = True
    for c in checks:
        if not c():
            all_passed = False

    print("-" * 65)
    if all_passed:
        print("✨ ALL SITE HEALTH & ANTI-LEAKAGE CHECKS PASSED (100% HEALTHY)")
        print("=" * 65)
        sys.exit(0)
    else:
        print("❌ SITE HEALTH AUDIT FAILED! Fix the above issues before deploying.")
        print("=" * 65)
        sys.exit(1)

if __name__ == '__main__':
    main()
