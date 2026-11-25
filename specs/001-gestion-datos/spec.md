# Spec 001 — Gestión de datos e importación

| Campo | Valor |
|---|---|
| Estado | borrador |
| Fase | 1 |
| Depende de | 000 |
| Última actualización | 2026-11-25 |

## 1. Objetivo
Que el equipo de tab pueda dar de alta y mantener instituciones, equipos, oradores, jueces, salas, rondas y mociones de un torneo, tanto a mano como importando ficheros CSV o Excel, y marcar quién está disponible en cada ronda.

## 2. Actores
Miembro del equipo de tab.

## 3. Historias de usuario
- Como tab, quiero importar la hoja de inscripciones en un paso para no teclear 100 personas.
- Como tab, quiero ver los errores de la importación fila a fila antes de guardar nada.
- Como tab, quiero reutilizar instituciones y personas de torneos anteriores para no duplicarlas.
- Como tab, quiero marcar qué equipos, jueces y salas están disponibles en cada ronda.
- Como tab, quiero retirar a un equipo sin perder sus resultados anteriores.

## 4. Requisitos funcionales
- **RF-001-01** — El sistema deberá permitir crear, ver, editar, buscar y filtrar instituciones, equipos (con sus oradores), jueces, salas, rondas y mociones.
- **RF-001-02** — El sistema deberá ofrecer plantillas descargables (CSV y Excel) para: instituciones, equipos con oradores (una fila por orador), jueces, salas y conflictos.
- **RF-001-03** — Cuando el tab suba un fichero, el sistema deberá mostrar una vista previa con cada fila clasificada como "nueva", "actualiza existente" o "error", y el motivo de cada error.
- **RF-001-04** — Si hay alguna fila con error, el sistema no deberá permitir confirmar la importación hasta corregir el fichero. La importación es todo o nada.
- **RF-001-05** — Cuando una persona del fichero tenga el mismo email que una persona ya registrada en ADA, el sistema deberá reutilizarla en vez de crear otra.
- **RF-001-06** — Cuando un equipo o juez del fichero pertenezca a una institución inexistente, el sistema deberá proponer crearla en la vista previa.
- **RF-001-07** — El sistema deberá aceptar CSV separado por comas o punto y coma, en UTF-8 o Windows-1252, y ficheros .xlsx.
- **RF-001-08** — El sistema deberá permitir copiar instituciones, equipos y jueces desde un torneo anterior.
- **RF-001-09** — El sistema deberá permitir marcar la disponibilidad de equipos, jueces y salas por ronda, individualmente y en bloque. Al crear una ronda se copiará la disponibilidad de la anterior.
- **RF-001-10** — El sistema deberá permitir retirar equipos, jueces y salas (baja lógica) conservando su histórico.
- **RF-001-11** — El sistema deberá permitir añadir una o varias mociones por ronda, con infoslide opcional.
- **RF-001-12** — El sistema deberá mostrar avisos (no bloqueantes) cuando un equipo tenga menos o más oradores de los que permite el formato.

## 5. Reglas de negocio y validaciones
- Claves de coincidencia al importar: institución → código; equipo → nombre dentro del torneo; persona → email (o nombre completo + equipo si no hay email); sala → nombre.
- Una persona solo puede ser oradora de un equipo por torneo. Puede ser oradora y jueza a la vez solo si el tab lo confirma (aviso).
- Nombres de equipo y sala únicos dentro del torneo.
- Nota de juez dentro del rango configurado (por defecto 1,0–5,0).
- Un equipo retirado no se empareja en rondas posteriores; sus debates pasados siguen contando.

## 6. Criterios de aceptación
- **AC-001-01** — Dado un Excel con 20 equipos y 100 oradores válidos, cuando lo importo, entonces la vista previa muestra 20 equipos y 100 oradores "nuevos" y, al confirmar, aparecen todos en el torneo.
- **AC-001-02** — Dado un CSV con 3 filas con email inválido, cuando lo subo, entonces la vista previa marca esas 3 filas con el motivo y el botón de confirmar está deshabilitado.
- **AC-001-03** — Dado un CSV exportado de Excel en español (punto y coma, Windows-1252, con tildes), cuando lo subo, entonces los nombres con tildes se leen correctamente.
- **AC-001-04** — Dada una persona ya registrada con email ana@ejemplo.org, cuando importo un equipo que la incluye con ese email, entonces se vincula a la persona existente y no se crea un duplicado.
- **AC-001-05** — Dado un fichero que incluye a la misma persona en dos equipos, cuando lo subo, entonces ambas filas se marcan como error.
- **AC-001-06** — Dado un torneo con la ronda 2 creada, cuando creo la ronda 3, entonces su disponibilidad es la misma que la de la ronda 2.
- **AC-001-07** — Dado un equipo con resultados en las rondas 1 y 2, cuando lo retiro, entonces no aparece como disponible en la ronda 3 y sus resultados siguen en el histórico.
- **AC-001-08** — Dado un torneo anterior con 15 instituciones, cuando copio participantes desde él, entonces las instituciones y personas se reutilizan, no se duplican.

## 7. Casos límite
- Fichero vacío o solo con cabecera → mensaje claro.
- Columnas en otro orden o con mayúsculas/espacios distintos → se reconocen.
- Filas totalmente vacías intermedias → se ignoran.
- Importar dos veces el mismo fichero → la segunda vez todo sale como "actualiza existente" sin cambios.

## 8. Requisitos no funcionales
- Ficheros de hasta 5 MB y 5.000 filas; vista previa en < 5 s.
- Las listas de 200 elementos se cargan en < 500 ms.

## 9. Fuera de alcance
- Formulario público de inscripción de equipos.
- Sincronización con Google Sheets.
- Fusión manual de personas duplicadas (se valorará en fase 2).

## 10. Preguntas abiertas
- [ ] ¿Qué columnas tiene hoy la hoja de inscripciones de ADA? Pedir un ejemplo anonimizado. — ADA
- [ ] ¿Escala de nota de jueces que usa ADA (1–5, 1–10…)? — ADA

## Historial
- 2026-11-25 — creación.
