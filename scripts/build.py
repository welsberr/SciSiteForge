#!/usr/bin/env python3
"""
Static site generator for evo-edu framework.

Two modes:
1. --init : Prompt user for site config and save to site.json
2. --config <file> --output <dir> : Render templates using config
"""

import os
import json
import argparse
from pathlib import Path
import shutil

# Template directory (relative to this script)
TEMPLATE_DIR = Path(__file__).parent / "templates"

def prompt_for_config():
    """Prompt user for site configuration."""
    print("=== evo-edu Framework Site Config ===")
    config = {
        "lang": input("Language code (e.g., 'en'): ") or "en",
        "title": input("Page title (e.g., 'Notebook On Evolution'): ") or "Notebook On Evolution",
        "site_title": input("Site name (e.g., 'evo-edu.org'): ") or "evo-edu.org",
        "license": input("License text (e.g., 'CC BY-SA 4.0'): ") or "CC BY-SA 4.0",
        "github_url": input("GitHub URL: ") or "https://github.com/evo-edu",
        "contact_email": input("Contact email: ") or "admin@evo-edu.org",
        "languages": []
    }
    
    # Language options
    print("\nLanguage switcher options (e.g., en:English, es:Español):")
    lang_input = input("Enter as 'code:name' pairs (comma-separated): ") or "en:English"
    for pair in lang_input.split(','):
        code, name = pair.strip().split(':', 1)
        config["languages"].append({"code": code, "name": name})
    lang_options = "\n".join([
        f'<option value="{lang["code"]}" {"selected" if lang["code"] == config["lang"] else ""}>{lang["name"]}</option>'
        for lang in config["languages"]
    ])
    result = result.replace("{{language_options}}", lang_options)    
    # Save
    out_file = input("\nSave config as (default: site.json): ") or "site.json"
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    print(f"✅ Config saved to {out_file}")

def render_template(template_text, config):
    """Replace {{key}} and {{#each}} blocks with config values."""
    result = template_text
    
    # Simple key replacements
    for key, value in config.items():
        if key != "languages":
            result = result.replace("{{" + key + "}}", str(value))
    
    # Handle {{#each languages}}...{{/each}}
    if "{{#each languages}}" in result:
        lang_block_start = result.find("{{#each languages}}")
        lang_block_end = result.find("{{/each}}", lang_block_start)
        if lang_block_end != -1:
            block = result[lang_block_start + len("{{#each languages}}"):lang_block_end]
            rendered_langs = []
            for lang in config.get("languages", []):
                lang_item = block
                lang_item = lang_item.replace("{{code}}", lang["code"])
                lang_item = lang_item.replace("{{name}}", lang["name"])
                # Handle {{#if (eq code ../lang)}}
                if f'{{{{lang}}}}' in result:
                    selected = 'selected' if lang["code"] == config.get("lang", "") else ''
                    lang_item = lang_item.replace("{{selected_attr}}", f'selected="{selected}"' if selected else '')
                else:
                    lang_item = lang_item.replace("{{selected_attr}}", "")
                rendered_langs.append(lang_item)
            result = result[:lang_block_start] + "".join(rendered_langs) + result[lang_block_end + len("{{/each}}"):]
    
    return result

def build_site(config_file, output_dir):
    """Render all templates using config."""
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    # Copy theme assets
    theme_src = Path(__file__).parent / "theme"
    for asset in ["style.css", "main.js"]:
        shutil.copy(theme_src / asset, out_path / asset)
    
    # Render base.html → index.html (example)
    with open(theme_src / "base.html", 'r', encoding='utf-8') as f:
        template = f.read()
    
    rendered = render_template(template, config)
    with open(out_path / "index.html", 'w', encoding='utf-8') as f:
        f.write(rendered)
    
    print(f"✅ Site built in {output_dir}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true", help="Create site config interactively")
    parser.add_argument("--config", help="Path to site.json")
    parser.add_argument("--output", help="Output directory for built site")
    args = parser.parse_args()
    
    if args.init:
        prompt_for_config()
    elif args.config and args.output:
        build_site(args.config, args.output)
    else:
        print("Usage:")
        print("  python build.py --init")
        print("  python build.py --config site.json --output ../content/en/")

if __name__ == "__main__":
    main()
