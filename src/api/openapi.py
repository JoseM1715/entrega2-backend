"""Documentación OpenAPI de la API y página de Swagger UI (se sirve en /docs)."""

_META = {
    "type": "object",
    "properties": {
        "id_meta": {"type": "integer", "example": 3},
        "id_usuario": {"type": "integer", "example": 2},
        "meta": {"type": "number", "example": 2500000},
        "plazo": {"type": "integer", "example": 12},
        "extra": {"type": "number", "example": 100000},
        "mes_extra": {"type": "integer", "example": 6},
        "cuota_mensual": {"type": "number", "example": 196874.47},
    },
}
_ERROR = {"type": "object", "properties": {"detalle": {"type": "string"}}}


def _respuesta(descripcion, esquema=None):
    contenido = {"application/json": {"schema": esquema}} if esquema else None
    return {"description": descripcion, **({"content": contenido} if contenido else {})}


ESPECIFICACION = {
    "openapi": "3.0.3",
    "info": {
        "title": "Backend - Simulador de Ahorro Programado",
        "version": "1.0.0",
        "description": "Calcula la cuota mensual necesaria para alcanzar una meta de ahorro y la guarda en PostgreSQL.",
    },
    "paths": {
        "/health": {"get": {
            "tags": ["Estado"], "summary": "Comprueba que el backend está vivo",
            "responses": {"200": _respuesta("ok")}}},
        "/api/usuarios": {"get": {
            "tags": ["Usuarios"], "summary": "Lista los usuarios",
            "responses": {"200": _respuesta("Lista de usuarios", {"type": "array", "items": {
                "type": "object", "properties": {"id_usuario": {"type": "integer"},
                                                   "nombre": {"type": "string"}, "email": {"type": "string"}}}}),
                          "503": _respuesta("Base de datos no disponible", _ERROR)}}},
        "/api/metas": {"post": {
            "tags": ["Metas"], "summary": "Calcula la cuota mensual y guarda la meta",
            "requestBody": {"required": True, "content": {"application/json": {"schema": {
                "type": "object", "required": ["id_usuario", "meta", "plazo"],
                "properties": {"id_usuario": {"type": "integer", "example": 2},
                               "meta": {"type": "number", "example": 2500000},
                               "plazo": {"type": "integer", "example": 12},
                               "extra": {"type": "number", "example": 100000},
                               "mes_extra": {"type": "integer", "example": 6}}}}}},
            "responses": {"201": _respuesta("Meta guardada", _META),
                          "404": _respuesta("El usuario no existe", _ERROR),
                          "422": _respuesta("Datos inválidos", _ERROR),
                          "503": _respuesta("Base de datos no disponible", _ERROR)}}},
        "/api/metas/{id_meta}": {"get": {
            "tags": ["Metas"], "summary": "Busca una meta por su ID",
            "parameters": [{"name": "id_meta", "in": "path", "required": True, "schema": {"type": "integer"}}],
            "responses": {"200": _respuesta("La meta", _META),
                          "404": _respuesta("No existe esa meta", _ERROR),
                          "503": _respuesta("Base de datos no disponible", _ERROR)}}},
    },
}

PAGINA_SWAGGER = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Backend - Simulador de Ahorro Programado</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui.css">
</head>
<body>
  <div id="swagger"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui-bundle.js"></script>
  <script>SwaggerUIBundle({ url: "/openapi.json", dom_id: "#swagger" });</script>
</body>
</html>
"""
