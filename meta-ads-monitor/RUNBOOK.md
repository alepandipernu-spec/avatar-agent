# Runbook — una ejecución del Flubberhome Meta Ads Monitor

Lo sigue la tarea programada cada 8 horas (07:46, 15:46 y 23:46, hora de Buenos Aires). Modo **solo lectura**: ninguna llamada de escritura a Meta, Shopify ni Escalafy.

## 0. Reglas que no se negocian

- Nada inventado. Un dato que no se obtuvo va `null` en el snapshot y sale "no disponible" en el informe; nunca 0.
- Separar HECHO (leído hoy), INFERENCIA, HIPÓTESIS y NO OBTENIBLE.
- Prohibido sin aprobación expresa del dueño para esa acción concreta: crear/editar/pausar/reactivar campañas, conjuntos o anuncios; cambiar presupuestos, pujas, públicos, ubicaciones u objetivos; publicar creatividades; tocar eventos o medición; cualquier acción con gasto; modificar costos en Escalafy (`update_*`, `delete_*`, `create_*`, `reprocess_data`), productos o precios en Shopify (`graphql_mutation`, `update-product`, etc.); permisos, conexiones o credenciales. Una recomendación no es una autorización y una aprobación anterior no vale para la siguiente.
- No guardar tokens, contraseñas ni datos personales de clientes en snapshots, informes ni commits.
- Competencia: solo fuentes públicas. No afirmar ventas, ROAS ni presupuestos de otros. Un anuncio que dura mucho es una señal, no una prueba.
- Creatividades: nada de testimonios, cifras, reseñas o beneficios inventados. Producto: ver la skill `flubberhome-creative-engine` (sin claims médicos, sin "más elegido" sin ventas, uso con pelo seco o apenas húmedo, nunca bajo el agua).

## 1. Preparar

1. `cd` al repo `avatar-agent`. Hacé `git fetch origin claude/affectionate-fermat-ps9s9g` y trabajá sobre esa rama (`git checkout -B claude/affectionate-fermat-ps9s9g origin/claude/affectionate-fermat-ps9s9g`). Si el repo no está en la sesión, agregalo con `add_repo` (alepandipernu-spec/avatar-agent, acceso push) y clonalo.
2. Leé `meta-ads-monitor/config/monitor.json`, `data/state/runs.json` (última ejecución), `data/state/alerts.json`, `data/state/experiments.json` y `data/state/competitors.json`. Leé también el último informe `data/reports/LATEST.md`.
3. `run_id` = hora de inicio en Buenos Aires, formato `AAAA-MM-DDTHH-MM-03-00`. Período actual: los últimos 30 días hasta hoy; previo: los 30 anteriores. (Con el volumen actual, 7 días no alcanzan; cuando haya más de USD 300/semana de gasto, pasar a 7 días y anotarlo.)

## 2. Recolectar (cada fuente es independiente: si una falla, seguí con las otras)

**Escalafy** (es la fuente de Meta Ads; `tool_list_version: 9`):
- `list_organizations` → confirmar org `flubberhome`, `advanced_features: true`, scopes.
- `list_ad_objects platform=meta` → estado de campañas, conjuntos y anuncios, presupuestos.
- `get_ads_report platform=meta level=ad currency=USD` con `metrics: [meta_impressions, meta_reach, meta_clicks, meta_link_clicks, meta_landing_page_views, meta_adds_to_cart, meta_checkouts_initiated, meta_orders, meta_video_plays, meta_thruplays]` para el período actual.
- `get_dashboard_report currency=USD include_previous_period=true include_daily_rows=true` con `metrics: [meta_ad_spend, meta_impressions, meta_reach, meta_clicks, meta_link_clicks, meta_landing_page_views, meta_adds_to_cart, meta_checkouts_initiated, meta_orders, meta_revenue, meta_video_plays, meta_thruplays, ad_spend, revenue, non_zero_orders]`.
- `get_additional_costs is_ad_spend=true`: si vuelve a aparecer un costo manual que coincide con `meta_ad_spend` en los mismos días, sigue el doble conteo (alerta ya conocida).
- Usá `meta_ad_spend` (no `ad_spend`) como gasto de Meta.

