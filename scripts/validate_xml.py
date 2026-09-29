# -*- coding: utf-8 -*-
"""
Mandatory XML validator for imtechboss.com:
Validates sitemap.xml and feed.xml with xml.etree.ElementTree.
Exits with code 1 if any unescaped ampersand or syntax error exists.
"""

import sys
import xml.etree.ElementTree as ET

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def validate():
    has_error = False

    # Check sitemap.xml
    try:
        tree1 = ET.parse('sitemap.xml')
        root1 = tree1.getroot()
        print(f"[PASS] sitemap.xml is 100% valid XML ({len(root1)} URL entries).")
    except Exception as e:
        print(f"[FAIL] CRITICAL ERROR in sitemap.xml: {e}", file=sys.stderr)
        has_error = True

    # Check feed.xml
    try:
        tree2 = ET.parse('feed.xml')
        channel = tree2.getroot().find('channel')
        items = channel.findall('item') if channel is not None else []
        print(f"[PASS] feed.xml is 100% valid XML ({len(items)} feed items).")
    except Exception as e:
        print(f"[FAIL] CRITICAL ERROR in feed.xml: {e}", file=sys.stderr)
        has_error = True

    if has_error:
        print("\n[DEPLOYMENT BLOCKED] Fix XML syntax errors before deploying to production.", file=sys.stderr)
        sys.exit(1)
    else:
        print("[PASS] All XML files passed validation successfully.")

if __name__ == '__main__':
    validate()
