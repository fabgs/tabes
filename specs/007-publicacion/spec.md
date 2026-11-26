# Spec 007 — Publicación

| Campo | Valor |
|---|---|
| Estado | borrador |
| Fase | 1 |
| Depende de | 003, 004, 005, 006 |
| Última actualización | 2026-11-26 |

## 1. Objetivo
Ofrecer una web pública por torneo, sin necesidad de cuenta, donde equipos, jueces y público consulten el draw, las mociones, los resultados y las clasificaciones en cuanto el tab decida publicarlos, que aguante a todo el torneo consultándola a la vez desde el móvil y que pueda proyectarse en pantalla.

## 2. Actores
- Público, debatientes y jueces (sin cuenta).
- Miembro del equipo de tab (controla qué se publica).

## 3. Historias de usuario
- Como debatiente, quiero encontrar mi sala y mi rival en segundos desde el móvil.
- Como público, quiero ver la moción cuando se anuncie y los resultados de cada ronda.
- Como tab, quiero publicar el draw o los resultados con un clic y poder despublicarlos si me equivoco.
- Como tab, quiero proyectar el draw en pantalla grande.
- Como ADA, quiero que, si hay menores, solo se muestren iniciales.

## 4. Requisitos funcionales
- **RF-007-01** — El sistema deberá ofrecer una portada pública por torneo con nombre, fechas, lugar, rondas y enlaces a lo publicado, con la identidad visual de la organización (RF-000-13).
- **RF-007-02** — El sistema deberá permitir al tab publicar y despublicar, por ronda: draw, mociones y resultados; y por torneo: clasificación de equipos, clasificación de oradores, break y lista de participantes. Cada acción quedará en auditoría.
- **RF-007-03** — El sistema no deberá mostrar en público nada que no esté publicado explícitamente.
- **RF-007-04** — El draw público deberá mostrarse por sala y por equipo, con búsqueda por nombre de equipo, e indicar posición, rival(es), sala y jueces.
- **RF-007-05** — El sistema deberá mostrar las mociones publicadas de cada ronda, con su infoslide, y un archivo de mociones del torneo.
- **RF-007-06** — El sistema deberá mostrar los resultados publicados por ronda (ganador o puestos) y, según la configuración del torneo, las puntuaciones de orador: nunca, al finalizar el torneo o en directo.
- **RF-007-07** — Si una ronda es silenciosa, sus resultados no se mostrarán ni influirán en la clasificación pública hasta que el tab los publique.
- **RF-007-08** — El sistema deberá mostrar los nombres de las personas según la configuración del torneo: completo, iniciales u ocultos.
- **RF-007-09** — El sistema deberá ofrecer un modo proyector para draw y mociones: letra grande, alto contraste, paso automático de páginas si no cabe, un control para pausarlo y reanudarlo (también con la barra espaciadora) y un código QR hacia la web pública.
- **RF-007-10** — Cuando se publique algo nuevo, las páginas abiertas deberán mostrar un aviso "hay una actualización" en menos de 30 s sin recargar a mano. El aviso se anunciará a los lectores de pantalla sin mover el foco.
- **RF-007-11** — El sistema deberá permitir que el torneo no se indexe en buscadores.
- **RF-007-12** — El sistema deberá ofrecer una versión imprimible del draw.

## 5. Reglas de negocio y validaciones
- Despublicar no borra nada: solo oculta.
- Las clasificaciones públicas solo incluyen rondas cuyos resultados estén publicados.
- Las notas de conflictos, notas de jueces y el registro de auditoría nunca son públicos.

## 6. Criterios de aceptación
- **AC-007-01** — Dado un draw confirmado sin publicar, cuando un visitante abre la página del draw, entonces ve "El draw de esta ronda aún no se ha publicado".
- **AC-007-02** — Dado un draw publicado, cuando busco "Jorge Juan A" desde un móvil, entonces veo su sala, posición y rival en la primera pantalla.
- **AC-007-03** — Dada una ronda silenciosa con boletas confirmadas, cuando consulto la clasificación pública, entonces esa ronda no cuenta.
- **AC-007-04** — Dado un torneo con visualización "iniciales", cuando veo la lista de oradores, entonces aparece "Ana G." en lugar de "Ana García López".
- **AC-007-05** — Dado un draw publicado por error, cuando el tab lo despublica, entonces en menos de 10 s la página pública vuelve a mostrar que no está publicado.
- **AC-007-06** — Dada la prueba de carga de 500 usuarios virtuales consultando el draw recién publicado durante 2 minutos, entonces el p95 es < 500 ms y no hay errores.
- **AC-007-07** — La primera carga de la página del draw pesa menos de 200 KB (sin contar fuentes cacheadas).
- **AC-007-08** — Dado el modo proyector con 15 debates, entonces el draw se pagina solo y cada página es legible a 5 metros (tamaño de letra mínimo definido en el plan).
- **AC-007-09** — Dado el modo proyector paginando solo, cuando pulso la barra espaciadora o el botón de pausa, entonces se queda en la página actual hasta que lo reanudo.
- **AC-007-10** — Dada la página del draw abierta con un lector de pantalla, cuando el tab publica una actualización, entonces se anuncia "Hay una actualización" sin perder la posición de lectura.

## 7. Casos límite
- Torneo marcado como no público: todas sus páginas devuelven "no encontrado".
- Publicar resultados de una ronda con boletas sin confirmar: se avisa y se pide confirmación.
- Conexión intermitente: la página muestra el último contenido cargado y la hora de actualización.

## 8. Requisitos no funcionales
- 250 usuarios simultáneos como mínimo; diseño y prueba para 500.
- Legible y usable en móvil de 360 px de ancho, sin desplazamiento horizontal.
- WCAG 2.2 AA. Las tablas de draw y clasificaciones tienen encabezados de fila y columna asociados.
- Modo proyector con contraste de al menos 7:1, porque los proyectores lo reducen.

## 9. Fuera de alcance
- Páginas privadas para cada participante (fase 2, con enlaces privados).
- Notificaciones push (fase 3, app).
- Exportación a PDF/Excel (fase 2, spec 105).

## 10. Preguntas abiertas
- [ ] ¿Se publican las mociones en la web en el momento del anuncio o solo al final? — ADA
- [ ] ¿Puntuaciones de orador visibles en directo o solo al final? — ADA
- [ ] ¿Hay torneos con menores? (determina el modo de nombres por defecto) — ADA

## Historial
- 2026-11-25 — creación.
- 2026-11-26 — accesibilidad: RF-007-09 y RF-007-10 ampliados, AC-007-09 y AC-007-10.
