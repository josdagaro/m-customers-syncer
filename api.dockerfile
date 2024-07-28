# Utilizar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Copiar el archivo requirements.txt al contenedor
COPY api-requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r api-requirements.txt

# Copiar el script de espera al contenedor
COPY wait-for-db-ready.sh /app/wait-for-db-ready.sh
RUN chmod +x /app/wait-for-db-ready.sh

# Copiar el código de la aplicación al contenedor
COPY . .

# Ejecutar la aplicación usando el script de espera
CMD ["./wait-for-db-ready.sh", "db", "--", "python", "api.py"]
