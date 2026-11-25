# Glosario y formatos de ADA

Vocabulario común para specs, código e interfaz. En el código los identificadores van en inglés (columna "Código"); en la interfaz, en español.

## Términos del dominio

| Término (UI) | Código | Definición |
|---|---|---|
| Torneo | `Tournament` | Competición con varias rondas, participantes y reglas propias. |
| Institución | `Institution` | Centro, universidad o club al que pertenecen equipos y jueces. |
| Equipo | `Team` | Grupo de oradores que compite junto en un torneo. |
| Orador / debatiente | `Speaker` | Participación de una persona como miembro de un equipo en un torneo. |
| Persona | `Person` | Identidad global (entre torneos) de un debatiente o juez. Base del histórico y de las cuentas de la app. |
| Juez | `Adjudicator` | Participación de una persona como juez en un torneo. Tiene una **nota** (nivel) usada para la asignación. |
| Sala | `Venue` | Aula donde se celebra un debate. |
| Ronda preliminar | `Round(stage=prelim)` | Ronda abierta a todos los equipos; se empareja por sistema suizo. |
| Ronda eliminatoria | `Round(stage=elim)` | Octavos, cuartos, semifinal, final. Solo equipos clasificados (spec 008). |
| Draw / emparejamiento | `Debate` + `DebateTeam` | Lista de debates de una ronda: quién contra quién, en qué posición y sala. |
| Sistema suizo / power pairing | — | Emparejar equipos con puntuación similar ronda a ronda. |
| Bracket | `Debate.bracket` | Grupo de equipos con los mismos puntos de equipo antes de la ronda. |
| Pull-up | `DebateTeam.flags.pullup` | Equipo que sube a un bracket superior para completar un debate. |
| Revancha | — | Dos equipos que ya se han enfrentado. Se evita en formato de 2 equipos. |
| Posición / lado | `DebateTeam.side` | A favor / En contra (Académico) o una de las 4 posiciones de BP. Se guarda como índice 0..N-1. |
| Equipo comodín (swing) | `Team.is_swing` | Equipo formado ad hoc para completar un número impar. No clasifica. |
| Bye | — | Ronda sin rival para un equipo (alternativa al swing). |
| Moción | `Motion` | Tema del debate. Puede tener **infoslide** (contexto). |
| Boleta | `Ballot` | Resultado de un debate: ganador/posiciones y puntos de orador. Tiene versiones; solo una confirmada. |
| Hoja de boleta | `BallotSheet` | Lo que rellena un juez concreto (panel con voto individual) o el panel entero (consenso). |
| Panel | `DebateAdjudicator` | Jueces asignados a un debate: **presidente** (chair), **vocales** (panellists) y **en prácticas** (trainees). |
| Importancia | `Debate.importance` | Prioridad del debate para recibir mejores jueces y salas (−2..+2). |
| Conflicto | `*Conflict` | Restricción: un juez no puede juzgar a un equipo, a una institución o junto a otro juez. |
| Puntos de equipo | `TeamResult.points` | Puntos por resultado: Académico 1/0 (victoria/derrota); BP 3/2/1/0. |
| Puntos de orador | `SpeechScore.score` | Nota individual por intervención, dentro del rango del formato. |
| Desempate | `team_tiebreaks` | Criterios ordenados que deciden la clasificación cuando hay igualdad. |
| Draw strength | `draw_strength` | Suma de los puntos de los rivales a los que se ha enfrentado un equipo. |
| Who-beat-whom | `who_beat_whom` | Si dos equipos empatados se enfrentaron, gana quien venció ese debate. |
| Iron-man | `SpeechScore.is_iron` | Un orador que interviene dos veces porque falta un compañero. |
| Break | `BreakingTeam` | Equipos que pasan a eliminatorias. Puede haber varias **categorías de break** (general, noveles…). |
| Ronda silenciosa | `Round.is_silent` | Ronda cuyos resultados no se publican hasta el final. |
| Publicar (liberar) | `*_released_at` | Hacer visible en la web pública el draw, las mociones o los resultados. Siempre acción explícita. |
| Equipo de tab | rol `tab` | Personas que gestionan el torneo en la herramienta. |
| CA (Chief Adjudicator) | rol `ca` | Responsable de jueces y mociones (fase 2: permisos propios). |
| Boleta electrónica | `Ballot(source=eballot)` | Boleta que el juez rellena desde el móvil con un enlace privado (fase 2). |
| Feedback | `FeedbackSubmission` | Valoración de equipos (y jueces) sobre los jueces (fase 2). |

