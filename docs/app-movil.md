# App móvil para debatientes (fase 3)

Proyecto separado (`tabes-app`, iOS y Android) que consume la API de esta plataforma. Este documento recoge la propuesta funcional, la arquitectura de notificaciones, la publicación en tiendas y sus plazos. Las specs de backend (201–203) viven en este repo; las de pantallas, en `tabes-app`.

**Marca blanca en la app**: para ADA se publica una app con su nombre, icono y colores, bajo sus propias cuentas de Apple y Google. El mismo código genera, mediante variantes de configuración de Expo (`app.config.ts` por organización), una app con la marca de cada asociación que la quiera. Alternativa para asociaciones sin cuentas propias: una única app "TabES" en la que cada usuario ve la marca de su asociación. Se decidirá cuando haya un segundo cliente.

## 1. Objetivo
Que cada debatiente tenga en el bolsillo lo que necesita durante un torneo (dónde, contra quién, a qué hora y qué ha cambiado), avisado al momento con notificaciones push, y su histórico de torneos con ADA.

## 2. Funcionalidades propuestas

### v1 — lanzamiento

| # | Funcionalidad | Valor |
|---|---|---|
| 1 | **Cuenta personal** vinculada a su ficha de ADA (invitación por email o alta con el mismo email de la inscripción). Recuperar contraseña. Borrar cuenta desde la app. | Identidad única entre torneos. El borrado es obligatorio en Apple y Google. |
| 2 | **"Mi ronda"**: sala (con edificio/planta), rival(es), posición, jueces, hora y cuenta atrás. | Responde a "¿dónde tengo que ir?" en 2 segundos. |
| 3 | **Notificaciones push** (ver §3). | El motivo principal de la app. |
| 4 | **Horario en vivo** del torneo con los cambios resaltados. | Retrasos y cambios de hora sin depender de un grupo de WhatsApp. |
| 5 | **Tablón de avisos**: historial de todas las notificaciones recibidas. | Lo que se perdió por tener el móvil en silencio. |
| 6 | **Resultados y clasificaciones** publicados; mis puntuaciones de orador cuando el torneo las publique. | |
| 7 | **Cronómetro de debate** integrado, sin conexión, con los formatos de ADA (Académico y BP) y avisos por vibración. | Reutiliza la lógica del cronómetro web de ADA; útil también para entrenar. |
| 8 | **Perfil**: mi equipo, mi institución, mis torneos. | |

### v2 — después del lanzamiento (a valorar)

- Archivo de mociones de ADA con buscador por tema y torneo (útil para entrenar).
- Estadísticas personales: evolución de puntuaciones, posiciones jugadas, victorias.
- Feedback a jueces desde la app (si se ha hecho la fase 2).
- Check-in de equipos el día del torneo con código QR (ayuda al tab con la disponibilidad).
- Calendario de torneos y actividades de ADA con inscripción.
- Recursos de formación (guías, vídeos).
- Valenciano e inglés.
- Widget / actividad en vivo con la próxima ronda (iOS y Android).

Descartado a propósito: **chat** entre usuarios (moderación y riesgo con menores).

## 3. Notificaciones push

| Evento | Se dispara cuando | Quién lo recibe | Ejemplo |
|---|---|---|---|
| Draw publicado | El tab publica el draw de una ronda | Cada debatiente y juez del torneo, **personalizado** | "Ronda 3: aula A-12, En contra frente a IES Miguel Hernández A. 16:30." |
| Cambio en tu debate | Se edita un draw ya publicado y te afecta | Solo los afectados | "Cambio de sala: ahora en A-14." |
| Cambio de horario | Se edita un elemento del horario con aviso activado | Todo el torneo | "La ronda 4 se retrasa a 17:15." |
| Moción publicada | El tab publica la moción (si ADA lo quiere) | Todo el torneo | |
| Resultados publicados | El tab publica resultados de una ronda | Todo el torneo | "Ya están los resultados de la ronda 2." |
| Break | El tab publica el break | Todo el torneo; mensaje propio a los clasificados | "¡Estáis en cuartos de final!" |
| Recordatorio | X minutos antes del inicio de tu ronda (programado) | Participantes de la ronda | "Tu debate empieza en 10 min en A-12." |
| Aviso manual | El tab lo redacta | Torneo, un equipo, los jueces o una persona | "Comida en la cafetería del edificio B." |

Reglas: cada persona elige qué categorías recibe (por defecto todas); los avisos de draw y cambios en tu debate se recomiendan siempre activos; cada envío queda registrado; un botón de "enviar prueba" para el tab.

**Flujo técnico**: acción de publicar en Django → tarea en cola (Celery) → construye mensajes personalizados → API de Expo Push en lotes de 100 → Expo entrega a APNs (iOS) y FCM (Android) → se guardan los justificantes de entrega → una tarea posterior consulta los recibos y desactiva los tokens caducados. Cada notificación lleva un enlace profundo (`ada://torneo/<slug>/ronda/<n>`) que abre la pantalla correspondiente. Coste: 0 € (el servicio de Expo, FCM y APNs es gratuito).

## 4. Cuentas, privacidad y menores

