-- Tabla maestra: parámetros del cálculo (se llena con sql/seed.sql)
CREATE TABLE IF NOT EXISTS parametros (
    clave VARCHAR(50) PRIMARY KEY,
    valor DECIMAL(18,4) NOT NULL,
    descripcion TEXT NOT NULL
);
