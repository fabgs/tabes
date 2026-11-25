# Spec 002 — Conflictos

| Campo | Valor |
|---|---|
| Estado | borrador |
| Fase | 1 |
| Depende de | 001 |
| Última actualización | 2026-11-25 |

## 1. Objetivo
Registrar qué jueces no pueden evaluar a qué equipos o instituciones (o juzgar junto a qué otros jueces), para que la asignación automática los respete y la manual los señale.

## 2. Actores
Miembro del equipo de tab.

## 3. Historias de usuario
- Como tab, quiero que un juez no evalúe automáticamente a equipos de su propia institución.
- Como tab, quiero marcar conflictos personales (exalumnos, familiares, entrenadores) entre un juez y un equipo o institución.
- Como tab, quiero importar los conflictos declarados en la inscripción.
- Como tab, quiero ver todos los conflictos de un juez de un vistazo.

## 4. Requisitos funcionales
- **RF-002-01** — El sistema deberá permitir registrar conflictos juez–equipo, juez–institución y juez–juez, con una nota opcional.
- **RF-002-02** — Si el torneo tiene activada la opción "conflicto con la propia institución", el sistema deberá considerar en conflicto a cada juez con su institución sin que nadie lo registre a mano.
- **RF-002-03** — Un conflicto juez–institución deberá aplicarse a todos los equipos de esa institución, incluidos los que se añadan después.
- **RF-002-04** — El sistema deberá permitir importar conflictos desde CSV/Excel con la misma vista previa y validación de la spec 001.
- **RF-002-05** — El sistema deberá mostrar, para cada juez, sus conflictos (directos y derivados) y, para cada equipo, los jueces en conflicto con él.
- **RF-002-06** — El sistema deberá ofrecer una consulta "¿puede el juez X juzgar el debate Y?" que devuelva sí/no y los motivos; la usarán la asignación (spec 004) y el tablero manual.
- **RF-002-07** — El sistema deberá permitir registrar conflictos entre un equipo y una institución (por ejemplo, un equipo mixto con miembros de otra institución) para que el emparejamiento lo trate como "misma institución".
- **RF-002-08** — Las notas de los conflictos solo serán visibles para el equipo de tab.

## 5. Reglas de negocio y validaciones
- Conflictos duros (bloquean la asignación automática): juez–equipo, juez–institución (incluida la propia), juez–juez dentro del mismo panel.
- No se puede registrar un conflicto de un juez consigo mismo ni duplicado.
- Al retirar un juez o equipo, sus conflictos se conservan (histórico) pero dejan de aplicarse.

## 6. Criterios de aceptación
- **AC-002-01** — Dado un juez de la institución "IES Jorge Juan" con la opción de propia institución activada, cuando consulto si puede juzgar a un equipo de esa institución, entonces la respuesta es "no" con motivo "propia institución".
- **AC-002-02** — Dado un conflicto juez–institución con "Universidad de Alicante", cuando añado después un equipo nuevo de esa universidad, entonces el juez queda en conflicto con ese equipo.
- **AC-002-03** — Dado un conflicto entre los jueces A y B, cuando consulto si B puede unirse a un panel donde está A, entonces la respuesta es "no".
- **AC-002-04** — Dado un CSV de conflictos con un juez inexistente, cuando lo subo, entonces esa fila se marca como error y no se importa nada.
- **AC-002-05** — Dado un juez sin institución (independiente) y sin conflictos, cuando consulto cualquier debate, entonces la respuesta es "sí".

## 7. Casos límite
- Juez de una institución sin equipos en el torneo.
- Conflicto registrado dos veces por vías distintas (manual e importación) → uno solo.
- Juez que también es orador de un equipo (caso raro): en conflicto con su propio equipo automáticamente.

## 8. Requisitos no funcionales
- La consulta de conflictos para una ronda completa (50 debates × 150 jueces) tarda < 200 ms.

## 9. Fuera de alcance
- Conflictos declarados por los propios participantes desde un formulario (fase 2, con roles).
- Conflictos "blandos" por historial (ya vio al equipo): se tratan en la spec 004 como penalización.

## 10. Preguntas abiertas
- [ ] ¿ADA recoge hoy conflictos en la inscripción? ¿En qué formato? — ADA

## Historial
- 2026-11-25 — creación.
