"""
Rule-based natural calamity risk model.

This is intentionally NOT a black-box ML model -- it's a transparent,
explainable scoring system that combines:
  1. Live/forecast weather signals (rain, wind, temp, pressure, humidity)
  2. Static geographic risk factors per state (coastal, hilly, seismic zone,
     historically flood/drought/cyclone prone)

Each calamity type gets a 0-100 risk score and a risk band
(Low / Moderate / High / Severe), plus the human-readable reasons
behind the score so users can trust *why* it fired.
"""

RISK_BANDS = [(0, 25, "Low"), (25, 50, "Moderate"), (50, 75, "High"), (75, 101, "Severe")]


def _band(score: float) -> str:
    for lo, hi, label in RISK_BANDS:
        if lo <= score < hi:
            return label
    return "Severe"


def assess_flood_risk(current: dict, forecast_3day, state_info: dict) -> dict:
    score = 0
    reasons = []

    rain_today = current.get("rain_1h", 0.0)
    total_rain_3d = forecast_3day["rain_total"].sum() if len(forecast_3day) else 0
    humidity = current.get("humidity", 0)

    if rain_today > 4:
        score += 20
        reasons.append(f"Heavy current rainfall ({rain_today:.1f} mm/h)")
    elif rain_today > 1:
        score += 8
        reasons.append(f"Moderate current rainfall ({rain_today:.1f} mm/h)")

    if total_rain_3d > 100:
        score += 35
        reasons.append(f"Very high cumulative rain expected over 3 days ({total_rain_3d:.0f} mm)")
    elif total_rain_3d > 50:
        score += 20
        reasons.append(f"Significant rain expected over 3 days ({total_rain_3d:.0f} mm)")
    elif total_rain_3d > 20:
        score += 8
        reasons.append(f"Moderate rain expected over 3 days ({total_rain_3d:.0f} mm)")

    if humidity > 85:
        score += 8
        reasons.append(f"Very high humidity ({humidity}%)")

    if state_info.get("flood_prone"):
        score += 15
        reasons.append("State has a history of flooding")
    if state_info.get("hilly") and total_rain_3d > 50:
        score += 10
        reasons.append("Hilly terrain increases flash-flood/landslide runoff risk")

    score = min(score, 100)
    return {"type": "Flood", "score": score, "band": _band(score), "reasons": reasons}


def assess_cyclone_risk(current: dict, forecast_3day, state_info: dict) -> dict:
    score = 0
    reasons = []

    wind = current.get("wind_speed", 0) * 3.6  # m/s -> km/h
    pressure = current.get("pressure", 1013)
    max_forecast_wind = forecast_3day["wind_max"].max() * 3.6 if len(forecast_3day) else wind

    if not state_info.get("coastal"):
        return {"type": "Cyclone", "score": 0, "band": "Low",
                "reasons": ["Non-coastal state \u2014 cyclone landfall risk negligible"]}

    if wind > 60 or max_forecast_wind > 60:
        score += 35
        reasons.append(f"High wind speeds ({max(wind, max_forecast_wind):.0f} km/h)")
    elif wind > 35 or max_forecast_wind > 35:
        score += 15
        reasons.append(f"Elevated wind speeds ({max(wind, max_forecast_wind):.0f} km/h)")

    if pressure < 995:
        score += 30
        reasons.append(f"Low atmospheric pressure ({pressure} hPa) \u2014 storm system signature")
    elif pressure < 1005:
        score += 12
        reasons.append(f"Below-normal pressure ({pressure} hPa)")

    if state_info.get("cyclone_prone"):
        score += 20
        reasons.append("Coastal state with cyclone history")

    score = min(score, 100)
    return {"type": "Cyclone", "score": score, "band": _band(score), "reasons": reasons}


def assess_heatwave_risk(current: dict, forecast_3day, state_info: dict) -> dict:
    score = 0
    reasons = []

    temp = current.get("temp", 0)
    max_forecast_temp = forecast_3day["temp_max"].max() if len(forecast_3day) else temp
    humidity = current.get("humidity", 50)

    peak = max(temp, max_forecast_temp)
    if peak >= 45:
        score += 45
        reasons.append(f"Extreme temperature ({peak:.1f}\u00b0C)")
    elif peak >= 40:
        score += 28
        reasons.append(f"Very high temperature ({peak:.1f}\u00b0C)")
    elif peak >= 37:
        score += 12
        reasons.append(f"High temperature ({peak:.1f}\u00b0C)")

    if humidity < 30 and peak >= 35:
        score += 10
        reasons.append("Low humidity intensifying heat stress")

    if state_info.get("drought_prone"):
        score += 10
        reasons.append("Region historically prone to heat/drought stress")

    score = min(score, 100)
    return {"type": "Heatwave", "score": score, "band": _band(score), "reasons": reasons}


def assess_drought_risk(current: dict, forecast_3day, state_info: dict) -> dict:
    score = 0
    reasons = []

    humidity = current.get("humidity", 50)
    total_rain_3d = forecast_3day["rain_total"].sum() if len(forecast_3day) else 0
    temp = current.get("temp", 0)

    if total_rain_3d < 1:
        score += 20
        reasons.append("No meaningful rainfall expected in next 3 days")
    if humidity < 35:
        score += 15
        reasons.append(f"Low humidity ({humidity}%)")
    if temp > 35:
        score += 10
        reasons.append(f"High temperature increasing evaporation ({temp:.1f}\u00b0C)")
    if state_info.get("drought_prone"):
        score += 25
        reasons.append("State has a documented history of drought")

    score = min(score, 100)
    return {"type": "Drought", "score": score, "band": _band(score), "reasons": reasons}


def assess_earthquake_risk(state_info: dict) -> dict:
    """
    Earthquake risk is NOT weather-driven -- it's included as a static
    seismic-zone awareness indicator (BIS zoning), clearly labeled as such.
    """
    zone = state_info.get("seismic_zone", "II")
    zone_scores = {"II": 15, "III": 35, "IV": 60, "V": 85}
    score = zone_scores.get(zone, 15)
    reasons = [f"Located in Seismic Zone {zone} (BIS classification)"]
    return {"type": "Earthquake (baseline seismic risk, not weather-based)",
            "score": score, "band": _band(score), "reasons": reasons}


def assess_all_risks(current: dict, forecast_3day, state_info: dict) -> list:
    """Run every calamity model and return results sorted by score desc."""
    results = [
        assess_flood_risk(current, forecast_3day, state_info),
        assess_cyclone_risk(current, forecast_3day, state_info),
        assess_heatwave_risk(current, forecast_3day, state_info),
        assess_drought_risk(current, forecast_3day, state_info),
        assess_earthquake_risk(state_info),
    ]
    return sorted(results, key=lambda r: r["score"], reverse=True)
