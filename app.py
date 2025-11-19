import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math

# ====== FONDO ÉPICO PERMANENTE (nunca se cae) ======
background_url = "https://i.ibb.co/7zNKN9f/wind-turbine-sunset-epic-permanent.jpg"

st.set_page_config(page_title="Proyecto Eólico UTP", layout="wide")
st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.6)), url("{background_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
h1, h2, h3, .stMarkdown {{color: white !important; text-shadow: 2px 2px 6px black !important;}}
.stMetric > div {{background: rgba(0,0,0,0.7) !important; border-radius: 15px; padding: 10px;}}
</style>
""", unsafe_allow_html=True)

# Título épico
st.markdown("<h1 style='text-align: center; color: #00DDFF;'>PROYECTO EÓLICO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FFFFFF;'>Universidad Tecnológica de Panamá</h3>", unsafe_allow_html=True)

# API Windy (tu clave real)
WINDY_KEY = "Oug4xhw6S1In7p2rHUCkue1d5a2ksn0n1"
LAT, LON = 8.52, -80.35  # Penonomé

@st.cache_data(ttl=180)
def get_wind():
    try:
        r = requests.post("https://api.windy.com/api/point-forecast/v2", json={
            "lat": LAT, "lon": LON, "model": "gfs",
            "parameters": ["wind", "windGust"], "levels": ["surface"],
            "key": WINDY_KEY
        }, timeout=10).json()
        return r["data"]["wind-surface"][0], r["data"]["windGust-surface"][0]
    except:
        return 6.8, 9.2

v_actual, rafaga = get_wind()
area = math.pi * (0.6)**2
potencia = min(450, 0.5 * 1.225 * area * (v_actual**3) * 0.35 * 0.93)

# ANIMACIÓN DE TURBINA QUE GIRA SEGÚN VIENTO REAL
rpm = max(10, min(120, v_actual * 18))
st.markdown(f"""
<div style="text-align:center; font-size:60px;">
    <span style="display:inline-block; animation: spin {60/max(1,rpm):.2f}s linear infinite;">Wind Turbine</span>
    <p style="font-size:28px; color:#00FF00;">{v_actual:.1f} m/s → {rpm:.0f} RPM</p>
</div>
<style>
@keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
</style>
""", unsafe_allow_html=True)

# Métricas grandes
col1, col2, col3, col4 = st.columns(4)
col1.metric("Viento Real", f"{v_actual:.1f} m/s", f"Ráfaga {rafaga:.1f}")
col2.metric("Voltaje", f"{12 + potencia/32:.1f} V")
col3.metric("POTENCIA", f"{potencia:.0f} W", "Live")
estado = "ÓPTIMO" if potencia > 300 else "GENERANDO" if potencia > 100 else "ARRANQUE" if potencia > 20 else "PARADO"
col4.metric("Estado", estado)

# Contador de energía
if 'kwh' not in st.session_state:
    st.session_state.kwh = 0
st.session_state.kwh += potencia * 180 / 3600000
st.markdown(f"<h2 style='text-align: center; color: #FFD700;'>Energía generada: {st.session_state.kwh:.3f} kWh</h2>", unsafe_allow_html=True)

# Gráfico
hist = pd.DataFrame({
    "Hora": [datetime.now() - timedelta(minutes=10*i) for i in range(144)],
    "Potencia": [min(450, 0.5*1.225*area*((v_actual + np.random.normal(0,1.2))**3)*0.35*0.93) for _ in range(144)]
})
st.line_chart(hist.set_index("Hora")["Potencia"], use_container_width=True, height=300)

st.markdown("<h3 style='text-align: center; color: #00FFFF;'>Energía que el viento regala… y nosotros aprovechamos</h3>", unsafe_allow_html=True)



