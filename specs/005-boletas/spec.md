# Spec 005 — Boletas

| Campo | Valor |
|---|---|
| Estado | borrador |
| Fase | 1 |
| Depende de | 000, 003 |
| Última actualización | 2026-11-26 |

## 1. Objetivo
Que el equipo de tab introduzca el resultado de cada debate (ganador o posiciones y puntos de orador) a partir de las boletas en papel, con validaciones que impidan resultados imposibles, un paso de confirmación y la posibilidad de corregir sin perder la versión anterior.

## 2. Actores
Miembro del equipo de tab. (En fase 2, el juez desde su móvil con el mismo formulario y las mismas validaciones.)

## 3. Historias de usuario
- Como tab, quiero ver qué debates de la ronda tienen ya resultado y cuáles faltan.
- Como tab, quiero introducir una boleta en menos de un minuto y que el sistema me avise si algo no cuadra.
- Como tab, quiero que otra persona confirme lo que he tecleado para evitar errores.
- Como tab, quiero corregir un resultado ya confirmado dejando constancia del motivo.

## 4. Requisitos funcionales
- **RF-005-01** — El sistema deberá mostrar el estado de resultados de la ronda: total de debates, sin boleta, en borrador, pendientes de confirmar y confirmadas.
- **RF-005-02** — El sistema deberá ofrecer un formulario por debate con: moción debatida (si había varias), para cada turno puntuable el orador que lo hizo y su puntuación, y el resultado (ganador en 2 equipos; puesto 1.º–4.º en BP).
- **RF-005-03** — El sistema deberá proponer por defecto el orden de oradores de la ronda anterior de cada equipo.
- **RF-005-04** — Si la regla de ganador es `by_totals`, el sistema deberá calcular el ganador o los puestos a partir de los totales y mostrarlos.
- **RF-005-05** — Si la regla de ganador es `declared`, el sistema deberá permitir declarar el ganador; si contradice los totales y `allow_low_point_win` está desactivado, deberá impedir guardar; si está activado, deberá pedir confirmación.
- **RF-005-06** — El sistema deberá rechazar puntuaciones fuera del rango o que no sean múltiplo del paso del formato.
- **RF-005-07** — Si el formato no permite empates, el sistema deberá rechazar totales iguales entre equipos (2 equipos) o entre cualesquiera dos equipos (BP).
- **RF-005-08** — El sistema deberá rechazar que un mismo orador haga dos turnos salvo que el formato permita iron-man; en ese caso pedirá confirmación y lo marcará.
- **RF-005-09** — En modo de voto individual, el sistema deberá recoger una hoja por juez del panel, decidir el ganador por mayoría y calcular las puntuaciones de orador según la agregación configurada (media de todos o de la mayoría).
- **RF-005-10** — Si el formato tiene rúbrica por criterios, el sistema deberá pedir la nota de cada criterio y calcular la puntuación del turno con sus pesos.
- **RF-005-11** — El sistema deberá permitir guardar una boleta como borrador y enviarla a confirmar. Si el torneo exige doble control, la confirmación deberá hacerla un usuario distinto del que la introdujo.
- **RF-005-12** — Cuando se confirme una boleta, el sistema deberá fijar sus resultados para la clasificación y registrar quién y cuándo.
- **RF-005-13** — El sistema no deberá permitir editar una boleta confirmada; para corregir, se crea una versión nueva y, al confirmarla, la anterior pasa a descartada con el motivo indicado.
- **RF-005-14** — El sistema deberá permitir registrar una incomparecencia (forfeit): el equipo presente gana sin puntuaciones de orador.
- **RF-005-15** — Cuando todas las boletas de una ronda estén confirmadas, el sistema deberá permitir marcar la ronda como completada.

## 5. Reglas de negocio y validaciones
- Totales: suma de puntuaciones de los turnos puntuables de cada equipo.
- Margen (2 equipos): diferencia de totales, positiva para el ganador.
- BP: puestos únicos 1–4; con `by_totals`, mayor total = mejor puesto.
- Turnos no puntuables (p. ej. preguntas cruzadas, si así se configura) no piden nota.
- Puntos de equipo según `points_by_rank`.

## 6. Criterios de aceptación
- **AC-005-01** — Dado un formato con rango 60–80 y paso 0,5, cuando introduzco 80,5 o 72,3, entonces el formulario lo rechaza indicando el rango y el paso.
- **AC-005-02** — Dado Académico sin empates y regla `by_totals`, cuando ambos equipos suman 350, entonces no se puede guardar y se indica "empate no permitido".
- **AC-005-03** — Dado BP con `by_totals`, cuando introduzco puntuaciones, entonces los puestos se calculan solos y no puedo asignar el 1.º a un equipo con menos total que otro.
- **AC-005-04** — Dada una regla `declared` con `allow_low_point_win` desactivado, cuando declaro ganador al equipo con menos total, entonces no se puede guardar.
- **AC-005-05** — Dado doble control activado, cuando el usuario que introdujo la boleta intenta confirmarla, entonces la acción no está disponible para él.
- **AC-005-06** — Dada una boleta confirmada, cuando creo una corrección y la confirmo con motivo "error de transcripción", entonces la anterior queda descartada con ese motivo, la clasificación usa la nueva y ambas siguen consultables.
- **AC-005-07** — Dado un panel de 3 jueces con voto individual en el que 2 dan ganador a "A favor", cuando confirmo, entonces gana "A favor" con 2 votos de 3.
- **AC-005-08** — Dada una ronda con 10 debates y 10 boletas confirmadas, entonces el estado muestra 10/10 y se puede marcar la ronda como completada.
- **AC-005-09** — Dado un orador que aparece en dos turnos sin iron-man permitido, cuando guardo, entonces se rechaza.
- **AC-005-10** — Dada una boleta con un punto de orador fuera de rango, cuando guardo, entonces el foco va a un resumen de errores que indica qué orador falla y qué rango se admite, con un enlace que lleva al campo.

## 7. Casos límite
- Dos personas introduciendo a la vez la boleta del mismo debate: la segunda ve que ya existe un borrador.
- Equipo con un orador ausente (iron-man) o con menos oradores que turnos.
- Cambio de reglas de puntuación después de tener boletas (ver RF-000-07).

## 8. Requisitos no funcionales
- Formulario utilizable solo con teclado (tabulación en orden lógico) para introducir rápido.
- WCAG 2.2 AA. Cada error aparece en texto junto a su campo y en un resumen al principio del formulario.
- Guardar una boleta < 500 ms.

## 9. Fuera de alcance
- Boletas electrónicas desde el móvil del juez (fase 2, spec 101), que reutilizarán estas validaciones.
- Doble entrada ciega (dos personas teclean por separado y se comparan): se valorará.

## 10. Preguntas abiertas
- [ ] ¿Cómo es hoy la boleta en papel de ADA en cada formato? Pedir una foto. — ADA
- [ ] ¿Quieren doble control obligatorio? — ADA
- [ ] ¿Cuántos puntos se dan por incomparecencia? — ADA

## Historial
- 2026-11-25 — creación.
- 2026-11-26 — accesibilidad: AC-005-10 y requisito de errores accesibles.
