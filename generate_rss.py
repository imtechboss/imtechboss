import os
import re
import json
import datetime
import xml.etree.ElementTree as ET

def generate_feed():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'js', 'data.js')
    feed_path = os.path.join(base_dir, 'feed.xml')

    with open(data_path, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);', content, re.DOTALL)
    if not match:
        print("Error: initialArticles not found")
        return

    articles = json.loads(match.group(1))
    # Take latest 30 articles
    latest = articles[:30]

    # Namespaces
    ATOM_NS = "http://www.w3.org/2005/Atom"
    MEDIA_NS = "http://search.yahoo.com/mrss/"
    CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"

    ET.register_namespace('atom', ATOM_NS)
    ET.register_namespace('media', MEDIA_NS)
    ET.register_namespace('content', CONTENT_NS)

    rss = ET.Element("rss", {
        "version": "2.0",
        f"{{{ATOM_NS}}}dummy": "hack" # temporary to declare ns
    })
    del rss.attrib[f"{{{ATOM_NS}}}dummy"]
    rss.attrib["xmlns:atom"] = ATOM_NS
    rss.attrib["xmlns:media"] = MEDIA_NS
    rss.attrib["xmlns:content"] = CONTENT_NS

    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "Tech Boss"
    ET.SubElement(channel, "link").text = "https://imtechboss.com"
    ET.SubElement(channel, "description").text = "Latest Technology News, AI Breakthroughs, Software Guides & Gaming"
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "managingEditor").text = "binodbhatt500k@gmail.com (Binod Bhatt)"

    atom_link = ET.SubElement(channel, f"{{{ATOM_NS}}}link", {
        "href": "https://imtechboss.com/feed.xml",
        "rel": "self",
        "type": "application/rss+xml"
    })

    # Channel Image for RSS readers
    chan_image = ET.SubElement(channel, "image")
    ET.SubElement(chan_image, "url").text = "https://imtechboss.com/og-image.png"
    ET.SubElement(chan_image, "title").text = "Tech Boss"
    ET.SubElement(chan_image, "link").text = "https://imtechboss.com"

    for a in latest:
        post_id = a.get('id', '')
        title = a.get('title', '')
        excerpt = a.get('excerpt', '')
        date_str = a.get('date', '2026-09-24')
        cat = a.get('category', 'Technology')
        img_url = a.get('image', '')

        if img_url and not img_url.startswith('http'):
            img_url = 'https://imtechboss.com/' + img_url.lstrip('/')
        if not img_url:
            img_url = 'https://imtechboss.com/og-image.png'

        post_url = f"https://imtechboss.com/post.html?id={post_id}"

        # RFC 822 format for pubDate
        try:
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except:
            dt = datetime.datetime.now()
        pub_date = dt.strftime("%a, %d %b %Y 00:00:00 GMT")

        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = title
        ET.SubElement(item, "link").text = post_url
        ET.SubElement(item, "guid").text = post_url
        ET.SubElement(item, "pubDate").text = pub_date
        ET.SubElement(item, "category").text = cat

        # Rich description with image for Pinterest and RSS readers
        rich_desc = f'<p><img src="{img_url}" alt="{title}" /></p><p>{excerpt}</p>'
        ET.SubElement(item, "description").text = rich_desc

        # Standard Media RSS for Pinterest
        ET.SubElement(item, f"{{{MEDIA_NS}}}content", {
            "url": img_url,
            "medium": "image",
            "type": "image/jpeg"
        })
        ET.SubElement(item, f"{{{MEDIA_NS}}}thumbnail", {
            "url": img_url
        })

        # Standard Enclosure for Podcast / RSS tools
        ET.SubElement(item, "enclosure", {
            "url": img_url,
            "type": "image/jpeg",
            "length": "102400"
        })

    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ", level=0)
    tree.write(feed_path, encoding="utf-8", xml_declaration=True)
    print(f"Successfully generated feed.xml with {len(latest)} rich articles.")

if __name__ == '__main__':
    generate_feed()
