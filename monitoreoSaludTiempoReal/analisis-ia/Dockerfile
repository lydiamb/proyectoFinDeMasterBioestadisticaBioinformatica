FROM python:3.11-slim
WORKDIR /app
# Copiamos los requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copiamos el resto del código
COPY . .
EXPOSE 8501
# Comando para lanzar Streamlit
ENTRYPOINT ["streamlit", "run", "dashboard_medico.py", "--server.port=8501", "--server.address=0.0.0.0"]