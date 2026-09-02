"""
India States & Union Territories dataset.

Each entry gives the capital city's coordinates plus geographic risk
metadata that the rule-based calamity model uses to weight its scoring.

seismic_zone: Bureau of Indian Standards seismic zoning (II=low risk .. V=highest)
"""

STATES = {
    "Andhra Pradesh":       {"capital": "Amaravati",     "lat": 16.5062, "lon": 80.6480, "coastal": True,  "hilly": False, "flood_prone": True,  "drought_prone": True,  "cyclone_prone": True,  "seismic_zone": "II"},
    "Arunachal Pradesh":    {"capital": "Itanagar",      "lat": 27.0844, "lon": 93.6053, "coastal": False, "hilly": True,  "flood_prone": True,  "drought_prone": False, "cyclone_prone": False, "seismic_zone": "V"},
    "Assam":                {"capital": "Dispur",        "lat": 26.1433, "lon": 91.7898, "coastal": False, "hilly": False, "flood_prone": True,  "drought_prone": False, "cyclone_prone": False, "seismic_zone": "V"},
    "Bihar":                {"capital": "Patna",         "lat": 25.5941, "lon": 85.1376, "coastal": False, "hilly": False, "flood_prone": True,  "drought_prone": True,  "cyclone_prone": False, "seismic_zone": "IV"},
    "Chhattisgarh":         {"capital": "Raipur",        "lat": 21.2514, "lon": 81.6296, "coastal": False, "hilly": True,  "flood_prone": False, "drought_prone": True,  "cyclone_prone": False, "seismic_zone": "II"},
    "Goa":                  {"capital": "Panaji",        "lat": 15.4909, "lon": 73.8278, "coastal": True,  "hilly": False, "flood_prone": True,  "drought_prone": False, "cyclone_prone": True,  "seismic_zone": "III"},
    "Gujarat":              {"capital": "Gandhinagar",   "lat": 23.2156, "lon": 72.6369, "coastal": True,  "hilly": False, "flood_prone": True,  "drought_prone": True,  "cyclone_prone": True,  "seismic_zone": "V"},
    "Haryana":              {"capital": "Chandigarh",    "lat": 30.7333, "lon": 76.7794, "coastal": False, "hilly": False, "flood_prone": False, "drought_prone": True,  "cyclone_prone": False, "seismic_zone": "IV"},
    "Himachal Pradesh":     {"capital": "Shimla",        "lat": 31.1048, "lon": 77.1734, "coastal": False, "hilly": True,  "flood_prone": True,  "drought_prone": False, "cyclone_prone": False, "seismic_zone": "V"},
    "Jharkhand":            {"capital": "Ranchi",        "lat": 23.3441, "lon": 85.3096, "coastal": False, "hilly": True,  "flood_prone": False, "drought_prone": True,  "cyclone_prone": False, "seismic_zone": "III"},
    "Karnataka":            {"capital": "Bengaluru",     "lat": 12.9716, "lon": 77.5946, "coastal": True,  "hilly": True,  "flood_prone": True,  "drought_prone": True,  "cyclone_prone": False, "seismic_zone": "III"},
    "Kerala":               {"capital": "Thiruvananthapuram", "lat": 8.5241, "lon": 76.9366, "coastal": True, "hilly": True, "flood_prone": True, "drought_prone": False, "cyclone_prone": True, "seismic_zone": "III"},
    "Madhya Pradesh":       {"capital": "Bhopal",        "lat": 23.2599, "lon": 77.4126, "coastal": False, "hilly": True,  "flood_prone": False, "drought_prone": True,  "cyclone_prone": False, "seismic_zone": "III"},
    "Maharashtra":          {"capital": "Mumbai",        "lat": 19.0760, "lon": 72.8777, "coastal": True,  "hilly": True,  "flood_prone": True,  "drought_prone": True,  "cyclone_prone": True,  "seismic_zone": "III"},
    "Manipur":              {"capital": "Imphal",        "lat": 24.8170, "lon": 93.9368, "coastal": False, "hilly": True,  "flood_prone": True,  "drought_prone": False, "cyclone_prone": False, "seismic_zone": "V"},
    "Meghalaya":            {"capital": "Shillong",      "lat": 25.5788, "lon": 91.8933, "coastal": False, "hilly": True,  "flood_prone": True,  "drought_prone": False, "cyclone_prone": False, "seismic_zone": "V"},
    "Mizoram":              {"capital": "Aizawl",        "lat": 23.7271, "lon": 92.7176, "coastal": False, "hilly": True,  "flood_prone": True,  "drought_prone": False, "cyclone_prone": False, "seismic_zone": "V"},
    "Nagaland":             {"capital": "Kohima",        "lat": 25.6751, "lon": 94.1086, "coastal": False, "hilly": True,  "flood_prone": True,  "drought_prone": False, "cyclone_prone": False, "seismic_zone": "V"},
    "Odisha":               {"capital": "Bhubaneswar",   "lat": 20.2961, "lon": 85.8245, "coastal": True,  "hilly": False, "flood_prone": True,  "drought_prone": True,  "cyclone_prone": True,  "seismic_zone": "III"},
    "Punjab":               {"capital": "Chandigarh",    "lat": 30.7333, "lon": 76.7794, "coastal": False, "hilly": False, "flood_prone": True,  "drought_prone": False, "cyclone_prone": False, "seismic_zone": "IV"},
    "Rajasthan":            {"capital": "Jaipur",        "lat": 26.9124, "lon": 75.7873, "coastal": False, "hilly": False, "flood_prone": False, "drought_prone": True,  "cyclone_prone": False, "seismic_zone": "III"},
    "Sikkim":               {"capital": "Gangtok",       "lat": 27.3389, "lon": 88.6065, "coastal": False, "hilly": True,  "flood_prone": True,  "drought_prone": False, "cyclone_prone": False, "seismic_zone": "IV"},
    "Tamil Nadu":           {"capital": "Chennai",       "lat": 13.0827, "lon": 80.2707, "coastal": True,  "hilly": True,  "flood_prone": True,  "drought_prone": True,  "cyclone_prone": True,  "seismic_zone": "III"},
    "Telangana":            {"capital": "Hyderabad",     "lat": 17.3850, "lon": 78.4867, "coastal": False, "hilly": False, "flood_prone": False, "drought_prone": True,  "cyclone_prone": False, "seismic_zone": "II"},
    "Tripura":              {"capital": "Agartala",      "lat": 23.8315, "lon": 91.2868, "coastal": False, "hilly": True,  "flood_prone": True,  "drought_prone": False, "cyclone_prone": False, "seismic_zone": "V"},
    "Uttar Pradesh":        {"capital": "Lucknow",       "lat": 26.8467, "lon": 80.9462, "coastal": False, "hilly": False, "flood_prone": True,  "drought_prone": True,  "cyclone_prone": False, "seismic_zone": "IV"},
    "Uttarakhand":          {"capital": "Dehradun",      "lat": 30.3165, "lon": 78.0322, "coastal": False, "hilly": True,  "flood_prone": True,  "drought_prone": False, "cyclone_prone": False, "seismic_zone": "V"},
    "West Bengal":          {"capital": "Kolkata",       "lat": 22.5726, "lon": 88.3639, "coastal": True,  "hilly": True,  "flood_prone": True,  "drought_prone": False, "cyclone_prone": True,  "seismic_zone": "IV"},
    # Union Territories
    "Andaman and Nicobar Islands": {"capital": "Port Blair", "lat": 11.6234, "lon": 92.7265, "coastal": True, "hilly": False, "flood_prone": True, "drought_prone": False, "cyclone_prone": True, "seismic_zone": "V"},
    "Chandigarh":           {"capital": "Chandigarh",    "lat": 30.7333, "lon": 76.7794, "coastal": False, "hilly": False, "flood_prone": False, "drought_prone": False, "cyclone_prone": False, "seismic_zone": "IV"},
    "Dadra and Nagar Haveli and Daman and Diu": {"capital": "Daman", "lat": 20.3974, "lon": 72.8328, "coastal": True, "hilly": False, "flood_prone": True, "drought_prone": False, "cyclone_prone": True, "seismic_zone": "III"},
    "Delhi":                {"capital": "New Delhi",     "lat": 28.6139, "lon": 77.2090, "coastal": False, "hilly": False, "flood_prone": False, "drought_prone": False, "cyclone_prone": False, "seismic_zone": "IV"},
    "Jammu and Kashmir":    {"capital": "Srinagar",      "lat": 34.0837, "lon": 74.7973, "coastal": False, "hilly": True,  "flood_prone": True,  "drought_prone": False, "cyclone_prone": False, "seismic_zone": "V"},
    "Ladakh":               {"capital": "Leh",           "lat": 34.1526, "lon": 77.5771, "coastal": False, "hilly": True,  "flood_prone": False, "drought_prone": False, "cyclone_prone": False, "seismic_zone": "IV"},
    "Lakshadweep":          {"capital": "Kavaratti",     "lat": 10.5669, "lon": 72.6420, "coastal": True,  "hilly": False, "flood_prone": True,  "drought_prone": False, "cyclone_prone": True,  "seismic_zone": "III"},
    "Puducherry":           {"capital": "Puducherry",    "lat": 11.9416, "lon": 79.8083, "coastal": True,  "hilly": False, "flood_prone": True,  "drought_prone": False, "cyclone_prone": True,  "seismic_zone": "II"},
}


def get_state_names():
    """Sorted list of all state/UT names for the dropdown."""
    return sorted(STATES.keys())


def get_state_info(state_name: str):
    """Return the metadata dict for a given state name."""
    return STATES.get(state_name)
