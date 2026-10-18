# -*- coding: utf-8 -*-
import urllib.request
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def check_devto():
    url = 'https://dev.to/api/articles/me?per_page=15'
    req = urllib.request.Request(url, headers={'api-key': 'ZtmMvBpzm7EgsBquEstMv5mq', 'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("=" * 65)
            print("   📊 DEV.TO SYNDICATION & ENGAGEMENT METRICS")
            print("=" * 65)
            total_views = 0
            total_reactions = 0
            total_comments = 0
            for a in data:
                views = a.get('page_views_count', 0)
                reactions = a.get('positive_reactions_count', 0)
                comments = a.get('comments_count', 0)
                title = a.get('title', '')
                pub_date = a.get('published_at', '')[:10]
                total_views += views
                total_reactions += reactions
                total_comments += comments
                print(f"[{pub_date}] {views:>5} views | {reactions:>2} reactions | {comments} comments | {title[:55]}")
            print("-" * 65)
            print(f"Total Tracked Views: {total_views} | Total Reactions: {total_reactions} | Total Comments: {total_comments}")
            print("=" * 65)

            for a in data:
                if a.get('comments_count', 0) > 0:
                    a_id = a.get('id')
                    c_url = f"https://dev.to/api/comments?a_id={a_id}"
                    c_req = urllib.request.Request(c_url, headers={'api-key': 'ZtmMvBpzm7EgsBquEstMv5mq', 'User-Agent': 'Mozilla/5.0'})
                    try:
                        with urllib.request.urlopen(c_req) as c_resp:
                            comments_data = json.loads(c_resp.read().decode('utf-8'))
                            print(f"\n💬 Comments on '{a.get('title')[:50]}':")
                            for c in comments_data:
                                user_name = c.get('user', {}).get('name', 'Anonymous')
                                print(f"  - @{user_name}: {c.get('body_html', '')[:100]}...")
                    except Exception as ce:
                        pass
    except Exception as e:
        print("Dev.to Fetch Error:", e)

if __name__ == '__main__':
    check_devto()
