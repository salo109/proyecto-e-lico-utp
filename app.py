import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(page_title="Proyecto Eólico UTP", layout="wide")
st.markdown("<h1 style='text-align: center; color: #0066cc;'>🌬️ PROYECTO EÓLICO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Universidad Tecnológica de Panamá</h3>", unsafe_allow_html=True)

# Logo UTP
st.image("https://www.utp.ac.pa/sites/default/files/logo_utp.png", width=200, use_container_width=True)

# Datos simulados (luego conectamos el PZEM real)
@st.cache_data(ttl=60)
def datos_simulados():
    ahora = datetime.now()
    horas = [ahora - timedelta(hours=i) for i in range(24)]
    potencia = np.random.normal(80, 50, 24)
    potencia = np.clip(potencia, 0, 450)
    return pd.DataFrame({"Hora": horas, "Potencia (W)": potencia})

df = datos_simulados()

# Métricas en tiempo real
ultimo = df.iloc[0]
col1, col2, col3, col4 = st.columns(4)
col1.metric("Voltaje", f"{np.random.uniform(10,15):.1f} V")
col2.metric("Corriente", f"{np.random.uniform(0,25):.2f} A")
col3.metric("Potencia Actual", f"{ultimo['Potencia (W)']:.0f} W")
estado = "PARADO" if ultimo['Potencia (W)'] < 10 else "GENERANDO"
col4.metric("Estado", estado)

# Gráfico
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Hora"], y=df["Potencia (W)"], 
                         fill='tozeroy', line=dict(color='#00ff00'), name="Potencia"))
fig.update_layout(title="Generación Eólica - Últimas 24 horas", 
                  xaxis_title="Hora", yaxis_title="Potencia (W)")
st.plotly_chart(fig, use_container_width=True)

st.success("¡Dashboard funcionando! Ahora conectaremos los datos reales de tu PZEM")
