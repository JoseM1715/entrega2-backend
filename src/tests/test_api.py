"""Pruebas de la API. No necesitan base de datos: los controladores se reemplazan por mocks."""
import unittest
from unittest.mock import patch

from psycopg2 import OperationalError

from app import app
from src.controller.ahorro_controller import ErrorUsuarioNoExiste
from src.model.meta_ahorro import MetaAhorro
from src.model.usuario import Usuario


def cuerpo(**cambios):
    datos = {"id_usuario": 2, "meta": 2500000, "plazo": 12, "extra": 100000, "mes_extra": 6}
    datos.update(cambios)
    return datos


class TestApi(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.cliente = app.test_client()

    def test_health(self):
        self.assertEqual(self.cliente.get("/health").get_json(), {"estado": "ok"})

    def test_swagger_y_openapi(self):
        especificacion = self.cliente.get("/openapi.json").get_json()
        self.assertEqual(especificacion["info"]["title"], "Backend - Simulador de Ahorro Programado")
        self.assertIn("/api/metas", especificacion["paths"])
        self.assertEqual(self.cliente.get("/docs").status_code, 200)

    @patch("src.api.routes.UsuarioController")
    def test_listar_usuarios(self, controlador):
        controlador.listar.return_value = [Usuario("Ana", "ana@x.com", 2)]
        respuesta = self.cliente.get("/api/usuarios")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.get_json(), [{"id_usuario": 2, "nombre": "Ana", "email": "ana@x.com"}])

    @patch("src.api.routes.AhorroController")
    def test_crear_meta_devuelve_201_con_la_cuota(self, controlador):
        def guardar(meta):
            meta.id_meta = 7
            meta.cuota_mensual = 196874.47
        controlador.insertar_ahorro.side_effect = guardar
        respuesta = self.cliente.post("/api/metas", json=cuerpo())
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(respuesta.get_json()["id_meta"], 7)
        self.assertEqual(respuesta.get_json()["cuota_mensual"], 196874.47)
        enviada = controlador.insertar_ahorro.call_args[0][0]
        self.assertEqual((enviada.id_usuario, enviada.meta, enviada.plazo), (2, 2500000.0, 12))

    @patch("src.api.routes.AhorroController")
    def test_crear_meta_con_datos_invalidos_da_422_y_no_guarda(self, controlador):
        from src.core.logica import ErrorMetaInvalida
        controlador.insertar_ahorro.side_effect = ErrorMetaInvalida(-5)
        for json in (cuerpo(meta=-5), {"id_usuario": 2}, {"id_usuario": "x", "meta": 1, "plazo": 1}, [1, 2]):
            with self.subTest(json=json):
                respuesta = self.cliente.post("/api/metas", json=json)
                self.assertEqual(respuesta.status_code, 422)
                self.assertIn("detalle", respuesta.get_json())

    @patch("src.api.routes.AhorroController")
    def test_crear_meta_con_usuario_inexistente_da_404(self, controlador):
        controlador.insertar_ahorro.side_effect = ErrorUsuarioNoExiste(99)
        respuesta = self.cliente.post("/api/metas", json=cuerpo(id_usuario=99))
        self.assertEqual(respuesta.status_code, 404)

    @patch("src.api.routes.AhorroController")
    def test_obtener_meta(self, controlador):
        controlador.buscar_meta.return_value = MetaAhorro(2, 2500000, 12, 100000, 6, 196874.47, id_meta=7)
        respuesta = self.cliente.get("/api/metas/7")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.get_json()["cuota_mensual"], 196874.47)

    @patch("src.api.routes.AhorroController")
    def test_obtener_meta_que_no_existe_da_404(self, controlador):
        controlador.buscar_meta.return_value = None
        self.assertEqual(self.cliente.get("/api/metas/999").status_code, 404)

    @patch("src.api.routes.AhorroController")
    def test_base_de_datos_caida_da_503(self, controlador):
        controlador.buscar_meta.side_effect = OperationalError("connection refused")
        respuesta = self.cliente.get("/api/metas/1")
        self.assertEqual(respuesta.status_code, 503)
        self.assertEqual(respuesta.get_json(), {"detalle": "Base de datos no disponible"})


if __name__ == "__main__":
    unittest.main()
