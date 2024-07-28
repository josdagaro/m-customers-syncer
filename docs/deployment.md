# Despliegues

A continuación algunas aclaraciones con respecto a las fases de despliegue de la solución:

## Despliegue Local (Docker Compose)

Esta configuración se disponibiliza para pruebas locales, por lo cual para correr la aplciación en local, se hace uso los siguientes archivos y una breve descripción del motivo:

- `api.dockerfile`: Permite construir una imagen Docker de la API interna preparada para ambiente local.
- `api.py`: Contiene el código/funcionalidad de la API interna de clientes.
- `docker-compose.yml`: Contiene la configuración de servicios Docker para levantar un entorno completo local.
- `syncer.dockerfile`: Permite construir una imagen Docker del fetcher/sincronizador de API externa de provider preparada para ambiente local.
- `syncer.py`: Contiene el código/funcionalidad de obtención de datos de clientes desde el API externa del proveedor.
- `wait-for-db-ready.sh`: Es un script que garantiza que la base de datos MySQL se haya inicializado adecuadamente.

Tras levantar el entorno como ya se indicó la descripción principal del proyecto (`docker-compose up --build`), se puede interactuar con la solución, por ende algunas recomendaciones de herramientas útiles para conexión al entorno local.

**Para Conectarse a MySQL**: usar DBeaver Comunity Edition, la cual es una aplicación de software cliente de SQL y una herramienta de administración de bases de datos. Ejemplo:

![Herramienta DBeaver](https://github.com/josdagaro/ml-challenge-customers-mngr/blob/main/docs/dbeaver.png)

**Para Probar la API**: usar Postman, la cual es un software global que ofrece una plataforma API para que los desarrolladores diseñen, creen, prueben y colaboren en API. Ejemplo:

![Herramienta Postman](https://github.com/josdagaro/ml-challenge-customers-mngr/blob/main/docs/postman.png)

## Despliegue En Nube (AWS)

Esta configuración se disponibiliza para pruebas locales, por lo cual para correr la aplciación en local, se hace uso los siguientes archivos y una breve descripción del motivo:

- `api-aws.dockerfile`: Permite construir una imagen Docker de la API interna preparada para ambiente nube AWS.
- `api.py`: Contiene el código/funcionalidad de la API interna de clientes.
- `syncer-aws.dockerfile`: Permite construir una imagen Docker del fetcher/sincronizador de API externa de provider preparada para ambiente nube AWS.
- `syncer.py`: Contiene el código/funcionalidad de obtención de datos de clientes desde el API externa del proveedor.
- `task-definition.json`: Contiene la definición de una tarea para el servicio ECS (alusivo a la definición de un "Pod Specification" en K8s).

**Nota Importante**: Para que este despliegue pueda funcionar, es importante haber realizado previamente el aprovisionamiento de infraestructura mediante el proyecto `ml-challenge-iac`, para verlo haz click [aquí](https://github.com/josdagaro/ml-challenge-iac).

### Escaneo de Vulnerabilidades de Imágenes Docker en ECR

En este despliegue hacia la nube, se cuenta con un escaneo de vulnerabilidades activo, de las imágenes Docker que se compilan y publican contra los dos repositorios creados en ECR (`customers-mngr` y `synchronizer`).
En la configuración del despliegue, es decir, en el archivo [.github/workflows/deploy.yml](https://github.com/josdagaro/ml-challenge-customers-mngr/blob/main/.github/workflows/deploy.yml) encontrará que en los `jobs` denominados `deploy-syncer` y `deploy-customers-mngr`, se encuentran `steps` relacionados a realizar el escaneo de vulnerabilidades, para efectos de esta prueba como un paso `soft` que no genera un bloqueo, pero sí una alerta de las vulnerabilidades de mayor criticidad. Vea este ejemplo:

![Vulnerabilidades ECR](https://github.com/josdagaro/ml-challenge-customers-mngr/blob/main/docs/ecr-scan-0.png)
![Vulnerabilidades ECR](https://github.com/josdagaro/ml-challenge-customers-mngr/blob/main/docs/ecr-scan-1.png)

En estas imágenes vemos una prueba en que el la detección de vulnerabilidades era bloqueante para continuar con el despliegue de las aplicaciones.

## Flujo de Despliegue con GitHub Actions

El flujo consta de dos fases, uno para revisión, y otro para aplicar los cambios y lograr el compilado de imagen Docker, su publicación en ECR, y la actualización del servicio en ECS. A continuación el diagrama:

![Flujo Despliegue IaC GitHub](https://github.com/josdagaro/ml-challenge-customers-mngr/blob/main/docs/ml-challenge-gh-ecs-deployment.drawio.png)
