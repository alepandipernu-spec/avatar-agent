# RUNBOOK — Flubberhome Competitor Intelligence

Tarea programada independiente del monitor de Meta Ads. Cada 8 horas (03:54, 11:54 y 19:54, Buenos Aires). Todo en español.
Especificación completa del dueño: `SPEC.md` (en esta carpeta). Este runbook dice cómo cumplirla en cada ejecución.

## 0. Reglas que no se negocian
- Solo lectura y fuentes públicas o accesos autorizados. Nunca: modificar campañas, publicar anuncios, comprar, completar checkouts, contactar competidores o proveedores, comprometer dinero, tocar Shopify/Escalafy/Meta (ninguna mutación), eludir logins o captchas, recopilar datos privados.
- Hechos, estimaciones e hipótesis siempre separados y etiquetados [HECHO] / [ESTIMACIÓN] / [HIPÓTESIS]. Toda afirmación con fuente (URL) y fecha de consulta.
- Nunca inventar ventas, unidades, facturación, presupuestos, segmentaciones, fechas de lanzamiento ni resultados. No confundir reseñas con unidades, seguidores con clientes, agotado con éxito, anuncio activo con rentabilidad, tráfico con ventas.
- Estimaciones solo con método explícito y margen de incertidumbre.
- No copiar textos, imágenes ni testimonios de otros: describir y parafrasear (citas de menos de 15 palabras, como máximo una por fuente).
- Ideas para Flubberhome: respetar la skill `flubberhome-creative-engine` (sin claims médicos, sin "más elegido", sin luz roja como beneficio, uso con pelo seco o apenas húmedo, nunca bajo el agua; sin nombrar competidores en piezas propias).
- No afirmar haber consultado una fuente que falló. Si una fuente falla, seguir con las demás y anotarlo en Limitaciones.

## 1. Privacidad (verificar al empezar)
`gh api repos/alepandipernu-spec/avatar-agent --jq .private`
- Si da `false` (repo público): no escribir en esta carpeta datos internos de Flubberhome (gasto, ventas, sesiones, costo unitario, margen). Usarlos solo para razonar y escribir conclusiones cualitativas ("el margen del Pack Dúo no soporta un regalo de más de X% del precio" sí; el costo exacto no). Anotar en Limitaciones que el repo sigue público.
- Si da `true`: se pueden escribir con fuente.

## 2. Preparación
1. `git fetch origin claude/competitor-intel && git checkout claude/competitor-intel && git pull --rebase`.
2. `run_id` = hora de inicio en Buenos Aires (`TZ=America/Argentina/Buenos_Aires date +%Y-%m-%dT%H-%M`).
3. Leer `data/flubberhome_context.md`, `data/runs.json` (últimas 3), `data/opportunities.json`, `reports/LATEST.md`.
4. Verificar en Shopify (solo lectura: `search_products status:active`) precios y variantes de ScalpCare Pro. Si cambiaron, actualizar el contexto y anotarlo.
5. Elegir el foco según la hora (rotación, para profundizar sin repetir):
   - **03:54 → Catálogo, tiendas y precios** (secciones 5, 8, 9 de la SPEC).
   - **11:54 → Anuncios, creatividades y demanda** (secciones 6, 7).
   - **19:54 → Reseñas, nuevos competidores y oportunidades** (secciones 4, 10, 11, 12).
   Si una ejecución anterior falló, retomar su foco primero. Cada ejecución hace además un chequeo rápido de cambios de precio en los 3 competidores directos de mayor relevancia.

## 3. Fuentes (en este orden)
- `mcp__Exa__web_search_exa` / `WebSearch` para descubrir; `mcp__Exa__web_fetch_exa` / `WebFetch` para leer páginas de producto, políticas y reseñas públicas.
- Mercados: AR, CO, MX, US. Búsquedas base: masajeador capilar eléctrico (con depósito / aplicador de tónico), scalp massager with oil applicator, cepillo exfoliante cuero cabelludo eléctrico; Mercado Libre AR/MX/CO (listados públicos: precio, "+N vendidos" que muestra ML, reseñas), Amazon (precio, cantidad y fecha de reseñas, ranking visible), TikTok Shop si es accesible.
- Anuncios: Biblioteca de anuncios de Meta. Desde la nube está bloqueada (verificado el 17/10/2026). Intentar una vez por ejecución de foco 11:54; si hay herramientas de navegador conectadas (`mcp__remote-devices__Claude_Browser__*` o `mcp__claude-in-chrome__*`), usarlas en modo lectura. Si no, usar fuentes alternativas públicas: TikTok Creative Center (Top Ads, si carga), videos publicados en las páginas de producto, perfiles públicos de Instagram/TikTok de las marcas, y artículos o agregadores públicos. Marcar claramente cuando un anuncio no viene de la Biblioteca.
- Mercado Libre: "+N vendidos" es un dato público de la plataforma, pero agrupado y redondeado; registrarlo como [HECHO: indicador de ML] con la fecha, nunca como ventas mensuales.

