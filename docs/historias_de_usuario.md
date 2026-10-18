# Historias de usuario — Calculadora de Ahorro Programado

Roles: **Ahorrador** (persona que quiere cumplir una meta), **Administrador** y **Equipo de desarrollo**.

| ID | Historia | Prioridad | Estado |
|----|----------|-----------|--------|
| HU-01 | Calcular mi cuota mensual de ahorro | Alta | Implementada |
| HU-02 | Incluir un abono extra en un mes | Alta | Implementada |
| HU-03 | Recibir mensajes claros cuando los datos son inválidos | Alta | Implementada |
| HU-04 | Guardar mi meta y ver mi cuota | Alta | Implementada |
| HU-05 | Consultar una meta guardada por su ID | Media | Implementada |
| HU-06 | Que el sistema recuerde mi historial de cálculos | Media | Implementada (se guarda; falta pantalla para verlo) |
| HU-07 | Usar la calculadora desde consola | Baja | Implementada |
| HU-08 | Usar la calculadora desde el celular (Android) | Baja | Implementada (GUI Kivy, sin guardado en BD) |
| HU-09 | Crear usuarios | Media | Implementada por consola (falta pantalla web) |
| HU-10 | Iniciar sesión como administrador | Media | **Pendiente** (el usuario `admin` ya se crea con el seeding) |
| HU-11 | Levantar todo el entorno con un solo comando | Alta | Implementada |
| HU-12 | Tener datos iniciales al crear la base de datos | Media | Implementada |
| HU-13 | Ejecutar pruebas automáticas | Alta | Implementada |

---

## HU-01 — Calcular mi cuota mensual de ahorro
**Como** ahorrador, **quiero** indicar mi meta y el plazo en meses, **para** saber cuánto debo ahorrar cada mes.

**Criterios de aceptación**
- **Dado** una meta de $1.200.000 a 12 meses sin abono extra, **cuando** calculo, **entonces** la cuota mensual es $95.941,77.
- El cálculo usa una tasa de rendimiento del 0,75 % mensual con la fórmula de anualidad de valor futuro.
- Los valores monetarios se muestran con 2 decimales.

## HU-02 — Incluir un abono extra en un mes
**Como** ahorrador, **quiero** indicar un abono extra y el mes en que lo haré, **para** reducir mi cuota mensual.

**Criterios de aceptación**
- **Dado** una meta de $2.000.000 a 10 meses con un abono de $1.000.000 en el mes 5, **cuando** calculo, **entonces** la cuota mensual es $92.991,27.
- El abono gana intereses desde el mes en que se deposita hasta el final del plazo.
- Si el abono cubre toda la meta, la cuota es $0.

## HU-03 — Recibir mensajes claros cuando los datos son inválidos
**Como** ahorrador, **quiero** que me digan qué dato está mal, **para** corregirlo sin perder lo que ya escribí.

**Criterios de aceptación**
- Se rechaza una meta menor o igual a 0, un plazo menor o igual a 0 y un abono negativo.
- Se rechaza un abono mayor que la meta.
- Se rechaza un mes de abono fuera del plazo, y también un abono sin mes (antes se ignoraba en silencio).
- En la web el mensaje aparece sobre el formulario, que conserva los datos escritos; no se guarda nada.
- Un error de la base de datos no muestra detalles internos (usuario, contraseña, host).

## HU-04 — Guardar mi meta y ver mi cuota
**Como** ahorrador, **quiero** que mi meta quede guardada con su cuota calculada, **para** consultarla después.

**Criterios de aceptación**
- **Dado** datos válidos y un ID de usuario existente, **cuando** presiono *Calcular y guardar*, **entonces** la meta se guarda con su cuota mensual y veo la pantalla de la meta con su ID.
- **Dado** que recargo esa pantalla, **entonces** no se crea una meta duplicada.
- **Dado** un ID de usuario que no existe, **entonces** veo "No existe un usuario con ID …" y no se guarda nada.

