# Spec 003 — Emparejamientos (draw)

| Campo | Valor |
|---|---|
| Estado | borrador |
| Fase | 1 |
| Depende de | 001, 002 |
| Última actualización | 2026-11-25 |

## 1. Objetivo
Generar automáticamente el draw de cada ronda preliminar por sistema suizo (equipos con puntos similares se enfrentan), evitando revanchas y choques de la misma institución, equilibrando las posiciones, y permitir que el tab lo revise y corrija antes de confirmarlo.

## 2. Actores
Miembro del equipo de tab.

## 3. Historias de usuario
- Como tab, quiero generar el draw con un clic y tener una propuesta válida en segundos.
- Como tab, quiero ver de un vistazo los avisos del draw (revanchas, misma institución, posición repetida, pull-ups).
- Como tab, quiero intercambiar equipos o posiciones a mano cuando lo necesite.
- Como tab, quiero poder regenerar el draw y, si hace falta, reproducir exactamente uno anterior.
- Como equipo, quiero que a lo largo del torneo me toque defender a favor y en contra un número parecido de veces (o cada posición de BP de forma equilibrada).

## 4. Requisitos funcionales

### Generales
- **RF-003-01** — Cuando el tab pida generar el draw de una ronda, el sistema deberá crear una propuesta con todos los equipos disponibles, cada uno exactamente una vez, en debates de `teams_per_debate` equipos.
- **RF-003-02** — En la primera ronda, el sistema deberá emparejar al azar evitando, si es posible, equipos de la misma institución. Si hay sembrado (seed), deberá permitir usarlo.
- **RF-003-03** — En las rondas siguientes, el sistema deberá agrupar a los equipos por puntos de equipo acumulados (brackets) y emparejar dentro de cada bracket.
- **RF-003-04** — Si un bracket no se puede completar, el sistema deberá subir equipos del bracket inmediatamente inferior (pull-up) según la regla configurada: el mejor, el peor, al azar o el que menos pull-ups lleve.
- **RF-003-05** — El sistema deberá guardar la semilla usada; con la misma semilla y los mismos datos deberá generar exactamente el mismo draw.
- **RF-003-06** — El sistema deberá calcular y mostrar para cada debate sus avisos: revancha, misma institución, posición repetida o desequilibrada, pull-up, diferencia de bracket.
- **RF-003-07** — El sistema deberá permitir editar el draw: intercambiar dos equipos entre debates, intercambiar posiciones dentro de un debate y crear o eliminar debates, recalculando los avisos al momento.
- **RF-003-08** — El sistema deberá permitir regenerar el draw (nueva semilla) mientras no esté confirmado, pidiendo confirmación si hay cambios manuales que se perderían.
- **RF-003-09** — Cuando el tab confirme el draw, el sistema deberá fijarlo; cualquier edición posterior quedará registrada en auditoría. La publicación es aparte (spec 007).
- **RF-003-10** — Si el número de equipos disponibles no es múltiplo de `teams_per_debate`, el sistema deberá impedir generar el draw e indicar cuántos equipos comodín (swing) faltan o sobran, salvo que el torneo use la política "bye" en formato de 2 equipos.

### Formato de 2 equipos (Académico)
- **RF-003-11** — Dentro de cada bracket el sistema deberá emparejar según el método configurado: `slide` (1.º contra el primero de la mitad inferior), `fold` (1.º contra último) o al azar.
- **RF-003-12** — El sistema deberá evitar revanchas siempre que exista un draw sin ellas respetando los brackets o moviendo equipos lo mínimo posible.
- **RF-003-13** — Si `avoid_same_institution` está activo, el sistema deberá evitar enfrentar equipos de la misma institución siempre que sea posible, con menos prioridad que las revanchas.
- **RF-003-14** — El sistema deberá asignar "A favor" al equipo que menos veces lo haya sido; con empate, al azar con la semilla.
- **RF-003-15** — Con política "bye", el sistema deberá dar el bye al equipo de menor clasificación que aún no lo haya recibido, y sumarle los puntos configurados.

### Formato BP
- **RF-003-16** — El sistema deberá formar salas de 4 equipos por brackets de puntos (0–3 por ronda), completando con pull-ups cuando haga falta.
- **RF-003-17** — El sistema deberá asignar las posiciones (Cámara Alta a favor, Cámara Alta en contra, Cámara Baja a favor, Cámara Baja en contra) minimizando el desequilibrio acumulado de posiciones de cada equipo, según el coste configurado (`squared` o `entropy`), pudiendo mover equipos entre salas del mismo bracket para lograrlo.
- **RF-003-18** — En BP no se evitan revanchas (es normal coincidir); sí se aplica la preferencia de no coincidir con la misma institución si está activa.

