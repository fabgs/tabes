# Spec 004 — Asignación de jueces y salas

| Campo | Valor |
|---|---|
| Estado | borrador |
| Fase | 1 |
| Depende de | 002, 003 |
| Última actualización | 2026-11-26 |

## 1. Objetivo
Proponer automáticamente qué jueces juzgan cada debate (presidente, vocales y jueces en prácticas) y en qué sala se celebra, respetando conflictos y priorizando a los mejores jueces en los debates más importantes; y permitir ajustarlo arrastrando y soltando.

## 2. Actores
Miembro del equipo de tab (y, en fase 2, el CA).

## 3. Historias de usuario
- Como tab, quiero una asignación automática válida en segundos tras confirmar el draw.
- Como tab, quiero mover jueces entre debates arrastrándolos y ver al instante si creo un conflicto.
- Como tab, quiero ver qué jueces quedan sin asignar y ordenarlos por nota.
- Como tab, quiero marcar un debate como más o menos importante para que reciba mejores jueces.
- Como juez con movilidad reducida, quiero que me asignen una sala accesible.

## 4. Requisitos funcionales
- **RF-004-01** — El sistema deberá calcular la importancia de cada debate a partir de su bracket (más puntos = más importante) y permitir ajustarla a mano entre −2 y +2.
- **RF-004-02** — Cuando el tab pida la asignación automática, el sistema deberá asignar un presidente por debate entre los jueces disponibles que no estén en prácticas, dando las mejores notas a los debates más importantes.
- **RF-004-03** — El sistema deberá completar los paneles con vocales hasta el tamaño configurado para la ronda y, si quedan, repartir los jueces en prácticas.
- **RF-004-04** — La asignación automática no deberá poner nunca a un juez en conflicto duro (spec 002) con un equipo del debate ni con otro juez del panel.
- **RF-004-05** — La asignación automática deberá penalizar (sin prohibir) que un juez vuelva a ver a un equipo que ya juzgó.
- **RF-004-06** — Si no hay jueces suficientes o válidos, el sistema deberá dejar huecos en los debates menos importantes primero y avisar de cada hueco.
- **RF-004-07** — El sistema deberá mostrar un tablero con una fila por debate (equipos, posición, bracket, sala, importancia) y huecos de presidente, vocales y prácticas, más una lista de jueces sin asignar filtrable y ordenable por nota.
- **RF-004-08** — El sistema deberá permitir arrastrar un juez a un hueco libre, a un hueco ocupado (intercambio) o a la lista de sin asignar, guardando cada movimiento automáticamente.
- **RF-004-09** — El sistema deberá marcar al momento cada juez en conflicto duro (rojo) y cada aviso blando (naranja: ya vio al equipo, misma institución que otro miembro del panel), con icono y texto además del color, y con el motivo visible al pasar el ratón, al enfocar o al tocar.
- **RF-004-10** — Toda acción de arrastrar deberá poder hacerse también sin arrastrar, con teclado y con clics o toques sueltos (seleccionar juez → seleccionar hueco), y cada movimiento deberá anunciarse a los lectores de pantalla junto con los avisos que genere.
- **RF-004-11** — Si otro usuario ha cambiado la asignación mientras tanto, el sistema deberá avisar y recargar en vez de sobrescribir.
- **RF-004-12** — El sistema deberá asignar salas automáticamente: las de mayor prioridad a los debates más importantes, respetando las necesidades de accesibilidad de equipos y jueces, y permitir cambiar la sala de un debate a mano.
- **RF-004-13** — Los cambios manuales después de confirmar el draw deberán registrarse en auditoría.

## 5. Reglas de negocio y validaciones
- Un juez en prácticas nunca preside.
- Un juez solo puede estar en un debate por ronda (garantizado por la BD).
- Conflicto duro manual: se permite guardar pero el debate muestra un aviso persistente hasta resolverlo.
- La nota usada es la nota base del juez (en fase 2 se combinará con el feedback).

## 6. Criterios de aceptación
- **AC-004-01** — Dados 10 debates y 30 jueces sin conflictos, con paneles de 3, cuando ejecuto la asignación automática, entonces cada debate tiene 1 presidente y 2 vocales y los 10 presidentes son los 10 jueces de mayor nota (no en prácticas), ordenados según la importancia de los debates.
- **AC-004-02** — Dado un torneo simulado con conflictos aleatorios (200 semillas), cuando ejecuto la asignación automática en cada ronda, entonces ningún juez queda asignado a un debate con el que tiene conflicto duro.
- **AC-004-03** — Dados 10 debates y 8 jueces válidos, cuando ejecuto la asignación, entonces los 2 debates de menor importancia quedan sin presidente y se muestran 2 avisos.
- **AC-004-04** — Dado un juez en conflicto con el equipo X, cuando lo arrastro al debate de X, entonces el juez se muestra en rojo con el motivo y el debate muestra un aviso de conflicto.
- **AC-004-05** — Dado el tablero abierto por dos usuarios, cuando el usuario A mueve un juez y después el B mueve otro en el mismo debate, entonces B recibe un aviso de cambio y la vista se recarga sin perder el movimiento de A.
- **AC-004-06** — Dado un equipo que necesita sala accesible, cuando se asignan salas, entonces su debate recibe una sala marcada como accesible si hay alguna libre.
- **AC-004-07** — Usando solo el teclado, puedo mover un juez de la lista de sin asignar al hueco de presidente de un debate.
- **AC-004-08** — Sin arrastrar, con un clic en un juez de la lista de sin asignar y otro en un hueco de vocal, el juez pasa a ese debate; si tiene conflicto, un lector de pantalla anuncia el movimiento y el motivo del conflicto.

## 7. Casos límite
- Más debates que salas disponibles: debates sin sala con aviso.
- Todos los jueces de nivel alto en conflicto con el debate más importante: se asigna el mejor juez válido y se avisa si su nota es muy baja.
- Juez retirado a mitad de ronda: el tab lo quita y el hueco queda marcado.

## 8. Requisitos no funcionales
- Asignación automática de 50 debates y 150 jueces en < 5 s.
- Cada movimiento en el tablero se refleja en < 300 ms.
- Usable en portátil de 13"; en tablet, deseable.
- WCAG 2.2 AA; el estado de cada juez y de cada debate no depende solo del color.

## 9. Fuera de alcance
- Nota de juez ajustada por feedback (fase 2, spec 102).
- Reglas propias de paneles en eliminatorias (las define la spec 008, que reutiliza esta asignación).
- "Bloquear" jueces en un debate antes de la asignación automática (se valorará).

## 10. Preguntas abiertas
- [ ] ¿Tamaño habitual de panel en Académico y en BP? ¿Hay jueces en prácticas? — ADA
- [ ] ¿Las salas tienen prioridad (mejores aulas) o da igual? — ADA

## Historial
- 2026-11-25 — creación.
- 2026-11-26 — accesibilidad: RF-004-09 y RF-004-10 ampliados, AC-004-08.
