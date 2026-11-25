# Spec 006 — Clasificaciones, desempates y break

| Campo | Valor |
|---|---|
| Estado | borrador |
| Fase | 1 |
| Depende de | 005 |
| Última actualización | 2026-11-25 |

## 1. Objetivo
Calcular en todo momento la clasificación de equipos y de oradores con los criterios de desempate que configure cada torneo, y determinar qué equipos pasan a eliminatorias (break) en cada categoría, señalando los empates que necesiten decisión humana.

## 2. Actores
Miembro del equipo de tab. (Publicación al público en la spec 007.)

## 3. Historias de usuario
- Como tab, quiero ver la clasificación actualizada en cuanto confirmo boletas.
- Como tab, quiero elegir el orden de los desempates del torneo.
- Como tab, quiero saber qué equipos pasan al break y si hay un empate en la línea de corte.
- Como tab, quiero clasificaciones de oradores, también por categorías (p. ej. noveles).
- Como tab, quiero ver la clasificación tal como estaba al acabar una ronda concreta.

## 4. Requisitos funcionales
- **RF-006-01** — El sistema deberá calcular la clasificación de equipos usando solo boletas confirmadas y excluyendo a los equipos comodín.
- **RF-006-02** — El sistema deberá ordenar a los equipos por la lista de métricas configurada, en orden; cada métrica solo se aplica si las anteriores empatan.
- **RF-006-03** — El sistema deberá ofrecer estas métricas de equipo: puntos de equipo, victorias, total de puntos de orador, media de puntos de orador, suma de márgenes, draw strength (suma de puntos de los rivales), who-beat-whom, número de primeros y de segundos puestos (BP), votos de jueces ganados (voto individual) y sorteo (con semilla).
- **RF-006-04** — `who-beat-whom` solo se aplicará cuando exactamente dos equipos sigan empatados y se hayan enfrentado.
- **RF-006-05** — Si tras todas las métricas siguen empatados, el sistema deberá mostrarlos con el mismo puesto (p. ej. "5=") y marcarlos.
- **RF-006-06** — El sistema deberá calcular la clasificación de oradores con las métricas: total, media, media recortada (sin mejor ni peor nota), desviación típica (menor es mejor) y número de rondas habladas, con un mínimo de rondas configurable para aparecer.
- **RF-006-07** — El sistema deberá permitir filtrar la clasificación de oradores por categoría de orador.
- **RF-006-08** — El sistema deberá permitir ver ambas clasificaciones a fecha de cualquier ronda completada.
- **RF-006-09** — El sistema deberá permitir definir categorías de break (general, noveles…) con tamaño, prioridad, equipos elegibles y límite opcional de equipos por institución.
- **RF-006-10** — Cuando el tab calcule el break de una categoría, el sistema deberá listar a los equipos elegibles en orden de clasificación, marcar los N que pasan y explicar las exclusiones: no elegible, superado el límite por institución, ya clasificado en una categoría de mayor prioridad, retirado o descalificado.
- **RF-006-11** — Si hay empate en la línea de corte del break, el sistema deberá marcarlo y no cerrar el break hasta que el tab lo resuelva a mano (con nota) o aplique sorteo.
- **RF-006-12** — El sistema deberá permitir ajustes manuales del break con motivo, registrados en auditoría.
- **RF-006-13** — El sistema deberá generar la lista de mejores oradores (top N configurable).

## 5. Reglas de negocio y validaciones
- Draw strength excluye a los rivales comodín.
- Media de oradores: sobre los turnos efectivamente hablados; los iron-man cuentan una vez por turno.
- Un equipo retirado sigue en la clasificación con los resultados que tenga, marcado como retirado, y no puede entrar al break.
- Categorías de break se procesan por prioridad: un equipo que pasa en la general no ocupa plaza en noveles (salvo configuración contraria).

## 6. Criterios de aceptación
- **AC-006-01** — Dado el fixture `standings_academico_6eq` con resultados conocidos, cuando calculo la clasificación con desempates [puntos, total orador], entonces el orden coincide exactamente con el calculado a mano en el fixture.
- **AC-006-02** — Dados dos equipos empatados en puntos y total en los que A ganó a B, con desempates [puntos, total, who-beat-whom], entonces A queda por delante.
- **AC-006-03** — Dados tres equipos empatados en todo, con who-beat-whom en la lista, entonces no se aplica y los tres aparecen como empatados ("=").
- **AC-006-04** — Dado un break de 4 equipos donde el 4.º y el 5.º empatan en todas las métricas, cuando calculo el break, entonces se marca "empate en el corte" y no se puede confirmar hasta resolverlo.
- **AC-006-05** — Dado un límite de 2 equipos por institución y 3 equipos de la misma institución entre los 4 primeros, cuando calculo el break, entonces el tercero se marca "límite por institución" y pasa el siguiente elegible.
- **AC-006-06** — Dado un orador con 2 rondas habladas y mínimo de 3, entonces no aparece en la clasificación de oradores.
- **AC-006-07** — Dado un torneo con 4 rondas completadas, cuando consulto la clasificación "tras la ronda 2", entonces solo se usan las boletas de las rondas 1 y 2.
- **AC-006-08** — Dado un BP con desempates [puntos, total, primeros], entonces el equipo con más primeros puestos queda por delante cuando empatan en puntos y total.

## 7. Casos límite
- Equipo que no jugó una ronda (llegó tarde): media frente a total.
- Boleta corregida: la clasificación cambia al momento.
- Rondas silenciosas: se calculan igual, pero no se publican (spec 007).

## 8. Requisitos no funcionales
- Clasificación de 200 equipos y 9 rondas en < 1 s.
- Cálculo determinista (el sorteo usa semilla guardada).

## 9. Fuera de alcance
- Generación de rondas eliminatorias a partir del break (spec 008).
- Rankings de la liga o temporada entre torneos (se valorará; el modelo de datos lo permite).

## 10. Preguntas abiertas
- [ ] ¿Orden de desempates oficial de ADA para Académico y BP? — ADA
- [ ] ¿Categorías de break y de oradores (noveles, secundaria, universidad…)? — ADA
- [ ] ¿Hay límite de equipos por institución en el break? — ADA

## Historial
- 2026-11-25 — creación.
