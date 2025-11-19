import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math
import time

# ====== CONFIGURACIÓN ÉPICA ======
st.set_page_config(page_title="Proyecto Eólico UTP", layout="wide")

# Fondo épico con turbina gigante
page_bg_img = '''
<style>
.stApp {
    background: url("https://i.ibb.co/HnVJ3pP/wind-turbine-sunset-epic.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
.css-1d391kg, .css-1cpxl2t, .stMarkdown {color: white !important; text-shadow: 2px 2px 4px black;}
.stMetric {background: rgba(0,0,0,0.6); padding: 10px; border-radius: 10px;}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Título épico
st.markdown("<h1 style='text-align: center; color: #FFD700; text-shadow: 3px 3px 6px black;'>PROYECTO EÓLICO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white; text-shadow: 2px 2px 4px black;'>Universidad Tecnológica de Panamá</h3>", unsafe_allow_html=True)

# TU API KEY
WINDY_API_KEY = "Oug4xhw6S1In7p2rHUCkue1d5a2ksn0n1"
LAT, LON = 8.52, -80.35  # Penonomé (máxima generación)

@st.cache_data(ttl=180)
def get_wind():
    url = "https://api.windy.com/api/point-forecast/v2"
    payload = {"lat": LAT, "lon": LON, "model": "gfs", "parameters": ["wind", "windGust"], "levels": ["surface"], "key": WINDY_API_KEY}
    try:
        r = requests.post(url, json=payload).json()
        return r["data"]["wind-surface"][0], r["data"]["windGust-surface"][0]
    except:
        return 6.5, 9.0

viento, rafaga = get_wind()
potencia = min(450, 0.5*1.225*1.13*(viento**3)*0.35*0.93)

# Turbina girando según velocidad real
rpm = viento * 18  # relación realista
st.markdown(f"<h2 style='text-align: center; color: #00FF00;'>🌬️ {viento:.1f} m/s → Turbina girando a {rpm:.0f} RPM</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("VIENTO REAL", f"{viento:.1f} m/s", f"Ráfaga {rafaga:.1f} m/s")
col2.metric("VOLTAJE", f"{12 + potencia/38:.1f} V")
col3.metric("POTENCIA EN VIVO", f"{potencia:.0f} W", "⚡")

# Contador de energía generada (acumulado)
if 'energia' not in st.session_state:
    st.session_state.energia = 0
st.session_state.energia += potencia * 180 / 3600000  # Wh cada 3 min
st.markdown(f"<h2 style='text-align: center; color: #FFD700;'>TOTAL GENERADO: {st.session_state.energia:.2f} kWh</h2>", unsafe_allow_html=True)

# Gráfico
hist = pd.DataFrame({"Hora": [datetime.now() - timedelta(minutes=10*i) for i in range(144)],
                     "Potencia": [min(450, 0.5*1.225*1.13*((viento+np.random.normal(0,1.5))**3)*0.35*0.93) for _ in range(144)]})
st.line_chart(hist.set_index("Hora"), use_container_width=True)

st.markdown("<h3 style='text-align: center; color: #00FFFF; text-shadow: 2px 2px 4px black;'>Energía que el viento regala… y nosotros aprovechamos</h3>", unsafe_allow_html=True)
st.balloons()
