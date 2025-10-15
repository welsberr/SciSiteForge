#!/usr/bin/env python3
"""
Offline multilingual translation for evo-edu.org using Llamafile.
Requires: BeautifulSoup4, requests
Install with: pip install beautifulsoup4 requests
"""

import os
import json
import argparse
import time
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import requests

# --- Configuration ---
MODEL_API_URL = "http://localhost:8080/completion"
LANGUAGES = {
    "es": "Spanish",
    "fr": "French",
    "pt": "Portuguese",
    "de": "German"
}

def translate_text(text, target_lang_name, glossary=None):
    """Translate a block of text using Llamafile."""
    if not text.strip():
        return text

    glossary_text = ""
    if glossary:
        glossary_text = "Use these translations:\n" + "\n".join(f"'{k}' â†’ '{v}'" for k, v in glossary.items()) + "\n\n"

    prompt = f"""You are a scientific translator. Translate the following English text into {target_lang_name}.
Preserve technical terms like "genetic drift" or "natural selection" unless a standard translation exists.
Maintain paragraph structure. Do not add commentary.

{glossary_text}Text:
"{text}"

Translation:"""

    try:
        response = requests.post(MODEL_API_URL, json={
            "prompt": prompt,
            "temperature": 0.1,
            "stop": ["\n\n", "Text:", "Translation:"],
            "n_predict": 1024
        }, timeout=120)
        response.raise_for_status()
        result = response.json()["content"].strip()
        return result
    except Exception as e:
        print(f"  âš ï¸ Translation failed: {e}")
        return text  # fallback to original

def extract_translatable_text(soup):
    """Extract text nodes for translation, preserving structure."""
    texts = []
    for elem in soup.descendants:
        if isinstance(elem, NavigableString) and elem.parent.name not in ['script', 'style']:
            if elem.strip():
                texts.append(elem)
    return texts

def translate_html_file(src_path, dest_path, target_lang_code):
    """Translate an HTML file."""
    print(f"Translating {src_path} â†’ {dest_path}")
    with open(src_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    text_nodes = extract_translatable_text(soup)

    # Optional: load glossary for this language
    glossary = {}
    glossary_path = Path(__file__).parent / f"glossary_{target_lang_code}.json"
    if glossary_path.exists():
        with open(glossary_path, 'r') as f:
            glossary = json.load(f)

    # Translate each text node
    for node in text_nodes:
        original = str(node)
        translated = translate_text(original, LANGUAGES[target_lang_code], glossary)
        node.replace_with(translated)
        time.sleep(0.1)  # be gentle on CPU

    # Save translated HTML
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--langs", required=True, help="Comma-separated language codes (e.g., es,fr)")
    parser.add_argument("--src", default="content/en", help="Source directory (English)")
    parser.add_argument("--dest", default="content", help="Base destination directory")
    args = parser.parse_args()

    lang_codes = args.langs.split(',')
    src_base = Path(args.src)
    dest_base = Path(args.dest)

    for lang_code in lang_codes:
        if lang_code not in LANGUAGES:
            print(f"Unsupported language: {lang_code}")
            continue

        print(f"\n=== Translating to {LANGUAGES[lang_code]} ({lang_code}) ===")
        for html_file in src_base.rglob("*.html"):
            rel_path = html_file.relative_to(src_base)
            dest_file = dest_base / lang_code / rel_path
            translate_html_file(html_file, dest_file, lang_code)

    print("\nâœ… Translation complete.")

if __name__ == "__main__":
    main()
