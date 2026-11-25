# Spec 000 — Base de la plataforma

| Campo | Valor |
|---|---|
| Estado | borrador |
| Fase | 1 |
| Depende de | — |
| Última actualización | 2026-11-25 |

## 1. Objetivo
Dejar lista la base sobre la que se construye todo: acceso seguro del equipo de tab, creación de torneos a partir de los formatos de ADA (Académico y BP) con reglas configurables, gestión de rondas, registro de auditoría y un entorno publicado en internet con copias de seguridad.

## 2. Actores
- **Administrador de ADA**: crea torneos y usuarios del tab.
- **Miembro del equipo de tab**: opera un torneo.

## 3. Historias de usuario
- Como administrador, quiero crear un torneo eligiendo el formato Académico o BP para no configurar todo desde cero.
- Como administrador, quiero ajustar las reglas de un torneo concreto (tiempos, número de refutaciones, rango de puntos, empates, desempates) porque cada torneo puede variar.
- Como miembro del tab, quiero entrar con mi email y contraseña y recuperar la contraseña si la olvido.
- Como ADA, quiero que quede registrado quién hizo cada cambio relevante para resolver reclamaciones.
- Como ADA, quiero que los datos estén a salvo aunque falle el servidor.

## 4. Requisitos funcionales
- **RF-000-01** — El sistema deberá exigir autenticación para toda la zona de tab.
- **RF-000-02** — Cuando un usuario solicite restablecer su contraseña, el sistema deberá enviarle un enlace de un solo uso que caduque en 24 h.
- **RF-000-03** — El sistema deberá incluir dos plantillas de formato, "Académico" y "British Parliament", con los turnos, posiciones y tiempos de `docs/glosario.md` como valores por defecto. Cada organización podrá crear sus propias plantillas a partir de ellas.
- **RF-000-04** — Cuando se cree un torneo a partir de una plantilla, el sistema deberá copiar sus reglas al torneo; los cambios posteriores en la plantilla no afectarán a ese torneo.
- **RF-000-05** — El sistema deberá permitir configurar por torneo: equipos por debate (2 o 4), nombres de posiciones, turnos (orden, posición, nombre, duración, si puntúa), oradores por equipo (mínimo y máximo), rango y paso de puntos de orador, puntos de equipo por puesto, empates permitidos, regla de ganador, modo de panel (consenso o voto individual), rúbrica por criterios opcional, tamaño de panel por defecto, reglas de emparejamiento y orden de desempates.
- **RF-000-06** — El sistema deberá permitir modificar el número de refutaciones del formato Académico y el tiempo de la última refutación, regenerando la lista de turnos.
- **RF-000-07** — Si un torneo ya tiene boletas confirmadas, cuando se modifique una regla que afecte a puntuaciones o clasificaciones, el sistema deberá pedir confirmación explícita y registrar el cambio.
- **RF-000-08** — El sistema deberá gestionar los estados del torneo: borrador, en curso, finalizado y archivado. Un torneo archivado será de solo lectura.
- **RF-000-09** — El sistema deberá permitir crear varias rondas preliminares de una vez y editar su nombre, abreviatura y hora de inicio.
- **RF-000-10** — El sistema deberá registrar en un log de auditoría consultable por torneo cada acción que cambie el estado del torneo: usuario, acción, objeto, fecha y valores antes/después.
- **RF-000-11** — El sistema deberá mostrar toda la interfaz en español, con los textos preparados para traducirse.
- **RF-000-12** — El sistema deberá estar accesible por HTTPS y hacer copias de seguridad automáticas diarias, y cada hora durante los días de torneo, en una ubicación distinta del servidor.
- **RF-000-13** — El sistema deberá mostrar cada página (zona de tab, web pública y correos) con la identidad de la organización a la que pertenece: nombre visible, logotipo, colores, favicon, email de contacto y enlaces legales. Ningún texto ni imagen de una organización concreta estará fijado en el producto.
- **RF-000-14** — Cuando llegue una petición por el dominio propio de una organización, el sistema deberá identificar esa organización. Si no tiene dominio propio, la identificará por su ruta (`/o/<slug>/`).
- **RF-000-15** — Si los colores configurados no alcanzan el contraste mínimo AA, el sistema deberá avisar al guardarlos.
- **RF-000-16** — El sistema deberá mostrar en el pie de todas las páginas un aviso discreto "Funciona con TabES", con enlace al código fuente y a su licencia. La AGPL obliga a ofrecer el código a los usuarios de una versión que se use a través de la red. El enlace apuntará al código de la versión desplegada (configurable si la instalación usa una versión modificada).

