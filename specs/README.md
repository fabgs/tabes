# Especificaciones (SDD)

Cada funcionalidad tiene su carpeta `specs/NNN-slug/` con tres documentos:

| Documento | Responde a | Lo escribe | Lo aprueba |
|---|---|---|---|
| `spec.md` | **Qué** y **por qué**. Sin tecnología. | `/sdd-spec` + revisión humana | Desarrollador (y ADA si cambia el alcance contratado) |
| `plan.md` | **Cómo**: modelo, servicios, vistas, tests. | `/sdd-plan` | Desarrollador |
| `tasks.md` | **Pasos** de ≤ 2 h con verificación. | `/sdd-tasks` | — |

## Estados de una spec

`borrador` → `en revisión` → `aprobada` → `en curso` → `implementada` → (`obsoleta`)

- Solo se planifica e implementa una spec **aprobada**.
- Un cambio de comportamiento sobre una spec implementada se hace editando la spec (nueva fecha y nota en su historial) antes de tocar código.
- Si el cambio altera el alcance contratado con ADA, se valora como ampliación.

## Convenciones

- Numeración de 3 cifras; 000–099 fase 1, 100–199 fase 2, 200–299 fase 3 (API y backend de la app).
- IDs estables: `RF-NNN-xx` (requisitos), `AC-NNN-xx` (criterios de aceptación). Los tests los citan.
- Requisitos en formato **EARS**: "Cuando <evento>, el sistema deberá…", "Si <condición>, el sistema deberá…", "El sistema deberá…".
- Criterios de aceptación en **Dado / Cuando / Entonces**, con datos concretos y verificables.
- Lo desconocido va a "Preguntas abiertas"; no se inventa.

## Índice

El estado de cada spec se lleva en un solo sitio: la tabla §6 de [PLAN.md](../PLAN.md).

| Spec | Fase |
|---|---|
| [000 Base de la plataforma](000-base-plataforma/spec.md) | 1 |
| [001 Gestión de datos e importación](001-gestion-datos/spec.md) | 1 |
| [002 Conflictos](002-conflictos/spec.md) | 1 |
| [003 Emparejamientos](003-emparejamientos/spec.md) | 1 |
| [004 Asignación de jueces y salas](004-asignacion-jueces/spec.md) | 1 |
| [005 Boletas](005-boletas/spec.md) | 1 |
| [006 Clasificaciones y break](006-clasificaciones-break/spec.md) | 1 |
| [007 Publicación](007-publicacion/spec.md) | 1 |
| [008 Rondas eliminatorias](008-eliminatorias/spec.md) | 1 |
| 101 Boletas electrónicas · 102 Feedback · 104 Roles · 105 Exportación | Mejoras opcionales (por escribir) |
| 201 Cuentas de debatientes · 202 API para la app · 203 Notificaciones y horario | 3 (por escribir) |

Las specs de la app móvil (pantallas) viven en el repositorio `tabes-app`; ver [docs/app-movil.md](../docs/app-movil.md).
