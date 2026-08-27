 ORION Maintenance Lite

Technical test project for an equipment maintenance management API.

## Technologies

- Python
- FastAPI
- PostgreSQL 16
- Docker Compose

## Project structure

orion-maintenance-lite/
├── backend/
│   └── app/
│       └── main.py
└── docker-compose.yml
API
Health check
GET /health

Returns:

{
  "status": "healthy"
}
Root endpoint
GET /

Returns:

{
  "message": "ORION Maintenance Lite API is running"
}

Base de datos

El proyecto incluye PostgreSQL 16 configurado mediante Docker Compose.

Configuración:

        Base de datos: orion_maintenance
        Usuario: orion_user
        Puerto: 5432
        Persistencia: volumen Docker postgres_data

Ejecución del proyecto

1. Iniciar PostgreSQL mediante Docker Compose

Desde la carpeta raíz del proyecto:

docker compose up -d
2. Iniciar la API

La API puede ejecutarse localmente con:

uvicorn backend.app.main:app --reload

Una vez iniciada, la documentación interactiva de FastAPI estará disponible en:

http://localhost:8000/docs

También se puede comprobar el estado de la API mediante:

http://localhost:8000/health
Estado de la implementación

Actualmente se encuentra implementada la estructura inicial del proyecto, incluyendo:

API REST con FastAPI.
Endpoint principal.
Endpoint de verificación de salud.
Configuración de PostgreSQL.
Configuración de Docker Compose.
Persistencia de datos mediante volumen Docker.
Documentación inicial del proyecto.
Nota sobre el entorno de desarrollo

Durante la preparación de la prueba técnica, Docker Desktop presentó un inconveniente al iniciar el motor de Docker, por lo que la ejecución de los contenedores no pudo ser validada completamente en el entorno local.

La configuración de Docker Compose queda incluida para permitir la ejecución del proyecto en un entorno con Docker correctamente configurado.