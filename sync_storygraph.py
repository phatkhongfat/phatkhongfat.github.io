import os
import random
import requests
import datetime
import urllib.parse
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from storygraph_api.request.user_request import UserScraper

load_dotenv()
RAW_TOKEN = os.getenv("STORYGRAPH_TOKEN")
USERNAME = os.getenv("STORYGRAPH_USERNAME")
TOKEN = urllib.parse.unquote(RAW_TOKEN)

base_path = 'content/bookshelf'
os.makedirs(base_path, exist_ok=True)
colors = ["#1B1A17", "#461111", "#0F3D3E", "#100720", "#313131", "#541212", "#2D4263", "#191919", "#3E432E", "#2C3333"]

def parse_and_sync(html_content, status_label):
    soup = BeautifulSoup(html_content, 'html.parser')
    book_panes = soup.find_all('div', class_='book-pane-content')
    seen_titles = set()
    for pane in book_panes:
        title = "Unknown"
        title_h3 = pane.find('h3', class_='font-bold')
        if title_h3 and title_h3.find('a'):
            title = title_h3.find('a').text.strip().replace('"', '\\"')
        
        if title == "Unknown" or title in seen_titles: continue
        seen_titles.add(title)
        
        author = "Unknown Author"
        author_p = pane.find('p', class_='font-body')
        if author_p and author_p.find('a', href=lambda x: x and '/authors/' in x):
            author = author_p.find('a', href=lambda x: x and '/authors/' in x).text.strip()
        
        rating = 0
        r_span = pane.find('span', class_='-ml-1')
        if r_span:
            try: rating = float(r_span.text.strip())
            except: pass

        isbn = ""
        ed_info = pane.find('div', class_='edition-info')
        if ed_info:
            isbn_p = ed_info.find('p', string=lambda x: x and 'ISBN/UID:' in x)
            if isbn_p: isbn = isbn_p.text.replace('ISBN/UID:', '').strip()

        img_tag = pane.find('img', class_='rounded-sm')
        cover_url = img_tag.get('src', "") if img_tag else ""

        folder_name = "".join([c for c in title if c.isalnum() or c==' ']).rstrip().replace(' ', '-').lower()
        folder_path = os.path.join(base_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # DOWNLOAD COVER ONLY IF MISSING
        feature_img = os.path.join(folder_path, "feature.jpg")
        if cover_url and not os.path.exists(feature_img):
            try:
                r = requests.get(cover_url, timeout=15)
                if r.status_code == 200:
                    with open(feature_img, 'wb') as f: f.write(r.content)
                    print(f"Synced Cover: {title}")
            except Exception as e:
                print(f"Cover Error for {title}: {e}")

        # Hugo File - Check if we need to update
        index_path = os.path.join(folder_path, "index.md")
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # We preserve existing spine_color and width if the file exists to avoid flickering colors on every sync
        existing_color = random.choice(colors)
        existing_width = random.randint(28, 45)
        
        if os.path.exists(index_path):
            try:
                with open(index_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if 'spine_color:' in line: existing_color = line.split(':')[1].strip().strip('"')
                        if 'spine_width:' in line: existing_width = line.split(':')[1].strip()
            except: pass

        content = f"""---
title: "{title}"
authors: ["{author}"]
date: {today}
feature: "feature.jpg"
thumbnail: "feature.jpg"
status: {status_label}
rating: {rating}
isbn: "{isbn}"
storygraph_url: "https://app.thestorygraph.com/browse?search_term={urllib.parse.quote(title)}"
spine_color: "{existing_color}"
spine_width: {existing_width}
---
Fetched from StoryGraph.
"""
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)

def sync_all():
    print(f"Cleaning and Syncing StoryGraph for {USERNAME}...")
    
    # Wipe old folders to ensure a fresh, randomized look every time
    import shutil
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
    
    # Fetch Read
    print("Fetching Read list...")
    parse_and_sync(UserScraper.books_read(USERNAME, TOKEN), "read")
    # Fetch Currently Reading
    print("Fetching Currently Reading list...")
    parse_and_sync(UserScraper.currently_reading(USERNAME, TOKEN), "currently-reading")
    # Fetch To Read
    print("Fetching To Read list...")
    parse_and_sync(UserScraper.to_read(USERNAME, TOKEN), "to-read")
    print("\nSync Complete!")

if __name__ == "__main__":
    sync_all()
