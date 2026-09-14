# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static website generator for https://frechen.bayern - a site about a house in the mountains near Berchtesgaden/Bischofswiesen. This is a sister project to `summa_site`, sharing the same build architecture but with a white theme (vs dark).

## Architecture

- **Technology:** Python 3.13+, Jinja2 templates, Markdown content, Tailwind CSS
- **Content:** Markdown files with YAML frontmatter in `content/`
- **Templates:** Jinja2 HTML templates in `templates/`
- **Output:** Static HTML generated to `docs/` (GitHub Pages deployment)
- **Site Generator:** `generator/` - vendored static site generator (originally from `tillg/tills-static-site-generator`, pinned at commit `234a7a6`)

## Build Commands

```bash
# Development server with auto-rebuild (watches for changes)
python generator/dev_server.py

# Manual build only
python generator/generate_site.py

# Preview static output (without auto-rebuild)
cd docs && python3 -m http.server 8000
```

## Custom Slash Commands

- `/spec-build-out` - Build out a draft idea into a specification (iterate on architecture, UI options, pros/cons)
- `/spec-iterate` - Process feedback marked with "->" and consolidate into coherent spec
- `/spec-finish` - Review and finalize spec after implementation

## Key Design Decisions

- White background theme (different from summa_site's dark theme)
- Goal is one shared codebase for static site generation with separate content repos
- Deployed via GitHub Pages from `/docs` folder
