#!/usr/bin/env python3
"""
Static site generator for Jinja2/Markdown sites.

Supports both flat content structure (content/*.md) and directory-per-page
structure (content/pagename/pagename.md with co-located images).
"""

import argparse
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
import yaml
import markdown
from jinja2 import Environment, FileSystemLoader, ChoiceLoader
from defaults import DEFAULT_STYLES


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate static site from markdown content.')
    parser.add_argument('--content-path', type=str, help='Site directory containing config.py and content/')
    parser.add_argument('--target-path', type=str, help='Output directory (overrides config OUTPUT_DIR)')
    parser.add_argument('--set-date', type=str, help='Override current date (YYYY-MM-DD format)')
    return parser.parse_args()


def load_config(content_path=None):
    """Load config from the specified path or cwd."""
    if content_path:
        sys.path.insert(0, str(content_path))
    else:
        sys.path.insert(0, os.getcwd())

    # Force reimport if already loaded
    if 'config' in sys.modules:
        del sys.modules['config']

    import config
    return config


def get_generator_dir():
    """Get the directory where this generator script lives."""
    return Path(__file__).parent.resolve()


def parse_markdown_file(filepath):
    """Parse markdown file with YAML frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter and content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            markdown_content = parts[2].strip()
        else:
            frontmatter = {}
            markdown_content = content
    else:
        frontmatter = {}
        markdown_content = content

    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['extra', 'codehilite'])

    return frontmatter, html_content


def discover_content(content_dir):
    """
    Discover content files supporting both flat and directory structures.

    Returns list of tuples: (markdown_path, page_slug, asset_dir_or_none)
    """
    content_dir = Path(content_dir)
    pages = []

    # Check for flat structure: content/*.md
    for md_file in content_dir.glob('*.md'):
        slug = md_file.stem
        pages.append((md_file, slug, None))

    # Check for directory structure: content/pagename/pagename.md
    for subdir in content_dir.iterdir():
        if subdir.is_dir() and not subdir.name.startswith('.'):
            # Look for markdown file with same name as directory
            md_file = subdir / f"{subdir.name}.md"
            if md_file.exists():
                slug = subdir.name
                # Check if already found in flat structure
                if not any(p[1] == slug for p in pages):
                    pages.append((md_file, slug, subdir))
            else:
                # Also check for index.md in directory
                md_file = subdir / "index.md"
                if md_file.exists():
                    slug = subdir.name
                    if not any(p[1] == slug for p in pages):
                        pages.append((md_file, slug, subdir))

    return pages


def copy_page_assets(asset_dir, output_dir, page_slug):
    """Copy non-markdown assets from page directory to output."""
    if asset_dir is None:
        return

    asset_dir = Path(asset_dir)
    # For index page, assets go to root; otherwise to page directory
    if page_slug == 'index':
        dest_dir = Path(output_dir)
    else:
        dest_dir = Path(output_dir) / page_slug
        dest_dir.mkdir(parents=True, exist_ok=True)

    for asset in asset_dir.iterdir():
        if asset.is_file() and not asset.suffix == '.md':
            shutil.copy2(asset, dest_dir / asset.name)


def validate_landing_page(frontmatter, filepath):
    """Validate landing page frontmatter has all required fields."""
    errors = []

    # Check required top-level fields
    required_fields = ['tagline', 'hero_description', 'features', 'contact_section']
    for field in required_fields:
        if field not in frontmatter:
            errors.append(f"Missing required field: '{field}'")

    # Validate cta_buttons (optional, can be empty)
    if 'cta_buttons' in frontmatter and frontmatter['cta_buttons']:
        if not isinstance(frontmatter['cta_buttons'], list):
            errors.append("'cta_buttons' must be a list/array")
        else:
            for i, button in enumerate(frontmatter['cta_buttons']):
                button_required = ['label', 'url', 'color', 'icon']
                for field in button_required:
                    if field not in button:
                        errors.append(f"cta_buttons[{i}] missing required field: '{field}'")

    # Validate features
    if 'features' in frontmatter:
        if not isinstance(frontmatter['features'], list):
            errors.append("'features' must be a list/array")
        elif len(frontmatter['features']) == 0:
            errors.append("'features' array cannot be empty")
        else:
            for i, feature in enumerate(frontmatter['features']):
                feature_required = ['title', 'description', 'icon', 'color']
                for field in feature_required:
                    if field not in feature:
                        errors.append(f"features[{i}] missing required field: '{field}'")

    # Validate screenshots (optional, can be empty)
    if 'screenshots' in frontmatter and frontmatter['screenshots']:
        if not isinstance(frontmatter['screenshots'], list):
            errors.append("'screenshots' must be a list/array")
        else:
            for i, screenshot in enumerate(frontmatter['screenshots']):
                screenshot_required = ['image', 'alt']
                for field in screenshot_required:
                    if field not in screenshot:
                        errors.append(f"screenshots[{i}] missing required field: '{field}'")

    # Validate contact_section
    if 'contact_section' in frontmatter:
        if not isinstance(frontmatter['contact_section'], dict):
            errors.append("'contact_section' must be an object/dictionary")
        else:
            contact_required = ['title', 'description', 'email']
            for field in contact_required:
                if field not in frontmatter['contact_section']:
                    errors.append(f"contact_section missing required field: '{field}'")

    if errors:
        error_message = f"\n  Validation failed for {filepath}:\n"
        for error in errors:
            error_message += f"     {error}\n"
        raise ValueError(error_message)

    print(f"     Validation passed for landing page")


def generate_site(content_path=None, target_path=None, set_date=None):
    """Main site generation function.

    Args:
        content_path: Site directory containing config.py and content/ (default: cwd)
        target_path: Output directory (default: config.OUTPUT_DIR or 'docs')
        set_date: Override current date as 'YYYY-MM-DD' string (default: today)
    """
    # Load config from content_path
    config = load_config(content_path)
    base_path = Path(content_path) if content_path else Path.cwd()

    site_name = getattr(config, 'SITE_NAME', 'Site')
    print(f"  Generating {site_name} website...")

    # Setup paths - relative to content_path
    content_dir = base_path / getattr(config, 'CONTENT_DIR', 'content')
    static_dir = base_path / getattr(config, 'STATIC_DIR', 'static')

    # Output dir: use target_path if provided, else config value (relative to base_path)
    if target_path:
        output_dir = Path(target_path)
    else:
        output_dir = base_path / getattr(config, 'OUTPUT_DIR', 'docs')

    # Determine current year - use set_date if provided
    if set_date:
        current_year = datetime.strptime(set_date, '%Y-%m-%d').year
    else:
        current_year = datetime.now().year

    # Templates: site-first, generator-fallback
    generator_dir = get_generator_dir()
    generator_template_dir = generator_dir / 'templates'
    site_template_dir = base_path / 'templates'

    # Clean and create output directory
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize Jinja2 with ChoiceLoader: site templates first, then generator
    loaders = []
    if site_template_dir.exists():
        loaders.append(FileSystemLoader(site_template_dir))
    loaders.append(FileSystemLoader(generator_template_dir))
    env = Environment(loader=ChoiceLoader(loaders))

    # Build navigation from config
    nav_items = getattr(config, 'NAV_ITEMS', [])

    # Build footer navigation (falls back to nav_items if not specified)
    footer_nav_items = getattr(config, 'FOOTER_NAV_ITEMS', nav_items)

    # Merge styles: defaults + site overrides
    site_styles = getattr(config, 'STYLES', {})
    styles = {**DEFAULT_STYLES, **site_styles}

    # Add config to template context
    template_context = {
        'site': {
            'name': site_name,
            'tagline': getattr(config, 'SITE_TAGLINE', ''),
            'description': getattr(config, 'SITE_DESCRIPTION', ''),
            'domain': getattr(config, 'DOMAIN', ''),
            'logo_file': getattr(config, 'LOGO_FILE', 'logo.svg'),
        },
        'nav_items': nav_items,
        'footer_nav_items': footer_nav_items,
        'styles': styles,
        'contact_email': getattr(config, 'CONTACT_EMAIL', ''),
        'testflight_link': getattr(config, 'TESTFLIGHT_LINK', ''),
        'macos_download_link': getattr(config, 'MACOS_DOWNLOAD_LINK', ''),
        'google_analytics_id': getattr(config, 'GOOGLE_ANALYTICS_ID', ''),
        'enable_analytics': getattr(config, 'ENABLE_ANALYTICS', False),
        'current_year': current_year,
        # Design system variables
        'brand_colors': getattr(config, 'BRAND_COLORS', {}),
        'background_colors': getattr(config, 'BACKGROUND_COLORS', {}),
        'text_colors': getattr(config, 'TEXT_COLORS', {}),
        'border_colors': getattr(config, 'BORDER_COLORS', {}),
        'font_sizes': getattr(config, 'FONT_SIZES', {}),
        'font_weights': getattr(config, 'FONT_WEIGHTS', {}),
        'spacing': getattr(config, 'SPACING', {}),
        'icon_sizes': getattr(config, 'ICON_SIZES', {}),
        'logo_sizes': getattr(config, 'LOGO_SIZES', {}),
        'border_radius': getattr(config, 'BORDER_RADIUS', {}),
        'shadows': getattr(config, 'SHADOWS', {}),
        'button_styles': getattr(config, 'BUTTON_STYLES', {}),
        'feature_card_styles': getattr(config, 'FEATURE_CARD_STYLES', {}),
        'gradients': getattr(config, 'GRADIENTS', {}),
        'tailwind_config': getattr(config, 'get_tailwind_config', lambda: {})(),
    }

    # Discover and process content
    pages = discover_content(content_dir)
    print(f"   Found {len(pages)} content pages")

    for md_file, page_slug, asset_dir in pages:
        print(f"   Processing {md_file.name}...")
        frontmatter, html_content = parse_markdown_file(md_file)

        # Validate landing page (index) has required fields
        if page_slug == 'index' and frontmatter.get('template') == 'landing':
            validate_landing_page(frontmatter, md_file.name)

        # Determine output filename (clean URLs: /page/ instead of /page.html)
        if page_slug == 'index':
            output_file = output_dir / 'index.html'
        else:
            page_output_dir = output_dir / page_slug
            page_output_dir.mkdir(parents=True, exist_ok=True)
            output_file = page_output_dir / 'index.html'

        # Get template name from frontmatter or use default
        template_name = frontmatter.get('template', 'page.html')
        if not template_name.endswith('.html'):
            template_name = f'{template_name}.html'

        # Render template
        template = env.get_template(template_name)
        page_context = {
            **frontmatter,
            'content': html_content,
        }
        # Ensure title and description have defaults
        if 'title' not in page_context:
            page_context['title'] = site_name
        if 'description' not in page_context:
            page_context['description'] = getattr(config, 'SITE_DESCRIPTION', '')

        context = {
            **template_context,
            'page': page_context
        }

        rendered_html = template.render(**context)

        # Write output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rendered_html)

        print(f"     Generated {output_file}")

        # Copy page assets if directory structure
        copy_page_assets(asset_dir, output_dir, page_slug)

    # Copy static files
    print(f"   Copying static assets...")
    if static_dir.exists():
        static_output = output_dir / 'static'
        if static_output.exists():
            shutil.rmtree(static_output)
        shutil.copytree(static_dir, static_output)
        print(f"     Copied static files to {static_output}")

    # Generate CNAME file for GitHub Pages
    domain = getattr(config, 'DOMAIN', '')
    if domain:
        cname_file = output_dir / 'CNAME'
        with open(cname_file, 'w') as f:
            f.write(domain)
        print(f"   Generated CNAME file with domain: {domain}")

    print(f"\n  Site generation complete!")
    print(f"   Output directory: {output_dir.absolute()}")


if __name__ == '__main__':
    args = parse_args()
    generate_site(
        content_path=args.content_path,
        target_path=args.target_path,
        set_date=args.set_date
    )
