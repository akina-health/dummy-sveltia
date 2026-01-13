#!/usr/bin/env python3
import json
import os
from pathlib import Path
from typing import Set, Dict, Any

# --- CONFIGURATION ---
LANGUAGES = ['en', 'de', 'fr', 'it']
OUTPUT_DIR = Path('content')
TINA_CONFIG_PATH = Path('tina/config.ts')
REPO_NAME = 'your-org/your-repo' 

# Map your field names to Tina types
# We use 'rich-text' for your markdown content, 'string' for simple text
FIELD_MAPPING = {
    "Text": "string",
    "Title": "string",
    "SubText": "rich-text", # Renders a Markdown editor
    "MainText": "rich-text",
    "Content": "rich-text",
    "BoxTitle": "string",
    "TooltipText": "string",
    "ContentExample": "string",
    "DisplayedName": "string",
    "PageTitle": "string"
}

def load_language_file(lang: str) -> Dict[str, Any] | None:
    source_file = Path(f"{lang}.json")
    if not source_file.exists():
        print(f"⚠️  Missing {source_file}, skipping.")
        return None
    with open(source_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def process_content(found_folders: Set[str]):
    print("🚀 Splitting content...")
    
    for lang in LANGUAGES:
        data = load_language_file(lang)
        if not data: continue
        
        print(f"   Processing {lang.upper()}...")
        for key, story in data.items():
            # Key: "portal/difficulty/easy"
            # Key: "portal/difficulty/easy" or "de/portal/difficulty/easy"
            parts = key.split('/')
            
            # Remove lang prefix if present (e.g. "de/portal" -> "portal")
            if parts[0] == lang:
                parts = parts[1:]

            if len(parts) < 2: parts = ['misc'] + parts
            
            filename = f"{parts[-1]}.json"
            # Folder: content/en/portal/difficulty
            relative_folder = "/".join(parts[:-1])
            full_folder = OUTPUT_DIR / lang / relative_folder
            
            # Create folder
            full_folder.mkdir(parents=True, exist_ok=True)
            
            # Save File
            with open(full_folder / filename, 'w', encoding='utf-8') as f:
                json.dump(story, f, indent=2, ensure_ascii=False)
            
            # Track distinct root folders (e.g. "portal") instead of every subfolder
            # to prevent having 300+ collections which crashes Tina
            root_folder = parts[0]
            if lang == 'en':
                found_folders.add(root_folder)

def generate_tina_config(found_folders: Set[str]):
    print("⚙️  Generating tina/config.ts...")
    
    # We create a collection for every folder found
    collections_ts = ""
    
    for folder in sorted(list(found_folders)):
        # folder: "portal/difficulty"
        # Collection Name: "en_portal_difficulty" (Must be unique per lang)
        # Label: "Portal / Difficulty"
        
        label_parts = [p.title() for p in folder.split('/')]
        human_label = " / ".join(label_parts)
        safe_name = folder.replace('/', '_').replace('-', '_')
        
        # We define ONE collection per language for this folder
        # This gives you "EN Portal Difficulty", "DE Portal Difficulty" in the sidebar
        for lang in LANGUAGES:
            lang_label = f"[{lang.upper()}] {human_label}"
            lang_name = f"{lang}_{safe_name}"
            path = f"content/{lang}/{folder}"
            
            collections_ts += f"""
      {{
        name: "{lang_name}",
        label: "{lang_label}",
        path: "{path}",
        format: "json",
        ui: {{
          // Don't let editors create new files if you want strict sync with code
          allowedActions: {{ create: true, delete: true }},
        }},
        fields: [
          {{
            type: "string",
            name: "full_slug",
            label: "Slug",
            ui: {{ component: "hidden" }}
          }},
          {{
            type: "object",
            name: "content",
            label: "Content Data",
            fields: [
              // --- Generated Fields based on your App ---
              {{
                 type: "string",
                 name: "Text",
                 label: "Text",
                 ui: {{ component: "textarea" }} 
              }},
              {{
                 type: "string",
                 name: "Title",
                 label: "Title"
              }},
              {{
                 type: "rich-text",
                 name: "SubText",
                 label: "Sub Text (Markdown)"
              }},
              {{
                 type: "rich-text",
                 name: "MainText",
                 label: "Main Text (Markdown)"
              }},
              {{
                 type: "string",
                 name: "BoxTitle",
                 label: "Box Title"
              }},
              {{
                 type: "string",
                 name: "TooltipText",
                 label: "Tooltip Text"
              }},
              {{
                 type: "string",
                 name: "ContentExample",
                 label: "Content Example"
              }},
              // --- COMPLEX OBJECTS ---
              {{
                type: "object",
                name: "PDF",
                label: "PDF Attachment",
                fields: [
                  {{ type: "image", name: "filename", label: "File" }},
                  {{ type: "string", name: "alt", label: "Alt Text" }}
                ]
              }},
              {{
                type: "object",
                name: "Icon",
                label: "Icon",
                fields: [
                  {{ type: "image", name: "filename", label: "Image" }},
                  {{ type: "string", name: "name", label: "Name" }}
                ]
              }},
              {{
                type: "object",
                list: true,
                name: "Links",
                label: "Links",
                ui: {{ itemProps: (item) => ({{ label: item?.title }}) }},
                fields: [
                  {{ type: "string", name: "title", label: "Title" }},
                  {{ type: "string", name: "subtitle", label: "Subtitle" }},
                  {{ 
                    type: "object", 
                    name: "link", 
                    label: "Link Target",
                    fields: [{{ type: "string", name: "url", label: "URL" }}]
                  }}
                ]
              }},
              {{
                type: "object",
                list: true,
                name: "Releases",
                label: "Releases",
                ui: {{ itemProps: (item) => ({{ label: item?.ReleaseTitle }}) }},
                fields: [
                  {{ type: "string", name: "ReleaseTitle", label: "Version" }},
                  {{ type: "datetime", name: "ReleaseDate", label: "Date" }},
                  {{ type: "string", name: "Content", label: "Notes", ui: {{ component: "textarea" }} }}
                ]
              }},
              // Add a generic 'catch-all' for other fields if needed, 
              // or define them explicitly here like Sveltia.
              {{
                 type: "string",
                 name: "component",
                 label: "Component Type",
                 ui: {{ component: "hidden" }}
              }}
            ]
          }}
        ]
      }},
"""

    config_content = f"""
import {{ defineConfig }} from "tinacms";

export default defineConfig({{
  branch: "main",
  clientId: process.env.NEXT_PUBLIC_TINA_CLIENT_ID,
  token: process.env.TINA_TOKEN,
  build: {{
    outputFolder: "admin",
    publicFolder: "public",
  }},
  media: {{
    tina: {{
      mediaRoot: "images",
      publicFolder: "public",
    }},
  }},
  schema: {{
    collections: [
      {collections_ts}
    ],
  }},
}});
"""
    
    with open(TINA_CONFIG_PATH, 'w', encoding='utf-8') as f:
        f.write(config_content)

def main():
    found_folders = set()
    process_content(found_folders)
    generate_tina_config(found_folders)
    print("✅ Done! Run 'npx tinacms dev' to start.")

if __name__ == "__main__":
    main()