# SciSiteForge Scripts

## 🛠️ Build & Translate

This site framework supports offline multilingual translation using Llamafile.

### Prerequisites
- Download a multilingual GGUF model (e.g., `mistral-7b-instruct.Q5_K_M.gguf`)
- Install [Llamafile](https://github.com/Mozilla-Ocho/llamafile)
- Python 3 with `requests` and `beautifulsoup4`

### Steps
1. Launch Llamafile:
   ```bash
   ./mistral-7b-instruct.Q5_K_M.llamafile --port 8080
   ```
2. Run translation:
   ```bash
   python scripts/translate_site.py --langs es,fr
   ```
3. Commit translated content:
   ```bash
   git add es/ fr/
   ```

> Translated files are saved to `/es/`, `/fr/`, etc., and served alongside English content.
```

#### 📁 `example/content/scripts/glossary_es.json`  
→ Language-specific scientific term mappings

