# Setup Site

Build a static site for frechen.bayern, reusing the generator from summa_site. White theme, content about our house near Berchtesgaden/Bischofswiesen.

## Architecture

**Repositories:**

| Repo | Purpose |
| ---- | ------- |
| `tillg/tills-static-site-generator` | Generator code + templates (public) |
| `tillg/frechen.bayern` | Content + config + generated `docs/` |
| `tillg/summarum.app` | Content + config + generated `docs/` |

Templates live in the generator repo (shared across sites). Site-specific config (`config.py`, `design_variables.py`) lives in each site repo, following the existing summa_site structure.

**GitHub Action workflow:**

1. Checkout self (content + config)
2. Checkout generator into `./generator/`
3. Run `python generator/generate_site.py`
4. Commit `docs/` changes

**Local development:**

```bash
python ../tills-static-site-generator/dev_server.py
```

## Content Structure

One subdirectory per page, so images can live alongside the markdown:

```text
content/
  index/
    index.md
    hero-image.jpg
  about/
    about.md
    photo.jpg
```

Hero image path is specified in the markdown frontmatter.

**Note:** summa_site currently uses a flat structure (`content/*.md`). The generator must be modified to support both patterns.

## Decisions

* **Templates:** Shared in generator repo
* **Config:** Same schema as summa_site (`config.py` + `design_variables.py`)
* **Dependencies:** Generator includes `requirements.txt` (jinja2, markdown, pyyaml, watchdog)
* **Regression testing:** HTML diff of summarum.app output vs current summa_site, manually validated
* **Analytics:** Add to frechen.bayern later
* **Icon generation:** Not needed for frechen.bayern

## White Theme (Starting Point)

```python
BACKGROUND_COLORS = {
    "primary": "#ffffff",
    "secondary": "#f8f9fa",
    "tertiary": "#e9ecef",
}

TEXT_COLORS = {
    "primary": "#212529",
    "secondary": "#495057",
    "muted": "#6c757d",
}

BRAND_COLORS = {
    "primary": "#2563eb",  # Blue accent
    "secondary": "#3b82f6",
}
```

## Implementation Plan

1. **Create `tills-static-site-generator` repo**
   * Extract `generate_site.py`, `dev_server.py`, templates, `requirements.txt` from summa_site
   * Modify generator to support directory-per-page content structure
   * Modify `landing.html` to read hero image from frontmatter

2. **Create `summarum.app` repo**
   * Move content from summa_site
   * Add `config.py` and `design_variables.py` (copied from summa_site)
   * Set up GitHub Action
   * HTML diff output vs current summa_site — validate manually

3. **Create `frechen.bayern` repo**
   * Add minimal content (one landing page using directory structure)
   * Add `config.py` with white theme
   * Set up GitHub Action
