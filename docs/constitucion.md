# Constitución del proyecto

Principios no negociables. Toda spec, plan y cambio de código debe cumplirlos; si alguno choca con un requisito, se para y se decide explícitamente (y se documenta como ADR en [arquitectura.md](arquitectura.md)).

## I. Spec antes que código
No se implementa nada sin una spec **aprobada** en `specs/`. Si al programar aparece un hueco o contradicción, se corrige primero la spec. El código sigue a la spec, no al revés.

## II. El modelo de datos es la fuente de verdad
El esquema se diseña en [modelo-datos.md](modelo-datos.md) antes de migrar. Las invariantes del torneo se garantizan **en PostgreSQL** (`UNIQUE`, `CHECK`, índices parciales), no solo en Python. Una migración aplicada en producción no se edita nunca.

## III. La corrección del tab está por encima de todo
Un error en un draw o en una clasificación afecta a personas reales en directo. Por eso:
- Los algoritmos de emparejamiento y asignación son **deterministas** dada una semilla, y la semilla se guarda.
- Se prueban con tests de propiedades (Hypothesis) y con un **simulador de torneos** completo.
- Una boleta confirmada no se modifica: se corrige creando una versión nueva, con motivo y registro.
- Las clasificaciones solo usan resultados confirmados.

## IV. Las personas mandan; el sistema propone
Todo lo automático (draw, jueces, salas, break) es una **propuesta editable**. Las incidencias blandas (revancha, misma institución, posición repetida) son **avisos visibles**, no bloqueos. Solo bloquean las invariantes duras (un equipo dos veces en la misma ronda, conflicto de juez en asignación automática, puntuación fuera de rango).

## V. Nada se publica sin una acción explícita
Draw, mociones, resultados, clasificaciones y break solo son visibles en la web pública (y en la app) cuando alguien del tab pulsa "publicar". Cada publicación queda en el registro de auditoría.

## VI. Trazabilidad
Toda acción del tab que cambie el estado del torneo (generar o editar draw, asignar jueces, confirmar o descartar boletas, publicar) se registra: quién, qué, cuándo, valor anterior y nuevo.

## VII. Simplicidad deliberada
Monolito Django con plantillas del servidor y HTMX. Sin microservicios ni SPA. Cada dependencia nueva necesita un ADR. Preferimos 100 líneas claras a una librería que no entendemos.

## VIII. Privacidad por defecto
Hay debatientes menores de edad. Se guardan los datos mínimos; nada personal en logs, URLs ni mensajes de error públicos; los enlaces privados usan tokens aleatorios revocables; la web pública permite mostrar solo iniciales. El tratamiento cumple RGPD y LOPDGDD.

## IX. Funciona en un aula con mala Wi-Fi
Las páginas públicas son ligeras (objetivo < 200 KB en primera carga), se sirven desde caché y se leen bien en un móvil. La herramienta de tab funciona en un portátil normal.

## X. Español primero, preparada para traducir
Interfaz en español con todas las cadenas marcadas para traducción (valenciano e inglés más adelante). Código e identificadores en inglés; documentación en español.

## XI. Probado antes de entregado
Cada criterio de aceptación de una spec tiene al menos un test que lo referencia (`AC-NNN-xx`). Lógica de dominio con cobertura ≥ 90 %. Antes de cada torneo real: simulación completa y prueba de carga.

## XII. Código abierto y repositorio público
TabES es software libre: la plataforma web, bajo **AGPL-3.0-or-later** (ver `LICENSE` y `NOTICE`); la app móvil, bajo **MIT**. El repositorio es público. Por eso:
- **Dependencias de la web**: compatibles con AGPL-3.0 (MIT, BSD, Apache-2.0, ISC, PSF, LGPL, GPL-3.0, AGPL-3.0). Nada con licencia privativa ni incompatible (p. ej. GPL-2.0-only, SSPL).
- Los servicios que se ejecutan aparte y sin modificar (PostgreSQL, Redis) no cuentan como dependencias a efectos de licencia. Para la caché se prefiere **Valkey** (BSD, compatible con Redis) para evitar dudas.
- **Dependencias de la app**: solo permisivas (MIT, BSD, Apache-2.0, ISC), porque se distribuye por App Store y Google Play.
- Se puede reutilizar código de proyectos compatibles (incluido Tabbycat, AGPL-3.0) **conservando su aviso de copyright** y anotándolo en `NOTICE`.
- **Nunca** se suben al repositorio secretos, copias de la base de datos ni datos reales de participantes. Los datos de ejemplo y los fixtures son inventados.
- Las aportaciones externas se aceptan bajo la misma licencia, con firma DCO (`git commit -s`).
