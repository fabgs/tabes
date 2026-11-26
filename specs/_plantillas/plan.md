# Plan técnico NNN — Título

Spec: [spec.md](spec.md) (versión del AAAA-MM-DD)

## 1. Resumen de la solución
Enfoque en un párrafo.

## 2. Modelo de datos
Modelos nuevos o modificados, campos, restricciones de BD (`UNIQUE`, `CHECK`, parciales), índices y migraciones. Enlaza el cambio en `docs/modelo-datos.md`.

## 3. Servicios y motores
Firmas tipadas, transacciones, auditoría.

```python
def generate_draw(round_id: int, *, seed: int | None = None, user: User) -> DrawProposal: ...
```

## 4. Interfaz
URLs, vistas, plantillas, fragmentos HTMX.
Accesibilidad (WCAG 2.2 AA): estructura y encabezados, dónde queda el foco tras cada actualización parcial, qué se anuncia a los lectores de pantalla y alternativa sin arrastrar.

## 5. Permisos y auditoría
Quién puede hacer qué; qué acciones se registran.

## 6. Pruebas
| AC | Test(s) | Tipo |
|---|---|---|
| AC-NNN-01 | `apps/x/tests/test_y.py::test_z` | unitario / propiedad / integración / e2e |

## 7. Riesgos y alternativas descartadas

## 8. Impacto en documentación

## 9. Checklist de constitución
- [ ] I Spec aprobada · [ ] II Invariantes en BD · [ ] III Determinismo y tests · [ ] IV Propuesta editable, avisos visibles
- [ ] V Publicación explícita · [ ] VI Auditoría · [ ] VII Sin dependencias nuevas (o ADR) · [ ] VIII Privacidad
- [ ] IX Ligero en móvil · [ ] X Cadenas traducibles · [ ] XI AC con tests · [ ] XII Sin código AGPL
