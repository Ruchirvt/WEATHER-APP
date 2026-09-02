# 🌦️ India Weather Forecast & Natural Calamity Risk Dashboard

A Streamlit app that shows **live weather**, a **3-day forecast**, a rule-based
**natural calamity risk assessment** (flood, cyclone, heatwave, drought,
earthquake baseline) for any Indian state/UT, plus a built-in **rescue/safety
chatbot**.

## Features
- Live weather for all 28 states + 8 UTs (temperature, humidity, wind, pressure, rain)
- 3-day forecast built from OpenWeatherMap's 5-day/3-hour data, aggregated per day
- Transparent, explainable calamity risk scoring (0–100) that combines weather
  signals with each state's geography (coastal, hilly, seismic zone, historical
  flood/drought/cyclone patterns) — every score comes with the reasons behind it
- Interactive charts (Plotly): temperature trend, rainfall forecast, risk comparison
- Rule-based rescue chatbot with safety tips per hazard type and India emergency helplines

## Project Structure
```
weather-app/
├── app.py                      # Main Streamlit app
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── secrets.toml.example    # Template — rename to secrets.toml locally, never commit the real one
├── data/
│   └── india_states.py         # States/UTs + geographic risk metadata
└── utils/
    ├── weather_api.py          # OpenWeatherMap API wrapper
    ├── calamity_model.py       # Rule-based risk scoring engine
    └── chatbot.py              # Rescue chatbot logic
```

## 1. Get a free OpenWeatherMap API key
1. Sign up at https://openweathermap.org/
2. Verify your email
3. Go to "My API keys" and copy your default key
4. Keys can take up to 2 hours to activate — if you get "Invalid API key" right away, just wait and retry

Free tier: 1,000 calls/day — plenty for this app's Current Weather + 5-day Forecast calls.

## 2. Run locally
```bash
git clone <your-repo-url>
cd weather-app
pip install -r requirements.txt

# Set up your key
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# then edit .streamlit/secrets.toml and paste your real API key

streamlit run app.py
```

## 3. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: weather & calamity dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```
**Important:** `.streamlit/secrets.toml` is in `.gitignore` on purpose — never commit your real API key.
Only `secrets.toml.example` (with a placeholder) should go to GitHub.

## 4. Deploy on Streamlit Community Cloud
1. Go to https://share.streamlit.io/ and sign in with GitHub
2. Click "New app" → select your repo, branch (`main`), and `app.py` as the entry point
3. Before/after deploying, go to **App settings → Secrets** and paste:
   ```toml
   OPENWEATHER_API_KEY = "your_real_key_here"
   ```
4. Click Deploy. Your app will be live at `https://<your-app-name>.streamlit.app`

## How the calamity risk model works
This is a **rule-based** system, not a trained ML model — chosen deliberately so
every score is explainable and doesn't need a training dataset:
- **Flood**: current rainfall + 3-day cumulative rain forecast + humidity + whether the state is historically flood-prone/hilly
- **Cyclone**: wind speed + atmospheric pressure drop, only scored for coastal states
- **Heatwave**: peak forecast temperature + low humidity amplification
- **Drought**: lack of forecast rain + low humidity + high temp + historical drought-proneness
- **Earthquake**: a static baseline from the state's official BIS Seismic Zone (not weather-driven — clearly labeled as such)

## Optional upgrades (if you want to extend this project)
- **Smarter chatbot**: swap `utils/chatbot.py`'s `get_response()` for a call to an LLM API
  (e.g. Anthropic's Claude or OpenAI) for more natural conversation — keep the risk-context
  passing so it stays grounded in real data instead of hallucinating advice.
- **Real ML model**: replace `calamity_model.py` with a trained classifier using historical
  IMD/NDMA disaster datasets, if you want to move beyond rules for a research-grade project.
- **Map view**: add `st.map()` or `folium` to plot all states colored by risk level.
- **Historical trends**: cache daily snapshots to a small SQLite/CSV store to chart risk over time.

## Disclaimer
This tool is for educational/demo purposes. It is **not** an official disaster warning
system. In a real emergency, always follow guidance from IMD, NDMA, and local authorities,
and call **112** (India's National Emergency Number).