## 4. Qué registrar (base de conocimiento, `data/`)
Antes de crear algo, buscar si ya existe (por id o dominio). Actualizar campos y agregar una entrada en `history` con fecha, cambio y fuente. Nunca borrar historial.
- `competitors.json`: id, name, domain, market, category (A_directo / B_indirecto / C_inspiracional), relevant_products, price_visible, value_prop, channels, sources, last_reviewed, relevance (alta/media/baja), follow_reason, facts/inferences/hypotheses/unknowns, history.
- `products.json`: id `<competidor>:<producto>`, problema, variantes/packs, precio por variante, promos, garantía, devolución, envío, beneficios, objeciones resueltas, diferenciadores, cambios en el tiempo, merece_investigar (y por qué).
- `ads.json`: id, competidor, fuente, fecha vista, formato, gancho, primeros segundos, problema, demostración, beneficio, objeciones, estructura, texto en pantalla, CTA, oferta, motivaciones [INTERPRETACIÓN], primera y última vez visto (solo si es visible), repeticiones.
- `demand_signals.json`: señal, valor, fuente, fecha, alcance, tipo (HECHO/ESTIMACIÓN), qué indica y qué no.
- `reviews.json`: `items` (fuente, producto, problema clasificado, fecha, paráfrasis) y `patterns` (problema, nº de fuentes y competidores, aislado/tendencia, oportunidad para Flubberhome).
- `opportunities.json`: los 15 campos de la sección 11 de la SPEC + puntajes 1–5 de impacto, confianza, facilidad, costo, riesgo y urgencia, `score` = impacto×confianza×facilidad ÷ (costo×riesgo) (+1 si urgencia ≥ 4), estado (nueva / en evaluación / recomendada / probada / descartada) y historial.
- `experiments.json`: hipótesis, cambio, métrica, umbral, costo, estado, resultado (solo con datos reales).
- `runs.json`: run_id, foco, fuentes OK/fallidas, competidores revisados, novedades, oportunidades nuevas/actualizadas, privacidad (repo público/privado).

## 5. Informe
Escribir `reports/<run_id>.md` y copiarlo a `reports/LATEST.md`, con las secciones A a L de la SPEC (Resumen ejecutivo, Competidores analizados, Productos y ofertas, Análisis publicitario, Demanda y señales de ventas, Experiencia de compra, Reseñas y debilidades, Estrategias adaptables, Oportunidades priorizadas, Próximas acciones, Nuevos hallazgos, Limitaciones).
- Las secciones fuera del foco de la ejecución: una línea ("sin revisión en esta ejecución; último dato: <fecha>").
- Cada recomendación: evidencia + interpretación + confianza + acción concreta.
- Sin novedades relevantes: informe corto con las comprobaciones hechas. No rellenar.
- Ideas propias (ganchos, guiones, packs, mejoras de página): originales, basadas en una observación o hipótesis explícita, y con la métrica para evaluarlas. Nunca recomendar sumar un producto solo porque otro lo vende; evaluar demanda, competencia, diferenciación, costos, logística y riesgo.

## 6. Verificar y guardar
1. Validar que todos los JSON parsean: `python3 -c "import json,glob;[json.load(open(f)) for f in glob.glob('competitor-intel/data/*.json')]"`.
2. Revisar el informe: cada número tiene fuente y fecha; no hay datos internos si el repo es público; no hay textos copiados.
3. `git add competitor-intel && git commit -m "competitor-intel: <run_id> (<foco>)" && git pull --rebase && git push origin claude/competitor-intel`. Si el push falla, reintentar una vez después del pull; si sigue fallando, decirlo en el resumen final.

## 7. Aviso al dueño
- PushNotification de una línea solo si hay algo accionable y nuevo: una oportunidad con score alto, un cambio fuerte de precio u oferta de un competidor directo, un competidor nuevo relevante, o una fuente clave que dejó de funcionar.
- Resumen final (también con SendUserMessage si está disponible): 3–5 líneas con lo más importante, la oportunidad nº 1 y qué no se pudo consultar.
