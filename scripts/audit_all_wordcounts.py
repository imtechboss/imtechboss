import json, re

with open("posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

print(f"Total posts audited: {len(posts)}")

results = []
for p in posts:
    pid = p.get("id", "")
    title = p.get("title", "")
    content = p.get("content", "")
    # clean HTML tags
    text = re.sub(r'<[^>]+>', ' ', content)
    words = len(text.split())
    results.append({
        "id": pid,
        "title": title,
        "words": words
    })

# Sort ascending by word count
results.sort(key=lambda x: x["words"])

under_500 = [r for r in results if r["words"] < 500]
under_600 = [r for r in results if 500 <= r["words"] < 600]
between_600_800 = [r for r in results if 600 <= r["words"] < 800]
above_800 = [r for r in results if r["words"] >= 800]

print(f"\n--- Summary Statistics ---")
print(f"Under 500 words: {len(under_500)}")
print(f"500 to 599 words: {len(under_600)}")
print(f"600 to 799 words: {len(between_600_800)}")
print(f"800+ words: {len(above_800)}")

print(f"\n--- ALL POSTS UNDER 600 WORDS ({len(under_500) + len(under_600)} posts) ---")
for r in under_500 + under_600:
    print(f"[{r['words']} words] {r['id']} -> {r['title']}")
