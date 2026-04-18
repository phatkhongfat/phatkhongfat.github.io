import pandas as pd
import os
import requests
import shutil

# 1. Load your export
df = pd.read_csv('book.csv')

# 2. Base directory
base_path = 'content/bookshelf'
os.makedirs(base_path, exist_ok=True)

for index, row in df.iterrows():
    title = str(row['Title'])
    author = str(row['Authors'])
    status = str(row['Read Status']).lower().replace(' ', '-')
    rating = row['Star Rating'] if pd.notnull(row['Star Rating']) else 0
    isbn = str(row['ISBN/UID']).split('.')[0] if pd.notnull(row['ISBN/UID']) else ""
    
    # Create folder name
    folder_name = "".join([c for c in title if c.isalnum() or c==' ']).rstrip().replace(' ', '-').lower()
    folder_path = os.path.join(base_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    # Download the Image automatically
    if isbn:
        image_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
        img_data = requests.get(image_url).content
        with open(os.path.join(folder_path, "feature.jpg"), 'wb') as handler:
            handler.write(img_data)
            print(f"Downloaded cover for: {title}")

    # Create the index.md
    content = f"""---
title: "{title}"
author: "{author}"
date: {pd.to_datetime('today').strftime('%Y-%m-%d')}
feature: "feature.jpg"
thumbnail: "feature.jpg"
status: "{status}"
rating: {rating}
isbn: "{isbn}"
---

{row['Review'] if pd.notnull(row['Review']) else "No reflection yet."}
"""
    
    with open(os.path.join(folder_path, "index.md"), 'w', encoding='utf-8') as f:
        f.write(content)

print("\nFinished! Your library is now local, with images downloaded.")
