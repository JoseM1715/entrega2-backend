class HistorialCalculo:
    def __init__(self, id_usuario: int, meta: float, plazo: int, extra: float, mes_extra: int, cuota_mensual: float, id_historial: int = None):
        self.id_historial = id_historial
        self.id_usuario = id_usuario
        self.meta = meta
        self.plazo = plazo
        self.extra = extra
        self.mes_extra = mes_extra
        self.cuota_mensual = cuota_mensual