## Formatos de ADA

Fuente: configuración por defecto del [cronómetro de ADA](https://cronometro-ada.vercel.app/). Todos los valores son **configurables por torneo**. Los datos marcados con ⚠ hay que confirmarlos con ADA.

### Formato Académico (2 equipos)

- Equipos por debate: **2** → posiciones `0 = A favor`, `1 = En contra`.
- Tamaño de equipo: hasta **5** personas ⚠ (¿mínimo? ¿cada persona hace un único turno?).
- Puntos de equipo: victoria 1, derrota 0 ⚠ (¿se permiten empates?).

| # | Turno | Posición | Duración | ¿Puntúa? |
|---|---|---|---|---|
| 1 | Introducción | A favor | 4:00 | sí |
| 2 | Preguntas cruzadas a A favor | A favor (responde) | 2:00 | ⚠ |
| 3 | Introducción | En contra | 4:00 | sí |
| 4 | Preguntas cruzadas a En contra | En contra (responde) | 2:00 | ⚠ |
| 5 | Refutación 1 | A favor | 5:00 | sí |
| 6 | Refutación 1 | En contra | 5:00 | sí |
| 7 | Refutación 2 | A favor | 5:00 | sí |
| 8 | Refutación 2 | En contra | 5:00 | sí |
| 9 | Refutación 3 (última, tiempo propio) | A favor | 1:30 | sí |
| 10 | Refutación 3 (última, tiempo propio) | En contra | 1:30 | sí |
| 11 | Conclusión | En contra | 3:00 | sí |
| 12 | Conclusión | A favor | 3:00 | sí |

Parámetros del cronómetro: número de refutaciones (1–10, por defecto 3) y tiempo diferente para la última refutación (por defecto activado, 1:30). Fases auxiliares: deliberación de jueces 10:00 y feedback 15:00.

### British Parliament (BP, 4 equipos)

- Equipos por debate: **4**, 2 oradores por equipo.
- Posiciones: `0 = Cámara Alta a favor`, `1 = Cámara Alta en contra`, `2 = Cámara Baja a favor`, `3 = Cámara Baja en contra`.
- Puntos de equipo: 1.º 3, 2.º 2, 3.º 1, 4.º 0. Sin empates.
- Rango de puntos de orador ⚠ (en el circuito internacional se usa 50–100; confirmar el de ADA).

| # | Turno | Posición | Duración |
|---|---|---|---|
| 1 | Primer Ministro | Cámara Alta a favor | 7:00 |
| 2 | Líder de Oposición | Cámara Alta en contra | 7:00 |
| 3 | Viceprimer Ministro | Cámara Alta a favor | 7:00 |
| 4 | Vicelíder de Oposición | Cámara Alta en contra | 7:00 |
| 5 | Extensión de Gobierno | Cámara Baja a favor | 7:00 |
| 6 | Extensión de la Oposición | Cámara Baja en contra | 7:00 |
| 7 | Látigo de Gobierno | Cámara Baja a favor | 7:00 |
| 8 | Látigo de la Oposición | Cámara Baja en contra | 7:00 |

### Implicación para el sistema

La definición de turnos (`speech_slots`) vive en las reglas del torneo y alimenta tres cosas: el formulario de boleta (qué intervenciones se puntúan y de qué equipo), el horario del torneo y, más adelante, el cronómetro integrado en la app y el cronómetro web, que podrá cargar el formato directamente desde el torneo.
