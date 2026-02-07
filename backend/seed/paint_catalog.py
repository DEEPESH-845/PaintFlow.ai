from __future__ import annotations
"""
Paint product catalog: 5 products, 60 shades across 6 families, 240 SKUs.
All hex colors are real and visually accurate.
"""

PRODUCTS = [
    {
        "name": "Royale Luxury Emulsion",
        "category": "Interior Wall",
        "sub_category": "Luxury",
        "base_type": "Water-based",
        "finish": "Soft Sheen",
        "sizes_available": '["1L","4L","10L","20L"]',
        "price_per_litre": 520.0,
    },
    {
        "name": "Tractor Emulsion",
        "category": "Interior Wall",
        "sub_category": "Economy",
        "base_type": "Water-based",
        "finish": "Matt",
        "sizes_available": '["1L","4L","10L","20L"]',
        "price_per_litre": 180.0,
    },
    {
        "name": "Apex Weathercoat",
        "category": "Exterior Wall",
        "sub_category": "Premium",
        "base_type": "Water-based",
        "finish": "Matt",
        "sizes_available": '["1L","4L","10L","20L"]',
        "price_per_litre": 380.0,
    },
    {
        "name": "Apcolite Enamel",
        "category": "Wood & Metal",
        "sub_category": "Premium",
        "base_type": "Oil-based",
        "finish": "High Gloss",
        "sizes_available": '["1L","4L","10L","20L"]',
        "price_per_litre": 420.0,
    },
    {
        "name": "DampGuard Waterproofing",
        "category": "Waterproofing",
        "sub_category": "Premium",
        "base_type": "Water-based",
        "finish": "Matt",
        "sizes_available": '["1L","4L","10L","20L"]',
        "price_per_litre": 350.0,
    },
]

# 10 shades per family, 6 families = 60 shades
# Each shade: (name, hex_color, product_index, is_trending)
SHADES = {
    "Reds": [
        ("Bridal Red", "#C41E3A", 0, True),       # HERO PRODUCT
        ("Venetian Rose", "#CC5577", 0, False),
        ("Crimson Glory", "#DC143C", 0, False),
        ("Terracotta Dream", "#E2725B", 2, True),
        ("Coral Sunset", "#FF7F50", 0, False),
        ("Burnt Sienna", "#E97451", 2, False),
        ("Ruby Wine", "#9B111E", 3, False),
        ("Warm Blush", "#DE5D83", 0, True),
        ("Dusty Rose", "#DCAE96", 0, False),
        ("Cherry Blossom", "#FFB7C5", 0, False),
    ],
    "Blues": [
        ("Pacific Breeze", "#4F97A3", 0, True),
        ("Midnight Ocean", "#191970", 0, False),
        ("Sky Serenity", "#87CEEB", 0, False),
        ("Coastal Blue", "#5B9BD5", 2, False),
        ("Navy Admiral", "#000080", 3, False),
        ("Powder Blue", "#B0E0E6", 0, True),
        ("Indigo Night", "#4B0082", 0, False),
        ("Aegean Teal", "#367588", 2, False),
        ("Arctic Ice", "#D6ECEF", 0, False),
        ("Cobalt Dream", "#0047AB", 3, False),
    ],
    "Greens": [
        ("Olive Garden", "#6B8E23", 2, False),
        ("Forest Canopy", "#228B22", 2, True),
        ("Sage Whisper", "#B2AC88", 0, False),
        ("Emerald Isle", "#50C878", 0, False),
        ("Mint Fresh", "#98FF98", 0, True),
        ("Jade Harmony", "#00A86B", 0, False),
        ("Eucalyptus", "#44D7A8", 2, False),
        ("Moss Green", "#8A9A5B", 2, False),
        ("Lime Zest", "#C7EA46", 0, False),
        ("Fern Valley", "#4F7942", 2, False),
    ],
    "Yellows": [
        ("Sunrise Yellow", "#FFD700", 0, True),    # Demo shade for Snap & Find
        ("Golden Maize", "#E4A010", 0, False),
        ("Honey Glow", "#EB9605", 0, False),
        ("Buttercream", "#F9E4B7", 0, False),
        ("Lemon Chiffon", "#FFFACD", 0, False),
        ("Amber Warmth", "#FFBF00", 3, False),
        ("Sunflower", "#FFDA03", 0, True),
        ("Tuscan Sun", "#FAD6A5", 0, False),
        ("Saffron Spice", "#F4C430", 0, False),
        ("Mustard Field", "#FFDB58", 2, False),
    ],
    "Neutrals": [
        ("Warm Taupe", "#B5A189", 0, False),
        ("Espresso Brown", "#3C1414", 3, False),
        ("Smoky Grey", "#848482", 0, False),
        ("Charcoal Depth", "#36454F", 2, False),
        ("Desert Sand", "#EDC9AF", 0, True),
        ("Mocha Latte", "#967969", 0, False),
        ("Slate Stone", "#708090", 2, False),
        ("Beige Comfort", "#F5F5DC", 0, False),
        ("Graphite", "#383838", 3, False),
        ("Monsoon Shield", "#7B8B6F", 4, False),  # Waterproofing - Mumbai Rain hero
    ],
    "Whites": [
        ("Pure White", "#FFFFFF", 0, False),
        ("Ivory Dream", "#FFFFF0", 0, True),
        ("Pearl Glow", "#F0EAD6", 0, False),
        ("Snow Mist", "#FFFAFA", 0, False),
        ("Antique White", "#FAEBD7", 0, False),
        ("Moonlight", "#F8F8FF", 0, False),
        ("Vanilla Cream", "#F3E5AB", 0, False),
        ("Shell White", "#FFF5EE", 0, False),
        ("Cotton Cloud", "#F0F0F0", 0, False),
        ("Porcelain", "#F0EBE3", 0, False),
    ],
}

SIZE_MULTIPLIERS = {
    "1L": {"cost_mult": 1.0, "mrp_mult": 1.0},
    "4L": {"cost_mult": 3.6, "mrp_mult": 3.6},
    "10L": {"cost_mult": 8.5, "mrp_mult": 8.5},
    "20L": {"cost_mult": 16.0, "mrp_mult": 16.0},
}


def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)


def get_shade_code(family: str, index: int) -> str:
    family_codes = {
        "Reds": "RD", "Blues": "BL", "Greens": "GR",
        "Yellows": "YL", "Neutrals": "NT", "Whites": "WH",
    }
    return f"AP-{family_codes[family]}{index + 1:02d}"


def get_sku_code(product_name: str, shade_code: str, size: str) -> str:
    product_codes = {
        "Royale Luxury Emulsion": "RLE",
        "Tractor Emulsion": "TRE",
        "Apex Weathercoat": "AWC",
        "Apcolite Enamel": "AEN",
        "DampGuard Waterproofing": "DGW",
    }
    pcode = product_codes.get(product_name, "XXX")
    return f"PF-{pcode}-{shade_code}-{size}"
