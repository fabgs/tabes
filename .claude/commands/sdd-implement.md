---
description: Implementar tareas de una spec, test primero
argument-hint: <NNN> [T-xx]
---

Implementa tareas de la spec: $ARGUMENTS

1. Lee `tasks.md`, `plan.md` y `spec.md` de la spec. Elige la tarea indicada o, si no hay, la siguiente pendiente sin dependencias abiertas.
2. Por cada tarea:
   1. Escribe primero el test que refleja el AC (con `# AC-NNN-xx`) y comprueba que falla.
   2. Implementa lo mínimo para que pase, respetando capas y convenciones de `AGENTS.md`.
   3. Ejecuta `uv run poe check`. Si falla, arréglalo o informa con la salida.
   4. Marca la tarea `[x]` en `tasks.md` y anota cualquier desviación.
3. Si la spec o el plan resultan incorrectos o incompletos, detente y propone el cambio en el documento en lugar de improvisar.
4. Cuando no queden tareas: verifica cada AC, cambia el estado de la spec a `implementada` y actualiza `PLAN.md`.
5. No hagas commit ni push salvo que se pida.
