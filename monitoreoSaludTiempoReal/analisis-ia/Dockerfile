# 1. Usamos una base de Python
FROM python:3.11-slim

# 2. Instalamos R y dependencias del sistema para PDFs
RUN apt-get update && apt-get install -y \
    r-base \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    # Necesario para que R genere PDFs
    pandoc \
    && rm -rf /var/lib/apt/lists/*

# 3. Instalamos las librerías de R (ggplot2, qrcode, gridExtra)
# Lo hacemos aquí para que se queden grabadas en la imagen
RUN R -e "install.packages(c('ggplot2', 'gridExtra', 'qrcode'), repos='http://cran.rstudio.com/')"

# 4. Preparamos el entorno de Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto del código (incluyendo los scripts .R)
COPY . .

# 6. Exponemos el puerto de Streamlit
EXPOSE 8501

CMD ["streamlit", "run", "dashboard_medico.py", "--server.port=8501", "--server.address=0.0.0.0"]