## HU-05 — Consultar una meta guardada por su ID
**Como** ahorrador, **quiero** buscar una meta con su ID, **para** ver sus datos y su cuota mensual.

**Criterios de aceptación**
- **Dado** un ID existente, **entonces** veo usuario, meta, plazo, abono extra, mes del abono y cuota mensual.
- **Dado** un ID que no existe o que no es un número, **entonces** veo un mensaje claro en lugar de un error del servidor.

## HU-06 — Que el sistema recuerde mi historial de cálculos
**Como** ahorrador, **quiero** que cada cálculo quede en un historial, **para** comparar escenarios más adelante.

**Criterios de aceptación**
- Cada meta guardada genera una fila en `historial_calculos` con la tasa, el valor futuro del abono, el factor de anualidad y la cuota.
- La meta y su historial se guardan juntos: si uno falla, no se guarda ninguno.

## HU-07 — Usar la calculadora desde consola
**Como** ahorrador, **quiero** ejecutar la calculadora desde la terminal, **para** usarla sin navegador.

**Criterios de aceptación**
- `python src/view/console.py` calcula la cuota.
- `python src/view-console/crear_meta_ahorro.py` calcula y guarda; `buscar_ahorro.py` la consulta.

## HU-08 — Usar la calculadora desde el celular
**Como** ahorrador, **quiero** una app Android, **para** calcular desde el celular.

**Criterios de aceptación**
- La GUI de Kivy (`src/view/gui_calculadora.py`) usa la misma lógica (`src/core/logica.py`).
- Se puede empaquetar como APK con Buildozer.

## HU-09 — Crear usuarios
**Como** administrador, **quiero** registrar usuarios, **para** que puedan guardar metas.

**Criterios de aceptación**
- `python src/view-console/crear_usuario.py` crea un usuario y muestra el ID que le asignó la base de datos.
- Dos usuarios con el mismo email no pueden existir.
- *Pendiente:* una pantalla web para crearlos.

## HU-10 — Iniciar sesión como administrador *(pendiente)*
**Como** administrador, **quiero** entrar con usuario y contraseña, **para** gestionar usuarios y ver todas las metas.

**Criterios de aceptación**
- **Dado** el usuario `admin` creado por el seeding, **cuando** ingreso la contraseña correcta, **entonces** accedo a un panel de administración.
- Las contraseñas se guardan con hash (ya implementado en el seeding), nunca en texto plano.

## HU-11 — Levantar todo el entorno con un solo comando
**Como** integrante del equipo, **quiero** ejecutar `docker compose up --build`, **para** tener la base de datos y la aplicación funcionando sin instalar PostgreSQL ni Python.

**Criterios de aceptación**
- La app responde en http://localhost:5000, después de que la base de datos esté lista y poblada.
- Las credenciales salen de un archivo `.env` que no se sube a git (`.env.example` sirve de plantilla).
- Los datos persisten entre reinicios; `docker compose down -v` los borra.

## HU-12 — Tener datos iniciales al crear la base de datos
**Como** integrante del equipo, **quiero** que la base se cree con un administrador, una tabla maestra y datos de ejemplo, **para** probar la aplicación de inmediato.

**Criterios de aceptación**
- Se crean el usuario `admin`, el parámetro `tasa_mensual` y dos usuarios de ejemplo con una meta cada uno.
- Ejecutar el seeding varias veces no duplica datos.
- Una base creada con la versión anterior se actualiza sin perder sus registros.

## HU-13 — Ejecutar pruebas automáticas
**Como** integrante del equipo, **quiero** pruebas unitarias y de navegador, **para** detectar errores antes de entregar.

**Criterios de aceptación**
- `python -m unittest discover -s src/tests -t .` cubre la lógica de cálculo, la base de datos y las rutas web.
- `pytest e2e` (Playwright) recorre el flujo completo: calcular, guardar, buscar y los casos de error.
- Las pruebas no borran ni truncan datos de la base.
