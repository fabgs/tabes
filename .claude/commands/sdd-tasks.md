---
description: Descomponer el plan de una spec en tareas ejecutables
argument-hint: <NNN>
---

Descompón en tareas el plan de la spec $ARGUMENTS.

1. Requiere `specs/$ARGUMENTS-*/plan.md`. Si no existe, detente.
2. Crea `tasks.md` con la plantilla `specs/_plantillas/tasks.md`.
3. Tareas de 2 h como máximo, ordenadas por dependencias: modelos y migraciones → motores puros con tests → servicios → vistas y plantillas → tests e2e → documentación.
4. Cada tarea indica: objetivo, ficheros previstos, AC que cubre y comando de verificación.
5. Marca con `[P]` las que pueden hacerse en paralelo.
6. Comprueba que todos los AC de la spec aparecen en al menos una tarea; si falta alguno, dilo.
