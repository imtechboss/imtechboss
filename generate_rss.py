import xml.etree.ElementTree as ET
import datetime
import re

sitemap_path = r"c:\Users\aabir\OneDrive\Desktop\website\sitemap.xml"
feed_path = r"c:\Users\aabir\OneDrive\Desktop\website\feed.xml"

# Parse sitemap
tree = ET.parse(sitemap_path)
root = tree.getroot()
namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

articles = []
for url in root.findall('ns:url', namespace):
    loc = url.find('ns:loc', namespace).text
    if 'post.html?id=' in loc:
        lastmod = url.find('ns:lastmod', namespace).text
        articles.append({'loc': loc, 'lastmod': lastmod})

# Sort by lastmod descending (already mostly sorted, but let's be sure)
articles.sort(key=lambda x: x['lastmod'], reverse=True)

# Get top 20
top_20 = articles[:20]

def slug_to_title(slug):
    words = slug.split('-')
    return ' '.join([w.capitalize() for w in words])

def format_rfc822(date_str):
    # Parse YYYY-MM-DD
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return dt.strftime("%a, %d %b %Y 00:00:00 +0000")

# Generate RSS XML
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")

ET.SubElement(channel, "title").text = "Tech Boss"
ET.SubElement(channel, "description").text = "The pulse of AI technology, smartphone reviews, software utilities, and gaming guides."
ET.SubElement(channel, "link").text = "https://imtechboss.com"
ET.SubElement(channel, "language").text = "en"
ET.SubElement(channel, "managingEditor").text = "binodbhatt500k@gmail.com (Binod Bhatt)"

for item in top_20:
    url = item['loc']
    slug = url.split('post.html?id=')[-1]
    title = slug_to_title(slug)
    pubDate = format_rfc822(item['lastmod'])
    desc = f"Read more about {title.lower()} in our latest article."

    item_el = ET.SubElement(channel, "item")
    ET.SubElement(item_el, "title").text = title
    ET.SubElement(item_el, "link").text = url
    ET.SubElement(item_el, "guid").text = url
    ET.SubElement(item_el, "pubDate").text = pubDate
    ET.SubElement(item_el, "description").text = desc

# write RSS
tree_rss = ET.ElementTree(rss)
ET.indent(tree_rss, space="  ", level=0)
tree_rss.write(feed_path, encoding="utf-8", xml_declaration=True)

# Update sitemap to include feed.xml if not present
has_feed = False
for url in root.findall('ns:url', namespace):
    loc = url.find('ns:loc', namespace).text
    if 'feed.xml' in loc:
        has_feed = True
        break

if not has_feed:
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    new_url = ET.Element("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
    ET.SubElement(new_url, "{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text = "https://imtechboss.com/feed.xml"
    ET.SubElement(new_url, "{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod").text = datetime.datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(new_url, "{http://www.sitemaps.org/schemas/sitemap/0.9}changefreq").text = "daily"
    ET.SubElement(new_url, "{http://www.sitemaps.org/schemas/sitemap/0.9}priority").text = "1.0"
    
    root.insert(0, new_url) # insert at top
    
    ET.indent(tree, space="  ", level=0)
    tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)

print("RSS generation and sitemap update complete.")
