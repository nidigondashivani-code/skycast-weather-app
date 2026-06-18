import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.weather_dao import get_weather_history, get_top_hottest_cities, get_average_temperature
from database.db_connection import init_db
from services.prediction_service import predict_temperature
from services.report_service import generate_weather_report
from services.weather_service import fetch_weather_for_city, get_live_location_city, fetch_all_cities
import config

# Initialize DB
init_db()

st.set_page_config(page_title="SkyCast Monitoring", page_icon="🌤️", layout="wide")

# Auto-seed database if empty (Crucial for Streamlit Cloud deployments)
if not get_weather_history():
    with st.spinner("Initializing cloud database telemetry for the first time..."):
        fetch_all_cities()

# Custom CSS for Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Glassmorphism Metric Cards */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 20px 25px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        text-align: center;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px 0 rgba(79, 139, 249, 0.2);
        border: 1px solid rgba(79, 139, 249, 0.4);
        background: rgba(255, 255, 255, 0.05);
    }
    
    /* Modern Headers */
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #4F8BF9, #8C52FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    
    /* Button Aesthetics */
    div.stButton > button {
        background: linear-gradient(135deg, #4F8BF9 0%, #8C52FF 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(140, 82, 255, 0.2);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(140, 82, 255, 0.4);
        border: none;
        color: white;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Hide top padding */
    .block-container {
        padding-top: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.title("🌤️ SkyCast Weather Intelligence")
st.markdown("<p style='color: #8892b0; font-size: 1.1rem; margin-top: -15px; margin-bottom: 30px;'>Real-time atmospheric monitoring, historical analysis, and ML-powered predictions.</p>", unsafe_allow_html=True)

# Sidebar Design
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    menu = st.radio("", ["📊 Live Dashboard", "📈 Historical Trends", "🔮 Predictions & Exports"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### ⚙️ System Status")
    st.success("🟢 Background Sync Active\n\n*(Updating DB every 1 hour)*")
    st.markdown("---")
    st.markdown("### 🏙️ Monitored Cities")
    for city in config.CITIES:
        st.markdown(f"- {city}")

# Dashboard View
if menu == "📊 Live Dashboard":
    st.header("Atmospheric Overview")
    
    # Live Location Feature
    st.markdown("### 📍 Your Local Weather")
    with st.spinner("Detecting your live location..."):
        user_city = get_live_location_city()
        
    if user_city and user_city != "Unknown":
        st.write(f"Detected Location: **{user_city}**")
        local_weather = fetch_weather_for_city(user_city)
        if local_weather:
            lc1, lc2, lc3, lc4 = st.columns(4)
            lc1.metric("Temperature", f"{local_weather['temperature']}°C")
            lc2.metric("Condition", local_weather['weather_condition'])
            lc3.metric("Humidity", f"{local_weather['humidity']}%")
            lc4.metric("Wind Speed", f"{local_weather['wind_speed']} m/s")
        else:
            st.warning(f"Could not fetch weather data for {user_city}.")
    else:
        st.warning("Could not detect live location.")
        
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
    
    # Worldwide City Search
    st.markdown("### 🌍 Worldwide City Search")
    search_query = st.text_input("Search for any city in the world:", placeholder="e.g. Kyoto, Vancouver, Nairobi...")
    if search_query:
        with st.spinner(f"Connecting to satellite data for {search_query}..."):
            search_weather = fetch_weather_for_city(search_query)
            if search_weather:
                st.success(f"Live data for **{search_query.title()}**")
                sc1, sc2, sc3, sc4 = st.columns(4)
                sc1.metric("Temperature", f"{search_weather['temperature']}°C")
                sc2.metric("Condition", search_weather['weather_condition'])
                sc3.metric("Humidity", f"{search_weather['humidity']}%")
                sc4.metric("Wind Speed", f"{search_weather['wind_speed']} m/s")
            else:
                st.error(f"Could not fetch weather data for '{search_query}'. Please check the spelling.")

    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown("### 🌐 Global Monitored Network")
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    
    avg_temp = get_average_temperature()
    hottest_cities = get_top_hottest_cities()
    
    with col1:
        st.metric(label="Global Average Temp", value=f"{avg_temp}°C" if avg_temp else "--")
        
    with col2:
        if hottest_cities:
            hottest = sorted(hottest_cities, key=lambda x: x[1], reverse=True)[0]
            st.metric(label="Peak Heat Center", value=hottest[0], delta=f"{hottest[1]}°C", delta_color="inverse")
        else:
            st.metric(label="Peak Heat Center", value="--")
            
    with col3:
        st.metric(label="Active Monitors", value=len(config.CITIES))

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("Temperature Distribution Map")
    
    if hottest_cities:
        df_hot = pd.DataFrame(hottest_cities, columns=["City", "Max Temperature"])
        
        # Premium Custom Plotly Chart
        fig = px.bar(
            df_hot, x="City", y="Max Temperature", 
            color="Max Temperature",
            color_continuous_scale=px.colors.sequential.Plasma,
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_family="Outfit",
            margin=dict(l=20, r=20, t=30, b=20),
            hovermode="x unified"
        )
        fig.update_traces(marker_line_width=0, opacity=0.9, width=0.4)
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("Awaiting telemetry data...")

# Historical Data View
elif menu == "📈 Historical Trends":
    st.header("Temporal Analysis")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("### Filter Options")
        city_filter = st.selectbox("Select Region", ["Global View"] + config.CITIES)
    
    search_city = None if city_filter == "Global View" else city_filter
    history = get_weather_history(search_city)
    
    if history:
        df_history = pd.DataFrame([{
            "City": log.city,
            "Temp (°C)": log.temperature,
            "Humidity (%)": log.humidity,
            "Condition": log.weather_condition,
            "Wind (m/s)": log.wind_speed,
            "Timestamp": log.fetched_time
        } for log in history])
        
        with col2:
            if search_city:
                # Premium Line Chart
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    x=df_history["Timestamp"], y=df_history["Temp (°C)"],
                    mode='lines+markers',
                    name='Temperature',
                    line=dict(color='#8C52FF', width=3, shape='spline'),
                    marker=dict(size=8, color='#4F8BF9'),
                    fill='tozeroy',
                    fillcolor='rgba(140, 82, 255, 0.1)'
                ))
                fig2.update_layout(
                    title=f"Thermal Fluctuation: {search_city}",
                    template="plotly_dark",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_family="Outfit",
                    hovermode="x unified"
                )
                st.plotly_chart(fig2, width='stretch')
            else:
                st.markdown("### System-wide Telemetry Log")
                st.dataframe(df_history.head(100), width='stretch')
    else:
        st.warning("No historical telemetry found in the database.")

# Reports & Predictions View
elif menu == "🔮 Predictions & Exports":
    st.header("Intelligence & Export Center")
    
    col1, space, col2 = st.columns([1, 0.1, 1])
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); padding: 30px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); height: 100%;">
            <h3 style="margin-top:0;">🤖 AI Forecasting</h3>
            <p style="color: #8892b0; margin-bottom: 25px;">Utilize our scikit-learn regression model to forecast tomorrow's localized temperatures.</p>
        </div>
        """, unsafe_allow_html=True)
        
        predict_city = st.selectbox("Target City for Prediction", config.CITIES)
        if st.button("Generate Forecast", icon="✨"):
            with st.spinner("Analyzing atmospheric models..."):
                prediction = predict_temperature(predict_city)
                if prediction:
                    st.success(f"**Forecast for {predict_city}:** {prediction}°C expected tomorrow.")
                else:
                    st.error("Insufficient historical data for a high-confidence prediction.")
                
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); padding: 30px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); height: 100%;">
            <h3 style="margin-top:0;">📥 Data Extraction</h3>
            <p style="color: #8892b0; margin-bottom: 25px;">Download the complete raw dataset in CSV format for external analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Compile CSV Report", icon="📊"):
            report_path = generate_weather_report()
            if report_path and os.path.exists(report_path):
                with open(report_path, "rb") as file:
                    st.download_button(
                        label="Download Compiled Report",
                        data=file,
                        file_name="skycast_telemetry.csv",
                        mime="text/csv",
                        type="primary"
                    )
            else:
                st.error("Report generation failed.")
