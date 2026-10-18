"""Pruebas contra PostgreSQL real. Necesitan la conexión configurada (.env o variables PG_*).

No borran tablas ni truncan nada: cada prueba crea un usuario con un email único
y lo elimina al terminar (ON DELETE CASCADE se lleva sus metas e historial).
"""
import unittest
import uuid
from contextlib import closing

from psycopg2 import errors

from src.config import obtener_conexion
from src.controller.ahorro_controller import AhorroController, ErrorUsuarioNoExiste
from src.controller.usuario_controller import UsuarioController
from src.core.logica import AhorroProgramado, ErrorMetaInvalida, ErrorMesExtraFueraDeRango
from src.model.meta_ahorro import MetaAhorro
from src.model.usuario import Usuario


def contar(tabla: str, id_usuario: int) -> int:
    with closing(obtener_conexion()) as conexion, conexion.cursor() as cursor:
        cursor.execute(f"SELECT count(*) FROM {tabla} WHERE id_usuario = %s", (id_usuario,))
        return cursor.fetchone()[0]


class BaseDeDatosTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        UsuarioController.crear_tablas()  # idempotente: no borra datos

    def crear_usuario_temporal(self, nombre="Usuario de prueba") -> Usuario:
        usuario = Usuario(nombre=nombre, email=f"{uuid.uuid4().hex}@test.com")
        UsuarioController.insertar(usuario)
        self.addCleanup(UsuarioController.eliminar, usuario.id_usuario)
        return usuario


class TestUsuarioController(BaseDeDatosTestCase):

    def test_insertar_genera_id_y_se_puede_buscar(self):
        usuario = self.crear_usuario_temporal()
        self.assertIsNotNone(usuario.id_usuario)
        buscado = UsuarioController.buscar(usuario.id_usuario)
        self.assertEqual(buscado.email, usuario.email)

    def test_insertar_dos_usuarios_no_choca(self):
        # Antes crear_usuario.py insertaba siempre id=0 y el segundo fallaba.
        primero, segundo = self.crear_usuario_temporal(), self.crear_usuario_temporal()
        self.assertNotEqual(primero.id_usuario, segundo.id_usuario)

    def test_insertar_con_acentos(self):
        usuario = self.crear_usuario_temporal(nombre="José Jaramillo Peña")
        self.assertEqual(UsuarioController.buscar(usuario.id_usuario).nombre, "José Jaramillo Peña")

    def test_insertar_nombre_largo(self):
        usuario = self.crear_usuario_temporal(nombre="A" * 100)
        self.assertEqual(len(UsuarioController.buscar(usuario.id_usuario).nombre), 100)

    def test_email_duplicado_falla(self):
        usuario = self.crear_usuario_temporal()
        with self.assertRaises(errors.UniqueViolation):
            UsuarioController.insertar(Usuario(nombre="Otro", email=usuario.email))

    def test_buscar_no_existente(self):
        self.assertIsNone(UsuarioController.buscar(-1))

    def test_modificar_nombre_y_email(self):
        usuario = self.crear_usuario_temporal(nombre="Original")
        usuario.nombre, usuario.email = "Cambiado", f"{uuid.uuid4().hex}@nuevo.com"
        UsuarioController.actualizar(usuario)
        buscado = UsuarioController.buscar(usuario.id_usuario)
        self.assertEqual((buscado.nombre, buscado.email), ("Cambiado", usuario.email))

    def test_eliminar_usuario_borra_sus_metas_e_historial(self):
        usuario = Usuario(nombre="Temporal", email=f"{uuid.uuid4().hex}@test.com")
        UsuarioController.insertar(usuario)
        AhorroController.insertar_ahorro(MetaAhorro(usuario.id_usuario, 1_000_000, 10))
        UsuarioController.eliminar(usuario.id_usuario)
        self.assertEqual(contar("metas_ahorro", usuario.id_usuario), 0)
        self.assertEqual(contar("historial_calculos", usuario.id_usuario), 0)


class TestAhorroController(BaseDeDatosTestCase):

    def test_insertar_calcula_y_guarda_la_cuota(self):
        usuario = self.crear_usuario_temporal()
        meta = MetaAhorro(usuario.id_usuario, 2_000_000, 10, 1_000_000, 5)
        id_meta = AhorroController.insertar_ahorro(meta)

        guardada = AhorroController.buscar_meta(id_meta)
        esperada = AhorroProgramado(2_000_000, 10, 1_000_000, 5).calcular_cuota_mensual()
        self.assertAlmostEqual(float(guardada.cuota_mensual), esperada, places=2)
        self.assertAlmostEqual(float(guardada.cuota_mensual), 92991.27, places=2)
        self.assertEqual((guardada.id_usuario, guardada.plazo, guardada.mes_extra),
                         (usuario.id_usuario, 10, 5))

    def test_insertar_tambien_guarda_el_historial(self):
        usuario = self.crear_usuario_temporal()
        AhorroController.insertar_ahorro(MetaAhorro(usuario.id_usuario, 1_200_000, 12))
        AhorroController.insertar_ahorro(MetaAhorro(usuario.id_usuario, 450_000, 3))

        historial = AhorroController.listar_historial_usuario(usuario.id_usuario)
        self.assertEqual([float(h.cuota_mensual) for h in historial], [95941.77, 148880.60])
        self.assertEqual(AhorroController.buscar_historial(historial[0].id_historial).plazo, 12)

    def test_usuario_inexistente_lanza_error_y_no_guarda_nada(self):
        with self.assertRaises(ErrorUsuarioNoExiste):
            AhorroController.insertar_ahorro(MetaAhorro(2_000_000_000, 1_000_000, 12))

    def test_datos_invalidos_no_se_guardan(self):
        usuario = self.crear_usuario_temporal()
        with self.assertRaises(ErrorMetaInvalida):
            AhorroController.insertar_ahorro(MetaAhorro(usuario.id_usuario, -5, 12))
        with self.assertRaises(ErrorMesExtraFueraDeRango):
            AhorroController.insertar_ahorro(MetaAhorro(usuario.id_usuario, 1_000_000, 12, 500_000, 0))
        self.assertEqual(contar("metas_ahorro", usuario.id_usuario), 0)
        self.assertEqual(contar("historial_calculos", usuario.id_usuario), 0)

    def test_buscar_meta_no_existente(self):
        self.assertIsNone(AhorroController.buscar_meta(-1))

    def test_buscar_historial_no_existente(self):
        self.assertIsNone(AhorroController.buscar_historial(-1))


if __name__ == '__main__':
    unittest.main()
