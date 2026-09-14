"""
Default style values for the static site generator.

Sites can override any of these in their config.py STYLES dict.
"""

DEFAULT_STYLES = {
    # Body
    'body': 'bg-black text-white',

    # Navigation
    'nav_bg': 'bg-black',
    'nav_link': 'text-gray-300 hover:text-white transition-colors',
    'nav_brand': 'text-xl font-bold text-white hover:text-brand-orange transition-colors',
    'mobile_menu_btn': 'text-gray-300 hover:text-white focus:outline-none',
    'mobile_menu_bg': 'border-t',
    'mobile_menu_link': 'block px-3 py-2 text-gray-300 hover:text-white rounded transition-colors',

    # Footer
    'footer_bg': 'border-t mt-20',
    'footer_heading': 'text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4',
    'footer_link': 'text-gray-400 hover:text-white transition-colors',
    'footer_text': 'text-gray-400',
    'footer_tagline': 'text-gray-400 text-sm',
    'footer_copyright': 'text-gray-400 text-sm',

    # Landing page - Hero
    'hero_tagline': 'text-2xl md:text-3xl text-gray-300 mb-8',
    'hero_description': 'text-lg text-gray-400 max-w-3xl mx-auto mb-12',
    'hero_cta_statement': 'text-lg text-gray-400 mt-4',

    # Landing page - Features
    'feature_card': 'bg-black border rounded-lg p-8 transition-colors',
    'feature_title': 'text-xl font-semibold mb-3',
    'feature_description': 'text-gray-400',

    # Landing page - Screenshots
    'screenshot_card': 'rounded-lg overflow-hidden',

    # Landing page - Testimonials
    'testimonial_card': 'bg-black border rounded-lg p-8 hover:border-brand-yellow transition-colors',
    'testimonial_title': 'text-xl font-semibold mb-4 text-brand-yellow',
    'testimonial_text': 'text-gray-300 mb-6 leading-relaxed',
    'testimonial_author': 'text-gray-500 font-medium',

    # Landing page - Contact section
    'contact_description': 'text-lg text-gray-400 mb-8',

    # Content page
    'page_description': 'text-xl text-gray-400',
    'prose_text': 'text-gray-300',
}
