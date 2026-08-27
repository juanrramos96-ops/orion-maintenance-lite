# BACKLOG_REFINED.md

## Introducción

Este documento contiene el refinamiento del backlog inicial (`BACLOG.md`) entregado para la prueba técnica. El backlog original se define a nivel muy general, este refinamiento define la metodología de "como", de cada uno de los ítems impartidos para la prueba.

El refinamiento se hizo analizando cada una de las HU donde se encontro que todas comparten el mismo modelo de datos por lo que se hace una corelación para cada una de las mismas.

## Pautas

- Escalas: T-shirt (XS, S, M, L, XL) por tarea técnica. XS = 1-2h, S = 2-4h, M = 4-8h, L = 1-2 días, XL = 3 o más días.


## HU-001 — Gestión de Activos

- Como supervisor de mantenimiento, quiero administrar los activos ITS de la concesión, para mantener actualizado el inventario de infraestructura operativa.

## 1. Análisis

Ambigüedades:
- No se especifica el CRUD completo ni si se permite eliminar un activo o solo darlo de baja.
- No se define qué tipos de activo existen ni si la lista es cerrada o es posible seguir agregando activos 
- No se especifica si se puede consultar activos ya eliminados o si se van a listar activos según el estado asignado. 
- No se especifica si un activo pertenece a un área especifgica.
- No se especifica si se requiere mantener el historial de cambios por cada activo.

Dependencias:
- HU-002 Ordenes de trabajo se corelaciona ya que HU001 requiere que haya algún activo creado.
- HU-004 Dashboard operacional.
- HU-006 Aunque es un opcional tiene corelación con respecto a los estados y lista de activos.

Riesgos:
- Si se permite realizar un borrado fisíco se perdería la trazabilidad del activo, si se le realizaron mantenimientos, etc.
- No se cuenta con una generación de numeros de activos automatica, esto puede conllevar a activos que manejen los mismos codigos.

Supuestos:
- Un activo pertenece a un único tipo de activo.
- Un activo posee un código único dentro de la concesión.
- Un activo puede tener múltiples órdenes de trabajo a lo largo de su vida útil.
- Los activos no se eliminan físicamente si poseen información histórica.
- La ubicación se almacenará inicialmente como información textual.

## 2. Refinamiento

AssetTypr

- Se compone de:
    Sensores, cámaras, sistemas de peajes, equipos de comunicaciones.
- Campos propuestos:
    Name, ID, Description 

Asset 
- Se proponen los siguientes campos:
    ID, code, name, asset_type_id, location, status, installation_date, description, created_at, updated_at


## Estados del activo
Se contemplan los siguientes:
- OPERATIONAL, UNDER_MAINTENANCE, OUT_OF_SERVICE, RETIRED


## 3. Descomposición Técnica

|Actividad                                  | Estimación      |
|Diseño de entidad y esquema de persistencia|	S               |
|Implementación de migraciones	            | XS              |
|API para crear activos	                    | XS              |
|API para consultar activos	                | XS              |
|API para actualizar activos                |	XS              |
|Validaciones de negocio                    |	S               |
|Interfaz de listado de activos             |	S               |
|Formulario de creación y edición           |	S               |
|Filtros por estado y tipo	                | XS              |
|Pruebas unitarias                          |	S               |
|Pruebas de integración                     | M               |

### 4. Estimación total: M-L

### 5. Priorización: 
MVP
- Funcionalidades mínimas:

    Crear activo.
    Consultar activos.
    Editar activo.
    Cambiar estado.
    Validar código único.

### 6. Justificación

- Se incorpora la entidad AssetType para evitar manejar el tipo de activo como texto libre y facilitar futuras clasificaciones.
- Se evita la eliminación física como comportamiento principal para conservar la trazabilidad histórica de mantenimiento.

## HU-002 — Gestión de Órdenes de Trabajo

- Como supervisor de mantenimiento, quiero crear y gestionar órdenes de trabajo, para planificar y controlar actividades de mantenimiento preventivo y correctivo.

## 1. Análisis

Ambigüedades:
- Qué información contiene una orden.
- Qué estados puede tener.
- Qué transiciones entre estados son válidas.
- Si una orden requiere un activo.
- Si una orden puede tener más de una cuadrilla.
- Qué ocurre al completar una orden.
- Si una orden puede cancelarse.
- Cómo se diferencia el mantenimiento preventivo del correctivo.
- Cómo se genera el identificador de la orden.
- Si las fechas programadas son obligatorias.

Dependencias:
- Depende de HU-001 — toda OT referencia al menos un activo existente.
- Se relaciona con HU-003 — una OT se asigna a una cuadrilla.
- Alimenta HU-004— los indicadores se calculan sobre el estado de las OTs.
- Opcionalmente consume HU-005 — Gestión de inventarios 

