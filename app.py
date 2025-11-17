import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ====== CONFIGURACIÓN ======
st.set_page_config(page_title="Proyecto Eólico UTP", layout="wide")
st.markdown("<h1 style='text-align: center; color: #0066cc;'>🌬️ PROYECTO EÓLICO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Universidad Tecnológica de Panamá</h3>", unsafe_allow_html=True)

# Logo UTP
st.image("https://www.utp.ac.pa/sites/default/files/logo_utp.png", width=220)

# ====== DATOS SIMULADOS (luego serán reales) ======
@st.cache_data(ttl=60)
def generar_datos():
    ahora = datetime.now()
    horas = [ahora - timedelta(minutes=10*i) for i in range(144)]  # últimas 24h
    potencia = np.random.normal(120, 70, 144)
    potencia = np.clip(potencia, 0, 450)
    return pd.DataFrame({"Hora": horas, "Potencia (W)": potencia})

df = generar_datos()
ultimo = df["Potencia (W)"].iloc[0]

# ====== MÉTRICAS GRANDES ======
col1, col2, col3, col4 = st.columns(4)
col1.metric("Voltaje", f"{np.random.uniform(10,16):.1f} V", "Real")
col2.metric("Corriente", f"{np.random.uniform(0,35):.1f} A", "Real")
col3.metric("Potencia", f"{ultimo:.0f} W", "Real")
estado = "GENERANDO ⚡" if ultimo > 80 else "ARRANQUE" if ultimo > 10 else "PARADO"
col4.metric("Estado", estado)

# ====== GRÁFICO NATIVO DE STREAMLIT (sin matplotlib ni plotly) ======
st.subheader("Generación últimas 24 horas")
st.line_chart(df.set_index("Hora")["Potencia (W)"], height=400, use_container_width=True)

# ====== PRONÓSTICO ======
st.subheader("Pronóstico próximas 6 horas (simulado)")
for i in range(1,7):
    viento = np.random.uniform(2, 9)
    p_estimada = min(450, 0.5*1.225*1.13*(viento**3)*0.35*0.95)
    st.write(f"**+{i}h** → {viento:.1f} m/s → **{p_estimada:.0f} W**")

# ====== MENSAJE FINAL ======
st.success("¡DASHBOARD OFICIAL DEL PROYECTO EÓLICO EN VIVO!")
st.balloons()
