import os
from contextlib import closing

from src.config import obtener_conexion
from src.model.usuario import Usuario

RUTA_SQL = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'sql'))

# Orden estricto: usuarios primero porque las demás tablas la referencian.
ARCHIVOS_ESQUEMA = ['usuarios.sql', 'metas_ahorro.sql', 'historial_calculos.sql', 'parametros.sql']


class UsuarioController:

    @staticmethod
    def insertar(usuario: Usuario) -> int:
        """Inserta el usuario y devuelve el id_usuario que generó la base de datos."""
        with closing(obtener_conexion()) as conexion:
            with conexion, conexion.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO usuarios (nombre, email) VALUES (%s, %s) RETURNING id_usuario",
                    (usuario.nombre, usuario.email)
                )
                usuario.id_usuario = cursor.fetchone()[0]
        return usuario.id_usuario

    @staticmethod
    def buscar(id_usuario: int) -> Usuario | None:
        with closing(obtener_conexion()) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "SELECT id_usuario, nombre, email FROM usuarios WHERE id_usuario = %s",
                    (id_usuario,)
                )
                row = cursor.fetchone()
        if row:
            return Usuario(id_usuario=row[0], nombre=row[1], email=row[2])
        return None

    @staticmethod
    def listar() -> list[Usuario]:
        """Devuelve los usuarios (rol 'usuario') ordenados por id, para elegirlos en el frontend."""
        with closing(obtener_conexion()) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "SELECT id_usuario, nombre, email FROM usuarios WHERE rol = 'usuario' ORDER BY id_usuario"
                )
                filas = cursor.fetchall()
        return [Usuario(id_usuario=f[0], nombre=f[1], email=f[2]) for f in filas]

    @staticmethod
    def actualizar(usuario: Usuario) -> None:
        with closing(obtener_conexion()) as conexion:
            with conexion, conexion.cursor() as cursor:
                cursor.execute(
                    "UPDATE usuarios SET nombre = %s, email = %s WHERE id_usuario = %s",
                    (usuario.nombre, usuario.email, usuario.id_usuario)
                )

    @staticmethod
    def eliminar(id_usuario: int) -> None:
        """Borra el usuario y, por ON DELETE CASCADE, sus metas e historial."""
        with closing(obtener_conexion()) as conexion:
            with conexion, conexion.cursor() as cursor:
                cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))

    @staticmethod
    def crear_tablas() -> None:
        """Crea las tablas que falten (no borra datos). Lanza la excepción si algo falla."""
        with closing(obtener_conexion()) as conexion:
            with conexion, conexion.cursor() as cursor:
                for archivo in ARCHIVOS_ESQUEMA:
                    with open(os.path.join(RUTA_SQL, archivo), 'r', encoding='utf-8') as f:
                        cursor.execute(f.read())
