import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from data.india_states import get_state_names, get_state_info
from utils.weather_api import get_current_weather, get_3day_summary, WeatherAPIError
from utils.calamity_model import assess_all_risks
from utils.chatbot import get_response

st.set_page_config(page_title="India Weather & Calamity Forecast", page_icon="🌦️", layout="wide")

# ---------- API KEY ----------
API_KEY = st.secrets.get("OPENWEATHER_API_KEY", None)

# ---------- SIDEBAR ----------
st.sidebar.title("🌦️ Settings")

if not API_KEY:
    API_KEY = st.sidebar.text_input("OpenWeatherMap API Key", type="password",
                                     help="Get a free key at openweathermap.org")

state_name = st.sidebar.selectbox("Select State / UT", get_state_names(), index=get_state_names().index("Maharashtra") if "Maharashtra" in get_state_names() else 0)

st.sidebar.markdown("---")
st.sidebar.caption("Data: OpenWeatherMap (Current + 5-day/3-hour forecast). "
                    "Calamity risk is a transparent rule-based model combining live weather "
                    "with each state's geography (coastal, hilly, seismic zone, historical patterns).")

st.title("🇮🇳 India Weather Forecast & Natural Calamity Risk Dashboard")

if not API_KEY:
    st.warning("Enter your OpenWeatherMap API key in the sidebar to load live data. "
               "Get a free key at https://openweathermap.org/api")
    st.stop()

state_info = get_state_info(state_name)
lat, lon = state_info["lat"], state_info["lon"]

# ---------- FETCH DATA ----------
try:
    with st.spinner(f"Fetching live weather for {state_name}..."):
        current = get_current_weather(lat, lon, API_KEY)
        forecast_3day = get_3day_summary(lat, lon, API_KEY)
        risks = assess_all_risks(current, forecast_3day, state_info)
except WeatherAPIError as e:
    st.error(f"Weather API error: {e}")
    st.stop()
except Exception as e:
    st.error(f"Something went wrong fetching data: {e}")
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs(["🌡️ Live Weather", "📅 3-Day Forecast", "⚠️ Calamity Risk", "🆘 Rescue Chatbot"])

# ---------- TAB 1: LIVE WEATHER ----------
with tab1:
    st.subheader(f"Live Weather — {state_info['capital']}, {state_name}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Temperature", f"{current['temp']:.1f} °C", f"Feels like {current['feels_like']:.1f} °C")
    c2.metric("Humidity", f"{current['humidity']}%")
    c3.metric("Wind Speed", f"{current['wind_speed']:.1f} m/s")
    c4.metric("Pressure", f"{current['pressure']} hPa")

    c5, c6, c7 = st.columns(3)
    c5.metric("Condition", current["description"].title())
    c6.metric("Cloud Cover", f"{current['clouds']}%")
    c7.metric("Rain (last 1h)", f"{current['rain_1h']:.1f} mm")

    st.caption(f"Sunrise: {current['sunrise'].strftime('%H:%M')} | "
               f"Sunset: {current['sunset'].strftime('%H:%M')} | "
               f"Observed at: {current['observed_at'].strftime('%Y-%m-%d %H:%M')}")

# ---------- TAB 2: 3-DAY FORECAST ----------
with tab2:
    st.subheader("3-Day Forecast Outlook")
    display_df = forecast_3day.copy()
    display_df["date"] = display_df["date"].astype(str)
    cols = st.columns(len(display_df))
    for i, row in display_df.iterrows():
        with cols[i]:
            st.markdown(f"**{row['date']}**")
            st.markdown(f"{row['condition']}")
            st.markdown(f"🌡️ {row['temp_min']:.0f}° – {row['temp_max']:.0f}°C")
            st.markdown(f"💧 Rain: {row['rain_total']:.1f} mm ({row['pop_max']:.0f}% chance)")
            st.markdown(f"💨 Wind: {row['wind_max']*3.6:.0f} km/h")

    st.markdown("---")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=display_df["date"], y=display_df["temp_max"], name="Max Temp", mode="lines+markers"))
    fig.add_trace(go.Scatter(x=display_df["date"], y=display_df["temp_avg"], name="Avg Temp", mode="lines+markers"))
    fig.add_trace(go.Scatter(x=display_df["date"], y=display_df["temp_min"], name="Min Temp", mode="lines+markers"))
    fig.update_layout(title="Temperature Trend (Next 3 Days)", yaxis_title="°C", height=350)
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(display_df, x="date", y="rain_total", title="Expected Rainfall (mm) per Day")
    st.plotly_chart(fig2, use_container_width=True)

# ---------- TAB 3: CALAMITY RISK ----------
with tab3:
    st.subheader(f"Natural Calamity Risk Assessment — {state_name}")
    st.caption("Rule-based scoring using live/forecast weather + each state's geography. "
               "Not an official disaster warning — always follow guidance from NDMA / IMD / local authorities.")

    band_colors = {"Low": "#2ecc71", "Moderate": "#f1c40f", "High": "#e67e22", "Severe": "#e74c3c"}

    for r in risks:
        color = band_colors.get(r["band"], "#95a5a6")
        with st.expander(f"{r['type']} — {r['band']} ({r['score']}/100)", expanded=(r["band"] in ("High", "Severe"))):
            st.progress(r["score"] / 100)
            st.markdown(f"<span style='color:{color}; font-weight:bold'>{r['band']} risk</span>", unsafe_allow_html=True)
            if r["reasons"]:
                st.markdown("**Contributing factors:**")
                for reason in r["reasons"]:
                    st.markdown(f"- {reason}")
            else:
                st.markdown("No significant risk factors detected.")

    risk_df = pd.DataFrame(risks)
    fig3 = px.bar(risk_df, x="type", y="score", color="band",
                  color_discrete_map=band_colors, title="Risk Score Comparison")
    st.plotly_chart(fig3, use_container_width=True)

# ---------- TAB 4: CHATBOT ----------
with tab4:
    st.subheader("🆘 Rescue & Safety Chatbot")
    st.caption("Ask about flood/cyclone/heatwave/drought/earthquake safety, emergency helplines, "
               "or your current risk level. This is a rule-based assistant — for real emergencies, call 112.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            ("bot", "Hi! I'm your Rescue Assistant. Ask me for safety tips, emergency helplines, "
                    "or say 'what's my risk right now?' to check your selected state.")
        ]

    for role, text in st.session_state.chat_history:
        with st.chat_message("assistant" if role == "bot" else "user"):
            st.markdown(text)

    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        reply = get_response(user_input, state_name=state_name, risk_context=risks)
        st.session_state.chat_history.append(("bot", reply))
        st.rerun()
