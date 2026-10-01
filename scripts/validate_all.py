#!/usr/bin/env python3
"""
Pre-Flight Master Validator for Tech Boss (imtechboss.com)
Runs:
1. python scripts/validate_articles.py (Schema, 'content' key, Anti-AI words, images, author)
2. python scripts/validate_xml.py (Sitemap and RSS XML syntax & escaping)
DO NOT PROCEED WITH DEPLOYMENT IF THIS EXITS WITH CODE 1.
"""

import subprocess
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_check(script_name):
    script_path = os.path.join(BASE_DIR, 'scripts', script_name)
    print(f"\n>>> Running {script_name}...")
    result = subprocess.run([sys.executable, script_path], cwd=BASE_DIR)
    if result.returncode != 0:
        print(f"\n[BLOCKED] {script_name} FAILED! Deployment cannot proceed.")
        sys.exit(1)

def main():
    print("=" * 60)
    print("🚀 IMTECHBOSS MASTER PRE-FLIGHT VALIDATION CHECK")
    print("=" * 60)
    run_check('validate_articles.py')
    run_check('validate_xml.py')
    print("\n" + "=" * 60)
    print("✨ ALL PRE-FLIGHT CHECKS PASSED (100% HEALTHY & READY TO DEPLOY)")
    print("=" * 60)

if __name__ == '__main__':
    main()
