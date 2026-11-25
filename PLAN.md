# PLAN — TabES

Plataforma de tabulación de debate en marca blanca. Primer cliente: Asociación de Debate de Alicante (ADA).

Hoja de ruta del proyecto. Se actualiza al cerrar cada spec o hito.
Última actualización: 2026-11-25 · Estado global: **planificación**

## 1. Visión
La Asociación de Debate de Alicante gestiona sus torneos, y en especial su **Nacional anual**, con una herramienta propia en español adaptada a sus formatos (**Académico** y **British Parliament**), que:
1. Ahorra horas al equipo de tab y reduce errores en emparejamientos, jueces y resultados.
2. Publica al momento draw, mociones y resultados en una web que aguanta a todo el torneo a la vez.
3. Sienta la base (ficha única de cada debatiente) para una app móvil con avisos push y un histórico entre torneos.

**Perfil de uso**: un Nacional al año (2–3 días, 100–250 personas a la vez) y uso residual el resto del año. La infraestructura se dimensiona para ese pico, no para un uso continuo (ver [docs/arquitectura.md](docs/arquitectura.md) §6–7).

## 2. Partes

| Parte | Contenido | Desarrollo (con IA) |
|---|---|---|
| **1 — Tabulación** | Specs 000–008: gestión de datos e importación, conflictos, emparejamientos suizos (Académico y BP), jueces y salas con arrastrar y soltar, boletas, clasificaciones y break, web pública y **rondas eliminatorias**. | ~4 semanas + 1 semana de simulacro |
| **Mejoras opcionales** | Specs 101, 102, 104, 105: boletas electrónicas, feedback a jueces, roles y permisos, exportación PDF/Excel. | ~1 semana |
| **2 — App de debatientes** | Specs 201–203 (backend) + app iOS/Android (Expo): cuentas, mi ronda, horario en vivo, avisos push, resultados, cronómetro. Publicación en tiendas. | ~4 semanas + beta + trámites de tiendas (3–6 semanas, en paralelo) |

## 3. Calendario (relativo al Nacional = N)

| Cuándo | Qué |
|---|---|
| Antes de empezar | Reunión con ADA: respuestas a §7, boletas en papel, hoja de inscripción, fecha del Nacional. Aprobación en junta. |
| Semana 0 | Specs 000–008 aprobadas. Si hay app: ADA empieza el D-U-N-S y las cuentas de Apple y Google **ya**. |
| Semanas 1–4 | Parte 1. Demo a las 2 semanas (importación + emparejamientos) y a las 4 (torneo simulado completo). |
| Semana 5 | Mejoras opcionales + **simulacro de torneo con socios** (todos los flujos, móviles reales). |
| Semanas 6–9 | App (si se contrata). |
| Semana 10 | Beta con socios (TestFlight + prueba interna de Android). |
| Semana 11 | Envío a revisión de App Store y Google Play. |
| N − 3 semanas | Prueba de carga (500 usuarios virtuales) y simulacro general. Congelación de funcionalidades. |
| N − 1 semana | Refuerzo del servidor si la prueba lo pide; copias cada hora activadas; datos del Nacional importados. |
| **N** | Nacional, con soporte en directo. |
| N + 1 semana | Volver al servidor pequeño, retrospectiva, correcciones. |

Inicio más tarde posible: **N − 14/16 semanas** con app; **N − 8 semanas** solo con tabulación.

## 4. Hitos de la Parte 1

| Hito | Semana | Contenido | Demo |
|---|---|---|---|
| H0 | 0 | Specs aprobadas, repo + CI, servidor de pruebas con HTTPS y copias. | Entorno online vacío. |
| H1 | 1–2 | 000, 001, 002, 003: base, formatos, datos, importación, conflictos, emparejamientos. | Importar el último Nacional (anonimizado) y generar draws. |
| H2 | 3–4 | 004, 005, 006, 007, 008: jueces y salas, boletas, clasificaciones, break, web pública, eliminatorias. | Torneo simulado completo hasta la final. |
| H3 | 5 | Simulacro con socios, ajustes, manual y formación del tab. | Acta de aceptación. |

## 5. Estado de las specs

| Spec | Parte | Estado |
|---|---|---|
| 000 Base de la plataforma | 1 | borrador |
| 001 Gestión de datos e importación | 1 | borrador |
| 002 Conflictos | 1 | borrador |
| 003 Emparejamientos | 1 | borrador |
| 004 Asignación de jueces y salas | 1 | borrador |
| 005 Boletas | 1 | borrador |
| 006 Clasificaciones y break | 1 | borrador |
| 007 Publicación | 1 | borrador |
| 008 Rondas eliminatorias | 1 | borrador |
| 101 Boletas electrónicas · 102 Feedback · 104 Roles · 105 Exportación | Mejoras | por escribir |
| 201 Cuentas · 202 API · 203 Notificaciones y horario | 2 | por escribir |

