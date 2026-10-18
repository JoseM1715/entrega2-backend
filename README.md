# Backend - Simulador de Ahorro Programado

API REST desarrollada en Python con Flask y PostgreSQL para administrar usuarios y metas de ahorro programado. El sistema permite consultar usuarios registrados, crear metas de ahorro y calcular la cuota mensual necesaria para alcanzar un objetivo financiero dentro de un plazo determinado.

La aplicación cuenta con documentación interactiva mediante Swagger, validación de datos, manejo de errores y pruebas automatizadas.

## Tabla de contenido

1. [Descripción del proyecto](#descripción-del-proyecto)
2. [Objetivos](#objetivos)
3. [Tecnologías utilizadas](#tecnologías-utilizadas)
4. [Arquitectura del proyecto](#arquitectura-del-proyecto)
5. [Requisitos previos](#requisitos-previos)
6. [Instalación y configuración](#instalación-y-configuración)
7. [Ejecución local](#ejecución-local)
8. [Ejecución con Docker](#ejecución-con-docker)
9. [Documentación de la API](#documentación-de-la-api)
10. [Endpoints disponibles](#endpoints-disponibles)
11. [Ejemplos de uso](#ejemplos-de-uso)
12. [Base de datos](#base-de-datos)
13. [Pruebas](#pruebas)
14. [Manejo de errores](#manejo-de-errores)
15. [Seguridad y configuración](#seguridad-y-configuración)
16. [Solución de problemas](#solución-de-problemas)

## Descripción del proyecto

El Simulador de Ahorro Programado es una aplicación que permite registrar objetivos financieros y calcular cuánto dinero debe ahorrar una persona periódicamente para alcanzar una meta determinada.

El backend funciona como una API REST que recibe solicitudes HTTP, procesa la información, aplica las reglas de negocio y se comunica con una base de datos PostgreSQL para consultar o almacenar los datos.

La aplicación está diseñada para trabajar junto con un frontend y un servicio de base de datos mediante Docker Compose.

## Objetivos

- Administrar la información de los usuarios registrados.
- Crear y consultar metas de ahorro.
- Calcular la cuota mensual necesaria para alcanzar una meta.
- Registrar aportes adicionales y el mes en el que se realizarán.
- Validar la información recibida por la API.
- Proporcionar respuestas JSON y códigos HTTP adecuados.
- Facilitar la consulta de los servicios mediante documentación Swagger.

## Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python 3.12 | Lenguaje de programación del backend. |
| Flask | Framework para desarrollar la API REST. |
| PostgreSQL | Sistema gestor de base de datos relacional. |
| psycopg2 | Conexión entre Python y PostgreSQL. |
| python-dotenv | Carga de variables de entorno desde un archivo `.env`. |
| Gunicorn | Servidor de aplicaciones utilizado en producción. |
| Docker | Creación y ejecución de contenedores. |
| pytest | Ejecución de pruebas automatizadas. |
| Swagger / OpenAPI | Documentación y consulta interactiva de la API. |

## Arquitectura del proyecto

El backend está organizado por capas para separar las responsabilidades de cada componente.

- **API:** recibe las solicitudes HTTP, valida los datos de entrada y devuelve respuestas JSON.
- **Controller:** coordina las operaciones relacionadas con usuarios y metas de ahorro.
- **Core:** contiene la lógica de negocio y los cálculos financieros.
- **Model:** representa los datos y las entidades utilizadas por la aplicación.
- **SQL:** contiene las consultas y los scripts utilizados para preparar la base de datos.
- **Tests:** contiene las pruebas automatizadas del sistema.

### Estructura de directorios

```text
entrega2-backend/
├── docs/
├── sql/
├── src/
│   ├── api/
│   ├── controller/
│   ├── core/
│   ├── model/
│   └── tests/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── app.py
├── poblar_db.py
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Requisitos previos

Para ejecutar el proyecto localmente se necesita:

- Python 3.12.
- PostgreSQL.
- Git.
- Un editor de código, como Visual Studio Code.
- Un cliente HTTP, como Postman, para probar los endpoints (opcional).

Para ejecutarlo mediante contenedores también se necesita Docker Desktop o Docker Engine y Docker Compose.

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/JoseM1715/entrega2-backend.git
cd entrega2-backend
```

### 2. Crear un entorno virtual

En Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

En Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

Para instalar también las dependencias de desarrollo y pruebas:

```bash
python -m pip install -r requirements-dev.txt
```

### 4. Configurar las variables de entorno

Crea un archivo llamado `.env` en la raíz del proyecto.

Incluye las siguientes variables, reemplazando los valores de ejemplo por los de tu instalación local:

```dotenv
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=ahorro_programado
PG_USER=postgres
PG_PASSWORD=cambia_esta_clave
ADMIN_PASSWORD=cambia_la_clave_del_admin
```

**Importante:** los valores anteriores son ejemplos. Debes utilizar las credenciales reales de tu PostgreSQL. No publiques contraseñas ni archivos `.env` en GitHub.

### 5. Preparar la base de datos

Crea la base de datos `ahorro_programado` en PostgreSQL antes de continuar.

Puedes hacerlo desde `psql`:

```sql
CREATE DATABASE ahorro_programado;
```

Asegúrate de que el usuario configurado tenga permisos para conectarse y crear las tablas necesarias.

### 6. Inicializar los datos

Con PostgreSQL en ejecución y las variables de entorno configuradas, ejecuta:

```bash
python poblar_db.py
```

Este proceso prepara las tablas y carga el administrador, los datos base y los registros de ejemplo. Puede ejecutarse nuevamente sin volver a crear las metas de ejemplo que ya existan.

## Ejecución local

Una vez configurado el entorno y preparada la base de datos, inicia el backend con:

```bash
python app.py
```

Por defecto, el servidor de desarrollo utiliza la dirección:

```text
http://127.0.0.1:5000
```

La aplicación también permite configurar el puerto mediante la variable de entorno `PORT`.

Para detener el servidor, presiona `Ctrl + C` en la terminal.

## Ejecución con Docker

El repositorio contiene un `Dockerfile` para construir la imagen del backend.

### Construir la imagen

Desde la carpeta del backend:

```bash
docker build -t entrega2-backend:1.0.0 .
```

### Ejecutar el contenedor

La base de datos debe estar disponible y las variables de conexión deben configurarse en el contenedor.

```bash
docker run -d \
  --name entrega2-backend \
  -p 5000:5000 \
  -e PG_HOST=host.docker.internal \
  -e PG_PORT=5432 \
  -e PG_DATABASE=ahorro_programado \
  -e PG_USER=postgres \
  -e PG_PASSWORD=CAMBIA_ESTA_CLAVE \
  entrega2-backend:1.0.0
```

Este ejemplo está pensado para Docker Desktop en Windows o macOS cuando PostgreSQL se ejecuta directamente en el equipo anfitrión. En Linux puede ser necesario configurar una red de Docker o utilizar el nombre del servicio de base de datos.

Si PostgreSQL se encuentra en otro contenedor, ambos servicios deben compartir una red y `PG_HOST` debe apuntar al nombre del servicio de PostgreSQL.

**Nota:** el comando anterior inicia el backend, pero no inicializa automáticamente la base de datos. Debes preparar previamente las tablas y los datos requeridos.

### Ejecutar el proyecto completo

En el entorno del proyecto completo, el frontend, el backend y la base de datos se coordinan mediante Docker Compose.

Los comandos de construcción y ejecución deben ejecutarse desde la carpeta que contiene el archivo `compose.yaml` o `docker-compose.yml`:

```bash
docker compose build
docker compose up -d
docker compose ps
```

Para consultar los registros:

```bash
docker compose logs -f
```

Para detener los servicios:

```bash
docker compose down
```

La configuración del proyecto completo debe proporcionar las variables de entorno y el servicio de inicialización de la base de datos que necesita el backend.

## Documentación de la API

La API incorpora documentación interactiva basada en Swagger y una especificación OpenAPI en formato JSON.

Con el backend en ejecución, abre las siguientes direcciones:

- **Swagger:** `http://127.0.0.1:5000/docs`
- **Especificación OpenAPI:** `http://127.0.0.1:5000/openapi.json`
- **Estado del servicio:** `http://127.0.0.1:5000/health`

Swagger permite consultar los endpoints documentados, revisar los parámetros y probar las solicitudes directamente desde el navegador.

## Endpoints disponibles

La API utiliza JSON para intercambiar información.

| Método | Endpoint | Descripción | Respuesta esperada |
|---|---|---|---|
| GET | `/health` | Comprueba que el servicio esté activo. | 200 OK |
| GET | `/api/usuarios` | Lista los usuarios registrados. | 200 OK |
| POST | `/api/metas` | Crea una nueva meta de ahorro. | 201 Created |
| GET | `/api/metas/{id}` | Consulta una meta por su identificador. | 200 OK o 404 Not Found |
| GET | `/docs` | Muestra la documentación Swagger. | 200 OK |
| GET | `/openapi.json` | Devuelve la especificación OpenAPI. | 200 OK |

### 1. Consultar el estado del servicio

**Solicitud:**

```http
GET /health
```

**Respuesta de ejemplo:**

```json
{
  "estado": "ok"
}
```

### 2. Consultar los usuarios

**Solicitud:**

```http
GET /api/usuarios
```

Devuelve una lista de usuarios con su identificador, nombre y correo electrónico.

### 3. Crear una meta de ahorro

**Solicitud:**

```http
POST /api/metas
Content-Type: application/json
```

**Cuerpo de la solicitud:**

```json
{
  "id_usuario": 1,
  "meta": 2500000,
  "plazo": 12,
  "extra": 100000,
  "mes_extra": 6
}
```

Descripción de los campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id_usuario` | Entero | Identificador del usuario propietario de la meta. |
| `meta` | Número | Valor total que se desea ahorrar. |
| `plazo` | Entero | Número de meses del plan de ahorro. |
| `extra` | Número | Aporte adicional contemplado en el plan. |
| `mes_extra` | Entero | Mes en el que se realizará el aporte adicional. |

Los campos `id_usuario`, `meta` y `plazo` son obligatorios. Los campos `extra` y `mes_extra` pueden omitirse; cuando se omiten o se envían como cero, se utiliza el valor cero.

El usuario debe existir y los datos deben cumplir las reglas de validación del sistema.

**Respuesta:** cuando la operación se completa correctamente, el servicio devuelve el identificador de la meta, los datos registrados y la cuota mensual calculada.

### 4. Consultar una meta por su identificador

**Solicitud:**

```http
GET /api/metas/1
```

Si la meta existe, se devuelve su información. Si no existe, la API responde con un error `404 Not Found`.

## Ejemplos de uso

Las siguientes solicitudes se pueden ejecutar desde una terminal con `curl`.

### Consultar el estado del backend

```bash
curl http://127.0.0.1:5000/health
```

### Consultar usuarios registrados

```bash
curl http://127.0.0.1:5000/api/usuarios
```

### Crear una meta

```bash
curl -X POST http://127.0.0.1:5000/api/metas \
  -H "Content-Type: application/json" \
  -d '{"id_usuario":1,"meta":2500000,"plazo":12,"extra":100000,"mes_extra":6}'
```

### Consultar una meta

```bash
curl http://127.0.0.1:5000/api/metas/1
```

Los identificadores utilizados en estos ejemplos son ilustrativos. Para que las solicitudes funcionen, deben existir los usuarios y las metas correspondientes en la base de datos.

## Base de datos

El proyecto utiliza PostgreSQL para almacenar la información del sistema.

Las variables de conexión se leen desde el entorno o desde el archivo `.env` local.

| Variable | Función |
|---|---|
| `PG_HOST` | Dirección del servidor PostgreSQL. |
| `PG_PORT` | Puerto de conexión. |
| `PG_DATABASE` | Nombre de la base de datos. |
| `PG_USER` | Usuario de conexión. |
| `PG_PASSWORD` | Contraseña de conexión. |
| `ADMIN_PASSWORD` | Contraseña utilizada para inicializar el administrador. |

El script `poblar_db.py` utiliza estas configuraciones para preparar las tablas y los datos iniciales.

## Pruebas

El proyecto incluye pruebas automatizadas en `src/tests`.

Instala las dependencias de desarrollo:

```bash
python -m pip install -r requirements-dev.txt
```

Ejecuta las pruebas con:

```bash
python -m pytest src/tests
```

Las pruebas que dependen de PostgreSQL requieren una base de datos disponible y correctamente configurada.

## Manejo de errores

La API utiliza códigos de estado HTTP para comunicar el resultado de las operaciones.

| Código | Significado |
|---|---|
| 200 | Solicitud procesada correctamente. |
| 201 | Recurso creado correctamente. |
| 404 | Usuario o meta no encontrados. |
| 422 | Datos inválidos o incumplimiento de las reglas de negocio. |
| 503 | Base de datos no disponible. |

Los errores se devuelven en formato JSON, normalmente con un campo `detalle` que explica el problema.

## Seguridad y configuración

Para mantener una configuración segura:

- No publiques contraseñas ni credenciales en el repositorio.
- Utiliza variables de entorno para la configuración sensible.
- No compartas archivos `.env` con información real.
- Utiliza contraseñas seguras para la base de datos y el administrador.
- Evita habilitar el modo de depuración en producción.
- Restringe el acceso a PostgreSQL según las necesidades del entorno.

## Solución de problemas

**Error de conexión con PostgreSQL**

Verifica que PostgreSQL esté activo y que `PG_HOST`, `PG_PORT`, `PG_DATABASE`, `PG_USER` y `PG_PASSWORD` sean correctos.

**No se puede crear una meta**

Comprueba que el usuario exista, que los campos obligatorios estén presentes y que los valores enviados cumplan las reglas de validación.

**Swagger no carga**

Confirma que el backend esté ejecutándose y que estés utilizando la dirección y el puerto correctos.

**El contenedor se detiene**

Consulta los registros con `docker logs entrega2-backend` y verifica la conexión con PostgreSQL y las variables de entorno.

**Las pruebas fallan**

Comprueba que hayas instalado `requirements-dev.txt` y que la base de datos esté disponible para las pruebas que la necesitan.

## Autor y repositorio

Repositorio del backend:

https://github.com/JoseM1715/entrega2-backend

Este proyecto forma parte del desarrollo de un simulador de ahorro programado con una arquitectura basada en API REST, Python y PostgreSQL.

