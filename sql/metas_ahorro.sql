CREATE TABLE IF NOT EXISTS metas_ahorro (
    id_meta SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    meta DECIMAL(18,2) NOT NULL CHECK (meta > 0),
    plazo INT NOT NULL CHECK (plazo > 0),
    extra DECIMAL(18,2) NOT NULL DEFAULT 0 CHECK (extra >= 0),
    mes_extra INT NOT NULL DEFAULT 0 CHECK (mes_extra >= 0),
    tasa DECIMAL(6,4) NOT NULL DEFAULT 0.0075,
    cuota_mensual DECIMAL(18,2) NOT NULL CHECK (cuota_mensual >= 0),
    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
