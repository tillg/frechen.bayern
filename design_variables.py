"""
Design variables for frechen.bayern - White theme
"""

# Brand colors - Taubenblau (RAL 5014), matching the Fensterläden/Fensterrahmen
# Decision 2026-08-08; sRGB approx of RAL 5014 is #606E8C. Screen hex only —
# calibrate against a real RAL 5014 sample at the object (wiki to-do).
BRAND_COLORS = {
    "orange": "#606E8C",   # Primary — RAL 5014 Taubenblau
    "yellow": "#7C88A3",   # Secondary — lighter Taubenblau tint
    "coral": "#9AA4BA",    # Accent — lightest Taubenblau tint
}

# Background colors - Light theme
BACKGROUND_COLORS = {
    "primary": "#ffffff",
    "secondary": "#f8fafc",
    "tertiary": "#f1f5f9",
}

# Text colors - Dark on light
TEXT_COLORS = {
    "primary": "#0f172a",
    "secondary": "#334155",
    "tertiary": "#64748b",
}

# Border colors
BORDER_COLORS = {
    "primary": "#e2e8f0",
    "secondary": "#cbd5e1",
}

# Font sizes
FONT_SIZES = {
    "xs": "0.75rem",
    "sm": "0.875rem",
    "base": "1rem",
    "lg": "1.125rem",
    "xl": "1.25rem",
    "2xl": "1.5rem",
    "3xl": "1.875rem",
    "4xl": "2.25rem",
    "5xl": "3rem",
}

# Font weights
FONT_WEIGHTS = {
    "normal": "400",
    "medium": "500",
    "semibold": "600",
    "bold": "700",
}

# Spacing
SPACING = {
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "2rem",
    "2xl": "3rem",
}

# Icon sizes
ICON_SIZES = {
    "sm": "1rem",
    "md": "1.5rem",
    "lg": "2rem",
    "xl": "3rem",
}

# Logo sizes
LOGO_SIZES = {
    "nav": "2.5rem",
    "hero": "8rem",
    "footer": "2rem",
}

# Border radius
BORDER_RADIUS = {
    "sm": "0.25rem",
    "md": "0.5rem",
    "lg": "0.75rem",
    "xl": "1rem",
    "full": "9999px",
}

# Shadows
SHADOWS = {
    "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
    "md": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
    "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1)",
}

# Button styles
BUTTON_STYLES = {
    "primary": {
        "bg": BRAND_COLORS["orange"],
        "text": "#ffffff",
        "hover_bg": BRAND_COLORS["yellow"],
    },
    "secondary": {
        "bg": BACKGROUND_COLORS["secondary"],
        "text": TEXT_COLORS["primary"],
        "hover_bg": BACKGROUND_COLORS["tertiary"],
    },
}

# Feature card styles
FEATURE_CARD_STYLES = {
    "bg": BACKGROUND_COLORS["primary"],
    "border": BORDER_COLORS["primary"],
    "icon_bg": BRAND_COLORS["orange"],
    "title": TEXT_COLORS["primary"],
    "description": TEXT_COLORS["secondary"],
}

# Gradients
GRADIENTS = {
    "brand": f"linear-gradient(to right, {BRAND_COLORS['orange']}, {BRAND_COLORS['yellow']})",
    "hero": f"linear-gradient(to bottom, {BACKGROUND_COLORS['primary']}, {BACKGROUND_COLORS['secondary']})",
}


def get_tailwind_config():
    """Return Tailwind config object for template."""
    return {
        "colors": BRAND_COLORS,
        "backgroundColor": BACKGROUND_COLORS,
        "textColor": TEXT_COLORS,
        "borderColor": BORDER_COLORS,
    }
