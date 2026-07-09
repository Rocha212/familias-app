# Gestión de Fichas de Estandarización — Familias de Abastecimiento

Aplicación web profesional para crear, consultar, editar, eliminar, imprimir y exportar a PDF las
**fichas de estandarización de familias de abastecimiento** (Fase 1), replicando el formato visual
oficial del documento de referencia.

![Estado](https://img.shields.io/badge/estado-listo%20para%20producci%C3%B3n-brightgreen)
![Licencia](https://img.shields.io/badge/licencia-MIT-blue)

---

## 1. Arquitectura

```
Frontend (React + Vite + TailwindCSS)  ──HTTP/JSON──▶  Backend (FastAPI)  ──SQL──▶  PostgreSQL
        Nginx (prod) / Vite dev server                  Uvicorn + SQLAlchemy
```

| Capa           | Tecnología                                   |
|----------------|-----------------------------------------------|
| Frontend       | React 18, Vite, TailwindCSS, React Router, Recharts, Axios |
| Backend        | FastAPI, SQLAlchemy 2.0, Pydantic v2, python-jose (JWT), Passlib (bcrypt), ReportLab (PDF) |
| Base de datos  | PostgreSQL 16                                 |
| Autenticación  | JWT (Bearer token) + roles (Admin / Editor / Solo lectura) |
| Contenedores   | Docker + Docker Compose                       |

El backend sigue una **arquitectura por capas**:

```
app/
├── api/routes/     → Controladores HTTP (FastAPI routers). Sin lógica de negocio.
├── services/        → Lógica de negocio (casos de uso), independiente de HTTP.
├── models/          → Entidades ORM (SQLAlchemy).
├── schemas/         → Contratos de entrada/salida (Pydantic).
├── core/            → Configuración, seguridad (JWT/hash), conexión a BD.
└── main.py           → Punto de entrada, registro de routers y middlewares.
```

Esto respeta el principio de **responsabilidad única** (SOLID): las rutas validan y delegan, los
servicios contienen las reglas de negocio, y los modelos/esquemas están desacoplados entre sí
(el ORM nunca se expone directamente al cliente).

---

## 2. Estructura del repositorio

```
familias-app/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 3. Puesta en marcha (Docker Compose — recomendado)

### Requisitos
- Docker y Docker Compose instalados.

### Pasos

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd familias-app

# 2. Copiar el archivo de variables de entorno y ajustarlo si es necesario
cp .env.example .env

# 3. Levantar todo el stack
docker compose up --build -d

# 4. Verificar que los servicios estén activos
docker compose ps
```

Una vez levantado:

| Servicio  | URL                              |
|-----------|-----------------------------------|
| Frontend  | http://localhost                  |
| Backend / API docs | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 (usuario/clave en `.env`) |

El backend crea automáticamente las tablas y un **usuario administrador inicial** la primera vez
que se levanta, usando las credenciales definidas en `.env`:

```
Correo:     admin@empresa.com   (FIRST_ADMIN_EMAIL)
Contraseña: Admin123!            (FIRST_ADMIN_PASSWORD)
```

**Importante:** cambia estas credenciales (y `SECRET_KEY`) antes de usar la aplicación en un
entorno real, y crea usuarios adicionales desde el panel de **Usuarios** una vez inicies sesión
como administrador.

Para detener todo:
```bash
docker compose down          # detiene los contenedores
docker compose down -v       # además elimina el volumen de la base de datos
```

---

## 4. Puesta en marcha en modo desarrollo (sin Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configura una base de datos PostgreSQL local y exporta la URL de conexión
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/fichas_db"

# Crea las tablas y el usuario administrador inicial
python -m app.init_db

# Levanta el servidor de desarrollo
uvicorn app.main:app --reload
```

La API queda disponible en `http://localhost:8000` y la documentación interactiva (Swagger) en
`http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
cp .env.example .env    # ajusta VITE_API_URL si tu backend corre en otra URL
npm install
npm run dev
```

La aplicación queda disponible en `http://localhost:5173`.

---

## 5. Roles y permisos

| Acción                        | Administrador | Editor | Solo lectura |
|--------------------------------|:---:|:---:|:---:|
| Ver / buscar / filtrar fichas   | ✅ | ✅ | ✅ |
| Exportar a PDF / Imprimir       | ✅ | ✅ | ✅ |
| Crear / editar / duplicar fichas| ✅ | ✅ | ❌ |
| Eliminar fichas                 | ✅ | ❌ | ❌ |
| Gestionar usuarios              | ✅ | ❌ | ❌ |

---

## 6. Modelo de datos

### `usuarios`
| Campo | Tipo | Notas |
|---|---|---|
| id | PK | |
| email | string, único | |
| nombre | string | |
| hashed_password | string | hash bcrypt, nunca se expone |
| rol | enum: admin / editor / lector | |
| is_active | boolean | permite desactivar accesos sin borrar el usuario |
| created_at | datetime | |

### `familias` (ficha de estandarización)
Incluye los campos del encabezado (línea de abastecimiento, descripción, líder, estado, kraljic)
como columnas normales, y **tres bloques estructurados** (`status`, `clasificacion_proveedores`,
`clasificacion_cliente_interno`) como columnas `JSONB`. Esta decisión evita crear tablas
adicionales de una sola fila por ficha (lo que generaría joins innecesarios sin beneficio de
normalización real, ya que esos bloques siempre pertenecen 1 a 1 a una única ficha y no se
consultan de forma independiente). Los metadatos de auditoría (`created_by_id`, `updated_by_id`,
`created_at`, `updated_at`) están normalizados como llaves foráneas hacia `usuarios`, evitando
duplicar el nombre del usuario en cada ficha.

---

## 7. API REST

Documentación interactiva completa (OpenAPI/Swagger) disponible en `/docs` una vez el backend
está corriendo. Endpoints principales:

| Método | Endpoint | Descripción | Rol mínimo |
|---|---|---|---|
| POST | `/api/v1/auth/login` | Inicio de sesión, devuelve JWT | público |
| GET | `/api/v1/auth/me` | Usuario autenticado actual | cualquiera |
| GET | `/api/v1/familias` | Listado con búsqueda, filtros, orden y paginación | cualquiera |
| GET | `/api/v1/familias/{id}` | Detalle de una ficha | cualquiera |
| POST | `/api/v1/familias` | Crear ficha | editor |
| PUT | `/api/v1/familias/{id}` | Actualizar ficha | editor |
| DELETE | `/api/v1/familias/{id}` | Eliminar ficha | admin |
| POST | `/api/v1/familias/{id}/duplicar` | Duplicar ficha (como borrador) | editor |
| GET | `/api/v1/familias/{id}/pdf` | Descargar la ficha en PDF | cualquiera |
| GET | `/api/v1/dashboard` | KPIs y datos agregados para el panel | cualquiera |
| GET/POST/PUT | `/api/v1/usuarios` | Gestión de usuarios | admin |

---

## 8. Seguridad implementada

- Contraseñas con hash **bcrypt** (nunca se almacenan ni se transmiten en texto plano).
- Autenticación **JWT** con expiración configurable.
- Autorización por rol en cada endpoint sensible (`require_editor`, `require_admin`).
- Validación estricta de entrada con **Pydantic** (tipos, enums, longitudes).
- Uso de **SQLAlchemy ORM** con consultas parametrizadas: no hay concatenación de SQL, por lo que
  la aplicación no es vulnerable a inyección SQL.
- CORS restringido a orígenes configurables (`BACKEND_CORS_ORIGINS`).

---

## 9. Funcionalidades futuras (arquitectura preparada)

El sistema está diseñado para incorporar, sin necesidad de rediseño estructural:

- Carga y adjunto de archivos por ficha.
- Historial de cambios / control de versiones (ya existen `created_by`, `updated_by`, timestamps
  como base).
- Comentarios por ficha.
- Notificaciones.
- Flujo de aprobación y firmas digitales.
- Integración con Power BI y SAP.
- Exportación a Excel.
- Panel administrativo avanzado (auditoría, logs).

---

## 10. Scripts útiles

| Comando | Descripción |
|---|---|
| `python -m app.init_db` | Crea tablas y usuario administrador inicial (backend) |
| `npm run build` | Genera el build de producción del frontend |
| `docker compose up --build -d` | Levanta todo el stack en segundo plano |
| `docker compose logs -f backend` | Ver logs del backend en tiempo real |

---

## 11. Licencia

MIT — libre para adaptar a las necesidades de tu organización.