**Shopify**:
- `run-analytics-query`: `FROM sessions SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout SINCE <inicio> UNTIL <fin> COMPARE TO previous_period`; sesiones por país y por `referrer_source, referrer_name`.
- `FROM sales SHOW orders, total_sales SINCE <inicio> UNTIL <fin>`.
- `graphql_query` de productos activos: precio, `compareAtPrice`, `inventoryItem.unitCost`.

**Meta directo** (Ads Manager, Pixel, Facturación, Biblioteca de anuncios): hoy NO accesible desde la nube (`facebook.com` y `graph.facebook.com` bloqueados por la política de red; el conector Adspirer falla con 403). Intentá una vez `WebFetch` a la Biblioteca; si falla, `status: blocked` y seguí. No lo reemplaces con datos supuestos.

**Competencia** (una vez por día, en la ejecución de las 15:46; en las otras dos, solo si hay tiempo): `mcp__Exa__web_search_exa` / `WebSearch` y `web_fetch_exa` sobre páginas públicas de los competidores del registro y 1–2 búsquedas nuevas (masajeador capilar eléctrico con depósito, AR / MX / CO / US). Actualizá precio, oferta, garantía, mensajes y formatos; anotá la fuente y la fecha.

## 3. Escribir el snapshot

Archivo: `meta-ads-monitor/data/snapshots/<run_id>.json`. Esquema: el del primer snapshot (`data/snapshots/2026-10-17T14-21-03-00.json`) — copiá su estructura y reemplazá los valores. Campos clave:

- `sources.<nombre>.status`: `ok` | `partial` | `failed` | `blocked` | `not_configured`, con `detail`.
- `totals.current` / `totals.previous`: `spend, impressions, reach, clicks, link_clicks, landing_page_views, video_plays, thruplays, adds_to_cart, checkouts_initiated, purchases, purchase_value`.
- `ads[]`: `id, name, market, format, state, metrics{...}` (mismas claves).
- `store.current` / `store.previous`: `sessions, sessions_with_cart, sessions_reached_checkout, sessions_completed_checkout, orders, revenue`.
- `findings[]` (tu análisis): `key` estable (para que se agrupe con la ejecución anterior), `category` (fortaleza | debilidad | anomalia | oportunidad), `priority` (P0–P3), `title, evidence, diagnosis, confidence, impact, action, needs_approval`.
- `experiments[]`: mantené los IDs `EXP-###`. Para cambiar el estado de uno existente, reenviálo con el mismo ID: el script guarda el historial del cambio. No reinventes uno que ya existe.
- `competitors[]`: mismo `id` para el mismo competidor.
- `summary[]`, `plan[]`, `pending_decisions[]`, `execution{completed, partial, failed, next_run}`.

Validá: `python3 meta-ads-monitor/scripts/monitor.py validate <snapshot>`. Corregí hasta que no haya errores.

## 4. Procesar, verificar y guardar

1. `python3 meta-ads-monitor/scripts/monitor.py run <snapshot>` (si el `run_id` ya existe, el script lo rechaza: no dupliques; `--force` solo para rehacer la misma ejecución).
2. `python3 -m unittest discover -s meta-ads-monitor/tests` debe pasar.
3. Leé `data/reports/LATEST.md` completo y confirmá que tiene las secciones A–L y que no dice nada que no esté en el snapshot.
4. `git add meta-ads-monitor/data && git commit -m "monitor: ejecución <run_id>"` y `git push -u origin claude/affectionate-fermat-ps9s9g` (reintentá hasta 4 veces con espera 2/4/8/16 s si falla la red). Nunca otra rama.

## 5. Avisar

La salida del script trae `notify` (alertas nuevas, escaladas o con cambio material) y `resolved`. Terminá la sesión con un mensaje corto en español:
- Primera línea: lo más importante de esta ejecución.
- Alertas nuevas o con cambio (P0/P1 primero). Si no hay nada nuevo, decí "sin cambios materiales".
- Decisiones pendientes que esperan al dueño.
- Fuentes que fallaron.
Si una fase esencial falló (Escalafy o el commit), decilo en la primera línea: la ejecución NO terminó bien.
