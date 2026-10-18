class MetaAhorro:
    def __init__(self, id_usuario: int, meta: float, plazo: int, extra: float = 0, mes_extra: int = 0, cuota_mensual: float = 0.0, id_meta: int = None):
        self.id_meta = id_meta
        self.id_usuario = id_usuario
        self.meta = meta
        self.plazo = plazo
        self.extra = extra
        self.mes_extra = mes_extra
        self.cuota_mensual = cuota_mensual  