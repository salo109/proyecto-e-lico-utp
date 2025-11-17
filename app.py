import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Proyecto Eólico UTP", layout="wide")
st.markdown("<h1 style='text-align: center; color: #0066cc;'>🌬️ PROYECTO EÓLICO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Universidad Tecnológica de Panamá</h3>", unsafe_allow_html=True)
st.image("https://www.utp.ac.pa/sites/default/files/logo_utp.png", width=200, use_column_width=True)

# Datos simulados
@st.cache_data(ttl=60)
def datos():
    hora = datetime.now()
    horas = [hora - timedelta(hours=i) for i in range(24)]
    potencia = np.random.normal(120, 60, 24)
    potencia = np.clip(potencia, 0, 450)
    return pd.DataFrame({"Hora": horas, "Potencia (W)": potencia})

df = datos()
ultimo = df["Potencia (W)"].iloc[0]

# Métricas
col1, col2, col3, col4 = st.columns(4)
col1.metric("Voltaje", f"{np.random.uniform(10,16):.1f} V")
col2.metric("Corriente", f"{np.random.uniform(0,30):.1f} A")
col3.metric("Potencia", f"{ultimo:.0f} W")
col4.metric("Estado", "GENERANDO" if ultimo > 50 else "PARADO")

# Gráfico con matplotlib
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["Hora"], df["Potencia (W)"], color='green', linewidth=3)
ax.fill_between(df["Hora"], df["Potencia (W)"], alpha=0.3, color='green')
ax.set_title("Generación Eólica - Últimas 24h")
ax.set_ylabel("Potencia (W)")
ax.grid(True, alpha=0.3)
st.pyplot(fig)

st.success("¡DASHBOARD FUNCIONANDO PERFECTAMENTE!")
st.balloons()
