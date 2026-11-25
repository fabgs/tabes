# TabES — Tabulación de torneos de debate

Plataforma web de tabulación de debate en **marca blanca**: cada asociación la ve con su nombre, logo, colores y dominio. Incluye gestión de torneos, emparejamientos por sistema suizo (formato Académico y British Parliament), asignación de jueces, boletas, clasificaciones, break y publicación de resultados. En una fase posterior, una app móvil (iOS/Android) para debatientes con notificaciones push.

Primer cliente: **Asociación de Debate de Alicante (ADA)**.

> Estado: **planificación**. Todavía no hay código. Desarrollo guiado por especificaciones (SDD).
>
> Software libre: © 2026 [Fabián Godoy Silvestre](https://fabgs.dev). Web bajo [AGPL-3.0-or-later](LICENSE) (ver [NOTICE](NOTICE)); app móvil bajo MIT.
>
> Repositorios: [github.com/fabgs/tabes](https://github.com/fabgs/tabes) (web) · [github.com/fabgs/tabes-app](https://github.com/fabgs/tabes-app) (app, fase 3).

## Mapa del repositorio

| Documento | Para qué sirve |
|---|---|
| [PLAN.md](PLAN.md) | Hoja de ruta: fases, hitos, estado de las specs, riesgos y preguntas abiertas |
| [AGENTS.md](AGENTS.md) | Instrucciones para cualquier agente de código: stack, comandos, convenciones, flujo SDD |
| [CLAUDE.md](CLAUDE.md) | Instrucciones específicas de Claude Code (importa AGENTS.md) |
| [docs/constitucion.md](docs/constitucion.md) | Principios no negociables |
| [docs/arquitectura.md](docs/arquitectura.md) | Stack, componentes, despliegue, dimensionado, copias, seguridad, RGPD y ADR |
| [docs/modelo-datos.md](docs/modelo-datos.md) | Modelo de datos: entidades, relaciones e invariantes |
| [docs/glosario.md](docs/glosario.md) | Vocabulario del dominio y formatos de ADA |
| [docs/app-movil.md](docs/app-movil.md) | App de debatientes, notificaciones y publicación en tiendas |
| [specs/](specs/) | Especificaciones por funcionalidad (spec → plan → tasks) |
| [.claude/commands/](.claude/commands/) | Comandos `/sdd-spec`, `/sdd-plan`, `/sdd-tasks`, `/sdd-implement`, `/sdd-verify` |

## Primeros pasos tras clonar (obligatorio)

```bash
git config core.hooksPath .githooks          # activa el detector de fugas en commit y push
git config user.email "ID+usuario@users.noreply.github.com" # tu email anónimo de GitHub
chmod +x .githooks/*                          # solo en Linux/macOS
```

El repositorio es público. Antes de cada commit y cada push se ejecuta `scripts/check_leaks.py` (ver la sección "Antes de cada commit y cada push" en [AGENTS.md](AGENTS.md)).

## Flujo de trabajo

```
/sdd-spec 003   →  revisar y aprobar spec.md
/sdd-plan 003   →  plan.md
/sdd-tasks 003  →  tasks.md
/sdd-implement 003
/sdd-verify 003
```
