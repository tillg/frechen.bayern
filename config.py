"""
Configuration for frechen.bayern website
"""

from design_variables import (
    BRAND_COLORS,
    BACKGROUND_COLORS,
    TEXT_COLORS,
    BORDER_COLORS,
    FONT_SIZES,
    FONT_WEIGHTS,
    SPACING,
    ICON_SIZES,
    LOGO_SIZES,
    BORDER_RADIUS,
    SHADOWS,
    BUTTON_STYLES,
    FEATURE_CARD_STYLES,
    GRADIENTS,
    get_tailwind_config,
)

# Site metadata
SITE_NAME = "Frechenlehen"
#SITE_TAGLINE = "Unser Haus in den Bergen"
#SITE_DESCRIPTION = "Ein Haus in der Nähe von Berchtesgaden/Bischofswiesen"
DOMAIN = "frechen.bayern"

# Directories
CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"
STATIC_DIR = "static"
OUTPUT_DIR = "docs"

# Contact
CONTACT_EMAIL = "till.gartner@gmail.com"

# Google Analytics (add later)
GOOGLE_ANALYTICS_ID = ""
ENABLE_ANALYTICS = False

# Navigation items
NAV_ITEMS = [
    {"label": "Home", "url": "/"},
	{"label": "Fotos","url": "/fotos"}
]

# Footer navigation
FOOTER_NAV_ITEMS = [
    {"label": "Home", "url": "/"},
]

# Logo filename (in /static/images/)
LOGO_FILE = "logo.png"

# Custom styles - white background theme
STYLES = {
    'body': 'bg-white text-gray-900',
    'nav_bg': 'bg-white',
    'nav_link': 'text-gray-600 hover:text-gray-900 transition-colors',
    'nav_brand': 'text-xl font-bold text-gray-900 hover:text-blue-600 transition-colors',
    'mobile_menu_btn': 'text-gray-600 hover:text-gray-900 focus:outline-none',
    'mobile_menu_bg': 'bg-gray-50 border-t',
    'mobile_menu_link': 'block px-3 py-2 text-gray-600 hover:text-gray-900 rounded transition-colors',
    'footer_bg': 'bg-gray-100 border-t mt-20',
    'footer_heading': 'text-sm font-semibold text-gray-700 uppercase tracking-wider mb-4',
    'footer_link': 'text-gray-600 hover:text-gray-900 transition-colors',
    'footer_text': 'text-gray-600',
    'footer_tagline': 'text-gray-600 text-sm',
    'footer_copyright': 'text-gray-500 text-sm',
    'hero_tagline': 'text-2xl md:text-3xl text-gray-600 mb-8',
    'hero_description': 'text-lg text-gray-500 max-w-3xl mx-auto mb-12',
    'feature_card': 'bg-white border border-gray-200 rounded-lg p-8 transition-colors',
    'feature_title': 'text-xl font-semibold mb-3 text-gray-900',
    'feature_description': 'text-gray-600',
    'contact_description': 'text-lg text-gray-600 mb-8',
    'page_description': 'text-xl text-gray-500',
}
