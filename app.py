import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math

# ===================== CONFIGURACIÓN Y FONDO ÉPICO =====================
st.set_page_config(page_title="Proyecto Eólico UTP", layout="wide")

# Fondo local (la imagen que ya subiste como background.jpg)
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.65)), url("background.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
h1, h2, h3, h4 { color: white !important; text-shadow: 2px 2px 8px black !important; }
.stMetric { background: rgba(0,0,0,0.7); border-radius: 15px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# Logo UTP + Título épico
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    st.image("https://www.utp.ac.pa/sites/default/files/logo_utp.png", width=140)
with col_titulo:
    st.markdown("<h1 style='text-align:center; color:#FFD700; margin-top:20px;'>PROYECTO EÓLICO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#00FFFF;'>Universidad Tecnológica de Panamá - Penonomé</h3>", unsafe_allow_html=True)

# ===================== DATOS EN VIVO DE WINDY =====================
WINDY_KEY = "Oug4xhw6S1In7p2rHUCkue1d5a2ksn0n1"
LAT, LON = 8.52, -80.35

@st.cache_data(ttl=300)  # Se actualiza cada 5 minutos
def obtener_datos_viento():
    try:
        url = "https://api.windy.com/api/point-forecast/v2"
        payload = {
            "lat": LAT, "lon": LON,
            "model": "gfs",
            "parameters": ["wind", "windGust"],
            "levels": ["surface"],
            "key": WINDY_KEY
        }
        r = requests.post(url, json=payload, timeout=10).json()
        viento = r["data"]["wind-surface"][0]
        rafaga = r["data"]["windGust-surface"][0]
        return viento, rafaga
    except:
        return 6.8, 9.5  # Valores de respaldo

viento, rafaga = obtener_datos_viento()

# Cálculo de potencia (turbina pequeña realista)
area_barrido = math.pi * (0.6)**2
potencia_w = min(450, 0.5 * 1.225 * area_barrido * (viento**3) * 0.35 * 0.93)
voltaje = round(12 + potencia_w/32, 1)

# ===================== TURBINA QUE GIRA SEGÚN EL VIENTO REAL =====================
rpm = max(15, min(140, viento * 20))
st.markdown(f"""
<div style="text-align:center; margin:40px 0;">
    <div style="font-size:100px; display:inline-block; animation: girar {60/max(1,rpm):.2f}s linear infinite;">
        Wind Turbine
    </div>
    <h2 style="color:#00FFAA; margin-top:10px;">
        {viento:.1f} m/s → {rpm:.0f} RPM
    </h2>
</div>
<style>
@keyframes girar {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)

# ===================== MÉTRICAS GRANDES =====================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Viento Actual", f"{viento:.1f} m/s", f"Ráfaga {rafaga:.1f} m/s")
col2.metric("Voltaje", f"{voltaje:.1f} V")
col3.metric("Potencia en Vivo", f"{potencia_w:.0f} W", "Live")
estado = "ÓPTIMO Live" if potencia_w > 280 else "GENERANDO" if potencia_w > 80 else "ARRANQUE"
col4.metric("Estado Turbina", estado)

# ===================== ENERGÍA ACUMULADA =====================
if 'kwh_total' not in st.session_state:
    st.session_state.kwh_total = 0.0
st.session_state.kwh_total += potencia_w * 300 / 3600000  # cada 5 min
st.markdown(f"<h2 style='text-align:center; color:#FFD700; margin:30px;'>Energía Generada Total: {st.session_state.kwh_total:.3f} kWh</h2>", unsafe_allow_html=True)

# ===================== GRÁFICO DE GENERACIÓN =====================
st.subheader("Live Generación simulada (últimas 24h)")
historia = pd.DataFrame({
    "Hora": pd.date_range(end=datetime.now(), periods=144, freq='10min'),
    "Potencia (W)": [min(450, 0.5*1.225*area_barrido*((viento + np.random.normal(0,1.3))**3)*0.35*0.93) for _ in range(144)]
})
st.line_chart(historia.set_index("Hora"), use_container_width=True, height=300)

# ===================== FRASE FINAL ÉPICA =====================
st.markdown("<h3 style='text-align:center; color:#00FFFF; margin:40px;'>Energía que el viento regala… y nosotros aprovechamos Live Live</h3>", unsafe_allow_html=True)

# Globos porque ya ganaste
st.balloons()
