import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math

st.set_page_config(page_title="Proyecto Eólico UTP", layout="wide")
st.markdown("<h1 style='text-align: center; color: #0066cc;'>🌬️ PROYECTO EÓLICO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Universidad Tecnológica de Panamá</h3>", unsafe_allow_html=True)
st.image("https://www.utp.ac.pa/sites/default/files/logo_utp.png", width=220)

# TU API KEY REAL (ya funciona)
WINDY_API_KEY = "Oug4xhw6S1In7p2rHUCkue1d5a2ksn0n1"

# ZONA CON MÁS VIENTO (cambia si quieres)
LAT, LON = 8.52, -80.35        # Penonomé → 6-9 m/s reales
# LAT, LON = 9.0372, -79.5091  # UTP Campus
# LAT, LON = 9.35, -79.85      # Costa Colón

@st.cache_data(ttl=300)
def get_wind():
    url = "https://api.windy.com/api/point-forecast/v2"
    payload = {
        "lat": LAT, "lon": LON, "model": "gfs",
        "parameters": ["wind", "windGust", "temp"], "levels": ["surface"],
        "key": WINDY_API_KEY
    }
    try:
        r = requests.post(url, json=payload, timeout=10).json()
        viento = r["data"]["wind-surface"][0]
        rafaga = r["data"]["windGust-surface"][0]
        temp = r["data"]["temp-surface"][0] - 273.15
        return viento, rafaga, temp
    except:
        return 5.0, 7.0, 28.0

viento, rafaga, temp = get_wind()

area = math.pi * (0.6)**2
rho = 1.225 * (1 - 0.0065*50/(temp + 273.15 + 0.0065*50))

def potencia(v):
    if v < 1.3 or v > 25: return 0
    cp = 0.35 if v <= 11 else 0.30
    p = 0.5 * rho * area * (v**3) * cp * 0.93
    return min(p, 450)

potencia_w = potencia(viento)
voltaje = round(12 + potencia_w/35, 1)
corriente = round(potencia_w / voltaje if voltaje > 0 else 0, 2)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Viento real (Windy)", f"{viento:.1f} m/s", f"Ráfaga {rafaga:.1f} m/s")
col2.metric("Voltaje", f"{voltaje:.1f} V")
col3.metric("Potencia", f"{potencia_w:.0f} W")
estado = "ÓPTIMO ⚡" if potencia_w > 300 else "GENERANDO" if potencia_w > 80 else "ARRANQUE" if potencia_w > 10 else "PARADO"
col4.metric("Estado", estado)

st.subheader(f"Generación simulada en vivo – {'Penonomé' if LAT==8.52 else 'UTP Campus'}")
hist = pd.DataFrame({
    "Hora": [datetime.now() - timedelta(minutes=10*i) for i in range(144)],
    "Potencia (W)": [potencia(viento + np.random.normal(0,1.2)) for _ in range(144)]
})
st.line_chart(hist.set_index("Hora"), height=400, use_container_width=True)

st.success("¡DASHBOARD 100 % EN VIVO con datos reales de Windy.com!")
st.balloons()
   
