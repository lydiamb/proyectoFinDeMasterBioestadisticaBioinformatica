import requests
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# 1. Obtenemos los datos de tu API de Spring Boot
try:
    response = requests.get('http://localhost:8080/alertas')
    data = response.json()
    df = pd.DataFrame(data)
except:
    print("Error: Asegúrate de que Spring Boot esté corriendo en el puerto 8080")
    exit()

if df.empty:
    print("No hay datos suficientes para analizar.")
    exit()

# 2. Preparamos el modelo de detección de anomalías
# El algoritmo "aprenderá" qué frecuencias son normales
model = IsolationForest(contamination=0.1, random_state=42)
df['anomalia'] = model.fit_predict(df[['frecuencia']])

# -1 significa anomalía, 1 significa normal
alertas_graves = df[df['anomalia'] == -1]

print(f"✅ Se han analizado {len(df)} registros.")
print(f"🚨 Anomalías estadísticas detectadas:\n", alertas_graves)

# 3. Visualización (Muy útil para tu Máster)
plt.figure(figsize=(10, 6))
plt.scatter(df.index, df['frecuencia'], c=df['anomalia'], cmap='rdylgn')
plt.axhline(y=100, color='r', linestyle='--', label='Límite Taquicardia')
plt.title('Análisis de Frecuencia Cardíaca (Detección por ML)')
plt.xlabel('Número de Medición')
plt.ylabel('BPM')
plt.show()

input("\nPresiona Enter para cerrar el programa...")