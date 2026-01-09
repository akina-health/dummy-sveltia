import os
import json
import uuid
import random

# --- CONFIGURATION ---
FILE_COUNT = 1500
CONTENT_DIR = "content/snippets"
ADMIN_DIR = "public/admin"

# Ensure directories exist
os.makedirs(CONTENT_DIR, exist_ok=True)
os.makedirs(ADMIN_DIR, exist_ok=True)

print(f"🚀 Generating {FILE_COUNT} dummy files...")

# 1. GENERATE 1,500 JSON FILES
for i in range(FILE_COUNT):
    file_id = str(uuid.uuid4())
    filename = f"{CONTENT_DIR}/{file_id}.json"
    
    data = {
        "title": f"Test Story #{i} - {file_id[:8]}",
        "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10,
        "author": random.choice(["Alice", "Bob", "Charlie"]),
        "draft": random.choice([True, False])
    }
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

print("✅ Content generated.")

# 2. CREATE SVELTIA CONFIG (config.yml)
config_content = f"""
backend:
  name: github
  repo: YOUR_GITHUB_USERNAME/sveltia-load-test # <--- CHANGE THIS LATER IF NEEDED
  branch: main

media_folder: "public/images"
public_folder: "/images"

collections:
  - name: "snippets"
    label: "Text Snippets"
    folder: "{CONTENT_DIR}"
    create: true
    slug: "{{slug}}"
    format: "json"
    extension: "json"
    fields:
      - {{label: "Title", name: "title", widget: "string"}}
      - {{label: "Body", name: "body", widget: "markdown"}}
      - {{label: "Author", name: "author", widget: "select", options: ["Alice", "Bob", "Charlie"]}}
      - {{label: "Draft", name: "draft", widget: "boolean"}}
"""

with open(f"{ADMIN_DIR}/config.yml", "w") as f:
    f.write(config_content)

print("✅ Config generated.")

# 3. CREATE SVELTIA APP (index.html)
html_content = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Load Test CMS</title>
    <script src="https://unpkg.com/@sveltia/cms/dist/sveltia-cms.js"></script>
  </head>
  <body></body>
</html>
"""

with open(f"{ADMIN_DIR}/index.html", "w") as f:
    f.write(html_content)

print("✅ Admin UI generated.")
print("🎉 DONE! Run 'python3 -m http.server 8000' to test locally, or push to GitHub.")