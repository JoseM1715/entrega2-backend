-- Datos iniciales. Se puede ejecutar varias veces sin duplicar nada.
-- Lo ejecuta poblar_db.py, que le pasa %(admin_password)s desde la variable ADMIN_PASSWORD.
-- OJO: no escribir el signo de porcentaje en este archivo (psycopg2 lo interpreta).

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 1) Usuario administrador (la contraseña se guarda con hash bcrypt, nunca en texto plano)
INSERT INTO usuarios (nombre, email, rol, password_hash)
VALUES ('Administrador', 'admin@ahorro.local', 'admin', crypt(%(admin_password)s, gen_salt('bf')))
ON CONFLICT (email) DO NOTHING;

-- 2) Tabla maestra de parámetros
INSERT INTO parametros (clave, valor, descripcion) VALUES
    ('tasa_mensual', 0.0075, 'Tasa de rendimiento mensual (0.75 por ciento)')
ON CONFLICT (clave) DO NOTHING;

-- 3) Usuarios de ejemplo (las metas de ejemplo las crea poblar_db.py con la fórmula real)
INSERT INTO usuarios (nombre, email) VALUES
    ('Miguel Angel', 'miguel.angel@email.com'),
    ('Jose Angel', 'jose.angel@email.com')
ON CONFLICT (email) DO NOTHING;
