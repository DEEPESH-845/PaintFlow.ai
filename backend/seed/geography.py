from __future__ import annotations
"""
Geography: 5 regions, 10 warehouses (real Indian cities), 50 dealers.
Lat/lng are tuned for react-simple-maps India TopoJSON projection.
"""

import json

REGIONS = [
    {"name": "North", "states": json.dumps(["Delhi", "Uttar Pradesh", "Rajasthan", "Punjab", "Haryana"])},
    {"name": "South", "states": json.dumps(["Tamil Nadu", "Karnataka", "Kerala", "Andhra Pradesh", "Telangana"])},
    {"name": "East", "states": json.dumps(["West Bengal", "Odisha", "Bihar", "Jharkhand", "Assam"])},
    {"name": "West", "states": json.dumps(["Maharashtra", "Gujarat", "Goa", "Madhya Pradesh"])},
    {"name": "Central", "states": json.dumps(["Madhya Pradesh", "Chhattisgarh", "Uttarakhand"])},
]

# 2 warehouses per region = 10 total
WAREHOUSES = [
    # North
    {"name": "Delhi Central Warehouse", "code": "WH-DEL-01", "region_idx": 0,
     "city": "Delhi", "state": "Delhi", "lat": 28.6139, "lng": 77.2090, "capacity": 500000},
    {"name": "Jaipur Distribution Hub", "code": "WH-JAI-01", "region_idx": 0,
     "city": "Jaipur", "state": "Rajasthan", "lat": 26.9124, "lng": 75.7873, "capacity": 350000},
    # South
    {"name": "Chennai Supply Center", "code": "WH-CHE-01", "region_idx": 1,
     "city": "Chennai", "state": "Tamil Nadu", "lat": 13.0827, "lng": 80.2707, "capacity": 450000},
    {"name": "Bangalore Tech Warehouse", "code": "WH-BLR-01", "region_idx": 1,
     "city": "Bangalore", "state": "Karnataka", "lat": 12.9716, "lng": 77.5946, "capacity": 400000},
    # East
    {"name": "Kolkata Eastern Hub", "code": "WH-KOL-01", "region_idx": 2,
     "city": "Kolkata", "state": "West Bengal", "lat": 22.5726, "lng": 88.3639, "capacity": 380000},
    {"name": "Lucknow Storage Facility", "code": "WH-LKO-01", "region_idx": 2,
     "city": "Lucknow", "state": "Uttar Pradesh", "lat": 26.8467, "lng": 80.9462, "capacity": 320000},
    # West
    {"name": "Mumbai Central Warehouse", "code": "WH-MUM-01", "region_idx": 3,
     "city": "Mumbai", "state": "Maharashtra", "lat": 19.0760, "lng": 72.8777, "capacity": 600000},
    {"name": "Pune Distribution Center", "code": "WH-PUN-01", "region_idx": 3,
     "city": "Pune", "state": "Maharashtra", "lat": 18.5204, "lng": 73.8567, "capacity": 400000},
    # Central
    {"name": "Bhopal Central Hub", "code": "WH-BPL-01", "region_idx": 4,
     "city": "Bhopal", "state": "Madhya Pradesh", "lat": 23.2599, "lng": 77.4126, "capacity": 300000},
    {"name": "Ahmedabad West Hub", "code": "WH-AMD-01", "region_idx": 4,
     "city": "Ahmedabad", "state": "Gujarat", "lat": 23.0225, "lng": 72.5714, "capacity": 420000},
]

