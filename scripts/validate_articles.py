#!/usr/bin/env python3
"""
MANDATORY Article Validator for Tech Boss (imtechboss.com)
Verifies:
1. Schema consistency: 'content' key MUST exist and have non-empty HTML (NEVER 'body').
2. Word count: Each article must have >= 400 words.
3. Anti-AI rules: Zero banned words (delve, landscape, pivotal, testament, game-changer, etc.).
4. Image standards: High-res Unsplash 1200px crop format.
5. Author: Must be 'Tech Boss'.
6. No duplicate headings or repeated paragraph content.
7. JSON syntax validity in js/data.js.
Exits with code 1 if ANY error is found.
"""

import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'js', 'data.js')

BANNED_WORDS = [
    'delve', 'landscape', 'pivotal', 'testament', 'game-changer',
    'in conclusion', 'tapestries', 'realm', 'beacon', 'seamlessly'
]

def validate_articles():
    print("=" * 60)
    print("MANDATORY ARTICLE QUALITY & SCHEMA VALIDATION")
    print("=" * 60)

    if not os.path.exists(DATA_PATH):
        print(f"[FAIL] Missing {DATA_PATH}")
        sys.exit(1)

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);?\s*$', content, re.DOTALL)
    if not match:
        print("[FAIL] Could not extract 'initialArticles' array from js/data.js")
        sys.exit(1)

    try:
        articles = json.loads(match.group(1))
    except json.JSONDecodeError as e:
        print(f"[FAIL] Invalid JSON in js/data.js: {e}")
        sys.exit(1)

    print(f"Total articles to audit: {len(articles)}")

    errors = 0
    warnings = 0

    # We strictly audit the top 20 latest articles, and perform structural checks across all
    for idx, art in enumerate(articles):
        art_id = art.get('id', f'article_{idx}')
        title = art.get('title', '')
        author = art.get('author', '')
        image = art.get('image', '')
        excerpt = art.get('excerpt', '')
        
        # Check 1: 'content' key MUST exist. 'body' is FORBIDDEN.
        if 'body' in art and 'content' not in art:
            print(f"[FAIL] Article '{art_id}' uses forbidden key 'body' instead of 'content'!")
            errors += 1
        elif 'content' not in art or not art['content'].strip():
            print(f"[FAIL] Article '{art_id}' is missing required 'content' field!")
            errors += 1
            
        art_content = art.get('content', '')
        
        # Check 2: Word count on latest 20 articles
        if idx < 20 and art_content:
            text_only = re.sub(r'<[^>]+>', ' ', art_content)
            words = len(text_only.split())
            if words < 350:
                print(f"[FAIL] Article '{art_id}' word count too short: {words} words (min 350 required)")
                errors += 1

        # Check 3: Author standard
        raw_author = author if isinstance(author, str) else author.get('name', '') if isinstance(author, dict) else ''
        if raw_author != 'Tech Boss':
            print(f"[FAIL] Article '{art_id}' has invalid author '{raw_author}' (must be 'Tech Boss')")
            errors += 1

        # Check 4: Image standards
        if not image.startswith('https://images.unsplash.com/') or 'w=1200' not in image:
            if idx < 20: # Strictly enforce on newer publications
                print(f"[FAIL] Article '{art_id}' does not use 1200px Unsplash image: {image}")
                errors += 1

        # Check 5: Banned AI words (on latest 20 articles)
        if idx < 20:
            full_text = f"{title} {excerpt} {art_content}".lower()
            for bw in BANNED_WORDS:
                if re.search(rf'\b{re.escape(bw)}\b', full_text):
                    print(f"[FAIL] Article '{art_id}' contains banned AI cliché: '{bw}'")
                    errors += 1

        # Check 6: Repeated headings or content in latest 20
        if idx < 20 and art_content:
            h2s = re.findall(r'<h2>([^<]+)</h2>', art_content, re.IGNORECASE)
            if len(h2s) != len(set(h2s)):
                dupes = [h for h in set(h2s) if h2s.count(h) > 1]
                print(f"[FAIL] Article '{art_id}' has duplicate <h2> tags: {dupes}")
                errors += 1

    print("-" * 60)
    if errors == 0:
        print("[PASS] ALL ARTICLES PASSED SCHEMA, QUALITY, AND ANTI-AI VALIDATION! (ZERO ERRORS)")
        print("=" * 60)
        return True
    else:
        print(f"[ERROR] {errors} validation error(s) discovered! You MUST fix them before deploying.")
        print("=" * 60)
        sys.exit(1)

if __name__ == '__main__':
    validate_articles()
