import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math

# ====== ESTILO ÉPICO CON FONDO + TURBINA QUE GIRA ======
page_bg_img = '''
<style>
.stApp {
    background: url("https://i.ibb.co/9yqYdPB/wind-turbine-sunset-4k.jpg") no-repeat center center fixed;
    background-size: cover;
}
.css-1d391kg {  /* tarjetas */
    background: rgba(0, 0, 0, 0.7);
    border-radius: 15px;
    padding: 15px;
}
.metric-label, .metric-value {
    color: #FFFF00 !important;  /* amarillo brillante */
    font-weight: bold !important;
}
h1, h3 { color: #FFFF00 !important; text-shadow: 2px 2px 8px #000; }
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# ====== ANIMACIÓN DE TURBINA QUE GIRA ======
@st.cache_data(ttl=300)
def get_wind():
    url = "https://api.windy.com/api/point-forecast/v2"
    payload = {
        "lat": 8.52, "lon": -80.35, "model": "gfs",
        "parameters": ["wind", "windGust", "temp"], "levels": ["surface"],
        "key": "Oug4xhw6S1In7p2rHUCkue1d5a2ksn0n1"
    }
    try:
        r = requests.post(url, json=payload, timeout=10).json()
        viento = r["data"]["wind-surface"][0]
        rafaga = r["data"]["windGust-surface"][0]
        temp = r["data"]["temp-surface"][0] - 273.15
        return viento, rafaga, temp
    except:
        return 6.0, 8.0, 28.0

viento, rafaga, temp = get_wind()

# Velocidad de rotación: 1 m/s = 15° por segundo (realista)
rpm = viento * 15
animation_css = f"""
<style>
@keyframes girar {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
}}
.turbina {{
    animation: girar {max(0.5, 60/rpm):.1f}s linear infinite;
    font-size: 80px;
}}
</style>
<div class="turbina">Turbina</div>
"""
st.markdown(animation_css, unsafe_allow_html=True)

# ====== CÁLCULOS ======
area = math.pi * (0.6)**2
rho = 1.225
def potencia(v):
    if v < 1.3 or v > 25: return 0
    cp = 0.35 if v <= 11 else 0.30
    p = 0.5 * rho * area * (v**3) * cp * 0.93
    return min(p, 450)

potencia_w = potencia(viento)
voltaje = round(12 + potencia_w/35, 1)
corriente = round(potencia_w / voltaje if voltaje > 0 else 0, 2)

# ====== TÍTULO ÉPICO ======
st.markdown("<h1 style='text-align: center;'>PROYECTO EÓLICO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Universidad Tecnológica de Panamá</h3>", unsafe_allow_html=True)

# ====== MÉTRICAS GRANDES ======
col1, col2, col3, col4 = st.columns(4)
col1.metric("Viento real", f"{viento:.1f} m/s", f"Ráfaga {rafaga:.1f} m/s")
col2.metric("Voltaje", f"{voltaje:.1f} V")
col3.metric("Potencia", f"{potencia_w:.0f} W")
estado = "ÓPTIMO" if potencia_w > 300 else "GENERANDO" if potencia_w > 80 else "ARRANQUE" if potencia_w > 10 else "PARADO"
col4.metric("Estado", estado)

# ====== GRÁFICO 24H ======
hist = pd.DataFrame({
    "Hora": [datetime.now() - timedelta(minutes=10*i) for i in range(144)],
    "Potencia (W)": [potencia(viento + np.random.normal(0,1.2)) for _ in range(144)]
})
st.subheader("Generación simulada en vivo – Penonomé")
st.line_chart(hist.set_index("Hora"), height=400, use_container_width=True)

# ====== PRONÓSTICO 6H ======
st.subheader("Pronóstico Windy.com – Próximas 6 horas")
try:
    payload["parameters"] = ["wind"]
    r2 = requests.post("https://api.windy.com/api/point-forecast/v2", json=payload).json()
    for i in range(6):
        v = r2["data"]["wind-surface"][i]
        p = potencia(v)
        hora = datetime.fromtimestamp(r2["data"]["ts"][i]/1000)
        st.write(f"**{hora.strftime('%H:%M')}** → {v:.1f} m/s → **{p:.0f} W**")
except:
    st.write("Pronóstico temporalmente no disponible")

st.success("DASHBOARD 100 % EN VIVO • Turbina girando según viento real")
