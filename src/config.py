"""
Nassau Candy Logistics Analytics - Configuration and Constants
Contains geographical coordinates, factory locations, SLA definitions,
and corporate theme color tokens.
"""

# ==============================================================================
# FACTORY LOCATIONS & COORDINATES
# ==============================================================================
FACTORY_LOCATIONS = {
    "Wicked Choccy's": {"lat": 32.076176, "lon": -81.088371, "city": "Savannah", "state": "Georgia"},
    "Lot's O' Nuts": {"lat": 32.881893, "lon": -111.768036, "city": "Casa Grande", "state": "Arizona"},
    "Secret Factory": {"lat": 41.446333, "lon": -90.565487, "city": "Rock Island", "state": "Illinois"},
    "The Other Factory": {"lat": 35.117500, "lon": -89.971107, "city": "Memphis", "state": "Tennessee"},
    "Sugar Shack": {"lat": 48.119140, "lon": -96.181150, "city": "Thief River Falls", "state": "Minnesota"}
}

# Product to Factory mapping
PRODUCT_FACTORY_MAP = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory"
}

# ==============================================================================
# STATE & PROVINCE CENTROID COORDINATES (50 US States + DC + 8 Canadian Provinces)
# ==============================================================================
STATE_COORDINATES = {
    "Alabama": {"lat": 32.806671, "lon": -86.791130},
    "Alaska": {"lat": 61.370716, "lon": -152.404419},
    "Arizona": {"lat": 33.729759, "lon": -111.431221},
    "Arkansas": {"lat": 34.969704, "lon": -92.373123},
    "California": {"lat": 36.116203, "lon": -119.681564},
    "Colorado": {"lat": 39.059811, "lon": -105.311104},
    "Connecticut": {"lat": 41.597782, "lon": -72.755371},
    "Delaware": {"lat": 39.318523, "lon": -75.507141},
    "District of Columbia": {"lat": 38.897438, "lon": -77.026817},
    "Florida": {"lat": 27.766279, "lon": -81.686783},
    "Georgia": {"lat": 33.040619, "lon": -83.643074},
    "Hawaii": {"lat": 21.094318, "lon": -157.498337},
    "Idaho": {"lat": 44.240459, "lon": -114.478828},
    "Illinois": {"lat": 40.349457, "lon": -88.986137},
    "Indiana": {"lat": 39.849426, "lon": -86.258278},
    "Iowa": {"lat": 42.011539, "lon": -93.210526},
    "Kansas": {"lat": 38.526600, "lon": -96.726486},
    "Kentucky": {"lat": 37.668140, "lon": -84.670067},
    "Louisiana": {"lat": 31.169546, "lon": -91.867805},
    "Maine": {"lat": 44.693947, "lon": -69.381927},
    "Maryland": {"lat": 39.063946, "lon": -76.802101},
    "Massachusetts": {"lat": 42.230171, "lon": -71.530106},
    "Michigan": {"lat": 43.326618, "lon": -84.536095},
    "Minnesota": {"lat": 45.694454, "lon": -93.900192},
    "Mississippi": {"lat": 32.741646, "lon": -89.678696},
    "Missouri": {"lat": 38.456085, "lon": -92.288368},
    "Montana": {"lat": 46.921925, "lon": -110.454353},
    "Nebraska": {"lat": 41.125370, "lon": -98.268082},
    "Nevada": {"lat": 38.313515, "lon": -117.055374},
    "New Hampshire": {"lat": 43.452492, "lon": -71.563896},
    "New Jersey": {"lat": 40.298904, "lon": -74.521011},
    "New Mexico": {"lat": 34.840515, "lon": -106.248482},
    "New York": {"lat": 42.165726, "lon": -74.948051},
    "North Carolina": {"lat": 35.630066, "lon": -79.806419},
    "North Dakota": {"lat": 47.528912, "lon": -99.784012},
    "Ohio": {"lat": 40.388783, "lon": -82.764915},
    "Oklahoma": {"lat": 35.565342, "lon": -96.928917},
    "Oregon": {"lat": 44.572021, "lon": -122.070938},
    "Pennsylvania": {"lat": 40.590752, "lon": -77.209755},
    "Rhode Island": {"lat": 41.680893, "lon": -71.511780},
    "South Carolina": {"lat": 33.856892, "lon": -80.945007},
    "South Dakota": {"lat": 44.299782, "lon": -99.438828},
    "Tennessee": {"lat": 35.747845, "lon": -86.692345},
    "Texas": {"lat": 31.054487, "lon": -97.563461},
    "Utah": {"lat": 40.150032, "lon": -111.862434},
    "Vermont": {"lat": 44.045876, "lon": -72.710686},
    "Virginia": {"lat": 37.769337, "lon": -78.169968},
    "Washington": {"lat": 47.400902, "lon": -121.490494},
    "West Virginia": {"lat": 38.491226, "lon": -80.954453},
    "Wisconsin": {"lat": 44.268543, "lon": -89.616508},
    "Wyoming": {"lat": 42.755966, "lon": -107.302490},
    # Canadian Provinces in dataset
    "Alberta": {"lat": 53.933271, "lon": -116.576504},
    "British Columbia": {"lat": 53.726668, "lon": -127.647621},
    "Manitoba": {"lat": 53.760861, "lon": -98.813876},
    "New Brunswick": {"lat": 46.565316, "lon": -66.461916},
    "Newfoundland and Labrador": {"lat": 53.135509, "lon": -57.660436},
    "Nova Scotia": {"lat": 44.681987, "lon": -63.744311},
    "Ontario": {"lat": 51.253775, "lon": -85.323214},
    "Prince Edward Island": {"lat": 46.510712, "lon": -63.416814},
    "Quebec": {"lat": 52.939916, "lon": -73.549136},
    "Saskatchewan": {"lat": 52.939916, "lon": -106.450864}
}

