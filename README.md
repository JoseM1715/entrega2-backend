# Backend - Simulador de Ahorro Programado

API REST (Flask + PostgreSQL) que calcula la cuota mensual necesaria para llegar a una meta de ahorro.

- **Swagger:** `GET /docs` (especificación en `/openapi.json`)
- **Endpoints:** `GET /health`, `GET /api/usuarios`, `POST /api/metas`, `GET /api/metas/{id}`
- **Variables de entorno:** `PG_HOST`, `PG_PORT`, `PG_DATABASE`, `PG_USER`, `PG_PASSWORD`, `ADMIN_PASSWORD`
- **Seeding:** `python poblar_db.py` crea las tablas y carga admin, tabla maestra y datos de ejemplo (se puede repetir).
- **Pruebas:** `pip install -r requirements-dev.txt` y `python -m pytest src/tests` (las de `test_db.py` necesitan PostgreSQL).

Se ejecuta junto con el frontend y la base de datos desde el monorepo (docker compose).
