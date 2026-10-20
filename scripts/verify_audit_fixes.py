import os, re

def check_ps6():
    path = 'sony-playstation-6-ps6-specs-amd-zen-6-rdna-5-pssr-2-release-window-guide-2026/index.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    print("=== SONY PLAYSTATION 6 PAGE AUDIT ===")
    # 1. Check for Windows 11 / DISM
    has_windows = 'Windows 11' in html or 'DISM' in html or 'PowerShell' in html
    print(f"Contains Windows 11 / DISM / PowerShell: {has_windows} (Expected: False)")

    # 2. Check FAQs
    faqs_match = re.search(r'Frequently Asked Questions &amp; Technical Clarifications</h3>\s*</div>\s*<div class="space-y-3">([\s\S]*?)</div>\s*</div>', html)
    if faqs_match:
        questions = re.findall(r'<span>(.*?)</span>', faqs_match.group(1))
        print(f"FAQs count: {len(questions)}")
        for q in questions:
            print(f"  - FAQ: {q}")

    # 3. Check Takeaways Capsule
    capsule_match = re.search(r'<div id="aioAnswerCapsule"[\s\S]*?</div>\s*</div>', html)
    if capsule_match:
        c_text = capsule_match.group(0)
        sum_match = re.search(r'<strong>Direct Summary: </strong>([\s\S]*?)</div>', c_text)
        if sum_match:
            print(f"\nDirect Summary:\n  {sum_match.group(1).strip()[:140]}...")
        
        bullets = re.findall(r'<li[^>]*>[\s\S]*?<span class="leading-relaxed">([\s\S]*?)</span>\s*</li>', c_text)
        print(f"\nTakeaway Bullets ({len(bullets)} total):")
        for idx, b in enumerate(bullets, 1):
            print(f"  {idx}. {b.strip()[:140]}...")

    # 4. Check for broken post?id=
    post_id_links = re.findall(r'href=[\'"][^\'"]*post(?:\.html)?\?id=[^\'"]*[\'"]', html)
    print(f"\nBroken post?id= links: {len(post_id_links)} (Expected: 0)")

def check_blogger():
    print("\n=== BLOGGER POST AUDIT ===")
    path = 'blogger-1/index.html'
    if not os.path.exists(path):
        # find any blogger
        for d in os.listdir('.'):
            if d.startswith('blogger-') and os.path.isdir(d):
                path = os.path.join(d, 'index.html')
                break
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    robots_match = re.search(r'<meta name="robots" content="([^"]*)">', html)
    if robots_match:
        print(f"Blogger robots tag: {robots_match.group(0)} (Expected: noindex, follow)")

if __name__ == '__main__':
    check_ps6()
    check_blogger()
