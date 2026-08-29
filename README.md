# NOTASYA

NOTASYA es una API REST para gestionar estudiantes, profesores y cursos. El proyecto fue construido con FastAPI, Python, SQLAlchemy, PostgreSQL, Pydantic y Alembic, aplicando arquitectura por capas y separacion de responsabilidades.

## Datos del proyecto

- Proyecto: NOTASYA
- Integrante: Juan Esteban Montaño
- Arquitectura: DTOs -> Controladores -> Servicios -> Repositorios -> PostgreSQL
- Base de datos: PostgreSQL
- Documentacion interactiva: Swagger UI en `/docs`

## Cumplimiento de requisitos del taller

| Requisito | Estado | Donde se evidencia |
| --- | --- | --- |
| API con FastAPI y Python | Cumplido | `app/main.py`, `app/controllers/` |
| Conexion a PostgreSQL | Cumplido | `app/config/database.py`, `.env`, `alembic.ini` |
| Arquitectura por capas | Cumplido | `app/dtos/`, `app/controllers/`, `app/services/`, `app/repositories/` |
| Entidad Estudiante | Cumplido | `app/models/estudiante.py`, `app/dtos/estudiante_dto.py` |
| Entidad Profesor | Cumplido | `app/models/profesor.py`, `app/dtos/profesor_dto.py` |
| Entidad Curso | Cumplido | `app/models/curso.py`, `app/dtos/curso_dto.py` |
| Migraciones con Alembic | Cumplido | `alembic/versions/20260828_0001_create_notasya_tables.py` |
| Diagrama de clases | Cumplido | `diagrams/class_diagram.puml` |
| Diagramas de secuencia | Cumplido | `diagrams/sequence_consulta_estudiante.puml`, `diagrams/sequence_crear_curso.puml` |
| Diagrama de despliegue | Cumplido | `diagrams/deployment_diagram.puml` |
| Patron creacional | Cumplido | `ServiceFactory` y `DatabaseConnection` |
| Patron estructural | Cumplido | `EmailAdapter` |
| Patron de comportamiento | Cumplido | `CalificacionStrategy` |
| Principios SOLID | Cumplido | Explicados en la seccion "Principios SOLID" |
| Pruebas unitarias | Cumplido | `app/tests/` |

## Estructura del proyecto

```text
app/
|-- main.py
|-- config/
|   |-- database.py
|   |-- settings.py
|-- models/
|   |-- estudiante.py
|   |-- profesor.py
|   |-- curso.py
|-- dtos/
|   |-- estudiante_dto.py
|   |-- profesor_dto.py
|   |-- curso_dto.py
|-- repositories/
|   |-- estudiante_repository.py
|   |-- profesor_repository.py
|   |-- curso_repository.py
|-- services/
|   |-- estudiante_service.py
|   |-- profesor_service.py
|   |-- curso_service.py
|-- controllers/
|   |-- estudiante_controller.py
|   |-- profesor_controller.py
|   |-- curso_controller.py
|-- patterns/
|   |-- service_factory.py
|   |-- email_adapter.py
|   |-- calificacion_strategy.py
|-- tests/
```

## Flujo de la aplicacion

```text
Actor -> Controlador -> Servicio -> Repositorio -> PostgreSQL
Actor <- Controlador <- Servicio <- Repositorio <- PostgreSQL
```

El controlador recibe la solicitud HTTP, valida el DTO de entrada y llama al servicio. El servicio aplica reglas de negocio y usa repositorios para consultar o guardar informacion. El repositorio es la unica capa que accede directamente a SQLAlchemy y PostgreSQL.

## Entidades

### Estudiante

Campos: `id`, `nombre`, `telefono`, `correo`.

Restricciones:

- `correo` es unico.
- `nombre`, `telefono` y `correo` son obligatorios.
- `correo` se valida con `EmailStr` en Pydantic.

### Profesor

Campos: `id`, `nombre`, `tipo_identificacion`, `numero_identificacion`, `especialidad`.

Restricciones:

- La combinacion `tipo_identificacion` + `numero_identificacion` es unica.
- Todos los campos son obligatorios.

### Curso

Campos: `id`, `nombre`, `estudiante_id`, `profesor_id`, `calificacion`.

Relaciones:

- Un estudiante puede tener muchos cursos.
- Un profesor puede tener muchos cursos.
- Cada curso pertenece a un estudiante y a un profesor.

Restricciones:

- `estudiante_id` debe existir.
- `profesor_id` debe existir.
- `calificacion` debe estar entre `0` y `5`.

## Instalacion

Crear y activar el entorno virtual:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

Instalar dependencias:

```powershell
pip install -r requirements.txt
```

Crear el archivo de variables de entorno:

```powershell
copy .env.example .env
```

Editar `.env` con la conexion local a PostgreSQL:

```env
DATABASE_URL=postgresql+psycopg://postgres:TU_PASSWORD@localhost:5432/notasya
APP_NAME=NOTASYA API
APP_ENV=development
```


## Base de datos PostgreSQL

Crear la base de datos:

```sql
CREATE DATABASE notasya;
```

Ejecutar la migracion:

```powershell
alembic upgrade head
```

La migracion crea las tablas `estudiantes`, `profesores`, `cursos` y `alembic_version`.

## Ejecutar la API

```powershell
uvicorn app.main:app --reload
```

Abrir en el navegador:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/health`

## Endpoints

### Estudiantes

| Metodo | Ruta | Funcion |
| --- | --- | --- |
| GET | `/estudiantes` | ObtenerTodosLosEstudiantes |
| GET | `/estudiantes/{correo}` | ObtenerEstudiantePorCorreo |
| POST | `/estudiantes` | CrearEstudiante |
| PUT | `/estudiantes/{estudiante_id}` | ActualizarEstudiante |

Ejemplo para crear estudiante:

```json
{
  "nombre": "Ana Perez",
  "telefono": "3001234567",
  "correo": "ana@test.com"
}
```

### Profesores

| Metodo | Ruta | Funcion |
| --- | --- | --- |
| GET | `/profesores` | ObtenerTodosLosProfesores |
| GET | `/profesores/{tipo_identificacion}/{numero_identificacion}` | ObtenerProfesorPorTipoYNumeroIdentificacion |
| POST | `/profesores` | CrearProfesor |
| PUT | `/profesores/{profesor_id}` | ActualizarProfesor |

Ejemplo para crear profesor:

```json
{
  "nombre": "Carlos Ruiz",
  "tipo_identificacion": "CC",
  "numero_identificacion": "123456789",
  "especialidad": "Matematicas"
}
```

### Cursos

| Metodo | Ruta | Funcion |
| --- | --- | --- |
| GET | `/cursos` | ObtenerTodosLosCursos |
| GET | `/cursos/{curso_id}` | ObtenerCursoPorId |
| POST | `/cursos` | CrearCurso |
| PUT | `/cursos/{curso_id}` | ActualizarCurso |

Ejemplo para crear curso:

```json
{
  "nombre": "Diseno de Sistemas de Informacion",
  "estudiante_id": 1,
  "profesor_id": 1,
  "calificacion": 4.5
}
```

## Manejo de errores

La API responde con codigos HTTP claros:

- `404`: cuando no existe un estudiante, profesor o curso.
- `409`: cuando hay duplicados, por ejemplo correo de estudiante repetido o identificacion de profesor repetida.
- `422`: cuando los datos enviados no cumplen las validaciones del DTO.

Ejemplos en el codigo:

- `app/services/estudiante_service.py`: valida estudiante no encontrado y correo duplicado.
- `app/services/profesor_service.py`: valida profesor no encontrado e identificacion duplicada.
- `app/services/curso_service.py`: valida que existan estudiante y profesor antes de crear o actualizar un curso.

## Patrones de diseno

### Patron creacional: Factory Method

Archivo principal: `app/patterns/service_factory.py`

Clase: `ServiceFactory`

Problema que resuelve:

La aplicacion necesita crear servicios con sus repositorios correspondientes. Si cada controlador construyera manualmente sus servicios y repositorios, se repetiria codigo y los controladores conocerian demasiados detalles internos.

Como se aplica:

- `crear_estudiante_service(db)` crea un `EstudianteService` con un `EstudianteRepository`.
- `crear_profesor_service(db)` crea un `ProfesorService` con un `ProfesorRepository`.
- `crear_curso_service(db)` crea un `CursoService` con `CursoRepository`, `EstudianteRepository` y `ProfesorRepository`.

Donde se usa:

- `app/controllers/estudiante_controller.py`
- `app/controllers/profesor_controller.py`
- `app/controllers/curso_controller.py`

En esos controladores, las funciones `get_estudiante_service`, `get_profesor_service` y `get_curso_service` llaman a `ServiceFactory` para obtener el servicio correspondiente.

Prueba:

- `app/tests/test_patterns.py`, prueba `test_factory_method_crea_servicio_estudiante`.

### Patron creacional: Singleton

Archivo principal: `app/config/database.py`

Clase: `DatabaseConnection`

Problema que resuelve:

La aplicacion necesita una configuracion unica para el motor de base de datos y la fabrica de sesiones. Crear estas conexiones muchas veces en partes diferentes del sistema puede duplicar configuracion y desperdiciar recursos.

Como se aplica:

`DatabaseConnection` sobrescribe `__new__` y guarda una unica instancia en `_instance`. La primera vez crea `engine` con la URL de PostgreSQL y `session_factory` con `sessionmaker`. Las siguientes veces retorna la misma instancia.

Donde se usa:

- `app/config/database.py`, funcion `get_db`.
- `app/controllers/`, porque los controladores reciben `db: Session = Depends(get_db)`.

Prueba:

- `app/tests/test_patterns.py`, prueba `test_singleton_database_connection_reutiliza_instancia`.

### Patron estructural: Adapter

Archivo principal: `app/patterns/email_adapter.py`

Clases: `EmailProvider`, `ConsoleEmailProvider`, `EmailAdapter`.

Problema que resuelve:

La aplicacion podria necesitar enviar notificaciones sin depender directamente de un proveedor especifico. Hoy se usa un proveedor de consola, pero despues podria cambiarse por correo real, SMS o un servicio externo.

Como se aplica:

`EmailAdapter` expone el metodo `enviar_notificacion(destinatario, asunto, mensaje)` y por dentro llama al metodo `send` del proveedor. Asi la aplicacion trabaja con una interfaz estable y no con detalles concretos del proveedor.

Donde se evidencia:

- `app/patterns/email_adapter.py`

Ventaja:

Si cambia el proveedor externo, se crea una nueva clase que implemente `send`, pero no es necesario cambiar el resto de la aplicacion.

Prueba:

- `app/tests/test_patterns.py`, prueba `test_adapter_envia_notificacion_con_proveedor_externo`.

### Patron de comportamiento: Strategy

Archivo principal: `app/patterns/calificacion_strategy.py`

Clases: `CalificacionStrategy`, `CalificacionColombianaStrategy`, `EvaluadorCalificacion`.

Problema que resuelve:

La regla para interpretar una calificacion puede cambiar. Por ejemplo, en Colombia se puede aprobar desde `3.0`, pero otro sistema podria aprobar desde `3.5` o usar letras como A, B, C.

Como se aplica:

`CalificacionStrategy` define el contrato `estado(calificacion)`. `CalificacionColombianaStrategy` implementa la regla actual:

- `Aprobado` si la nota es mayor o igual a `3.0`.
- `Reprobado` si la nota es menor a `3.0`.

`EvaluadorCalificacion` recibe una estrategia y la ejecuta sin conocer la regla concreta.

Donde se evidencia:

- `app/patterns/calificacion_strategy.py`

Ventaja:

Se pueden crear nuevas estrategias de evaluacion sin modificar `EvaluadorCalificacion`.

Prueba:

- `app/tests/test_patterns.py`, prueba `test_strategy_evalua_estado_de_calificacion`.

## Principios SOLID

### S: Single Responsibility Principle

Cada clase tiene una responsabilidad principal.

Donde se aplica:

- `app/controllers/estudiante_controller.py`, `app/controllers/profesor_controller.py`, `app/controllers/curso_controller.py`: solo definen rutas HTTP, reciben DTOs y llaman servicios.
- `app/services/estudiante_service.py`, `app/services/profesor_service.py`, `app/services/curso_service.py`: contienen reglas de negocio, validaciones y errores.
- `app/repositories/estudiante_repository.py`, `app/repositories/profesor_repository.py`, `app/repositories/curso_repository.py`: solo consultan y modifican datos en PostgreSQL.
- `app/dtos/`: solo valida datos de entrada y define respuestas.
- `app/models/`: solo representa tablas y relaciones de base de datos.

Ejemplo:

`CursoService` valida que el estudiante y el profesor existan antes de crear un curso, pero no ejecuta SQL directamente. Esa consulta la hacen los repositorios.

### O: Open/Closed Principle

El codigo queda abierto para extenderse y cerrado para modificarse innecesariamente.

Donde se aplica:

- `app/patterns/calificacion_strategy.py`: se puede agregar otra estrategia de calificacion creando una nueva clase que herede de `CalificacionStrategy`, sin cambiar `EvaluadorCalificacion`.
- `app/patterns/email_adapter.py`: se puede agregar otro proveedor de notificaciones sin cambiar el adaptador ni los servicios consumidores.
- `app/repositories/`: si se agrega otra operacion de persistencia, se hace en el repositorio correspondiente sin modificar controladores.

Ejemplo:

Si se quiere evaluar notas con otra regla, se crea `CalificacionInternacionalStrategy` y se inyecta en `EvaluadorCalificacion`, sin cambiar la clase evaluadora.

### L: Liskov Substitution Principle

Las clases hijas o implementaciones pueden reemplazar a la abstraccion sin romper el comportamiento esperado.

Donde se aplica:

- `app/patterns/calificacion_strategy.py`: cualquier clase que implemente `CalificacionStrategy` puede reemplazar a `CalificacionColombianaStrategy`.
- `app/patterns/email_adapter.py`: cualquier proveedor que cumpla el contrato `EmailProvider` y tenga el metodo `send` puede reemplazar a `ConsoleEmailProvider`.

Ejemplo:

`EvaluadorCalificacion` no depende de una estrategia concreta. Solo necesita que exista el metodo `estado(calificacion)`.

### I: Interface Segregation Principle

Las interfaces y clases tienen contratos pequenos y especificos.

Donde se aplica:

- `EstudianteRepository` solo tiene operaciones de estudiantes.
- `ProfesorRepository` solo tiene operaciones de profesores.
- `CursoRepository` solo tiene operaciones de cursos.
- `EmailProvider` solo exige el metodo necesario para enviar un mensaje: `send`.

Ejemplo:

`CursoService` no depende de un repositorio gigante con todas las operaciones del sistema. Usa los repositorios concretos que necesita para validar relaciones y guardar cursos.

### D: Dependency Inversion Principle

Las capas superiores no deben depender directamente de detalles de infraestructura.

Donde se aplica:

- Los controladores no crean repositorios manualmente; los reciben mediante dependencias de FastAPI y `ServiceFactory`.
- Los servicios reciben repositorios en el constructor.
- La sesion de base de datos se obtiene con `get_db` en `app/config/database.py`, no se crea directamente dentro de los servicios.

Archivos relacionados:

- `app/patterns/service_factory.py`
- `app/config/database.py`
- `app/controllers/estudiante_controller.py`
- `app/controllers/profesor_controller.py`
- `app/controllers/curso_controller.py`
- `app/services/curso_service.py`

Ejemplo:

`CursoService` recibe `CursoRepository`, `EstudianteRepository` y `ProfesorRepository` desde afuera. Por eso, en las pruebas se pueden reemplazar por repositorios falsos como se hace en `app/tests/test_services.py`.

## Diagramas PlantUML

Los diagramas estan escritos en PlantUML dentro de la carpeta `diagrams/`. En GitHub se muestran como imagenes usando el servidor publico de PlantUML.

### Diagrama de clases

Archivo fuente: `diagrams/class_diagram.puml`

![Diagrama de clases](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/esteban105111/JuanEstebanMonta-o-Taller1-Dise-oSistemasInformacion/main/diagrams/class_diagram.puml)

### Diagrama de secuencia: consulta de estudiante

Archivo fuente: `diagrams/sequence_consulta_estudiante.puml`

![Diagrama de secuencia para consultar estudiante](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/esteban105111/JuanEstebanMonta-o-Taller1-Dise-oSistemasInformacion/main/diagrams/sequence_consulta_estudiante.puml)

### Diagrama de secuencia: creacion de curso

Archivo fuente: `diagrams/sequence_crear_curso.puml`

![Diagrama de secuencia para crear curso](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/esteban105111/JuanEstebanMonta-o-Taller1-Dise-oSistemasInformacion/main/diagrams/sequence_crear_curso.puml)

### Diagrama de despliegue

Archivo fuente: `diagrams/deployment_diagram.puml`

![Diagrama de despliegue](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/esteban105111/JuanEstebanMonta-o-Taller1-Dise-oSistemasInformacion/main/diagrams/deployment_diagram.puml)

## Pruebas

Ejecutar:

```powershell
.venv\Scripts\python -m pytest
```

Las pruebas cubren:

- Validaciones de DTOs.
- Reglas de negocio de servicios.
- Patrones de diseno.
- Casos de duplicados y registros inexistentes.

Resultado esperado:

```text
9 passed
```

## Despliegue sugerido en Railway

1. Crear un proyecto en Railway.
2. Agregar un servicio PostgreSQL.
3. Configurar la variable `DATABASE_URL` con la URL entregada por Railway.
4. Configurar el comando de inicio:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

5. Ejecutar migraciones en produccion:

```bash
alembic upgrade head
```

6. Probar `/health` y `/docs` en la URL publicada.

## Comandos rapidos

Activar entorno:

```powershell
.venv\Scripts\activate
```

Ejecutar API:

```powershell
uvicorn app.main:app --reload
```

Ejecutar migraciones:

```powershell
alembic upgrade head
```

Ejecutar pruebas:

```powershell
.venv\Scripts\python -m pytest
```
