# SCENARIO.md — Decisiones de Arquitectura 

## 1. Arquitectura general

┌───────────────────────────────┐        ┌──────────────────────────────────┐        ┌──────────────┐
│   Frontend (React+TypeScript) │  HTTP  │   Backend Python + FastAPI       │  SQL   │  PostgreSQL  │
│   Dashboard- Formularios      │ ─────► │   REST API                       | ─────► │  Persistencia│
│   Listados - CRUD             │  JSON  │   Validacioens, Reglas de negocio|        │              │
└───────────────────────────────┘        └──────────────────────────────────┘        └──────────────┘

## 2. Arquitectura de comunicación:

La comunicación entre el frontend y el backend se realizará mediante una API REST utilizando HTTP y JSON.

Ejemplo de creación de un activo.

Request
POST /api/assets
Content-Type: application/json
{
  "code": "ITS-001",
  "name": "Cámara de monitoreo",
  "asset_type_id": 1,
  "location": "Kilómetro 15",
  "status": "OPERATIONAL",
  "installation_date": "2025-01-15",
  "description": "Cámara de monitoreo de tráfico"
}
Response
{
  "id": 1,
  "code": "ITS-001",
  "name": "Cámara de monitoreo",
  "asset_type_id": 1,
  "location": "Kilómetro 15",
  "status": "OPERATIONAL",
  "installation_date": "2025-01-15",
  "description": "Cámara de monitoreo de tráfico",
  "created_at": "2026-08-26T10:00:00",
  "updated_at": "2026-08-26T10:00:00"
}

## 3. Tecnologias Seleccionadas:

Frontend
  React

  React será utilizado para construir la interfaz de usuario.

  TypeScript

  TypeScript permitirá definir tipos para las entidades del sistema.
  Esto permite detectar errores durante el desarrollo y mantener consistencia entre los datos del frontend y la API.

Backend: Python + FastAPI

  El backend se desarrollará utilizando Python y FastAPI.

  FastAPI permitirá:

  Recibir y responder información en formato JSON.
  Validar automáticamente los datos.
  Generar documentación automática de la API.
  Definir modelos de entrada y salida.
  Implementar reglas de negocio.

SQLAlchemy

  SQLAlchemy será utilizado como ORM para interactuar con PostgreSQL.

  El ORM permitirá representar las entidades de la base de datos mediante clases Python.

PostgreSQL

  PostgreSQL será utilizado como base de datos relacional.

Docker

  Docker permitirá ejecutar toda la aplicación en un entorno reproducible.
 
## 4. Arquitectura del Backend:

backend/
 ├── app/
     │ 
     ├── api/ 
         ├── assets.py 
         ├── asset_types.py 
         ├── work_orders.py 
         ├── crews.py 
         └── dashboard.py 
     ├── models/ 
     │   ├── asset.py 
     │   ├── asset_type.py
     │   ├── work_order.py 
     │   ├── crew.py 
     │   └── crew_member.py 
     │── schemas/ 
         ├── asset.py 
     │   ├── work_order.py 
     │   └── crew.py 
     ├── services/ 
     │   ├── asset_service.py 
     │   ├── work_order_service.py 
     │   └── dashboard_service.py
     ├── repositories/ 
     │   ├── asset_repository.py 
     │   ├── work_order_repository.py 
     │   └── crew_repository.py 
     │── database/ 
     │   ├── connection.py 
     │   └── base.py 
     └── main.py 
├── tests/ 
├── requirements.txt 
└── Dockerfile


## 5. Responsabilidades de cada Capa

La capa API será responsable de:

    Recibir solicitudes HTTP.
    Recibir datos JSON.
    Validar parámetros.
    Retornar respuestas HTTP.
    Convertir errores en respuestas apropiadas.

Services

    La capa de servicios contendrá las reglas de negocio.

Repositories

    La capa Repository será responsable del acceso a los datos.

Models

    Los modelos representan las entidades persistentes.

Schemas

    Los schemas representan los datos que entran y salen de la API.


## 6. Modelo de los datos

AssetType

|id                 | PK      |
|name               |         |
|description        |         |
|Asset              |         |
|id                 | PK      |
|code               | UNIQUE  |
|name               |         |
|asset_type_id      | FK      |
|location           |         |
|status             |         |
|installation_date  |         |
|description        |         |
|created_at         |         |
|updated_at         |         |

Relación:

AssetType 1 - N Asset

Crew

|id               |   PK      |
|name             |   UNIQUE  |
|specialty        |           |
|status           |           |
|created_at       |           |
|updated_at       |           |
|CrewMember       |           |
|id               |   PK      |
|crew_id          |   FK      |
|name             |           |
|role             |           |

Relación:

Crew 1 - N CrewMember.

WorkOrder

|id                  | PK         |
|code                | UNIQUE     |
|asset_id            | FK         |
|crew_id             | FK NULL    | 
|maintenance_type    |            |
|description         |            |
|priority            |            |
|status              |            |
|scheduled_date      |            |
|started_at          |            |
|completed_at        |            |
|created_at          |            |
|updated_at          |            |

Relaciones:

Asset 1 - WorkOrder

Crew 1 - N WorkOrder

## 7. Endpoints principales:
Activos
  GET    /api/assets
  GET    /api/assets/{id}
  POST   /api/assets
  PUT    /api/assets/{id}
  PATCH  /api/assets/{id}/status
Tipos de activos
  GET    /api/asset-types
  POST   /api/asset-types
Órdenes de trabajo
  GET    /api/work-orders
  GET    /api/work-orders/{id}
  POST   /api/work-orders
  PUT    /api/work-orders/{id}
  PATCH  /api/work-orders/{id}/status
  PATCH  /api/work-orders/{id}/crew
Cuadrillas
  GET    /api/crews
  GET    /api/crews/{id}
  POST   /api/crews
  PUT    /api/crews/{id}
Miembros de cuadrilla
  POST   /api/crews/{id}/members
  PUT    /api/crews/{id}/members/{member_id}
  DELETE /api/crews/{id}/members/{member_id}

Dashboard
  GET /api/dashboard/summary

## 8. Manejo de errores

La API utilizará códigos HTTP estándar.

Validación incorrecta
  400 Bad Request

Recurso no encontrado
  404 Not Found

Conflicto

Se utilizará cuando una regla de negocio impida una operación.
  409 Conflict
## 9. Estrategia de pruebas

La aplicación contará con pruebas automatizadas enfocadas principalmente en las reglas de negocio críticas.

Activos
    Crear activo.
    Validar código único.
    Impedir fecha de instalación futura.
    Impedir crear orden sobre activo retirado.
Órdenes
    Crear orden.
    Validar activo existente.
    Validar transición de estados.
    Impedir iniciar una orden sin cuadrilla.
    Impedir modificar una orden completada.
Cuadrillas
    Crear cuadrilla.
    Validar nombre único.
    Impedir asignar una cuadrilla inactiva.
Dashboard
    Validar cálculo de indicadores.

## 10. Estrategia de docker

La solución será ejecutable mediante Docker Compose.
Los servicios serán:

frontend
backend
database

El objetivo es que el sistema pueda ejecutarse mediante un único comando:

docker compose up --build
