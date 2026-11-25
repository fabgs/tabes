---
description: Generar el plan técnico de una spec aprobada
argument-hint: <NNN>
---

Genera el plan técnico de la spec $ARGUMENTS.

1. Localiza `specs/$ARGUMENTS-*/spec.md`. Si su estado no es `aprobada`, detente y dilo.
2. Lee `AGENTS.md`, `docs/constitucion.md`, `docs/arquitectura.md` y las secciones afectadas de `docs/modelo-datos.md`.
3. Explora el código existente relacionado antes de proponer piezas nuevas; reutiliza lo que haya.
4. Escribe `plan.md` junto a la spec con la plantilla `specs/_plantillas/plan.md`:
   - cambios de modelo con campos, restricciones de BD e índices;
   - servicios y motores con sus firmas tipadas;
   - URLs, vistas, plantillas e interacciones HTMX;
   - auditoría y permisos;
   - mapa completo `AC-NNN-xx → test(s)`;
   - riesgos y alternativas descartadas.
5. Si el plan cambia el modelo de datos o la arquitectura, actualiza `docs/modelo-datos.md` o añade un ADR en `docs/arquitectura.md` en el mismo cambio.
6. Completa el checklist de constitución. Si algo la incumple, para y pregunta.
7. Resume al usuario las decisiones que ha tomado el plan y las dudas que quedan.
