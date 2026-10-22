import json
import re
import os
import subprocess

BANNED_PHRASES = [
    "Hardware Acceleration, VRAM Allocations",
    "below 78 degrees Celsius",
    "do not modify protected kernel modules",
    "In-Depth Hardware Benchmarks, System Stability",
    "1.2K reads"
]

def validate_and_clean_post(post: dict) -> dict:
    content = post.get("content", "")
    for phrase in BANNED_PHRASES:
        if phrase.lower() in content.lower():
            raise ValueError(f"CRITICAL: Boilerplate detected ('{phrase}') in {post.get('id')}")

    clean_text = re.sub(r"<[^>]+>", " ", content)
    words = clean_text.split()
    word_count = len(words)
    read_minutes = max(3, round(word_count / 200))
    post["readTime"] = f"{read_minutes} min read"

    h2_headings = [h.strip().lower() for h in re.findall(r"<h2[^>]*>(.*?)</h2>", content)]
    post["takeaways"] = [
        t for t in post.get("takeaways", [])
        if t.strip().lower() not in h2_headings
    ]
    post["_word_count"] = word_count
    return post

with open("scripts/bioware_post.json", "r", encoding="utf-8") as f:
    post = json.load(f)

# Ensure extra required fields for site
post["excerpt"] = post["summary"]
post["author"] = "Tech Boss Editorial Team"
post["image"] = "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=1200&q=80"

# Validate
validated_post = validate_and_clean_post(post)
word_count = validated_post.pop("_word_count")
print(f"Post validated! Words: {word_count}, Read Time: {validated_post['readTime']}")

# 1. Update posts.json
with open("posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

# Remove if exists to avoid duplication
posts = [p for p in posts if p.get("id") != validated_post["id"]]
posts.insert(0, validated_post)

with open("posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)
print(f"Updated posts.json! Total articles: {len(posts)}")

# 2. Update js/data.js
data_js_content = "var initialArticles = " + json.dumps(posts, indent=2, ensure_ascii=False) + ";\n"
with open("js/data.js", "w", encoding="utf-8") as f:
    f.write(data_js_content)
print("Updated js/data.js!")

# 3. Run build_static.py
print("Running build_static.py...")
res = subprocess.run(["python", "scripts/build_static.py"], capture_output=True, text=True)
if res.returncode != 0:
    print("build_static.py error:", res.stderr)
else:
    print("build_static.py completed successfully!")

# 4. Run sitemap generation
if os.path.exists("scripts/generate_sitemap.js"):
    print("Updating sitemap.xml...")
    subprocess.run(["node", "scripts/generate_sitemap.js"], capture_output=True, text=True)

print("Publishing sequence completed successfully!")
