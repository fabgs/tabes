# AGENTS.md

Instrucciones para cualquier agente de código (Claude Code, Codex, Cursor, Copilot…) que trabaje en este repositorio.

## Proyecto

**TabES**: plataforma web de tabulación de torneos de debate. Gestiona torneos, equipos, jueces y salas; genera emparejamientos por sistema suizo (formato Académico de 2 equipos y British Parliament de 4); asigna jueces; recoge boletas; calcula clasificaciones y break; y publica draw, mociones y resultados. La app móvil de debatientes (fase 3) vive en otro repositorio (`tabes-app`) y consume la API de este.

Repositorio: [github.com/fabgs/tabes](https://github.com/fabgs/tabes) (público). Autor: Fabián Godoy Silvestre ([fabgs.dev](https://fabgs.dev)).

**Marca blanca**: cada asociación (`Organization`) ve la plataforma con su nombre, logo, colores y dominio. El primer cliente es la **Asociación de Debate de Alicante (ADA)**, y sus formatos son las plantillas iniciales. Nunca escribas "ADA" ni su identidad visual en código o plantillas: sale siempre de la configuración de la organización.

Estado actual: **planificación**. Hoja de ruta en [PLAN.md](PLAN.md).

## Fuentes de verdad (por orden de prioridad)

1. [docs/constitucion.md](docs/constitucion.md): principios no negociables.
2. La spec **aprobada** de la funcionalidad: `specs/NNN-*/spec.md`.
3. [docs/modelo-datos.md](docs/modelo-datos.md): esquema e invariantes.
4. [docs/arquitectura.md](docs/arquitectura.md): stack, capas, ADR.
5. [docs/glosario.md](docs/glosario.md): vocabulario y formatos de ADA. Usa estos términos en código y UI.

Si dos fuentes se contradicen, gana la de mayor prioridad y avisas de la contradicción.

## Flujo de trabajo (SDD)

```
spec.md (qué y por qué) ─► plan.md (cómo) ─► tasks.md (pasos) ─► código + tests ─► verificación contra AC
```

- **No implementes nada sin spec aprobada** (`Estado: aprobada`). Solo una persona cambia ese estado.
- La spec no menciona tecnologías; el plan sí. Las tareas son pasos de ≤ 2 h, cada una con su verificación.
- Si al implementar descubres que la spec o el plan están mal o incompletos: **para**, explícalo y propone el cambio en el documento. No improvises comportamiento.
- Cada criterio de aceptación `AC-NNN-xx` debe tener al menos un test que lo cite en un comentario.
- Al terminar: marca tareas en `tasks.md`, actualiza el estado de la spec y la tabla de [PLAN.md](PLAN.md).
- Detalle del proceso y plantillas en [specs/README.md](specs/README.md).

## Stack

Python 3.13 · Django 5.2 LTS · PostgreSQL 17 · Redis · HTMX 2 + Alpine.js 3 + SortableJS · Tailwind 4 · pytest + Hypothesis + Playwright · uv · ruff · mypy · Docker Compose · Caddy. Detalle y motivos en [docs/arquitectura.md](docs/arquitectura.md).

## Comandos

> Se crean en la spec 000. Hasta entonces, no existen.

| Para | Comando |
|---|---|
| Instalar dependencias | `uv sync` |
| Levantar servicios (BD, Redis) | `docker compose up -d db redis` |
| Migrar | `uv run manage.py migrate` |
| Servidor de desarrollo | `uv run manage.py runserver` |
| Tests | `uv run pytest` (rápidos) · `uv run pytest -m e2e` (Playwright) |
| Lint y formato | `uv run ruff check --fix . && uv run ruff format .` |
| Tipos | `uv run mypy apps` |
| **Todo antes de terminar una tarea** | `uv run poe check` |
| Simular un torneo completo | `uv run manage.py simulate_tournament --format academico --teams 20 --rounds 5 --seed 1` |
| Datos de demo | `uv run manage.py load_demo` |

## Estructura

```
config/          settings, urls, celery
apps/<dominio>/  models.py · services/ · engine/ (algoritmos puros) · views.py · forms.py · templates/ · tests/
templates/ static/ tests/e2e tests/load deploy/ docs/ specs/
```

Apps: `core`, `tournaments`, `participants`, `conflicts`, `draw`, `allocation`, `results`, `standings`, `public` (+ `api`, `notifications` en fase 3).

## Convenciones

- **Idiomas**: identificadores, nombres de tablas y commits técnicos en inglés; textos de interfaz en español y siempre con `gettext` (`_()` / `{% translate %}`); documentación y specs en español.
- **Capas**: vista → servicio → motor → modelo. Nada de reglas de negocio en vistas, plantillas o `save()`. Los motores en `engine/` son funciones puras sobre dataclasses, sin ORM.
- **Tipado** completo en `services/` y `engine/`; mypy sin errores.
- **Base de datos**: toda invariante que se pueda expresar como `UNIQUE`/`CHECK` va en la BD (ver §6 del modelo de datos). Operaciones de tab dentro de `transaction.atomic`. Una migración por cambio lógico; nunca edites una migración ya desplegada.
- **Auditoría**: los servicios que cambian el estado del torneo llaman a `audit.log(...)`.
- **Aleatoriedad**: nunca `random` global; usa `random.Random(seed)` y guarda la semilla.
- **Frontend**: HTMX para peticiones parciales, Alpine para estado local, SortableJS para arrastrar y soltar. Sin frameworks SPA. Toda interacción de arrastrar tiene alternativa con teclado y con clics sueltos.
- **Accesibilidad**: WCAG 2.2 AA ([constitución](docs/constitucion.md), principio XIII). HTML semántico y elementos nativos antes que ARIA; nada depende solo del color; todo se usa con teclado y con el foco visible; cada fragmento HTMX anuncia el cambio (`aria-live`) y deja el foco en un sitio lógico; contraste comprobado también con los colores de cada organización.
- **Tests**: pytest + factory_boy; Hypothesis en motores; nombres `test_<comportamiento_esperado>`; nada de tests que dependan del orden o de la hora real.
- **Dependencias**: no añadas paquetes sin ADR en `docs/arquitectura.md`. Comprueba la licencia de cada paquete: en la web, compatible con AGPL-3.0 (MIT, BSD, Apache-2.0, ISC, PSF, LGPL, GPL-3.0); nada privativo, GPL-2.0-only ni SSPL.
- **Cabecera de licencia**: todo fichero de código nuevo empieza con `# SPDX-License-Identifier: AGPL-3.0-or-later` (o el comentario equivalente del lenguaje).
- **Ramas**: `NNN-slug-de-la-spec`. Commits estilo Conventional Commits: `feat(draw): ...`, `fix(results): ...`.

## Invariantes del dominio (no las rompas nunca)

1. Un equipo aparece como máximo una vez por ronda; un juez, en un debate por ronda; una sala, en un debate por ronda.
2. Cada debate tiene exactamente `teams_per_debate` equipos en posiciones distintas.
3. Como mucho una boleta confirmada por debate. Una boleta confirmada **no se edita**: se crea una versión nueva y la anterior pasa a `discarded` con motivo.
4. Las clasificaciones solo usan boletas confirmadas.
5. La asignación automática nunca pone a un juez en conflicto. La manual lo permite con aviso visible y registro.
6. Nada se hace público sin acción explícita (`*_released_at`).
7. Las reglas del torneo se copian de la plantilla al crearlo; cambiar la plantilla no afecta a torneos existentes.

## Seguridad y privacidad

- Nunca registres en logs datos personales (nombres, emails) ni tokens.
- Secretos solo por variables de entorno (`.env` está en `.gitignore`).
- Hay **menores** entre los debatientes: datos mínimos y opción de mostrar solo iniciales en público.
- **El repositorio es público.** Nunca subas secretos, volcados de la base de datos, copias de seguridad ni datos reales de participantes. Fixtures y datos de demo siempre inventados.
- Si reutilizas código de otro proyecto (p. ej. Tabbycat, AGPL-3.0), comprueba que su licencia es compatible, conserva su aviso de copyright y anótalo en `NOTICE`. No pegues código de foros ni de repositorios sin licencia.

## Antes de cada commit y cada push (obligatorio, sin excepciones)

El repositorio es **público**. Una fuga no se arregla borrándola: queda en el historial, en forks y en cachés. Por eso:

1. **Revisa qué entra**: `git status` y el diff completo (`git diff --cached`). Añade ficheros por ruta; no hagas `git add .` sin mirar la lista.
2. **Ejecuta el detector**: `python scripts/check_leaks.py --staged` antes del commit y `--push` antes del push. Busca ficheros prohibidos (`comercial/`, `.env`, claves `*.pem`/`*.p8`/`*.jks`/`*.keystore`, volcados `*.sql`/`*.dump`, hojas con datos fuera de `fixtures/`), secretos y tokens, DNI/NIE/CIF/IBAN válidos, teléfonos, emails reales, emails personales como autor de commit y las cadenas de la lista privada `.leakcheck-denylist.txt`.
3. **Está automatizado en tres capas**, y si alguna bloquea se corrige la causa:
   - hooks de Git en `.githooks/` (`pre-commit` y `pre-push`), que se activan con `git config core.hooksPath .githooks`;
   - hook de Claude Code (`.claude/settings.json`) antes de cualquier `git commit` o `git push`;
   - CI en GitHub (`.github/workflows/leak-check.yml`) sobre todo el historial, con el script y con gitleaks.
4. **Prohibido**: `--no-verify`, `commit -n`, `git add -f`, `-c core.hooksPath=...` o cualquier otra forma de esquivar las comprobaciones. Solo el autor humano puede decidir una excepción.
5. **Falso positivo** con un dato inventado: `leakcheck: allow` en esa línea, explicado en el PR.
6. **Email de Git**: solo el anónimo de GitHub (`ID+usuario@users.noreply.github.com`). El detector bloquea cualquier otro.
7. **Si algo se filtra**: revoca o rota la clave en ese momento, avisa al autor y reescribe el historial. Borrar el fichero no basta.

## Definición de hecho

- [ ] Todos los AC de la spec cubiertos por tests y en verde.
- [ ] `uv run poe check` sin errores.
- [ ] `python scripts/check_leaks.py --staged` sin hallazgos.
- [ ] Migraciones generadas y revisadas.
- [ ] Textos de UI traducibles.
- [ ] Accesibilidad: comprobación automática sin errores y páginas nuevas revisadas con teclado y lector de pantalla.
- [ ] `tasks.md`, estado de la spec y `PLAN.md` actualizados; `modelo-datos.md`/`arquitectura.md` si cambiaron.
- [ ] Flujo probado a mano en local (o con Playwright) y descrito en el PR.
