# frechen.bayern

The source of the website [frechen.bayern](https://frechen.bayern).

## Local Development

### Setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r generator/requirements.txt
```

### Run the dev server

With your virtual environment activated, run:

```bash
python generator/dev_server.py
```

This will:
1. Do an initial build
2. Start a local server at **http://localhost:8000**
3. Watch `content/`, `templates/`, `static/`, and config files for changes
4. Auto-rebuild when you edit any `.md`, `.html`, `.py`, `.css`, etc.

**Workflow:** Edit your markdown files → the site rebuilds automatically → refresh your browser to see changes.
