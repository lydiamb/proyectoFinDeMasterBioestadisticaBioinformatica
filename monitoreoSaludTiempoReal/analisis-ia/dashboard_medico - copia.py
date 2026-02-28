import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Monitor de Salud IA", layout="wide")

st.title("🏥 Panel de Control Médico - Análisis de Tendencias")

# URL interna de Docker hacia tu endpoint de Java
URL_JAVA = 'http://backend-medico:8080/alertas'
URL_CONCLUSION = "http://backend-medico:8080/alertas/conclusion"

# 1. Obtención de datos desde Java
try:
    response = requests.get(URL_JAVA, timeout=5)
    df = pd.DataFrame(response.json())
except:
    st.error("❌ No se pudo conectar con el servidor Java. ¿Está encendido?")
    st.stop()

if not df.empty:
    # 2. ANÁLISIS DE TENDENCIAS (Media Móvil)
    df['tendencia_frecuencia'] = df['frecuencia'].rolling(window=3).mean()
    df['tendencia_oxigeno'] = df['oxigeno'].rolling(window=3).mean()

    # 2.5 ANÁLISIS DE DERIVA (Cambio rápido)
    # Calculamos la diferencia entre la medición actual y la anterior
    df['cambio_pulso'] = df['frecuencia'].diff()

    # Si el pulso cambia más de 15 puntos entre dos mediciones, es una alerta de deriva
    derivas_peligrosas = df[df['cambio_pulso'].abs() > 15].copy()

    if not derivas_peligrosas.empty:
        st.warning(f"⚠️ Se han detectado {len(derivas_peligrosas)} cambios bruscos de ritmo (Deriva Peligrosa).")
    
    # 3. DISEÑO DEL PANEL (Columnas)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Tendencia de Ritmo Cardíaco")
        fig_pulso, ax_pulso = plt.subplots()
        ax_pulso.plot(df.index, df['frecuencia'], label="Real", alpha=0.4, color='gray')
        ax_pulso.plot(df.index, df['tendencia_frecuencia'], label="Tendencia (Media)", color='red', linewidth=2)
        ax_pulso.legend()
        st.pyplot(fig_pulso)

    with col2:
        st.subheader("📉 Tendencia de Oxígeno")
        fig_o2, ax_o2 = plt.subplots()
        ax_o2.plot(df.index, df['oxigeno'], label="Real", alpha=0.4, color='gray')
        ax_o2.plot(df.index, df['tendencia_oxigeno'], label="Tendencia (Media)", color='blue', linewidth=2)
        ax_o2.legend()
        st.pyplot(fig_o2)

    # 4. TABLA DE ALERTAS RECIENTES
    st.divider()
    st.subheader("📋 Últimos Registros en Base de Datos")
    st.dataframe(df.tail(10), use_container_width=True)
    
    st.subheader("🧠 Centro de Mando IA")

    # 5. BOTÓN PARA ENVIAR FEEDBACK A JAVA (CORREGIDO PARA DERIVAS)
    if st.button('Ejecutar diagnóstico IA y enviar a Java'):
        if not derivas_peligrosas.empty:
            conteo = 0
            with st.spinner('IA analizando derivas peligrosas...'):
                for _, fila in derivas_peligrosas.iterrows():
                    # Determinamos el tipo de deriva para el diagnóstico
                    tipo_deriva = "Aumento brusco" if fila['cambio_pulso'] > 0 else "Caída brusca"
                    
                    # Construimos el objeto para Java
                    conclusion = {
                        "alertaId": int(fila['id']), 
                        "diagnostico": f"DERIVA DETECTADA: {tipo_deriva} de {abs(fila['cambio_pulso']):.1f} bpm.",
                        "nivelRiesgo": "CRÍTICO" if abs(fila['cambio_pulso']) > 25 else "ALTO"
                    }
                    
                    try:
                        res = requests.post(URL_CONCLUSION, json=conclusion, timeout=5)
                        if res.status_code == 200:
                            conteo += 1
                    except Exception as e:
                        st.error(f"Error enviando conclusión para ID {fila['id']}: {e}")
            
            if conteo > 0:
                st.success(f"✅ Análisis completado: Enviadas {conteo} conclusiones por derivas peligrosas a Java.")
                st.balloons()
        else:
            st.info("La IA no ha detectado derivas peligrosas (cambios > 15 bpm) en los datos actuales.")
else:
    st.info("Esperando datos del simulador...")