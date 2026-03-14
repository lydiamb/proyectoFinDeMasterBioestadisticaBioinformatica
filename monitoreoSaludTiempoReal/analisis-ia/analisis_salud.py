import requests
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# 1. Obtención de datos
try:
    response = requests.get('http://localhost:8080/alertas')
    df = pd.DataFrame(response.json())
except:
    print("Error conectando con la API")
    exit()

# 2. IA Multivariable
# Ahora usamos 'frecuencia' y 'oxigeno' para entrenar
features = ['frecuencia', 'oxigeno']
model = IsolationForest(contamination=0.15, random_state=42)
df['anomalia'] = model.fit_predict(df[features])

<<<<<<< HEAD
<<<<<<< HEAD
# 3. Filtrar las anomalías
=======
# 3. Filtrar las anomalías (ESTO ES LO QUE FALTABA)
>>>>>>> e49bf05 (suida inicial de archivos del proyecto)
=======
# 3. Filtrar las anomalías
>>>>>>> 426f304 (revisión comentarios)
# Filtramos el dataframe para quedarnos solo con los que el modelo marcó como -1
alertas = df[df['anomalia'] == -1]

# 4. Gráfica de Correlación
plt.figure(figsize=(10, 7))
scatter = plt.scatter(df['frecuencia'], df['oxigeno'], 
                      c=df['anomalia'], cmap='RdYlGn', s=100, edgecolors='k')
plt.title('Detección Multivariable: Frecuencia vs Oxígeno')
plt.xlabel('Frecuencia Cardíaca (BPM)')
plt.ylabel('Saturación Oxígeno (%)')
plt.grid(True, alpha=0.3)
legend1 = plt.legend(*scatter.legend_elements(), title="Estado (1=Normal, -1=Anomalía)")
plt.gca().add_artist(legend1)

<<<<<<< HEAD
<<<<<<< HEAD
# Mostramos la gráfica
=======
# Mostramos la gráfica pero SIN BLOQUEAR (o ciérrala rápido para que siga el código)
>>>>>>> e49bf05 (suida inicial de archivos del proyecto)
=======
# Mostramos la gráfica
>>>>>>> 426f304 (revisión comentarios)
plt.show()

# 5. Enviar conclusiones de vuelta a Java
print(f"🤖 Procesando {len(alertas)} anomalías para enviar a Java...")

<<<<<<< HEAD
<<<<<<< HEAD


print(f"🔍 Revisando datos para enviar a Java. Total anomalías encontradas: {len(alertas)}")

=======
# ... (después de plt.show())

print(f"🔍 Revisando datos para enviar a Java. Total anomalías encontradas: {len(alertas)}")

# ... (después de plt.show())
>>>>>>> e49bf05 (suida inicial de archivos del proyecto)
=======


print(f"🔍 Revisando datos para enviar a Java. Total anomalías encontradas: {len(alertas)}")

>>>>>>> 426f304 (revisión comentarios)

print("\n--- 🕵️ INVESTIGANDO COLUMNAS ---")
columnas = list(df.columns)
print(f"Columnas detectadas: {columnas}")

alertas = df[df['anomalia'] == -1]

try:
    if alertas.empty:
        print("⚠️ No hay anomalías para enviar.")
    else:
        for index, row in alertas.iterrows():
            # Intentamos sacar el ID numérico, si no existe usamos el índice del bucle
            # para que Java no reciba un error.
            id_para_java = row.get('id', index) 
            
            # Si el ID que saca es un texto (como PAC-001), usamos el índice 'index'
            if isinstance(id_para_java, str):
                id_para_java = index

            conclusion = {
                "alertaId": int(id_para_java), 
                "diagnostico": f"IA detectó anomalía en {row['pacienteId']} (BPM: {row['frecuencia']})",
                "nivelRiesgo": "CRÍTICO" if row['oxigeno'] < 92 else "ALTO"
            }
            
            print(f"📤 Enviando a Java conclusion para: {row['pacienteId']}...")
            res = requests.post('http://localhost:8080/alertas/conclusion', json=conclusion, timeout=5)
            
            if res.status_code == 200:
                print(f"✅ ¡MENSAJE ENVIADO CON ÉXITO!")
            else:
                print(f"❌ Java rechazó el mensaje. Código: {res.status_code}")

except Exception as e:
    print("\n💥 Error inesperado:")
    import traceback
    traceback.print_exc()

input("\n🏁 Proceso terminado. Revisa la consola de Eclipse.")