## 5. Reglas de negocio y validaciones
- Puntos de equipo: los de `points_by_rank` del formato (Académico 1/0, BP 3/2/1/0) más, en su caso, los del bye.
- Los equipos comodín (swing) se emparejan pero no clasifican ni cuentan para el draw strength de sus rivales.
- Prioridad de criterios en 2 equipos: (1) cada equipo una vez; (2) sin revanchas; (3) respetar brackets / mínimos pull-ups; (4) sin misma institución; (5) equilibrio de posiciones.
- Ninguna restricción blanda impide generar un draw: si no se puede cumplir, se genera igualmente y se avisa.

## 6. Criterios de aceptación
- **AC-003-01** — Dados 20 equipos disponibles en Académico, cuando genero la ronda 1, entonces hay 10 debates, cada equipo aparece una vez y ningún debate enfrenta a equipos de la misma institución (con al menos 4 instituciones distintas y ninguna con más de la mitad de los equipos).
- **AC-003-02** — Dado un torneo simulado de 20 equipos y 5 rondas con resultados aleatorios, repetido con 200 semillas distintas, cuando genero todos los draws, entonces no hay ninguna revancha.
- **AC-003-03** — En la misma simulación, tras 4 rondas, al menos el 95 % de los equipos tiene una diferencia entre veces "A favor" y "En contra" ≤ 1 y ninguno > 2.
- **AC-003-04** — Dado un bracket de 3 equipos con 2 puntos y la regla `top`, cuando genero el draw, entonces sube el mejor clasificado del bracket de 1 punto y el debate se marca como pull-up.
- **AC-003-05** — Dado un draw generado con la semilla 42, cuando lo regenero con la semilla 42 sin cambios en los datos, entonces el resultado es idéntico.
- **AC-003-06** — Dados 21 equipos en Académico sin equipo comodín y con política `swing`, cuando intento generar el draw, entonces se muestra el mensaje "Falta 1 equipo comodín" y no se genera.
- **AC-003-07** — Dados 20 equipos en BP tras 3 rondas, cuando genero la ronda 4, entonces hay 5 salas de 4 equipos y la asignación de posiciones tiene coste mínimo dentro de cada bracket (comprobado contra fuerza bruta en casos de hasta 8 equipos).
- **AC-003-08** — Dado un torneo BP simulado de 20 equipos y 4 rondas con 200 semillas, entonces ningún equipo ha ocupado la misma posición más de 2 veces cuando existía una asignación que lo evitaba.
- **AC-003-09** — Dado un draw, cuando intercambio dos equipos que provoca una revancha, entonces el aviso "revancha" aparece en ese debate al instante y se puede guardar igualmente.
- **AC-003-10** — Dado un draw confirmado, cuando intercambio dos equipos, entonces el cambio queda en el log de auditoría con el estado anterior.
- **AC-003-11** — Dado cualquier draw generado o editado, entonces nunca hay un equipo en dos debates de la misma ronda (garantizado por la BD).

## 7. Casos límite
- Ronda en la que todos los emparejamientos posibles sin revancha rompen brackets (final de torneo con pocos equipos): se prioriza no repetir y se avisa del salto de bracket.
- Institución con más de la mitad de los equipos: se generan choques inevitables y se avisa.
- Equipo retirado a mitad de torneo: deja de contar; si queda número impar, aplica RF-003-10.
- Equipo que entra tarde (sin resultados en rondas previas): empieza en el bracket de 0 puntos.

## 8. Requisitos no funcionales
- Generación del draw de 200 equipos en < 5 s; de 20 equipos en < 1 s.
- Determinismo total con semilla (sin depender de la hora ni del orden de la BD).

## 9. Fuera de alcance
- Rondas eliminatorias (spec 008).
- Brackets intermedios u otras variantes avanzadas de pull-up (p. ej. reglas AIDA).
- Emparejamientos para formatos de 3 equipos.

## 10. Preguntas abiertas
- [ ] ¿Método preferido dentro del bracket en Académico (`slide` o `fold`)? — ADA
- [ ] ¿Regla de pull-up que usa ADA? — ADA
- [ ] ¿Swing o bye cuando sale número impar? ¿Cuántos puntos da un bye? — ADA
- [ ] ¿Hay sembrado (cabezas de serie) en la ronda 1? — ADA

## Historial
- 2026-11-25 — creación.
