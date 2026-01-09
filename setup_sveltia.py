#!/usr/bin/env python3
import json
import re
from pathlib import Path
from typing import Set, Dict, Any

# --- CONFIGURATION ---
# Ensure your source files are named exactly like this in the same folder
LANGUAGES = ['en', 'de', 'fr', 'it'] 
OUTPUT_DIR = Path('content')
ADMIN_DIR = Path('public/admin')
REPO_NAME = 'akina-health/dummy-sveltia' # <--- UPDATE THIS

def load_language_file(lang: str) -> Dict[str, Any] | None:
    source_file = Path(f"{lang}.json")
    if not source_file.exists():
        print(f"⚠️  Missing {source_file}, skipping.")
        return None
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error reading {source_file}: {e}")
        return None

def process_content_key(key: str, story: Dict[str, Any], lang: str, found_paths: Set[str]) -> None:
    # Key example: "portal/difficulty/exercise-review-difficulty/medium"
    parts = key.split('/')
    
    # Validation: We need at least a folder and a filename
    if len(parts) < 2:
        parts = ['misc'] + parts

    filename = f"{parts[-1]}.json" # "medium.json"
    
    # The folder path is everything EXCEPT the last part
    # "portal/difficulty/exercise-review-difficulty"
    relative_folder_path = "/".join(parts[:-1])
    
    # Track this path so we can make a menu item for it later
    if lang == 'en':
        found_paths.add(relative_folder_path)
    
    # Create the directory
    full_folder_path = OUTPUT_DIR / lang / relative_folder_path
    full_folder_path.mkdir(parents=True, exist_ok=True)
    
    # Write the file
    output_file = full_folder_path / filename
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(story, f, indent=2, ensure_ascii=False)

def generate_collection_config(relative_path: str) -> str:
    # 1. Create a clean Label: "Portal / Difficulty / Exercise Review"
    parts = relative_path.split('/')
    # Skip 'portal' in label if it's redundant, otherwise capitalize all
    formatted_parts = [p.replace('-', ' ').title() for p in parts]
    label = " / ".join(formatted_parts)
    
    # 2. Create a clean ID: "portal_difficulty_exercise_review"
    name = relative_path.replace('/', '_').replace('-', '_')

    # 3. Define the Fields based on your JSON structure
    # We use 'required: false' on everything to prevent errors if data is missing
    return f"""
  - name: "{name}"
    label: "📂 {label}"
    folder: "content/en/{relative_path}"
    create: true
    i18n: true
    path: "{{{{slug}}}}"
    extension: "json"
    format: "json"
    fields:
      - {{label: "ID", name: "id", widget: "number", required: false, i18n: false}}
      - {{label: "Full Slug", name: "full_slug", widget: "hidden", i18n: false}}
      
      - label: "Content"
        name: "content"
        widget: "object"
        i18n: true
        fields:
          # --- BASIC TEXT ---
          - {{label: "Text", name: "Text", widget: "string", required: false}}
          - {{label: "Title", name: "Title", widget: "string", required: false}}
          - {{label: "Sub Text", name: "SubText", widget: "markdown", required: false}}
          - {{label: "Main Text", name: "MainText", widget: "markdown", required: false}}
          - {{label: "Box Title", name: "BoxTitle", widget: "string", required: false}}
          - {{label: "Tooltip Text", name: "TooltipText", widget: "string", required: false}}
          - {{label: "Content Example", name: "ContentExample", widget: "string", required: false}}

          # --- COMPLEX OBJECTS (From your JSON) ---
          
          # PDF Handling
          - label: "PDF Attachment"
            name: "PDF"
            widget: "object"
            required: false
            fields:
              - {{label: "File", name: "filename", widget: "file", required: false}}
              - {{label: "Alt", name: "alt", widget: "string", required: false}}

          # Icon Handling
          - label: "Icon"
            name: "Icon"
            widget: "object"
            required: false
            fields:
              - {{label: "Image", name: "filename", widget: "image", required: false}}
              - {{label: "Name", name: "name", widget: "string", required: false}}

          # Links List
          - label: "Links"
            name: "Links"
            widget: "list"
            required: false
            fields:
              - {{label: "Title", name: "title", widget: "string"}}
              - {{label: "Subtitle", name: "subtitle", widget: "string"}}
              - label: "Link Target"
                name: "link"
                widget: "object"
                fields:
                  - {{label: "URL", name: "url", widget: "string"}}

          # Release Notes List
          - label: "Releases"
            name: "Releases"
            widget: "list"
            required: false
            fields:
              - {{label: "Version", name: "ReleaseTitle", widget: "string"}}
              - {{label: "Date", name: "ReleaseDate", widget: "datetime"}}
              - {{label: "Notes", name: "Content", widget: "markdown"}}

          # --- METADATA ---
          - {{label: "Component", name: "component", widget: "hidden"}}
"""

def generate_config_yml(found_paths: Set[str]) -> str:
    # Sort by depth (shorter paths first) or alphabetically
    sorted_paths = sorted(list(found_paths))
    
    collections_str = "".join(generate_collection_config(p) for p in sorted_paths)
    locales_str = ", ".join(LANGUAGES)
    
    return f"""
backend:
  name: github
  repo: {REPO_NAME}
  branch: main

i18n:
  structure: multiple_folders
  locales: [{locales_str}]
  default_locale: en

media_folder: "public/images"
public_folder: "/images"

# We disable the "Quick Search" globally to prevent lag with 1000s of files
search: false

collections:
{collections_str}
"""

def main():
    print("🚀 Starting Granular Setup...")
    
    # 1. Split Content & Find Folders
    found_paths: Set[str] = set()
    for lang in LANGUAGES:
        data = load_language_file(lang)
        if data:
            print(f"Processing {lang}...")
            for key, story in data.items():
                process_content_key(key, story, lang, found_paths)
    
    print(f"✅ Created {len(found_paths)} unique collections.")

    # 2. Generate Config
    print("⚙️  Generating config.yml...")
    ADMIN_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(ADMIN_DIR / 'config.yml', 'w', encoding='utf-8') as f:
        f.write(generate_config_yml(found_paths))
        
    # 3. Index HTML
    html = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sveltia CMS</title>
    <script src="https://unpkg.com/@sveltia/cms/dist/sveltia-cms.js"></script>
  </head>
  <body></body>
</html>"""
    with open(ADMIN_DIR / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("\n🎉 DONE! Run 'python3 -m http.server 8000'")

if __name__ == "__main__":
    main()