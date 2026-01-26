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
SITE_NAME = "Frechen Bayern"
SITE_TAGLINE = "Unser Haus in den Bergen"
SITE_DESCRIPTION = "Ein Haus in der Nähe von Berchtesgaden/Bischofswiesen"
DOMAIN = "frechen.bayern"

# Directories
CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"
STATIC_DIR = "static"
OUTPUT_DIR = "docs"

# Contact
CONTACT_EMAIL = "till.gartner@gmail.com"

# App Links (not used for this site)
TESTFLIGHT_LINK = ""
MACOS_DOWNLOAD_LINK = ""

# Google Analytics (add later)
GOOGLE_ANALYTICS_ID = ""
ENABLE_ANALYTICS = False

# Navigation items
NAV_ITEMS = [
    {"label": "Home", "url": "/"},
]

# Footer navigation
FOOTER_NAV_ITEMS = [
    {"label": "Home", "url": "/"},
]

# Logo filename
LOGO_PNG = "logo.png"
