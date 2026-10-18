CREATE TABLE IF NOT EXISTS historial_calculos (
    id_historial SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    meta DECIMAL(18,2) NOT NULL,
    plazo INT NOT NULL,
    extra DECIMAL(18,2) NOT NULL DEFAULT 0,
    mes_extra INT NOT NULL DEFAULT 0,
    tasa DECIMAL(6,4) NOT NULL DEFAULT 0.0075,
    valor_futuro_extra DECIMAL(18,2),
    factor_anualidad DECIMAL(18,6),
    cuota_mensual DECIMAL(18,2) NOT NULL,
    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