# 50 dealers, ~5 per warehouse
DEALER_NAMES = [
    # North - Delhi
    "Sharma Paint House", "Delhi Colour World", "Gupta Paints & Hardware",
    "Royal Paint Emporium", "Northern Colours Hub",
    # North - Jaipur
    "Rajasthan Paint Centre", "Pink City Paints", "Jaipur Colour Corner",
    "Mewar Paint Traders", "Desert Shade Gallery",
    # South - Chennai
    "Sri Lakshmi Paints", "Tamil Nadu Colour House", "Marina Paint Store",
    "Coromandel Paints Hub", "Southern Paint Bazaar",
    # South - Bangalore
    "Garden City Paints", "Bangalore Colour Works", "Silicon Valley Paints",
    "Karnataka Paint Mart", "MG Road Colour Shop",
    # East - Kolkata
    "Bengal Paint Traders", "Kolkata Colour House", "Eastern Paint Depot",
    "Hooghly Paints & More", "Park Street Colours",
    # East - Lucknow
    "Nawab Paint Palace", "Lucknow Colour Centre", "UP Paint Distributors",
    "Awadh Colour Gallery", "Gomti Paint House",
    # West - Mumbai
    "Marine Drive Paints", "Mumbai Colour Studio", "Borivali Paint Centre",
    "Western Paint Galaxy", "Dadar Colour Works",
    # West - Pune
    "Pune Paint Paradise", "Deccan Colour House", "Shivaji Paint Mart",
    "Koregaon Park Paints", "Pune Western Colours",
    # Central - Bhopal
    "Lake City Paints", "MP Paint Distributors", "Bhopal Colour Hub",
    "Central India Paints", "Habibganj Paint Store",
    # Central - Ahmedabad
    "Gujarat Paint Gallery", "Sabarmati Colour House", "Ahmedabad Paint Bazaar",
    "Navrangpura Paints", "CG Road Colour Works",
]

# City/state mapping for dealers (5 per warehouse)
DEALER_LOCATIONS = [
    # North - Delhi (5)
    *[{"city": "Delhi", "state": "Delhi", "lat": 28.6139 + i * 0.02, "lng": 77.2090 + i * 0.015, "wh_idx": 0} for i in range(5)],
    # North - Jaipur (5)
    *[{"city": "Jaipur", "state": "Rajasthan", "lat": 26.9124 + i * 0.02, "lng": 75.7873 + i * 0.015, "wh_idx": 1} for i in range(5)],
    # South - Chennai (5)
    *[{"city": "Chennai", "state": "Tamil Nadu", "lat": 13.0827 + i * 0.02, "lng": 80.2707 + i * 0.015, "wh_idx": 2} for i in range(5)],
    # South - Bangalore (5)
    *[{"city": "Bangalore", "state": "Karnataka", "lat": 12.9716 + i * 0.02, "lng": 77.5946 + i * 0.015, "wh_idx": 3} for i in range(5)],
    # East - Kolkata (5)
    *[{"city": "Kolkata", "state": "West Bengal", "lat": 22.5726 + i * 0.02, "lng": 88.3639 + i * 0.015, "wh_idx": 4} for i in range(5)],
    # East - Lucknow (5)
    *[{"city": "Lucknow", "state": "Uttar Pradesh", "lat": 26.8467 + i * 0.02, "lng": 80.9462 + i * 0.015, "wh_idx": 5} for i in range(5)],
    # West - Mumbai (5)
    *[{"city": "Mumbai", "state": "Maharashtra", "lat": 19.0760 + i * 0.02, "lng": 72.8777 + i * 0.015, "wh_idx": 6} for i in range(5)],
    # West - Pune (5)
    *[{"city": "Pune", "state": "Maharashtra", "lat": 18.5204 + i * 0.02, "lng": 73.8567 + i * 0.015, "wh_idx": 7} for i in range(5)],
    # Central - Bhopal (5)
    *[{"city": "Bhopal", "state": "Madhya Pradesh", "lat": 23.2599 + i * 0.02, "lng": 77.4126 + i * 0.015, "wh_idx": 8} for i in range(5)],
    # Central - Ahmedabad (5)
    *[{"city": "Ahmedabad", "state": "Gujarat", "lat": 23.0225 + i * 0.02, "lng": 72.5714 + i * 0.015, "wh_idx": 9} for i in range(5)],
]
