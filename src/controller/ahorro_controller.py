from contextlib import closing

import psycopg2
from psycopg2 import errors

from src.config import obtener_conexion
from src.core.logica import AhorroProgramado
from src.model.historial_calculo import HistorialCalculo
from src.model.meta_ahorro import MetaAhorro


class ErrorUsuarioNoExiste(Exception):
    def __init__(self, id_usuario):
        super().__init__(f"No existe un usuario con ID {id_usuario}. Créalo primero.")


class AhorroController:

    @staticmethod
    def insertar_ahorro(ahorro: MetaAhorro) -> int:
        """Calcula la cuota, guarda la meta y su historial en una sola transacción.

        Lanza un ErrorAhorro (ver core/logica.py) si los datos no son válidos y
        ErrorUsuarioNoExiste si el id_usuario no está registrado. Devuelve el id_meta.
        """
        calculo = AhorroProgramado(ahorro.meta, ahorro.plazo, ahorro.extra, ahorro.mes_extra)
        ahorro.cuota_mensual = calculo.calcular_cuota_mensual()

        try:
            with closing(obtener_conexion()) as conexion:
                with conexion, conexion.cursor() as cursor:  # commit o rollback automático
                    cursor.execute(
                        """INSERT INTO metas_ahorro
                           (id_usuario, meta, plazo, extra, mes_extra, cuota_mensual)
                           VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_meta""",
                        (ahorro.id_usuario, ahorro.meta, ahorro.plazo,
                         ahorro.extra, ahorro.mes_extra, ahorro.cuota_mensual)
                    )
                    ahorro.id_meta = cursor.fetchone()[0]
                    cursor.execute(
                        """INSERT INTO historial_calculos
                           (id_usuario, meta, plazo, extra, mes_extra, tasa,
                            valor_futuro_extra, factor_anualidad, cuota_mensual)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (ahorro.id_usuario, ahorro.meta, ahorro.plazo, ahorro.extra,
                         ahorro.mes_extra, AhorroProgramado.TASA_INTERES_MENSUAL,
                         round(calculo.valor_futuro_abono(), 2),
                         round(calculo.factor_acumulacion(), 6),
                         ahorro.cuota_mensual)
                    )
        except errors.ForeignKeyViolation:
            raise ErrorUsuarioNoExiste(ahorro.id_usuario)
        return ahorro.id_meta

    @staticmethod
    def buscar_meta(id_meta: int) -> MetaAhorro | None:
        with closing(obtener_conexion()) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """SELECT id_meta, id_usuario, meta, plazo, extra, mes_extra, cuota_mensual
                       FROM metas_ahorro WHERE id_meta = %s""",
                    (id_meta,)
                )
                row = cursor.fetchone()
        if row is None:
            return None
        return MetaAhorro(
            id_meta=row[0], id_usuario=row[1], meta=row[2], plazo=row[3],
            extra=row[4], mes_extra=row[5], cuota_mensual=row[6]
        )

    @staticmethod
    def buscar_historial(id_historial: int) -> HistorialCalculo | None:
        with closing(obtener_conexion()) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """SELECT id_historial, id_usuario, meta, plazo, extra, mes_extra, cuota_mensual
                       FROM historial_calculos WHERE id_historial = %s""",
                    (id_historial,)
                )
                row = cursor.fetchone()
        if row is None:
            return None
        return HistorialCalculo(
            id_historial=row[0], id_usuario=row[1], meta=row[2], plazo=row[3],
            extra=row[4], mes_extra=row[5], cuota_mensual=row[6]
        )

    @staticmethod
    def listar_historial_usuario(id_usuario: int) -> list[HistorialCalculo]:
        with closing(obtener_conexion()) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """SELECT id_historial, id_usuario, meta, plazo, extra, mes_extra, cuota_mensual
                       FROM historial_calculos WHERE id_usuario = %s ORDER BY id_historial""",
                    (id_usuario,)
                )
                filas = cursor.fetchall()
        return [HistorialCalculo(id_historial=f[0], id_usuario=f[1], meta=f[2], plazo=f[3],
                                 extra=f[4], mes_extra=f[5], cuota_mensual=f[6]) for f in filas]
