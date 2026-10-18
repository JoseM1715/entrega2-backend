"""API REST del simulador de ahorro programado (devuelve JSON). Swagger en /docs."""
from flask import Blueprint, jsonify, request
from psycopg2 import Error as ErrorBaseDeDatos

from src.api.openapi import ESPECIFICACION, PAGINA_SWAGGER
from src.controller.ahorro_controller import AhorroController, ErrorUsuarioNoExiste
from src.controller.usuario_controller import UsuarioController
from src.core.logica import ErrorAhorro
from src.model.meta_ahorro import MetaAhorro

api_bp = Blueprint("api", __name__)


def _error(mensaje: str, codigo: int):
    return jsonify({"detalle": mensaje}), codigo


def _meta_a_json(meta: MetaAhorro) -> dict:
    return {
        "id_meta": meta.id_meta,
        "id_usuario": meta.id_usuario,
        "meta": float(meta.meta),
        "plazo": int(meta.plazo),
        "extra": float(meta.extra),
        "mes_extra": int(meta.mes_extra),
        "cuota_mensual": float(meta.cuota_mensual),
    }


def _leer_json(cuerpo) -> dict:
    """Convierte el JSON recibido a números. Lanza ValueError si algo no es válido."""
    if not isinstance(cuerpo, dict):
        raise ValueError("Se esperaba un objeto JSON.")
    try:
        return dict(
            id_usuario=int(cuerpo["id_usuario"]),
            meta=float(cuerpo["meta"]),
            plazo=int(cuerpo["plazo"]),
            extra=float(cuerpo.get("extra") or 0),
            mes_extra=int(cuerpo.get("mes_extra") or 0),
        )
    except (KeyError, TypeError, ValueError):
        raise ValueError("Revisa los campos: id_usuario, meta y plazo son obligatorios y deben ser numéricos.")


@api_bp.errorhandler(ErrorBaseDeDatos)
def base_de_datos_caida(_error_bd):
    return _error("Base de datos no disponible", 503)


@api_bp.get("/health")
def health():
    return {"estado": "ok"}


@api_bp.get("/openapi.json")
def openapi():
    return jsonify(ESPECIFICACION)


@api_bp.get("/docs")
def docs():
    return PAGINA_SWAGGER


@api_bp.get("/api/usuarios")
def listar_usuarios():
    usuarios = UsuarioController.listar()
    return jsonify([{"id_usuario": u.id_usuario, "nombre": u.nombre, "email": u.email} for u in usuarios])


@api_bp.post("/api/metas")
def crear_meta():
    try:
        meta = MetaAhorro(**_leer_json(request.get_json(silent=True)))
        AhorroController.insertar_ahorro(meta)
    except ErrorUsuarioNoExiste as error:
        return _error(str(error), 404)
    except (ValueError, ErrorAhorro) as error:
        return _error(str(error), 422)
    return jsonify(_meta_a_json(meta)), 201


@api_bp.get("/api/metas/<int:id_meta>")
def obtener_meta(id_meta: int):
    meta = AhorroController.buscar_meta(id_meta)
    if meta is None:
        return _error("No hay ninguna meta guardada con ese ID.", 404)
    return jsonify(_meta_a_json(meta))
