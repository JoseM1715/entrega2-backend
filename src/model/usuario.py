class Usuario:
    def __init__(self, nombre: str, email: str, id_usuario: int = None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email