Riesgos:
-Permitir cambios de estado sin reglas puede generar inconsistencias.
- Una orden puede cerrarse sin haber sido ejecutada.
- Una cuadrilla puede ser asignada simultáneamente a múltiples órdenes incompatibles.
- La modificación de órdenes completadas puede afectar la trazabilidad,.
Supuestos:
  - Cada orden está asociada a un único activo.
  - Cada orden puede tener una cuadrilla asignada.
  - Una orden puede crearse sin cuadrilla y asignarse posteriormente.
  - Una orden completada no puede volver al estado anterior.
  - Las órdenes correctivas pueden originarse manualmente. 
  - La generación automática de averías pertenece a una funcionalidad opcional.

## 2. Refinamiento

  WorkOrder
    Se proponen los siguientes campos:
      id,code, asset_id, crew_id, maintenance_type, description, priority, status, scheduled_date, started_at, completed_at, created_at, updated_at
      
## 3. Descomposición Técnica

|Actividad                            |	Estimación    |
|Diseño del modelo de orden	          | S             |
|Migración de base de datos	          | XS            |
|Generación de código único	          | XS            |
|API CRUD	                            | M             |
|Implementación de máquina de estados	| M             |
|Validaciones de reglas de negocio	  | M             |
|Asignación de cuadrilla	            | S             |
|Listado y filtros	                  | S             |
|Formulario de creación	              | S             |
|Vista de detalle	                    | S             |
|Cambio de estados	                  | S             |
|Pruebas unitarias	                  | M             |
|Pruebas de integración	              | M             |


## 4. Estimación total: L 

## 5. Priorización: 

- MVP 
    Crear órdenes.
    Asociar activo.
    Definir tipo.
    Definir prioridad.
    Cambiar estados.
    Asignar cuadrilla.
    Completar orden.

## 6. Justificación

Se pretende un sistema que contenga estados para evitar la inconsistencias entre estados.
Solo se podrá crear y gestionar ordenes.


## HU-003 — Gestión de Cuadrillas

- Como coordinador de operaciones, quiero asignar cuadrillas a órdenes de trabajo, para asegurar la ejecución de las actividades programadas.

### 1. Análisis

Ambigüedades:
- No se especifica qué información debe tener una cuadrilla
- No se define si una cuadrilla puede tener varias ot asignadas simultáneamente o solo una a la vez.
- No se indica si existe el área de trabajo o el área al que se va a designar las ordenes de trabajo.
- No se indica si la cuadrilla va a poder gestionar sus ordenes de trabajo y podra asignar su estado según la ejecución que se este dando.
- No se indica el tiempo promedio que la cuadrilla va a poder solucionar la falla y estar activa de nuevo.

Dependencias:
- Depende de HU-002 
- Indirectamente depende de HU-001 (la especialidad de la cuadrilla puede validarse contra el tipo de activo).

Riesgos:
- Una cuadrilla puede estar con varias ordenes de trabajo al mismo tiempo lo que podría llegar a afectar los KPI´s
- No controlar la disponibilidad de la cuadrilla podria afectar la operación en varios sectores

Supuestos:
- Una cuadrilla tiene un área especifica para simplificar el MVP, como: electrica, comunicaciones, mecanicas, general y conexiones .
- Para el MVP, una cuadrilla solo puede tener una OT activa a la vez.
- El coordinadro puede asignar cuadrillas, el supervisor puede crear/editar cuadrillas y también asignar.

## 2. Refinamiento

Entidad (Crew):
Campoos:
  id, name, specialty, status, created_at, updated_at.

CrewMember: 
Campos:
  id, crew_id, name, role.


Estados de la cuadrilla:

Avaliable, assigned, Inactive.

Reglas de negocio:
1. No se puede asignar una cuadrilla en estado distinto a avaliabke.
2. Al asignar una cuadrilla a una OT, la cuadrilla pasa a assigned y la OT pasa a assigned.
3. Al completar o cancelar la OT, la cuadrilla vuelve automáticamente a avaliable.
4. Las cuadrillas deberán tener un nombre o identificación unica.

## 3. Descomposición Técnica

|Actividad                    |	Estimación   |
|Modelo de cuadrilla	        | XS           |
|Modelo de miembros	          | XS           |
|Migraciones	                | XS           |
|API CRUD cuadrillas	        | S            |
|API gestión de miembros	    | S            |
|Asignación a órdenes	        | S            | 
|Validación de disponibilidad	| S            |
|Interfaz de cuadrillas	      | S            |
|Pruebas	                    | S            |

## 4. Estimación total: M

## 5. Priorización: 
  MVP:
      Crear cuadrillas.
      Consultar cuadrillas.
      Asignar cuadrilla a una orden.
      Validar que esté activa.

## 6. Justificación

No se implementa planificación horaria detallada en el MVP debido a que aumentaría considerablemente la complejidad.
Se realiza la separación de entidades para permitir representar correctamente la cuadrilla como equipo y área de aplicaión 


## HU-004 — Dashboard Operacional

- Como supervisor, quiero visualizar indicadores operacionales, para conocer el estado general de las actividades de mantenimiento.

### 1. Análisis

