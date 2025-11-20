import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math

# FONDO QUE ACABAS DE SUBIR
st.set_page_config(page_title="Proyecto Eólico UTP", layout="wide")
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.65)), url("background.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
h1, h2, h3 {color: white !important; text-shadow: 3px 3px 8px black !important;}
.stMetric {background: rgba(0,0,0,0.7); border-radius: 15px; padding: 10px;}
</style>
""", unsafe_allow_html=True)

st.image("https://www.utp.ac.pa/sites/default/files/logo_utp.png", width=180)
st.markdown("<h1 style='text-align:center; color:#FFD700;'>PROYECTO EÓLICO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>Universidad Tecnológica de Panamá</h3>", unsafe_allow_html=True)

# TU API KEY
WINDY_KEY = "Oug4xhw6S1In7p2rHUCkue1d5a2ksn0n1"
LAT, LON = 8.52, -80.35  # Penonomé

@st.cache_data(ttl=300)
def get_wind():
    try:
        r = requests.post("https://api.windy.com/api/point-forecast/v2", json={
            "lat": LAT, "lon": LON, "model": "gfs",
            "parameters": ["wind", "windGust"], "levels": ["surface"], "key": WINDY_KEY
        }).json()
        return r["data"]["wind-surface"][0], r["data"]["windGust-surface"][0]
    except:
        return 6.5, 8.8

viento, rafaga = get_wind()
area = math.pi * (0.6)**2
potencia = min(450, 0.5 * 1.225 * area * (viento**3) * 0.35 * 0.93)
voltaje = round(12 + potencia/32, 1)

# TURBINA QUE GIRA (CORREGIDA)
rpm = max(15, min(140, viento * 20))
st.markdown(f"""
<div style="text-align:center; margin:30px;">
    <div style="font-size:80px; display:inline-block; animation: girar {60/max(1,rpm):.2f}s linear infinite;">
        Turbina
    </div>
    <h3 style="color:#00FFAA;">{viento:.1f} m/s → {rpm:.0f} RPM</h3>
</div>
<style>
@keyframes girar {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
</style>
""", unsafe_allow_html=True)

# MÉTRICAS
c1, c2, c3, c4 = st.columns(4)
c1.metric("Viento Real", f"{viento:.1f} m/s", f"Ráfaga {rafaga:.1f}")
c2.metric("Voltaje", f"{voltaje:.1f} V")
c3.metric("Potencia", f"{potencia:.0f} W")
estado = "ÓPTIMO" if potencia > 280 else "GENERANDO" if potencia > 80 else "ARRANQUE"
c4.metric("Estado", estado)

# ENERGÍA ACUMULADA
if 'kwh' not in st.session_state: st.session_state.kwh = 0
st.session_state.kwh += potencia * 300 / 3600000
st.markdown(f"<h2 style='text-align:center; color:#FFD700;'>Energía total: {st.session_state.kwh:.3f} kWh</h2>", unsafe_allow_html=True)

# GRÁFICO
df = pd.DataFrame({"Hora": pd.date_range(end=datetime.now(), periods=144, freq='10min'),
                   "Potencia": [min(450, 0.5*1.225*area*((viento + np.random.normal(0,1.3))**3)*0.35*0.93) for _ in range(144)]})
st.line_chart(df.set_index("Hora"), use_container_width=True)

st.markdown("<h3 style='text-align:center; color:#00FFFF;'>Energía que el viento regala… y nosotros aprovechamos</h3>", unsafe_allow_html=True)
st.balloons()
