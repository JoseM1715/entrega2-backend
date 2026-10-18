"""Crea las tablas (si faltan) y carga los datos iniciales. Se puede ejecutar varias veces.

    python poblar_db.py

Necesita las variables de conexión (PG_*) y ADMIN_PASSWORD en el entorno o en el archivo .env.
Con docker compose lo ejecuta automáticamente el servicio "seed".
"""
import os
import sys
from contextlib import closing

from src.config import obtener_conexion
from src.controller.ahorro_controller import AhorroController
from src.controller.usuario_controller import RUTA_SQL, UsuarioController
from src.model.meta_ahorro import MetaAhorro

# (email, meta, plazo, extra, mes_extra): la cuota la calcula la fórmula real.
METAS_EJEMPLO = [
    ("miguel.angel@email.com", 2_500_000, 12, 100_000, 6),
    ("jose.angel@email.com", 8_000_000, 24, 500_000, 12),
]


def cargar_datos_base(admin_password: str) -> None:
    with open(os.path.join(RUTA_SQL, "seed.sql"), encoding="utf-8") as archivo:
        consulta = archivo.read()
    with closing(obtener_conexion()) as conexion:
        with conexion, conexion.cursor() as cursor:
            cursor.execute(consulta, {"admin_password": admin_password})


def cargar_metas_ejemplo() -> int:
    """Crea las metas de ejemplo solo a los usuarios que todavía no tienen ninguna."""
    creadas = 0
    with closing(obtener_conexion()) as conexion:
        with conexion.cursor() as cursor:
            for email, meta, plazo, extra, mes_extra in METAS_EJEMPLO:
                cursor.execute(
                    """SELECT u.id_usuario FROM usuarios u
                       WHERE u.email = %s
                         AND NOT EXISTS (SELECT 1 FROM metas_ahorro m WHERE m.id_usuario = u.id_usuario)""",
                    (email,)
                )
                fila = cursor.fetchone()
                if fila:
                    AhorroController.insertar_ahorro(MetaAhorro(fila[0], meta, plazo, extra, mes_extra))
                    creadas += 1
    return creadas


def main() -> int:
    admin_password = os.getenv("ADMIN_PASSWORD")
    if not admin_password:
        print("❌ Define ADMIN_PASSWORD en el archivo .env (ver .env.example).")
        return 1
    try:
        print("Creando tablas...")
        UsuarioController.crear_tablas()
        print("Cargando administrador, tabla maestra y usuarios de ejemplo...")
        cargar_datos_base(admin_password)
        print(f"Metas de ejemplo nuevas: {cargar_metas_ejemplo()}")
    except Exception as error:
        print(f"❌ Error al poblar la base de datos: {error}")
        return 1
    print("✅ Base de datos lista.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
