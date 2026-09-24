import re

with open(r'C:/Users/aabir/.gemini/antigravity/brain/4158c5a1-1ae8-497a-86bd-7a5db11f6d6d/.system_generated/steps/7560/content.md', encoding='utf-8') as f:
    text = f.read()

# Search for any article cards in the Flipboard magazine HTML
urls = re.findall(r'https://imtechboss\.com/post[^\s"\'<>]+', text)
print("Imtechboss URLs in magazine:", set(urls))
