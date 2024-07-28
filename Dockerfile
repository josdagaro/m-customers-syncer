# Utilizar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Actualizar el sistema e instalar las dependencias necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    zlib1g \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script de espera al contenedor
COPY wait-for-db-ready.sh /app/wait-for-db-ready.sh
RUN chmod +x /app/wait-for-db-ready.sh

# Copiar el código de la aplicación al contenedor
COPY . .

# Ejecutar la aplicación usando el script de espera
CMD ["./wait-for-db-ready.sh", "db", "--", "python", "app.py"]
