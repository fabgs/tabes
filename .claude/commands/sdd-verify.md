---
description: Verificar la implementación de una spec contra sus criterios de aceptación
argument-hint: <NNN>
---

Verifica la spec $ARGUMENTS.

1. Lee `specs/$ARGUMENTS-*/spec.md` y extrae todos los `RF-` y `AC-`.
2. Para cada AC, localiza el test que lo cita (`AC-NNN-xx`) y comprueba que realmente verifica lo que dice el criterio (no solo que existe).
3. Ejecuta `uv run poe check` y los tests e2e relacionados.
4. Revisa las invariantes de `AGENTS.md` y la constitución afectadas por el cambio.
5. Entrega una tabla `AC | test | estado (cumple / parcial / no cumple / sin test) | nota` y una lista priorizada de huecos. No arregles nada salvo que se pida.
