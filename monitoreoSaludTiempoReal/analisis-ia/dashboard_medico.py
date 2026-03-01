import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import os
import numpy as np
from datetime import datetime

# Inicializar la memoria del Dashboard
if 'historial_envios' not in st.session_state:
    st.session_state.historial_envios = []
if 'registro_panico' not in st.session_state:
    st.session_state.registro_panico = []
if "historial_ia" not in st.session_state:
    st.session_state.historial_ia = []
       
st.set_page_config(page_title="Monitor de Salud IA - Pro", layout="wide")

# Estilo personalizado
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 40px; color: #ff4b4b; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 Sistema Inteligente de Monitoreo Médico")
st.caption("Análisis de telemetría en tiempo real con detección de derivas peligrosas")

# URLs
URL_JAVA = 'http://backend-medico:8080/alertas'
URL_CONCLUSION = "http://backend-medico:8080/alertas/conclusion"

# 1. Obtención de datos
try:
    response = requests.get(URL_JAVA, timeout=5)
    df = pd.DataFrame(response.json())
except:
    st.error("❌ Error de comunicación con el Backend de Java")
    st.stop()

if not df.empty:
    # --- PRE-PROCESAMIENTO ---
    df['tendencia_frecuencia'] = df['frecuencia'].rolling(window=3).mean()
    df['cambio_pulso'] = df['frecuencia'].diff()
    derivas_peligrosas = df[df['cambio_pulso'].abs() > 15].copy()

    # --- MÉTRICAS CLAVE (KPIs) ---
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Registros", len(df))
    with m2:
        max_pulso = int(df['frecuencia'].max())
        st.metric("Pulso Máx.", f"{max_pulso} BPM", delta=f"{max_pulso-80} vs normal")
    with m3:
        avg_o2 = round(df['oxigeno'].mean(), 1)
        st.metric("Media Oxígeno", f"{avg_o2}%")
    with m4:
        st.metric("Alertas Críticas", len(derivas_peligrosas), delta_color="inverse")

    st.divider()

    # --- GRÁFICOS PRINCIPALES ---
    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
        st.subheader("📈 Análisis de Frecuencia Cardíaca")
        fig_pulso, ax_pulso = plt.subplots(figsize=(8, 4))
        ax_pulso.plot(df.index, df['frecuencia'], color='#d3d3d3', alpha=0.5)
        ax_pulso.plot(df.index, df['tendencia_frecuencia'], color='#ff4b4b', linewidth=2)
        ax_pulso.axhline(y=100, color='r', linestyle='--', alpha=0.3)
        ax_pulso.axhline(y=60, color='g', linestyle='--', alpha=0.3)
        st.pyplot(fig_pulso) 

    with col_graf2:
        st.subheader("📉 Estabilidad de Oxígeno")
        fig_o2, ax_o2 = plt.subplots(figsize=(8, 4))
        ax_o2.fill_between(df.index, df['oxigeno'], 90, color='#3498db', alpha=0.2)
        ax_o2.plot(df.index, df['oxigeno'], color='#2980b9', linewidth=2)
        ax_o2.set_ylim(85, 102) 
        st.pyplot(fig_o2)
        
    # --- ANÁLISIS DE CORRELACIÓN ---
    st.divider()
    st.subheader("🧪 Análisis de Correlación: Pulso vs Oxígeno")
    col_corr1, col_corr2 = st.columns([2, 1])

    with col_corr1:
        fig_corr, ax_corr = plt.subplots(figsize=(10, 5))
        ax_corr.scatter(df['frecuencia'], df['oxigeno'], alpha=0.5, c='#3498db')
        rect = plt.Rectangle((60, 95), 40, 5, color='green', alpha=0.1, label="Zona Normalidad")
        ax_corr.add_patch(rect)
        ax_corr.set_xlabel("Frecuencia Cardíaca (BPM)")
        ax_corr.set_ylabel("Saturación Oxígeno (%)")
        st.pyplot(fig_corr)

    with col_corr2:
        st.write("**Interpretación del Analista**")
        correlacion = df['frecuencia'].corr(df['oxigeno'])
        st.info(f"Coeficiente de correlación: **{correlacion:.2f}**")
        if abs(correlacion) < 0.3:
            st.write("✅ Estabilidad detectada.")
        else:
            st.warning("⚠️ Relación detectada entre pulso y oxígeno.")

    # --- PREDICCIÓN ML ---
    st.divider()
    st.subheader("🔮 Predicción de Tendencia (Machine Learning)")
    if len(df) > 10:
        y = df['frecuencia'].tail(20).values
        x = np.arange(len(y)).reshape(-1, 1)
        slope, intercept = np.polyfit(x.flatten(), y, 1)
        prediccion_futura = slope * (len(y) + 60) + intercept
        
        cp1, cp2 = st.columns(2)
        cp1.metric("Velocidad de Cambio", f"{slope:.2f} BPM/seg")
        cp2.metric("Predicción +60s", f"{prediccion_futura:.1f} BPM", delta=f"{slope*60:.1f}")
    else:
        st.info("Esperando más datos para predecir...")

    # --- TABLA DE DATOS ---
    st.divider()
    st.subheader("📋 Registro de Telemetría")
    filtro_riesgo = st.checkbox("Mostrar solo anomalías")
    df_mostrar = derivas_peligrosas if filtro_riesgo else df.tail(15)
    st.dataframe(df_mostrar, use_container_width=True)

    # --- BARRA LATERAL (CENTRO DE MANDO) ---
    st.sidebar.header("🧠 IA Engine & Acciones")
    
    # Botón de Pánico
    if st.sidebar.button('🚨 BOTÓN DE PÁNICO', use_container_width=True):
        hora_p = datetime.now().strftime("%H:%M:%S")
        st.session_state.registro_panico.append(f"⚠️ [{hora_p}] Intervención manual.")
        st.sidebar.error("¡Pánico registrado!")

    # Botón Diagnóstico
    if st.sidebar.button('🚀 EJECUTAR DIAGNÓSTICO IA', use_container_width=True):
        f_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Lógica de envío a Java
        if not derivas_peligrosas.empty:
            for _, fila in derivas_peligrosas.iterrows():
                conc = {"alertaId": int(fila['id']), "diagnostico": "Deriva detectada por IA", "nivelRiesgo": "ALTO"}
                requests.post(URL_CONCLUSION, json=conc)
                st.session_state.historial_envios.append(f"PAC-{fila['id']} | Enviado {f_hora}")
        
        # Guardar en historial de sesión
        nuevo_reg = {"hora": f_hora, "bpm": df['frecuencia'].mean()}
        st.session_state.historial_ia.append(nuevo_reg)
        st.balloons()

    # --- HISTORIALES (Abajo del todo) ---
    st.divider()
    hcol1, hcol2 = st.columns(2)
    with hcol1:
        st.subheader("📜 Historial de Conclusiones")
        for h in reversed(st.session_state.historial_envios[-5:]): st.info(h)
    with hcol2:
        st.subheader("🚨 Registro de Pánico")
        for p in reversed(st.session_state.registro_panico[-5:]): st.warning(p)

    # --- MÓDULO R ---
    st.divider()
    st.subheader("🧬 Módulo de Bioestadística (R)")
    if st.button("📊 GENERAR REPORTE EN R"):
        df.to_csv("datos_para_r.csv", index=False)
        try:
            subprocess.run(["Rscript", "analisis_clinico.R"], check=True)
            if os.path.exists("informe_estadistico.pdf"):
                with open("informe_estadistico.pdf", "rb") as f:
                    st.download_button("📥 Descargar PDF de R", f, "analisis.pdf", "application/pdf")
        except:
            st.error("Error al ejecutar R")

# Historial sidebar siempre visible
st.sidebar.subheader("⏱️ Últimos Diagnósticos")
for item in st.session_state.historial_ia[-5:]:
    st.sidebar.write(f"{item['hora']} - {item['bpm']:.1f} BPM")