# CLAUDE.md

@AGENTS.md

## Específico de Claude Code

### Comandos SDD (en `.claude/commands/`)

| Comando | Qué hace |
|---|---|
| `/sdd-spec <NNN o idea>` | Crea o refina `specs/NNN-slug/spec.md`. Solo qué y por qué. |
| `/sdd-plan <NNN>` | Escribe `plan.md` a partir de una spec **aprobada**. |
| `/sdd-tasks <NNN>` | Descompone el plan en `tasks.md`. |
| `/sdd-implement <NNN> [T-xx]` | Implementa tareas una a una, test primero. |
| `/sdd-verify <NNN>` | Comprueba la implementación contra cada AC de la spec y lista huecos. |

### Forma de trabajar

- Carga solo el contexto necesario: la spec y el plan de la funcionalidad, la constitución y las secciones afectadas del modelo de datos. No leas todos los documentos en cada tarea.
- Usa el modo plan para cambios que toquen el modelo de datos o más de una app.
- Para revisar una funcionalidad terminada, lanza un subagente con la spec y el diff (no con tu conclusión) y pídele que busque AC incumplidos.
- Ejecuta `uv run poe check` antes de dar una tarea por hecha. Si falla, enséñalo con la salida; no lo maquilles.
- No hagas commit, push ni despliegues salvo que se te pida.
- Un hook (`.claude/settings.json` → `scripts/check_leaks.py --hook`) revisa cada `git commit` y `git push` y los bloquea si hay fugas. Si te bloquea, **nunca lo esquives**: enseña los hallazgos al usuario y corrige la causa. Antes de cada commit, revisa además el diff completo tú mismo (ver "Antes de cada commit y cada push" en AGENTS.md).
- La carpeta `comercial/` es interna: no la incluyas en commits ni la uses como contexto técnico.
