import unittest

from src.core.logica import (
    AhorroProgramado,
    ErrorAhorro,
    ErrorMetaInvalida,
    ErrorPlazoInvalido,
    ErrorAbonoInvalido,
    ErrorAbonoSuperaMeta,
    ErrorMesExtraFueraDeRango
)


def simular_saldo_final(cuota, plazo, abono, mes_abono, tasa=AhorroProgramado.TASA_INTERES_MENSUAL):
    """Calcula el saldo mes a mes (sin usar la fórmula cerrada) para comprobar el resultado."""
    saldo = 0.0
    for mes in range(1, plazo + 1):
        saldo = saldo * (1 + tasa) + cuota
        if mes == mes_abono:
            saldo += abono
    return saldo


class TestAhorroProgramado(unittest.TestCase):

    def test_calculo_cuota_sin_abonos_a_doce_meses(self):
        ahorro = AhorroProgramado(meta=1200000, plazo=12, abono_extra=0, mes_abono_extra=0)
        self.assertAlmostEqual(ahorro.calcular_cuota_mensual(), 95941.77, places=2)

    def test_calculo_cuota_meta_alta_a_largo_plazo(self):
        ahorro = AhorroProgramado(meta=5000000, plazo=20, abono_extra=0, mes_abono_extra=0)
        self.assertAlmostEqual(ahorro.calcular_cuota_mensual(), 232653.16, places=2)

    def test_calculo_cuota_meta_baja_a_corto_plazo(self):
        ahorro = AhorroProgramado(meta=450000, plazo=3, abono_extra=0, mes_abono_extra=0)
        self.assertAlmostEqual(ahorro.calcular_cuota_mensual(), 148880.60, places=2)

    def test_calculo_cuota_con_abono_parcial(self):
        ahorro = AhorroProgramado(meta=2000000, plazo=10, abono_extra=1000000, mes_abono_extra=5)
        self.assertAlmostEqual(ahorro.calcular_cuota_mensual(), 92991.27, places=2)

    def test_calculo_cuota_con_abono_total_cubre_meta(self):
        ahorro = AhorroProgramado(meta=8000000, plazo=24, abono_extra=8000000, mes_abono_extra=12)
        self.assertAlmostEqual(ahorro.calcular_cuota_mensual(), 0.00, places=2)

    def test_calculo_cuota_micro_ahorro(self):
        ahorro = AhorroProgramado(meta=60000, plazo=2, abono_extra=0, mes_abono_extra=0)
        self.assertAlmostEqual(ahorro.calcular_cuota_mensual(), 29887.92, places=2)

    def test_abono_en_el_ultimo_mes_no_gana_intereses(self):
        # Con el abono en el mes 12 de 12, no hay periodos restantes: se resta tal cual.
        sin_abono = AhorroProgramado(meta=900000, plazo=12).calcular_cuota_mensual()
        con_abono = AhorroProgramado(meta=1000000, plazo=12, abono_extra=100000, mes_abono_extra=12)
        self.assertAlmostEqual(con_abono.calcular_cuota_mensual(), sin_abono, places=2)

    def test_la_cuota_calculada_realmente_alcanza_la_meta(self):
        casos = [
            (1_200_000, 12, 0, 0),
            (5_000_000, 20, 0, 0),
            (2_000_000, 10, 1_000_000, 5),
            (3_000_000, 36, 500_000, 36),
            (3_000_000, 36, 500_000, 1),
        ]
        for meta, plazo, abono, mes in casos:
            with self.subTest(meta=meta, plazo=plazo, abono=abono, mes=mes):
                cuota = AhorroProgramado(meta, plazo, abono, mes).calcular_cuota_mensual()
                self.assertAlmostEqual(simular_saldo_final(cuota, plazo, abono, mes), meta, delta=1.0)

    def test_valor_futuro_del_abono_y_factor(self):
        ahorro = AhorroProgramado(meta=1000000, plazo=12, abono_extra=100000, mes_abono_extra=6)
        self.assertAlmostEqual(ahorro.valor_futuro_abono(), 100000 * 1.0075 ** 6, places=2)
        self.assertAlmostEqual(ahorro.factor_acumulacion(), 12.5076, places=4)
        self.assertEqual(AhorroProgramado(meta=1000000, plazo=12).valor_futuro_abono(), 0.0)

    def test_falla_al_ingresar_meta_negativa(self):
        with self.assertRaises(ErrorMetaInvalida):
            ahorro = AhorroProgramado(meta=-500000, plazo=12, abono_extra=0, mes_abono_extra=0)
            ahorro.calcular_cuota_mensual()

    def test_falla_al_ingresar_meta_cero(self):
        with self.assertRaises(ErrorMetaInvalida):
            ahorro = AhorroProgramado(meta=0, plazo=6, abono_extra=0, mes_abono_extra=0)
            ahorro.calcular_cuota_mensual()

    def test_falla_al_ingresar_plazo_cero(self):
        with self.assertRaises(ErrorPlazoInvalido):
            ahorro = AhorroProgramado(meta=1000000, plazo=0, abono_extra=0, mes_abono_extra=0)
            ahorro.calcular_cuota_mensual()

    def test_falla_al_ingresar_abono_negativo(self):
        with self.assertRaises(ErrorAbonoInvalido):
            AhorroProgramado(meta=1000000, plazo=12, abono_extra=-1, mes_abono_extra=3).calcular_cuota_mensual()

    def test_falla_cuando_abono_supera_meta(self):
        with self.assertRaises(ErrorAbonoSuperaMeta):
            ahorro = AhorroProgramado(meta=1500000, plazo=12, abono_extra=2000000, mes_abono_extra=6)
            ahorro.calcular_cuota_mensual()

    def test_falla_cuando_mes_abono_supera_plazo(self):
        with self.assertRaises(ErrorMesExtraFueraDeRango):
            ahorro = AhorroProgramado(meta=1000000, plazo=12, abono_extra=500000, mes_abono_extra=15)
            ahorro.calcular_cuota_mensual()

    def test_falla_cuando_mes_abono_es_negativo(self):
        with self.assertRaises(ErrorMesExtraFueraDeRango):
            AhorroProgramado(meta=1000000, plazo=12, abono_extra=0, mes_abono_extra=-2).calcular_cuota_mensual()

    def test_falla_cuando_hay_abono_pero_no_hay_mes(self):
        # Antes el abono se ignoraba en silencio y la cuota salía mal.
        with self.assertRaises(ErrorMesExtraFueraDeRango):
            AhorroProgramado(meta=1000000, plazo=12, abono_extra=500000, mes_abono_extra=0).calcular_cuota_mensual()

    def test_todos_los_errores_son_errores_de_ahorro(self):
        for error in (ErrorMetaInvalida, ErrorPlazoInvalido, ErrorAbonoInvalido,
                      ErrorAbonoSuperaMeta, ErrorMesExtraFueraDeRango):
            self.assertTrue(issubclass(error, ErrorAhorro))


if __name__ == '__main__':
    unittest.main(verbosity=2)
