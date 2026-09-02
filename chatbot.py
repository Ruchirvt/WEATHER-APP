"""
Rescue Chatbot -- a keyword-driven safety assistant.

It is intentionally rule-based (no external LLM call needed, works offline
and free of cost) and is context-aware: it can reference the live
calamity-risk scores computed for the state the user has selected.

If you later want to upgrade this to a full LLM chatbot, see the
"Optional: LLM upgrade" note in the README -- you'd swap the
`get_response()` body for a call to an LLM API and keep everything else.
"""

HELPLINES = {
    "National Emergency Number": "112",
    "Disaster Management Helpline (NDMA)": "1078",
    "Fire": "101",
    "Police": "100",
    "Ambulance": "108",
    "Women Helpline": "1091",
    "Flood/Disaster Relief (state control rooms)": "1070",
}

SAFETY_TIPS = {
    "flood": [
        "Move to higher ground immediately; avoid walking or driving through moving water.",
        "Turn off electricity and gas at the main switch/valve if flooding is imminent.",
        "Keep an emergency kit ready: drinking water, dry food, torch, phone charger/power bank, medicines.",
        "Avoid contact with flood water -- it may be contaminated or electrically charged.",
        "Follow official evacuation orders from local disaster authorities without delay.",
    ],
    "cyclone": [
        "Stay indoors, away from windows and glass doors.",
        "Secure loose objects outside your home (furniture, hoardings, sheets).",
        "Keep emergency supplies ready: torch, batteries, dry food, water, first-aid kit.",
        "Do not go out during the 'eye' of the storm -- winds resume suddenly and violently.",
        "Follow evacuation orders early; coastal low-lying areas are cleared first.",
    ],
    "heatwave": [
        "Avoid going outdoors between 12 PM and 4 PM if possible.",
        "Drink water regularly even if not thirsty; avoid alcohol, tea, and coffee.",
        "Wear light-colored, loose cotton clothing; use an umbrella or hat outdoors.",
        "Watch for heat-stroke signs: high body temperature, confusion, no sweating -- seek medical help immediately.",
        "Never leave children, elderly people, or pets in parked vehicles.",
    ],
    "drought": [
        "Store and ration water carefully; fix leaking taps/pipes.",
        "Prioritize drinking water use over non-essential uses.",
        "Contact local agricultural office for drought-relief and crop-insurance guidance.",
        "Check on elderly neighbors and livestock, which are especially vulnerable to water shortage.",
    ],
    "earthquake": [
        "Drop, Cover, and Hold On -- get under sturdy furniture immediately.",
        "Stay away from windows, mirrors, and heavy furniture that could fall.",
        "If outdoors, move to an open area away from buildings, trees, and power lines.",
        "After shaking stops, check for injuries and gas leaks before using electrical switches.",
        "Be prepared for aftershocks; keep an emergency kit accessible at all times.",
    ],
}

GREETINGS = ("hi", "hello", "hey", "namaste")
THANKS = ("thanks", "thank you", "thnx", "ty")


def _match_topic(text: str) -> str:
    text = text.lower()
    if any(w in text for w in ["flood", "flooding", "waterlog"]):
        return "flood"
    if any(w in text for w in ["cyclone", "hurricane", "storm", "typhoon"]):
        return "cyclone"
    if any(w in text for w in ["heat", "heatwave", "hot", "sunstroke", "heat stroke"]):
        return "heatwave"
    if any(w in text for w in ["drought", "water shortage", "no rain"]):
        return "drought"
    if any(w in text for w in ["earthquake", "quake", "tremor", "seismic"]):
        return "earthquake"
    if any(w in text for w in ["helpline", "emergency number", "contact", "call", "phone"]):
        return "helpline"
    return ""


def get_response(user_message: str, state_name: str = None, risk_context: list = None) -> str:
    """
    Generate a chatbot reply.
    risk_context: optional list of risk dicts (from calamity_model.assess_all_risks)
                  for the currently selected state, so answers can be personalized.
    """
    msg = user_message.strip().lower()

    if not msg:
        return "Please tell me what kind of help you need -- e.g. 'flood safety tips' or 'emergency numbers'."

    if any(g in msg for g in GREETINGS):
        return ("Hello! I'm your Rescue Assistant. Ask me about flood, cyclone, heatwave, "
                "drought, or earthquake safety, or say 'helpline' for emergency numbers. "
                "You can also ask 'what's my risk right now?' for a live read on your selected state.")

    if any(t in msg for t in THANKS):
        return "You're welcome. Stay safe, and don't hesitate to ask if you need anything else."

    if "my risk" in msg or "current risk" in msg or "how risky" in msg:
        if not risk_context:
            return "Select a state from the sidebar first so I can check its live risk levels."
        top = risk_context[0]
        lines = [f"For **{state_name}**, here's the current top risk:",
                 f"**{top['type']}: {top['band']} ({top['score']}/100)**"]
        if top["reasons"]:
            lines.append("Why: " + "; ".join(top["reasons"]))
        if top["band"] in ("High", "Severe"):
            key = top["type"].split()[0].lower()
            if key in SAFETY_TIPS:
                lines.append("\nImmediate safety tips:")
                lines += [f"- {tip}" for tip in SAFETY_TIPS[key][:3]]
        return "\n".join(lines)

    topic = _match_topic(msg)

    if topic == "helpline":
        lines = ["Here are key India emergency helpline numbers:"]
        lines += [f"- {name}: **{number}**" for name, number in HELPLINES.items()]
        return "\n".join(lines)

    if topic in SAFETY_TIPS:
        lines = [f"**{topic.capitalize()} safety tips:**"]
        lines += [f"- {tip}" for tip in SAFETY_TIPS[topic]]
        lines.append(f"\nIn a real emergency, call **112** (National Emergency Number) immediately.")
        return "\n".join(lines)

    return ("I can help with: flood, cyclone, heatwave, drought, and earthquake safety, "
            "plus emergency helpline numbers. Try asking, for example, 'flood safety tips' "
            "or 'what's my risk right now?'.")