- **Alta**: el tab pulsa "Invitar a la app" y cada participante con email recibe un enlace; o la persona se registra con el email de su inscripción y, tras verificarlo, se vincula a su ficha.
- **Menores**: en España, desde los 14 años pueden consentir por sí mismos (art. 7 LOPDGDD); por debajo hace falta consentimiento de madre, padre o tutor. **Recomendación**: app para 14 años o más; para menores de 14, la web pública sin cuenta. Si ADA necesita cuentas para menores de 14, se añade un flujo de consentimiento parental (estimación aparte).
- **Tiendas**: no se publica como app "para niños" (evita las políticas de familias de Google y la categoría Kids de Apple); público objetivo declarado: 14+.
- **Datos**: nombre, email, equipo, resultados, token del dispositivo. Nada de ubicación, contactos ni analítica publicitaria.
- **Borrado**: desde Ajustes de la app y desde una página web (Google exige ambas vías). Se elimina la cuenta y los dispositivos; los resultados de torneos se conservan anonimizados si la persona lo pide.

## 5. Stack de la app

React Native + **Expo** (TypeScript) · Expo Router · TanStack Query (caché y modo sin conexión) · expo-notifications · expo-secure-store (tokens) · i18n · Sentry · **EAS Build / Submit / Update** (compilación en la nube, envío a tiendas y actualizaciones OTA de JavaScript sin pasar revisión). Cliente de la API generado a partir del esquema OpenAPI del backend. Pruebas: Jest + React Native Testing Library; flujos e2e con Maestro.

**Accesibilidad**: la app sigue el principio XIII de la [constitución](constitucion.md) (WCAG 2.2 AA): etiquetas para VoiceOver y TalkBack en todos los controles, respeto del tamaño de texto del sistema, objetivos táctiles de 44 × 44 pt en iOS y 48 × 48 dp en Android, y el cronómetro avisa también con vibración, no solo con sonido o color.

El repo `tabes-app` ([github.com/fabgs/tabes-app](https://github.com/fabgs/tabes-app)) será público con licencia **MIT** (solo dependencias permisivas) y tendrá su propio `AGENTS.md`/`CLAUDE.md` con las mismas reglas SDD y una carpeta `specs/`.

## 6. Publicación en tiendas

### Costes

| Concepto | Coste | Notas |
|---|---|---|
| Apple Developer Program (organización) | **99 USD/año** (se cobra en moneda local) | Apple ofrece **exención de la cuota** a entidades sin ánimo de lucro con personalidad jurídica que no cobren dentro de las apps. Su página no publica la lista de países: ADA debe solicitarla; si la conceden, 0 €. |
| Google Play Console (organización) | **25 USD, pago único** | |
| Número D-U-N-S | 0 € | Obligatorio para cuentas de organización en Apple y Google. |
| Expo EAS (plan gratuito) | 0 € | 30 compilaciones/mes y 1.000 usuarios activos/mes de actualizaciones OTA. Plan Starter 19 USD/mes solo si hiciera falta más. |
| Notificaciones push | 0 € | |

### Plazos

| Paso | Plazo típico | Responsable |
|---|---|---|
| Obtener (o localizar) el D-U-N-S de ADA | hasta 5 días hábiles + hasta 2 días hábiles hasta que Apple lo reconoce | ADA |
| Alta en Apple Developer como organización (verificación de la entidad y del firmante) | 1–2 semanas | ADA (el desarrollador entra como miembro del equipo) |
| Alta en Google Play Console como organización (verificación de identidad) | unos días – 2 semanas | ADA |
| Beta: TestFlight (iOS) y prueba interna (Android) | 1–2 semanas de uso real en un torneo | Desarrollador + ADA |
| Revisión de la primera versión | Apple: normalmente 1–2 días; Google: de horas a una semana en apps nuevas | — |
| **Total desde que se empieza a tramitar** | **3–6 semanas**, en paralelo con el desarrollo | |

Importante: las cuentas deben ser **de ADA como organización**, no personales del desarrollador. Así la app aparece publicada por ADA, la asociación conserva el control y se evita el requisito de Google para cuentas personales nuevas (prueba cerrada con al menos 12 testers durante 14 días seguidos antes de poder publicar).

### Requisitos para pasar la revisión

- URL pública de política de privacidad y de soporte.
- Apple: etiquetas de privacidad de la app, cuenta de demostración para el revisor, borrado de cuenta dentro de la app, cuestionario de edad, capturas de iPhone (solo iPhone si no se da soporte a iPad).
- Google: formulario de seguridad de datos, enlace web de borrado de cuenta, cuestionario de clasificación de contenido, público objetivo, nivel de API de Android exigido ese año, gráfico destacado y capturas.
- Credenciales de push (clave APNs y proyecto de Firebase), gestionadas por EAS.
- Valor propio más allá de la web (push, cronómetro sin conexión, perfil): evita el rechazo por "funcionalidad mínima" que sufren las apps que solo envuelven una web.

## 7. Alternativa más barata: PWA

Una aplicación web instalable (PWA) daría casi lo mismo (mi ronda, horario, avisos, cronómetro) por un 35–40 % menos de coste, sin cuotas de tiendas ni revisiones. Inconvenientes: no aparece en App Store ni Google Play y, en iPhone, las notificaciones solo funcionan si el usuario la añade a la pantalla de inicio, lo que reduce mucho el alcance de los avisos. Es un buen plan B si la app nativa no compensa.

Con un único Nacional al año, la app nativa se usará sobre todo 2–3 días, pero la cuota de Apple (99 USD) se paga todo el año. Si ADA no le da uso durante el resto del año (ligas, entrenamientos, archivo de mociones, cronómetro), la PWA gana peso. Se decide al terminar la Parte 1.