Ambigüedades:
- No se especifica qué indicadores concretos debe mostrar.
- No se indica la frecuencia de actualización.
- No se especifica si los indicadores son historicos.
- No se indica si el dashboard debe filtrarse.
- No se aclara si los datos deben ser en tiempo real o pueden tener algún nivel de agregación/caché.

Dependencias:
- Depende de HU-001, HU-002 y HU-003 

Riesgos:
- Calcular indicadores con consultas pesadas sobre la tabla de OTs sin índices adecuados puede degradar el rendimiento a medida que crece el histórico.
- Definir demasiados indicadores puede exceder el tiempo de la prueba.
- Indicadores mal definidos podriam mostrar información inconsistente.

Supuestos:
- No se podrá integrar con otras aplicaciones externas para analisis de datos

## 2. Refinamiento

Activos
    Total de activos.
    Activos operativos.
    Activos en mantenimiento.
    Activos fuera de servicio.
    Activos retirados.
Órdenes
    Órdenes totales.
    Órdenes programadas.
    Órdenes en proceso.
    Órdenes completadas.
    Órdenes canceladas.
Distribución
    Órdenes por estado.
    Órdenes por tipo de mantenimiento.
    Órdenes por prioridad.

## 3. Descomposición Técnica

|Actividad                |	Estimación    |
|Definición de métricas	  | XS            |
|Endpoint de indicadores	| S             |
|Consultas agregadas	    | S             |
|Optimización básica	    | XS            |
|Componentes KPI	        | S             |
|Gráficas	                | M             |
|Filtros básicos	        | S             |
|Pruebas	                | S             |

## 4. Estimación total: M

## 5. Priorización: 

MVP

    KPIs principales.
    Órdenes por estado.
    Órdenes por tipo.
    Estado general de activos.

## 6. Justificación

- Se priorizan indicadores directamente relacionados con el estado operativo actual.
- Se requiere incormación adicional para poder mostrar mayor cantidad de datps.

## HU-005 — Gestión de Inventario (Opcional)

- Como técnico de mantenimiento, quiero registrar materiales y repuestos utilizados, para mantener actualizado el inventario disponible.

### 1. Análisis

Ambigüedades:
- No se especifica si existe control de stock mínimo
- No se tienen en cuenta alarmas para repuestos críticos
- No se indica si el registro de consumo debe estar necesariamente ligado a una Orden de Trabajo.
- No se aclara si el técnico también puede dar entrada a inventario o solo podrá consumirlo.
- No se especifica si existe una bodega de almacenamiento y si esta controlará las posiciones para facilitar su busqueda.

Dependencias:
- Depende de HU-002

Riesgos:
- Permitir consumo sin validar stock disponible puede generar inventario negativo.
- Si solo se modela consumo, el inventario solo puede decrecer, lo cual no refleja el ciclo real.

Supuestos:
- El registro de consumo de materiales siempre está asociado a una ot
- Solo el Técnico registra los repuestos que requiere y el supervisor registra la entrada de inventario.

## 2. Refinamiento

Material:
Campos:
  id, code name, description, stock_quantity, minimum_stock, unit.

WorkorderMaterial:
Campoos:
  id, work_order_id, material_id, quantity, created_at.

Regla de negocio

El consumo de material debe estar asociado a una orden de trabajo.

Al registrar un consumo:

stock_quantity =
stock_quantity - quantity_consumed

El sistema debe impedir que el inventario sea negativo.

## 3. Descomposición Técnica

|Actividad	                | Estimación    |
|Modelo de material     	  | XS            |
|Migraciones	              | XS            |
|CRUD inventario	          | S             |
|Registro de consumo	      | M             |
|Control de stock	          | S             |
|Historial de movimientos	  | M             |
|Interfaz	                  | M             |
|Pruebas	                  | M             |
## 4. Estimación total: L

## HU-006 — Generación Automática de Averías (Opcional)

- Como sistema, quiero generar averías automáticamente, para simular eventos operacionales y actividades de mantenimiento sobre los activos.

## 1. Análisis

Ambigüedades:
- Con qué frecuencia se generan averías.
- Qué probabilidad tiene cada activo de fallar.
- Si la avería genera automáticamente una orden.
- Si se trata de una simulación o integración real.

Supuestos: 
- La generación de una avería podría crear automáticamente una orden correctiva.
Dependencias:
- Depende de HU-001
- Se relaciona con HU-002
- Se realaciona con HU-004


Riesgos:
- Generar averías sin control puede inundar el sistema de datos.



## 2. Priorización: 
  MVP
    HU-001
      Gestión de activos.
    HU-002
      Gestión de órdenes de trabajo.
      Flujo de estados.
      Asociación con activos.
    HU-003
      Gestión básica de cuadrillas.
      Asignación a órdenes.
    HU-004
      Dashboard operacional básico.


## Conclusión

El análisis del backlog permite convertir las historias iniciales en funcionalidades técnicas ejecutables.
Las funcionalidades de inventario y generación automática de averías se consideran extensiones naturales del sistema y se priorizan después de garantizar el correcto funcionamiento del flujo principal.