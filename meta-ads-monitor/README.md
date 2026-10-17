# Flubberhome Meta Ads Monitor

Monitoreo de solo lectura de Meta Ads para Flubberhome. Corre como tarea programada de Claude Code cada 8 horas (07:46, 15:46, 23:46, America/Argentina/Buenos_Aires).

## Cómo funciona

1. La sesión programada sigue `RUNBOOK.md`: lee Meta Ads a través de **Escalafy**, la tienda en **Shopify** y la competencia en fuentes públicas (Exa / búsqueda web).
2. Escribe un snapshot JSON con lo que leyó (lo no obtenido va `null`).
3. `scripts/monitor.py run <snapshot>` valida, aplica las reglas, agrupa alertas, mantiene los registros y genera el informe (secciones A–L).
4. Commit y push a `claude/affectionate-fermat-ps9s9g`; aviso por notificación de la tarea.

## Archivos

| Ruta | Qué es |
| --- | --- |
| `config/monitor.json` | IDs, ventanas, umbrales provisionales, límites de gasto aprobados (vacíos), costos conocidos |
| `RUNBOOK.md` | Procedimiento de cada ejecución y lo que nunca se hace sin aprobación |
| `scripts/monitor.py` | Motor: validación, reglas, deduplicación, registros, informe |
| `tests/test_monitor.py` | Pruebas (`python3 -m unittest discover -s meta-ads-monitor/tests`) |
| `data/snapshots/` | Un JSON por ejecución |
| `data/reports/` | Un informe por ejecución y `LATEST.md` |
| `data/state/runs.json` | Historial de ejecuciones |
| `data/state/alerts.json` | Alertas agrupadas por huella: primera vez, veces, estado, resolución |
| `data/state/experiments.json` | Backlog de experimentos con historial de cambios |
| `data/state/competitors.json` | Registro de competidores con historial |

## Límites actuales

- No hay acceso directo a Meta (Ads Manager, Pixel, Facturación, Biblioteca de anuncios): `facebook.com` y `graph.facebook.com` están bloqueados por la política de red del entorno y el conector Adspirer falla con 403. Los datos de Meta llegan vía Escalafy (sin estado de facturación, ventana de atribución ni revisión de anuncios).
- Umbrales provisionales: con 0 ventas no hay base histórica de CPA/ROAS. Ajustarlos en `config/monitor.json`.
- Costos de envío, comisiones e impuestos no documentados: la rentabilidad sale como escenario estimado.
