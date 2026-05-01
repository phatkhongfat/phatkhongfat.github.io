import pandas as pd
import os
import requests
import random

# 1. Load your StoryGraph export
csv_file = 'book.csv'
if not os.path.exists(csv_file):
    print(f"Error: {csv_file} not found. Please export your StoryGraph library.")
    exit(1)

df = pd.read_csv(csv_file)

# Shuffle books for true randomness in piles
df = df.sample(frac=1).reset_index(drop=True)

# 2. Base directory
base_path = 'content/bookshelf'
os.makedirs(base_path, exist_ok=True)

# Spine colors (Gothic Collector palette)
colors = ["#1B1A17", "#461111", "#0F3D3E", "#100720", "#313131", "#541212", "#2D4263", "#191919", "#3E432E", "#2C3333"]

# Randomized Shelf Logic (All Vertical)
processed_books = []
for index, row in df.iterrows():
    processed_books.append(row)

for row in processed_books:
    title = str(row['Title']).replace('"', '\\"')
    # ... (rest of normalization logic)
    author = str(row['Authors'])
    status = str(row['Read Status']).lower().replace(' ', '-')
    rating = row['Star Rating'] if pd.notnull(row['Star Rating']) else 0
    isbn = str(row['ISBN/UID']).split('.')[0] if pd.notnull(row['ISBN/UID']) else ""
    
    folder_name = "".join([c for c in title if c.isalnum() or c==' ']).rstrip().replace(' ', '-').lower()
    if not folder_name: continue
    
    folder_path = os.path.join(base_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    sg_url = f"https://app.thestorygraph.com/browse?search_term={isbn}" if isbn else "https://app.thestorygraph.com"

    # Download Image logic...
    feature_img = os.path.join(folder_path, "feature.jpg")
    if isbn and not os.path.exists(feature_img):
        try:
            image_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
            r = requests.get(image_url, timeout=10)
            if r.status_code == 200 and len(r.content) > 1000:
                with open(feature_img, 'wb') as h: h.write(r.content)
        except: pass

    content = f"""---
title: "{title}"
author: "{author}"
date: {pd.to_datetime('today').strftime('%Y-%m-%d')}
feature: "feature.jpg"
thumbnail: "feature.jpg"
status: "{status}"
rating: {rating}
isbn: "{isbn}"
storygraph_url: "{sg_url}"
spine_color: "{random.choice(colors)}"
---

{row['Review'] if pd.notnull(row['Review']) else "No reflection yet."}
"""
    with open(os.path.join(folder_path, "index.md"), 'w', encoding='utf-8') as f:
        f.write(content)

print(f"\nFinished! Processed {len(df)} books into a clean vertical shelf.")
