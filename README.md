# ml-challenge-syncer

Esta aplicación consume datos desde una API externa y los almacena de manera segura en una base de datos MySQL. La aplicación implementa varias prácticas de seguridad para cumplir con estándares como PCI DSS y NIST, incluyendo el cifrado de datos sensibles.

## Funcionalidades

- Consume datos de una API externa.
- Cifra datos sensibles antes de almacenarlos.
- Almacena los datos en una base de datos MySQL.

## Requisitos Previos

- Docker
- Docker Compose

## Instalación de Docker

Para instalar Docker, sigue los pasos a continuación según tu sistema operativo:

### En Ubuntu

```sh
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### En MacOS

Descarga el instalador haciendo click [aquí](https://www.docker.com/products/docker-desktop).

## Instalación de Docker Compose

Para instalar Docker Compose, sigue los pasos a continuación:

### En Ubuntu

```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### En macOS y Windows

Docker Compose viene incluido con Docker Desktop.

## Ejecución de la Aplicación

1. Clona este repositorio y navega al directorio del proyecto:

```sh
git clone https://github.com/josdagaro/ml-challenge-syncer.git
cd ml-challenge-syncer
```

2. Asegúrate de que los siguientes archivos estén en el directorio del proyecto:
    - docker-compose.yml
    - Dockerfile
    - requirements.txt
    - wait-for-db-ready.sh
    - app.py

    Entre otros.

3. Ejecuta la aplicación con Docker Compose:

    `docker-compose up --build`

    Esto construirá las imágenes de Docker, instalará las dependencias necesarias y ejecutará la aplicación que consume los datos de la API y los almacena en la base de datos MySQL.

## Conexión a la Base de Datos MySQL
Para conectarte a la base de datos MySQL y verificar los datos almacenados:

1. Abre una terminal y ejecuta el siguiente comando para acceder al contenedor de MySQL:

    `docker exec -it mysql_db mysql -u root -p`

2. Cuando se te solicite, ingresa la contraseña de root configurada en el archivo `docker-compose.yml` (por ejemplo: example).

3. Una vez que estés en el shell de MySQL, selecciona la base de datos y consulta los datos:

    ```sql
    USE testdb;
    SELECT * FROM usuarios;
    ```

    Esto te permitirá ver los datos almacenados en la tabla usuarios.

## Seguridad y Cumplimiento

La aplicación app.py implementa varias prácticas de seguridad para cumplir con algunos estándares. Para conocer más detalles al respecto, por favor haga click [aquí](https://github.com/josdagaro/ml-challenge-syncer/blob/main/docs/sec-analysis.md).
