---
description: Crear o refinar una especificación SDD (qué y por qué, sin cómo)
argument-hint: <NNN o descripción de la funcionalidad>
---

Trabaja en la especificación: $ARGUMENTS

1. Lee `docs/constitucion.md`, `docs/glosario.md`, `specs/README.md` y la tabla de specs de `PLAN.md`.
2. Si ya existe `specs/NNN-*/spec.md`, refínala. Si no, crea `specs/<siguiente número libre>-<slug>/spec.md` a partir de `specs/_plantillas/spec.md`.
3. Describe **qué** debe hacer el sistema y **por qué**. No nombres tecnologías, modelos, tablas ni clases.
4. Requisitos funcionales con ID `RF-NNN-xx` en formato EARS ("Cuando <evento>, el sistema deberá <respuesta>"; "Si <condición>, el sistema deberá…").
5. Criterios de aceptación verificables con ID `AC-NNN-xx` en formato Dado / Cuando / Entonces, con datos concretos.
6. Incluye casos límite, requisitos no funcionales medibles y una sección "Fuera de alcance".
7. Lo que no puedas deducir de los documentos va a "Preguntas abiertas". **No lo inventes.**
8. Deja `Estado: borrador`, añade la spec a la tabla de `PLAN.md` y resume al usuario las preguntas abiertas. Solo el usuario la marca como `aprobada`.
