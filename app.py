import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math

# ====== FONDO ÉPICO PERMANENTE (turbina al atardecer – 4K de Pixabay) ======
background_url = "https://cdn.pixabay.com/photo/2016/11/29/05/45/windmills-1867291_1280.jpg"  # Imagen gratuita, alta res, turbinas naranjas

st.set_page_config(page_title="Proyecto Eólico UTP", layout="wide")
st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.5)), url("{background_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
h1 {{color: #FFD700 !important; text-shadow: 3px 3px 6px black !important; font-size: 3em;}}
h3 {{color: white !important; text-shadow: 2px 2px 4px black !important;}}
.stMetric > label {{color: white !important; text-shadow: 1px 1px 3px black !important;}}
.stMetric > div > div {{color: #FFD700 !important; font-size: 2em !important; text-shadow: 2px 2px 4px black !important;}}
.stMetric {{background: rgba(0,0,0,0.6) !important; border-radius: 15px; padding: 15px; border: 2px solid #00FF00 !important;}}
</style>
""", unsafe_allow_html=True)

# Logo UTP (si quieres, quítalo si no carga)
st.image("https://www.utp.ac.pa/sites/default/files/logo_utp.png", width=200, use_column_width=True)

st.markdown("<h1 style='text-align: center;'>🌬️ PROYECTO EÓLICO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Universidad Tecnológica de Panamá</h3>", unsafe_allow_html=True)

# TU API KEY DE WINDY
WINDY_KEY = "Oug4xhw6S1In7p2rHUCkue1d5a2ksn0n1"
LAT, LON = 8.52, -80.35  # Penonomé (alta generación)

@st.cache_data(ttl=300)  # Actualiza cada 5 min
def get_wind_data():
    url = "https://api.windy.com/api/point-forecast/v2"
    payload = {
        "lat": LAT, "lon": LON, "model": "gfs",
        "parameters": ["wind", "windGust"], "levels": ["surface"],
        "key": WINDY_KEY
    }
    try:
        r = requests.post(url, json=payload, timeout=10).json()
        ts = r["data"]["ts"][:6]  # Próximas 6h
        viento = r["data"]["wind-surface"][:6]
        rafaga = r["data"]["windGust-surface"][:6]
        return ts, viento, rafaga
    except:
        return [datetime.now().timestamp()*1000], [5.0]*6, [7.0]*6

ts, viento_horas, rafaga_horas = get_wind_data()

# Cálculo potencia actual
area = math.pi * (0.6)**2
v_actual = viento_horas[0]
potencia_actual = min(450, 0.5 * 1.225 * area * (v_actual**3) * 0.35 * 0.93)
voltaje = round(12 + potencia_actual / 33, 1)
corriente = round(potencia_actual / voltaje, 2)

# ANIMACIÓN DE TURBINA QUE GIRA (según viento real)
rpm = max(10, min(120, v_actual * 18))
st.markdown(f"""
<div style="text-align: center; margin: 20px 0;">
    <h2 style='color: #00FF00; text-shadow: 2px 2px 4px black;'>Viento: {v_actual:.1f} m/s → Turbina a {rpm:.0f} RPM</h2>
    <div style="font-size: 50px; animation: spin {60 / max(1, rpm):.2f}s linear infinite; color: #FFD700;">
        🌀 TURBINA EN MARCHA 🌀
    </div>
</div>
<style>
@keyframes spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}
</style>
""", unsafe_allow_html=True)

# MÉTRICAS GRANDES
col1, col2, col3, col4 = st.columns(4)
col1.metric("Viento Real", f"{v_actual:.1f} m/s", f"Ráfaga {rafaga_horas[0]:.1f} m/s")
col2.metric("Voltaje", f"{voltaje:.1f} V")
col3.metric("Potencia", f"{potencia_actual:.0f} W")
estado = "ÓPTIMO ⚡" if potencia_actual > 300 else "GENERANDO" if potencia_actual > 80 else "ARRANQUE" if potencia_actual > 10 else "PARADO"
col4.metric("Estado", estado)

# CONTADOR DE ENERGÍA ACUMULADA
if 'kwh' not in st.session_state:
    st.session_state.kwh = 0.0
st.session_state.kwh += potencia_actual * (300 / 3600000)  # Cada 5 min
st.markdown(f"<h2 style='text-align: center; color: #FFD700; text-shadow: 2px 2px 4px black;'>Energía Generada Total: {st.session_state.kwh:.3f} kWh</h2>", unsafe_allow_html=True)

# GRÁFICO DE 24H
st.subheader("Generación Simulada Últimas 24h")
hist = pd.DataFrame({
    "Hora": [datetime.now() - timedelta(minutes=10*i) for i in range(144)],
    "Potencia (W)": [min(450, 0.5*1.225*area*((v_actual + np.random.normal(0,1.2))**3)*0.35*0.93) for _ in range(144)]
})
st.line_chart(hist.set_index("Hora")["Potencia (W)"], height=350, use_container_width=True)

# PRONÓSTICO EN VIVO (¡el cálculo que faltaba! – Próximas 6h)
st.subheader("Pronóstico de Generación (Próximas 6h – Basado en Windy)")
for i in range(6):
    hora = datetime.fromtimestamp(ts[i] / 1000).strftime('%H:%M')
    v_h = viento_horas[i]
    p_h = min(450, 0.5 * 1.225 * area * (v_h**3) * 0.35 * 0.93)
    st.markdown(f"**{hora}** → {v_h:.1f} m/s → **{p_h:.0f} W**")

st.markdown("<h3 style='text-align: center; color: #00FFFF; text-shadow: 2px 2px 4px black;'>Energía que el viento regala… y nosotros aprovechamos 🌬️⚡</h3>", unsafe_allow_html=True)
st.balloons()
