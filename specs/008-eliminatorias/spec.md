# Spec 008 — Rondas eliminatorias

| Campo | Valor |
|---|---|
| Estado | borrador |
| Fase | 1 (adelantada desde la fase 2: el Nacional la necesita) |
| Depende de | 004, 005, 006 |
| Última actualización | 2026-11-25 |

## 1. Objetivo
Llevar el torneo desde el break hasta la final: generar el cuadro de eliminatorias a partir de los equipos clasificados, hacer avanzar a los ganadores ronda a ronda y publicarlo.

## 2. Actores
Miembro del equipo de tab; público (cuadro publicado).

## 3. Historias de usuario
- Como tab, quiero generar los cuartos de final directamente desde el break confirmado.
- Como tab, quiero que, al confirmar los resultados de una eliminatoria, la siguiente ronda se prepare sola con los ganadores.
- Como público, quiero ver el cuadro del torneo hasta la final.

## 4. Requisitos funcionales
- **RF-008-01** — Cuando el tab confirme el break de una categoría, el sistema deberá permitir crear las rondas eliminatorias necesarias (p. ej. con 8 equipos en formato de 2: cuartos, semifinal y final).
- **RF-008-02** — En formato de 2 equipos, el sistema deberá emparejar la primera eliminatoria por siembra (1.º–8.º, 4.º–5.º, 2.º–7.º, 3.º–6.º con 8 equipos) de forma que los mejores sembrados no se crucen hasta el final.
- **RF-008-03** — En BP, el sistema deberá formar salas de 4 por siembra (con 16 equipos: 1-8-9-16, 2-7-10-15, 3-6-11-14, 4-5-12-13) y hacer pasar a los 2 primeros de cada sala.
- **RF-008-04** — Si el número de clasificados no es potencia de 2 (formato de 2 equipos), el sistema deberá dar pase directo a los mejores sembrados en la primera eliminatoria.
- **RF-008-05** — El sistema deberá asignar las posiciones en eliminatorias según la regla configurada: elige el mejor sembrado, sorteo o equilibrio de posiciones.
- **RF-008-06** — Cuando todas las boletas de una eliminatoria estén confirmadas, el sistema deberá generar la siguiente con los equipos que avanzan, manteniendo el orden del cuadro.
- **RF-008-07** — El sistema deberá permitir configurar si en eliminatorias se recogen puntos de orador y el tamaño de panel (normalmente impar: 3 o 5).
- **RF-008-08** — En eliminatorias de 2 equipos no se permitirán empates, sea cual sea la configuración de las rondas preliminares.
- **RF-008-09** — El sistema deberá reutilizar la asignación de jueces (spec 004), las boletas (spec 005) y la publicación (spec 007), y mostrar en la web pública un cuadro con el avance de cada equipo.
- **RF-008-10** — Los resultados de eliminatorias no deberán afectar a la clasificación de las rondas preliminares ni a la de oradores (salvo configuración contraria).

## 5. Reglas de negocio y validaciones
- El cuadro se fija al generar la primera eliminatoria; cambios manuales posteriores quedan en auditoría.
- Un equipo eliminado no aparece en rondas posteriores.
- Equipo retirado tras el break: el tab decide si lo sustituye el siguiente clasificado (acción manual con motivo).

## 6. Criterios de aceptación
- **AC-008-01** — Dado un break confirmado de 8 equipos en Académico, cuando genero los cuartos, entonces los debates son 1–8, 4–5, 2–7 y 3–6, y los ganadores de 1–8 y 4–5 se enfrentan en semifinales.
- **AC-008-02** — Dado un break de 16 equipos en BP, cuando genero los cuartos, entonces hay 4 salas con siembras 1-8-9-16, 2-7-10-15, 3-6-11-14 y 4-5-12-13; al confirmar resultados, pasan los 2 primeros de cada sala a 2 semifinales.
- **AC-008-03** — Dado un break de 6 equipos en Académico, cuando genero la primera eliminatoria, entonces los sembrados 1.º y 2.º pasan directos y se juegan 3–6 y 4–5.
- **AC-008-04** — Dada una semifinal con las 2 boletas confirmadas, entonces la final se genera con los 2 ganadores y la regla de posiciones configurada.
- **AC-008-05** — Dado un torneo con eliminatorias jugadas, cuando consulto la clasificación de equipos de las rondas preliminares, entonces no ha cambiado.
- **AC-008-06** — Dado un cuadro publicado, cuando un visitante lo abre en el móvil, entonces ve cada ronda con los equipos, el ganador marcado y las rondas pendientes.

## 7. Casos límite
- Break con empate en el corte sin resolver: no se pueden generar eliminatorias (spec 006).
- Varias categorías de break (general y noveles) con cuadros independientes.
- Final de BP con 4 equipos: solo hay un ganador (1.º puesto).

## 8. Requisitos no funcionales
- Generar una ronda eliminatoria en < 1 s.

## 9. Fuera de alcance
- Re-siembra entre rondas (re-seeding) distinta del cuadro fijo.
- Rondas de repesca.

## 10. Preguntas abiertas
- [ ] Tamaño del break del Nacional y número de eliminatorias. — ADA
- [ ] ¿Quién elige posición en eliminatorias? — ADA
- [ ] ¿Puntos de orador en eliminatorias? ¿Tamaño de los paneles? — ADA
- [ ] ¿Hay break de noveles u otras categorías con cuadro propio? — ADA

## Historial
- 2026-11-25 — creación (adelantada de la fase 2, antigua 103).