## 5. Reglas de negocio y validaciones
- `score_min < score_max`; `score_step > 0` y `(score_max − score_min)` múltiplo del paso.
- Número de posiciones = equipos por debate; cada turno pertenece a una posición existente.
- `points_by_rank` tiene tantos valores como equipos por debate y es no creciente.
- El orden de desempates solo admite métricas conocidas (spec 006) y sin repetir.
- `speakers_per_team_min ≤ speakers_per_team_max`.

## 6. Criterios de aceptación
- **AC-000-01** — Dado un visitante sin sesión, cuando abre cualquier página de la zona de tab, entonces es redirigido al login.
- **AC-000-02** — Dada la plantilla "Académico", cuando creo un torneo con ella, entonces el torneo tiene 2 equipos por debate, posiciones "A favor" y "En contra" y los 12 turnos del glosario con sus duraciones.
- **AC-000-03** — Dado un torneo creado con "British Parliament", cuando cambio la duración de los turnos en la plantilla, entonces las reglas del torneo siguen igual.
- **AC-000-04** — Dado un torneo Académico, cuando cambio el número de refutaciones a 2, entonces la lista de turnos pasa a 10 y la última refutación de cada equipo usa el tiempo de "última refutación".
- **AC-000-05** — Dado un rango de puntos con mínimo 80 y máximo 70, cuando guardo, entonces se muestra un error y no se guarda.
- **AC-000-06** — Dado un torneo con una boleta confirmada, cuando cambio el rango de puntos, entonces se me pide confirmación y, si confirmo, el cambio aparece en el log de auditoría con valor anterior y nuevo.
- **AC-000-07** — Dado un torneo archivado, cuando intento editar cualquier dato, entonces la acción no está disponible.
- **AC-000-08** — Dado el entorno de producción, cuando se restaura la última copia en un servidor nuevo siguiendo `deploy/restore.md`, entonces la aplicación funciona con los datos en menos de 1 hora.
- **AC-000-09** — Dadas dos organizaciones con logos y colores distintos, cuando abro la web pública de cada una por su dominio, entonces cada una muestra solo su nombre, logo y colores.
- **AC-000-11** — Dada cualquier página pública o de tab, cuando miro el pie, entonces aparece "Funciona con TabES" con enlace al repositorio del código fuente y a la licencia AGPL.
- **AC-000-10** — Dada una búsqueda de "ADA" y "Alicante" en el código fuente y las plantillas (excluyendo datos de demo, fixtures y documentación), entonces no aparece ninguna coincidencia.

## 7. Casos límite
- Dos administradores editando las reglas a la vez: el segundo recibe aviso de que han cambiado.
- Torneo con fechas de un solo día.
- Restablecimiento de contraseña con email inexistente: misma respuesta que con uno existente (no revela usuarios).

## 8. Requisitos no funcionales
- Páginas del tab responden en < 500 ms (p95) con un torneo de 200 equipos.
- Copias: RPO ≤ 1 h en días de torneo; RTO ≤ 1 h.
- Accesible por teclado; contraste AA.

## 9. Fuera de alcance
- Roles diferenciados (admin, tab, CA, juez): fase 2. En fase 1 todo usuario del tab puede todo.
- Registro público de usuarios, inicio de sesión con Google.
- Panel propio para que cada asociación cambie su marca o se dé de alta sola: en el MVP lo configura el autor desde la administración interna.

## 10. Preguntas abiertas
- [ ] ¿Rango y paso de puntos de orador en Académico y en BP? — ADA
- [ ] ¿Se permiten empates en Académico? ¿El ganador lo deciden los puntos o lo declara el juez? — ADA
- [ ] ¿Los paneles votan individualmente o por consenso? — ADA
- [ ] ¿Las preguntas cruzadas se puntúan? ¿Se puntúa por criterios (rúbrica)? ¿Cuáles? — ADA
- [ ] ¿Dominio o subdominio que usará la plataforma? — ADA
- [ ] Logo en alta resolución (claro y oscuro), colores corporativos y nombre visible. — ADA

## Historial
- 2026-11-25 — creación.