# ==============================================================================
# LOGISTICS SLA AND SHIPPING MODE BASELINES
# ==============================================================================
# Standard target SLA (total business days from order to delivery)
SHIPPING_MODE_SPECS = {
    "Same Day": {
        "dispatch_days_min": 0, "dispatch_days_max": 0,
        "transit_speed_mph": 55, "sla_days": 1,
        "cost_multiplier": 2.2
    },
    "First Class": {
        "dispatch_days_min": 1, "dispatch_days_max": 2,
        "transit_speed_mph": 45, "sla_days": 3,
        "cost_multiplier": 1.5
    },
    "Second Class": {
        "dispatch_days_min": 2, "dispatch_days_max": 3,
        "transit_speed_mph": 40, "sla_days": 5,
        "cost_multiplier": 1.2
    },
    "Standard Class": {
        "dispatch_days_min": 3, "dispatch_days_max": 5,
        "transit_speed_mph": 35, "sla_days": 7,
        "cost_multiplier": 1.0
    }
}

# ==============================================================================
# NATURAL CORPORATE COLOR PALETTE (Human-designed, non-neon)
# ==============================================================================
COLORS = {
    "primary": "#1E3A8A",       # Classic Deep Navy
    "primary_light": "#3B82F6", # Slate Azure
    "primary_dark": "#172554",  # Midnight Blue
    "secondary": "#334155",     # Charcoal Slate
    "accent_warm": "#D97706",   # Warm Amber / Ochre
    "accent_green": "#15803D",  # Natural Forest Green
    "accent_red": "#B91C1C",    # Muted Terracotta Red
    "accent_blue": "#0284C7",   # Calm Ocean Blue
    "bg_light": "#F8FAFC",      # Clean soft off-white
    "card_bg": "#FFFFFF",       # Crisp white card
    "border": "#E2E8F0",        # Muted slate border
    "text_dark": "#0F172A",     # Deep Slate text
    "text_muted": "#64748B",    # Muted secondary text
    # Sequence for charts
    "chart_palette": [
        "#1E3A8A", # Deep Navy
        "#0F766E", # Deep Teal
        "#D97706", # Warm Amber
        "#4338CA", # Indigo
        "#15803D", # Forest Green
        "#B91C1C", # Terracotta
        "#64748B", # Slate
        "#854D0E"  # Warm Bronze
    ]
}
