"""Configuración de la conexión a PostgreSQL.

Los datos se leen de variables de entorno (o de un archivo .env en la raíz):
PG_HOST, PG_DATABASE, PG_USER, PG_PASSWORD y PG_PORT.
También se aceptan los nombres estándar de PostgreSQL (PGHOST, PGDATABASE, ...)
y, si existe, el antiguo archivo src/secret_config.py.
"""
import os

import psycopg2

try:  # python-dotenv es opcional: en Docker las variables ya vienen del entorno
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def _leer(nombre: str, defecto=None):
    """Busca PG_<nombre>, luego PG<nombre>, luego secret_config.PG_<nombre>."""
    for variable in (f"PG_{nombre}", f"PG{nombre}"):
        valor = os.getenv(variable)
        if valor:
            return valor.strip()
    try:
        from src import secret_config
        valor = getattr(secret_config, f"PG_{nombre}", None) or getattr(secret_config, f"PG{nombre}", None)
        if valor:
            return str(valor).strip()
    except ImportError:
        pass
    return defecto


def obtener_conexion():
    """Abre una conexión nueva. Quien la pide es responsable de cerrarla."""
    return psycopg2.connect(
        host=_leer("HOST", "localhost"),
        port=_leer("PORT", "5432"),
        dbname=_leer("DATABASE"),
        user=_leer("USER"),
        password=_leer("PASSWORD"),
        connect_timeout=10,
    )