## 6. Operación del Nacional (checklist)

- [ ] Prueba de carga con 500 usuarios virtuales en el entorno real (p95 < 500 ms en páginas públicas).
- [ ] Simulacro general con el equipo de tab y socios haciendo de jueces y equipos.
- [ ] Refuerzo del servidor si hace falta (y anotar cuándo volver al plan pequeño).
- [ ] Copias cada hora activadas y restauración ensayada esa misma semana.
- [ ] Draw imprimible y exportación del torneo preparados como plan B en papel.
- [ ] Wi-Fi de la sede comprobada; móvil con datos como respaldo para el tab.
- [ ] Congelar cambios de código desde N − 3 semanas salvo correcciones.

## 7. Preguntas abiertas para ADA (bloquean la aprobación de specs)

**Formatos y puntuación**
1. Rango y paso de los puntos de orador en Académico y en BP.
2. En Académico: ¿se puntúan las preguntas cruzadas? ¿Cada persona hace un único turno? ¿Mínimo de oradores?
3. ¿Se puntúa por criterios (rúbrica)? ¿Cuáles y con qué peso? Foto de la boleta en papel.
4. ¿Empates permitidos? ¿El ganador lo deciden los puntos o lo declara el juez?
5. Paneles: ¿consenso o voto individual? ¿Tamaño? ¿Jueces en prácticas?
6. Orden oficial de desempates de equipos y oradores.

**Nacional**
7. Fecha del próximo Nacional y formato que usa.
8. Número de rondas preliminares, tamaño del break y rondas eliminatorias; categorías (noveles…).
9. Reglas de eliminatorias: ¿quién elige posición? ¿Hay puntos de orador en eliminatorias? ¿Paneles de cuántos jueces?
10. Método de emparejamiento (`slide`/`fold`), regla de pull-up, swing o bye, sembrado en ronda 1.

**Operativa**
11. ¿Otros torneos durante el año (ligas, torneos internos)?
12. ¿Qué usan hoy (Tabbycat, Excel, papel)? ¿Qué les duele más?
13. ¿Participan menores? ¿Menores de 14?
14. Hoja de inscripción del último Nacional (anonimizada) y si recogen conflictos.
15. Dominio o subdominio; persona de contacto.

## 8. Riesgos

| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| El Nacional es la única prueba real del año: un fallo se ve mucho | Media | Alto | Simulacro con socios, prueba de carga, plan B en papel, copias cada hora, soporte en directo. |
| Reglas de ADA poco definidas | Alta | Medio | Resolver §7 antes de empezar; reglas configurables. |
| Calendario ajustado respecto al Nacional | Media | Alto | Empezar con margen (§3); si no llega, priorizar tabulación y dejar la app para el año siguiente. |
| Trámites de tiendas lentos (D-U-N-S, verificación) | Media | Medio | Iniciarlos en la semana 0; cuentas a nombre de ADA. |
| Algoritmo de emparejamiento BP más complejo de lo previsto | Media | Medio | Specs con propiedades verificables, Hypothesis y simulador. |
| Un único desarrollador | Media | Alto | Documentación SDD completa y cláusula de continuidad (código a ADA si se deja de mantener). |
| Mantenimiento anual de la app (Apple/Google cambian requisitos cada año) | Alta | Medio | Puesta a punto anual antes del Nacional; renovar la cuota de Apple a tiempo. |
| Datos de menores | Media | Alto | Datos mínimos, modo iniciales, acuerdo RGPD, app solo 14+. |

## 9. Próximos pasos
1. Presentar el proyecto a la junta de ADA.
2. Reunión para responder a §7 y conseguir boletas, hoja de inscripción y la fecha del Nacional.
3. Actualizar las specs 000–008 con las respuestas y pasarlas a "en revisión".
4. Inicializar Git y crear el esqueleto (spec 000) tras la aprobación. Al crear el repositorio:
   - `git config core.hooksPath .githooks` y `user.email` con el email anónimo de GitHub;
   - en GitHub, activar **Secret scanning** y **Push protection** (gratis en repos públicos), y en tu cuenta, "Keep my email addresses private" y "Block command line pushes that expose my email";
   - el primer push, solo cuando `python scripts/check_leaks.py --tree` salga limpio.
