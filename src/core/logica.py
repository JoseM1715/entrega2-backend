class ErrorAhorro(Exception):
    """Clase base de los errores de validación del ahorro programado."""


class ErrorMetaInvalida(ErrorAhorro):
    def __init__(self, meta):
        super().__init__(f"La meta ingresada ({meta}) debe ser mayor a 0.")


class ErrorPlazoInvalido(ErrorAhorro):
    def __init__(self, plazo):
        super().__init__(f"El plazo ingresado ({plazo}) debe ser mayor a 0 meses.")


class ErrorAbonoInvalido(ErrorAhorro):
    def __init__(self, abono):
        super().__init__(f"El abono extra ({abono}) no puede ser un valor negativo.")


class ErrorAbonoSuperaMeta(ErrorAhorro):
    def __init__(self, abono, meta):
        super().__init__(f"El abono extra ({abono}) supera la meta total ({meta}).")


class ErrorMesExtraFueraDeRango(ErrorAhorro):
    def __init__(self, mes, plazo):
        super().__init__(f"El mes del abono ({mes}) debe estar entre 1 y el plazo máximo ({plazo}).")


class AhorroProgramado:

    TASA_INTERES_MENSUAL = 0.0075

    def __init__(self, meta: float, plazo: int, abono_extra: float = 0.0, mes_abono_extra: int = 0):
        self.meta = meta
        self.plazo = plazo
        self.abono_extra = abono_extra
        self.mes_abono_extra = mes_abono_extra

    def _validar_datos(self) -> None:
        """Función privada con Responsabilidad Única: Solo validar datos."""
        if self.meta <= 0:
            raise ErrorMetaInvalida(self.meta)
        if self.plazo <= 0:
            raise ErrorPlazoInvalido(self.plazo)
        if self.abono_extra < 0:
            raise ErrorAbonoInvalido(self.abono_extra)
        if self.abono_extra > self.meta:
            raise ErrorAbonoSuperaMeta(self.abono_extra, self.meta)

        mes_fuera_del_plazo = not 0 <= self.mes_abono_extra <= self.plazo
        # Un abono con mes 0 se ignoraba en silencio: ahora se avisa.
        abono_sin_mes = self.abono_extra > 0 and self.mes_abono_extra == 0
        if mes_fuera_del_plazo or abono_sin_mes:
            raise ErrorMesExtraFueraDeRango(self.mes_abono_extra, self.plazo)

    def valor_futuro_abono(self) -> float:
        """Valor que tendrá el abono extra al final del plazo (0 si no hay abono)."""
        if self.mes_abono_extra <= 0:
            return 0.0
        periodos_restantes = self.plazo - self.mes_abono_extra
        return self.abono_extra * ((1 + self.TASA_INTERES_MENSUAL) ** periodos_restantes)

    def factor_acumulacion(self) -> float:
        """Factor de la anualidad ordinaria: ((1 + i)^n - 1) / i."""
        return ((1 + self.TASA_INTERES_MENSUAL) ** self.plazo - 1) / self.TASA_INTERES_MENSUAL

    def calcular_cuota_mensual(self) -> float:
        """Función con Responsabilidad Única: Solo aplicar matemáticas."""
        self._validar_datos()
        cuota = (self.meta - self.valor_futuro_abono()) / self.factor_acumulacion()
        return max(0.0, round(cuota, 2))
