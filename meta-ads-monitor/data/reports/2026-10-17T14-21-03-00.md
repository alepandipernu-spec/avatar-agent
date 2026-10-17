# Flubberhome · Meta Ads Monitor · 2026-10-17T14:21-03:00

Período: 2026-09-18 → 2026-10-17 · comparado con 2026-08-19 → 2026-09-17 · moneda USD · zona America/Argentina/Buenos_Aires · modo read_only

## A. Resumen ejecutivo

- Meta Ads está APAGADO: las 4 campañas (AR, CO, MX, US) están pausadas; último gasto el 14/10. En 30 días se gastaron USD 227,93 con 0 compras; en 365 días la tienda no registra ningún pedido.
- El problema principal no está en el clic: hubo 607 visitas a la página a USD 0,38 cada una. El embudo se corta después: 786 sesiones → 10 con carrito (1,3%) → 6 llegaron al checkout → 0 compras.
- EE. UU. consumió el 42% del gasto (USD 95,65) para 12 visitas (USD 7,97 cada una), contra USD 0,15–0,19 en Colombia y Argentina.
- Escalafy cuenta dos veces USD ~103 de gasto de septiembre (costo manual que repite el gasto sincronizado): ROAS y ganancia del panel combinado están mal hasta corregirlo.
- Los videos 'Pack Dúo (V10)' y 'Demo (V02)' en AR y CO traen visitas a USD 0,08–0,23; son los únicos candidatos a volver a probar, pero no hay ninguna señal de compra todavía.
- Alertas abiertas: 12 (3 P0/P1). Nuevas o con cambio en esta ejecución: 12. Resueltas: 0.

## B. Estado técnico

| Fuente | Estado | Detalle |
| --- | --- | --- |
| escalafy | ok | Org flubberhome (admin, advanced_features true). Cuenta Meta 3984236798375831: catálogo, reporte por anuncio, dashboard diario, costos. |
| shopify | ok | Tienda hfymza-82 / flubberhomme.com: sesiones, embudo, pedidos, productos y costos. |
| competencia_web | partial | Exa: páginas públicas; 9 fichas de competidores (12 vendedores). Sin datos de anuncios. |
| meta_ad_library | blocked | facebook.com no resuelve desde la nube (política de red). No se vieron anuncios de competidores. |
| meta_ads_manager_pixel_facturacion | blocked | graph.facebook.com rechazado por el proxy (403) y conector Adspirer caído (403). Sin estado de facturación, revisión de anuncios, ventana de atribución ni eventos del Pixel. |

- los últimos días hasta 2026-10-17 todavía pueden cambiar (pedidos tardíos, reexpresión de Meta)
- Gasto de Meta = meta_ad_spend de Escalafy (sincronizado). El 'ad_spend' combinado de Escalafy está inflado por un costo manual duplicado (ver alerta).
- Los presupuestos que informa Escalafy (10.000 y 15.400 ARS diarios) no se pudieron confirmar en Ads Manager; la unidad (pesos o centavos) queda sin verificar.
- El período previo tiene 1.289 clics en enlace y 0 visitas a la página: esa métrica no se registró entonces, no significa que no hubo visitas (Shopify contó 1.633 sesiones).
- Shopify reporta la zona horaria como EDT y Escalafy usa la de la organización; las cifras diarias pueden correrse un día.
- Moneda: tienda en USD; cuenta publicitaria en ARS; métricas convertidas por Escalafy a USD con su tasa diaria.
- Métricas no disponibles en esta ejecución: frecuencia por anuncio, CTR de enlace nativo de Meta, retención de video 25/50/75/95%, ventana de atribución, estado de revisión de anuncios, estado de facturación, historial de cambios de configuración, desglose por ubicación, dispositivo, edad.

## C. Rendimiento publicitario

| Métrica | Actual | Anterior | Cambio |
| --- | --- | --- | --- |
| Gasto | USD 227.93 | USD 82.50 | +176% |
| Impresiones | 27,157 | 23,568 | +15% |
| Alcance (suma diaria) | 24,362 | 19,446 | +25% |
| Clics (todos) | 1,050 | 1,212 | -13% |
| Clics en enlace | 773 | 1,289 | -40% |
| Visitas a la página | 607 | no disponible | sin comparación |
| Reproducciones 3 s | 5,236 | 7,746 | -32% |
| ThruPlays | 1,453 | 4,441 | -67% |
| Agregados al carrito (Meta) | 3 | 0 | nuevo (antes 0) |
| Inicios de pago (Meta) | 0 | 0 | sin comparación |
| Compras atribuidas (Meta) | 0 | 0 | sin comparación |
| Valor de compras (Meta) | USD 0.00 | USD 0.00 | sin comparación |
| CPM | USD 8.39 | USD 3.50 | +140% |
| CTR de enlace | 2.85% | 5.47% | -48% |
| CTR total (todos los clics) | 3.87% | 5.14% | -25% |
| CPC de enlace | USD 0.29 | USD 0.06 | +361% |
| Costo por visita a la página | USD 0.38 | no disponible | sin comparación |
| Frecuencia | 1.11 | 1.21 | -8% |
| CPA (compras Meta) | no disponible | no disponible | sin comparación |
| ROAS atribuido | 0.00 | 0.00 | sin comparación |

Por anuncio (ordenado por gasto):

| Anuncio | Estado | Gasto | Impr. | CPM | CTR enlace | Clics enlace | LPV | LPV/clic | Costo/LPV |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| US - VID Demo (V02) | paused | USD 60.13 | 438 | USD 137.29 | 1.60% | 7 | 4 | 57.14% | USD 15.03 |
| US - IMG Hook | paused | USD 20.24 | 208 | USD 97.30 | 2.88% | 6 | 7 | 116.67% | USD 2.89 |
| AR - VID Pack Dúo (V10) | paused | USD 19.69 | 2,752 | USD 7.15 | 3.85% | 106 | 87 | 82.08% | USD 0.23 |
| MX - VID Pack Dúo (V10) | paused | USD 18.90 | 4,864 | USD 3.88 | 1.48% | 72 | 54 | 75.00% | USD 0.35 |
| CO - VID Pack Dúo (V10) | paused | USD 18.01 | 4,137 | USD 4.35 | 6.67% | 276 | 225 | 81.52% | USD 0.08 |
| MX - IMG Hero | paused | USD 14.20 | 657 | USD 21.62 | 1.98% | 13 | 12 | 92.31% | USD 1.18 |
| AR - VID Demo (V02) | paused | USD 12.35 | 3,337 | USD 3.70 | 4.76% | 159 | 117 | 73.58% | USD 0.11 |
| CO - IMG Pack Dúo | paused | USD 11.79 | 5,291 | USD 2.23 | 1.23% | 65 | 39 | 60.00% | USD 0.30 |
| MX - IMG Hook | paused | USD 9.50 | 462 | USD 20.56 | 1.73% | 8 | 11 | 137.50% | USD 0.86 |
| US - IMG Duo Pack | paused | USD 7.55 | 140 | USD 53.94 | 1.43% | 2 | 1 | 50.00% | USD 7.55 |
| AR - IMG Hook | paused | USD 6.71 | 966 | USD 6.94 | 1.76% | 17 | 12 | 70.59% | USD 0.56 |
| AR - IMG Pack Dúo | paused | USD 5.71 | 1,577 | USD 3.62 | 1.20% | 19 | 19 | 100.00% | USD 0.30 |
| CO - IMG Hero | paused | USD 5.59 | 1,136 | USD 4.92 | 0.62% | 7 | 5 | 71.43% | USD 1.12 |
| CO - IMG Hook | paused | USD 4.77 | 391 | USD 12.20 | 1.53% | 6 | 8 | 133.33% | USD 0.60 |
| US - IMG Hero | paused | USD 4.36 | 53 | USD 82.28 | 3.77% | 2 | 0 | 0.00% | no disponible |
| US - VID Duo Pack (V10) | paused | USD 3.36 | 36 | USD 93.43 | 2.78% | 1 | 0 | 0.00% | no disponible |
| MX - IMG Pack Dúo | paused | USD 3.25 | 450 | USD 7.22 | 1.33% | 6 | 5 | 83.33% | USD 0.65 |
| AR - IMG Hero | paused | USD 1.45 | 127 | USD 11.44 | 0.79% | 1 | 1 | 100.00% | USD 1.45 |
| CO - VID Demo (V02) | paused | USD 0.33 | 120 | USD 2.77 | 0.00% | 0 | 0 | no disponible | no disponible |
| MX - VID Demo (V02) | paused | USD 0.03 | 15 | USD 1.73 | 0.00% | 0 | 0 | no disponible | no disponible |

## D. Análisis del embudo

| Etapa | Volumen | Tasa desde la etapa anterior |
| --- | --- | --- |
| Impresiones (Meta) | 27,157 | no disponible |
| Clics en enlace (Meta) | 773 | 2.85% |
| Visitas a la página de destino (Meta) | 607 | 78.53% |
| Sesiones de la tienda (Shopify, todas las fuentes) | 786 | 129.49% |
| Sesiones con agregado al carrito (Shopify) | 10 | 1.27% |
| Sesiones que llegaron al checkout (Shopify) | 6 | 60.00% |
| Compras (Shopify) | 0 | 0.00% |

Mayor punto de fuga medible: **Sesiones que llegaron al checkout (Shopify) → Compras (Shopify)** (0.00%).

Nota: las sesiones de Shopify incluyen tráfico orgánico y directo; el paso Meta → Shopify no es una tasa de conversión.
- Mejor etapa: impresión → clic en enlace en AR y CO (CTR de enlace 3,4% y 3,2%; CO - VID Pack Dúo 6,7%).
- Mayor fuga absoluta: sesión → carrito (786 → 10). Mayor fuga relativa: checkout → compra (6 → 0). Con 6 checkouts no se puede separar todavía un checkout roto de un abandono normal: falta la compra de prueba (EXP-001).
- Meta atribuyó 3 agregados al carrito; Shopify contó 10 sesiones con carrito (incluye tráfico directo y orgánico). No hay señal de eventos duplicados.
- Confianza del diagnóstico: media. Causas abiertas: precio en USD para tráfico argentino, confianza (marca nueva, sin reseñas reales), medios de pago, costo de envío de 1 unidad, o una falla del checkout. Ninguna está descartada.

## E. Fortalezas y debilidades

**FORTALEZA**

- [P3] Los videos traen visitas más baratas que las imágenes (sin contar EE. UU.) — Evidencia: AR+CO+MX: video USD 69,31 → 483 visitas (USD 0,14); imagen USD 62,98 → 108 visitas (USD 0,58). Mejor anuncio: CO - VID Pack Dúo (V10), 276 clics en enlace, 225 visitas, CTR de enlace 6,7%, USD 0,08 por visita. Diagnóstico: El video muestra el uso y retiene: 5.236 reproducciones de 3 s y 1.453 ThruPlays en el período. Confianza: media. Acción: Usar el V10 y el V02 como control en cualquier prueba nueva; no gastar más en imágenes estáticas hasta que una gane en visitas con intención.

**DEBILIDAD**

- [P1] Tráfico sin ventas: 0 pedidos en 365 días — Evidencia: 30 días: 786 sesiones, 10 con carrito, 6 en checkout, 0 completadas. 30 días previos: 1.633 sesiones, 14, 7, 0. Shopify 365 días: 0 pedidos, USD 0. Diagnóstico: La fuga está en la tienda y la oferta, no en el anuncio. Sin una compra de prueba no se puede descartar una falla técnica del checkout o del pago. Confianza: alta (hecho) / media (causa). Acción: EXP-001 (compra de prueba) antes de cualquier gasto nuevo; después EXP-002 y EXP-003. (requiere aprobación)
- [P1] USD 227.93 gastados en el período sin compras — Evidencia: Gasto Meta USD 227.93; compras Shopify 0; compras atribuidas por Meta 0. Diagnóstico: El embudo no llega a compra. No alcanza para culpar al anuncio: también pueden fallar oferta, precio, confianza o checkout. Confianza: media. Acción: Antes de reactivar gasto, probar el checkout de punta a punta y revisar la oferta (ver experimentos).
- [P2] EE. UU. se lleva el 42% del gasto con el peor costo por visita — Evidencia: US: USD 95,65, 875 impresiones (CPM USD 109), 18 clics en enlace, 12 visitas → USD 7,97 por visita. AR: USD 0,19; CO: USD 0,15; MX: USD 0,56. US - VID Demo (V02) solo: USD 60,13 por 4 visitas. Diagnóstico: Mercado caro con presupuesto chico (15.400 ARS/día) que no sale de aprendizaje; además la tienda tiene 66 sesiones de EE. UU. y 0 carritos en 30 días. Confianza: media. Acción: No reactivar la campaña US hasta tener una venta en LatAm. Si se prueba, que sea un experimento aparte. (requiere aprobación)
- [P2] 'US - VID Demo (V02)': CPM 20× la mediana — Evidencia: CPM USD 137.29 vs mediana USD 6.94. Diagnóstico: Audiencia o mercado caro (p. ej. US) o entrega con poca competencia por presupuesto bajo. Confianza: media. Acción: Comparar costo por visita de ese mercado antes de volver a asignarle presupuesto. (requiere aprobación)
- [P2] Precio tachado en 'ScalpCare Pro 1 unidad' sin precio anterior verificable — Evidencia: Precio USD 41.93, 'antes' USD 59.90, con 0 ventas registradas. Diagnóstico: Un precio de referencia que nunca se cobró puede leerse como engañoso y contradice la regla de la marca (sin precio tachado). Confianza: alta. Acción: Decidir si se quita el compare-at price en Shopify. (requiere aprobación)
- [P2] Precio tachado en 'ScalpCare Pro Pack Dúo' sin precio anterior verificable — Evidencia: Precio USD 71.88, 'antes' USD 119.80, con 0 ventas registradas. Diagnóstico: Un precio de referencia que nunca se cobró puede leerse como engañoso y contradice la regla de la marca (sin precio tachado). Confianza: alta. Acción: Decidir si se quita el compare-at price en Shopify. (requiere aprobación)
- [P2] Precio tachado en 'ScalpCare Pro Pack Familiar' sin precio anterior verificable — Evidencia: Precio USD 89.85, 'antes' USD 179.70, con 0 ventas registradas. Diagnóstico: Un precio de referencia que nunca se cobró puede leerse como engañoso y contradice la regla de la marca (sin precio tachado). Confianza: alta. Acción: Decidir si se quita el compare-at price en Shopify. (requiere aprobación)
- [P3] Afirmación sin respaldo en el catálogo: 'Pack Dúo · Más elegido - ScalpCare Pro' — Evidencia: Título con "Más elegido" sin ventas registradas (producto en borrador). Diagnóstico: Afirmación no verificable. Confianza: alta. Acción: Renombrar antes de publicar ese producto. (requiere aprobación)

**ANOMALIA**

- [P1] Escalafy cuenta dos veces el gasto de Meta del 7 al 16/09 — Evidencia: Costo manual 'Meta Ads · Ventajas - ScalpCare Pro - Septiembre (cuenta 3984236798375831)', marcado como inversión publicitaria, con montos diarios idénticos al gasto sincronizado (p. ej. 12/09: ARS 34.236,83 en ambos). Duplicado: ARS 126.277,25 (≈ USD 103). Del 3 al 5/09 el costo manual suma ARS 31.867,14 sin gasto sincronizado. Diagnóstico: La carga manual se hizo antes de que la sincronización trajera esos días. El ad_spend combinado del 1 al 17/09 es ARS 284.421,64 en vez de 158.144,39. Confianza: alta. Acción: Borrar en Escalafy los tramos del 7 al 16/09 del costo manual (dejar 3–5/09 si ese gasto no aparece sincronizado). Tenemos el permiso costs:write, pero es una modificación: requiere tu aprobación. (requiere aprobación)
- [P2] No hay campañas activas en la cuenta — Evidencia: 4 campañas, todas en estado pausado. Último día con gasto: 2026-10-14. Diagnóstico: Sin entrega no hay datos nuevos. Si la pausa fue intencional (decisión del dueño), no es un problema. Confianza: alta. Acción: Confirmar si la pausa es intencional. Reactivar solo con un experimento aprobado. (requiere aprobación)
- [P2] Entrega intermitente: el gasto se prende y se apaga — Evidencia: 9 de 30 días con gasto; 10 cortes en el período. Diagnóstico: Pausas manuales frecuentes, límite de gasto alcanzado o pagos rechazados. Cada corte reinicia el aprendizaje. Confianza: media. Acción: Revisar el historial de actividad y Facturación en Ads Manager.
- [P3] Campaña de agosto–septiembre que ya no existe: clics sin visitas registradas — Evidencia: Campaña 52604677081664 (10 anuncios, sin nombre en el catálogo): USD 82,50 del 7 al 16/09, 1.289 clics en enlace, 0 visitas a la página; el 12/09 tuvo 984 clics en 8.940 impresiones (11%). Shopify contó 913 sesiones esa semana. Diagnóstico: Probablemente la campaña 'Ventajas' (Advantage+) que se borró. Los clics llegaron a la tienda; Meta no registró la visita a la página (evento no configurado o campaña de tráfico). Un CTR de 11% en un día sugiere clics accidentales (Audience Network). Confianza: baja. Acción: Ninguna ahora. Si se reactiva una campaña de tráfico, excluir Audience Network.

**OPORTUNIDAD**

- [P2] Garantía más débil que la de la competencia — Evidencia: Flubberhome (según bible/product al 01/10): cambios 30 días sin abrir, defectos dentro de 72 h. Gadnic: 12 meses de garantía de fábrica + envío gratis. Hairrova: 30 días de devolución + 1 año. Nordic Biolabs: 120 días. Diagnóstico: Hipótesis: con una marca nueva y sin reseñas reales, la política de cambios 'sin abrir' frena la compra de un producto que hay que probar. Confianza: baja. Acción: Decisión del dueño sobre la política (ver EXP-003). No cambiar textos de la tienda sin aprobación. (requiere aprobación)
- [P3] Casi todos los competidores prometen crecimiento o anticaída: hay lugar para una marca honesta — Evidencia: Ver sección F: Lena Vegetal ('control caída'), Beltronic ('anticaída y densidad'), AUREVIA ('frenar la caída'), Hairrova ('clinically proven… 56 days'), Anyra ('93% saw thicker hair growth'). Diagnóstico: Esas promesas atraen clics pero son riesgo de rechazo en Meta y de desconfianza. Flubberhome no puede ni debe usarlas. Confianza: media. Acción: Probar ángulo 'aplicá tu tónico sin ensuciarte las manos' (EXP-004). (requiere aprobación)

## F. Inteligencia competitiva

**Gadnic (vía Bidcom)** (nuevo) · bidcom.com.ar · mercado AR · verificado 2026-10-17
- Precio/oferta: No visible en la página consultada; preventa ('disponible en 26 días'), envío gratis a todo el país, 10 disponibles.
- Propuesta: Marca local conocida; 3 modos + luz infrarroja, temporizador 10 min, depósito <6 ml, USB-C, 1400 mAh.
- Mensajes: Rutina doméstica; sin promesas de crecimiento en el texto leído. Garantía de fábrica 12 meses.
- Formatos: No obtenido (sin acceso a la Biblioteca de anuncios).
- Hecho observado: Ofrece 12 meses de garantía y envío gratis.
- Hecho observado: Ficha técnica completa y medible (batería, potencia, tiempos).
- Inferencia: Compite en confianza de marca local y garantía, no en precio.
- Hipótesis: La garantía larga es un argumento que Flubberhome no puede igualar hoy.
- No obtenible: Anuncios activos, presupuesto, ventas.
- Fuentes: https://home-test.bidcom.com.ar/masajeador-capilar/masajeador-capilar-electrico-gadnic-con-luz-infrarroja-3-modos-deposito-para-liquidos-1400-mah-5w-tipo-c

**Lena Vegetal** (nuevo) · lenacosmetica.com.ar · mercado AR · verificado 2026-10-17
- Precio/oferta: ARS 25.600 (tachado ARS 32.000, '20% OFF'); ARS 20.480 con transferencia.
- Propuesta: Kit masajeador + tónico de romero y salvia (60 ml).
- Mensajes: 'Control caída', 'frena la caída', 'estimula el crecimiento', 'activar el chi'.
- Formatos: No obtenido.
- Hecho observado: Vende el aparato junto con un tónico propio.
- Hecho observado: Descuento extra por transferencia.
- Inferencia: El bundle con líquido resuelve la pregunta '¿qué le pongo al depósito?'.
- Hipótesis: Un kit con tónico podría subir el valor percibido; requiere proveedor y verificar claims.
- No obtenible: Anuncios, ventas.
- Fuentes: https://www.lenacosmetica.com.ar/productos/scalp-masajeador-capilar-tonico-capilar-control-caida/

**Beltronic Beauty Tools** (nuevo) · beltronic.com.ar · mercado AR · verificado 2026-10-17
- Precio/oferta: Kit ARS 175.890 (lista ARS 185.990); 10% off por transferencia.
- Propuesta: Posicionamiento profesional ('uso profesional', técnicas capilares) con serum activo.
- Mensajes: 'Anticaída y densidad', 'reduce la caída'.
- Formatos: Tiene Facebook, Instagram, TikTok y YouTube (enlaces en la tienda); anuncios no obtenidos.
- Hecho observado: Precio alto apoyado en un activo nombrado (Capixyl).
- Inferencia: Apunta a un comprador que ya busca tratamiento, no a regalo/bienestar.
- No obtenible: Anuncios, ventas.
- Fuentes: https://www.beltronic.com.ar/productos/masajeador-scalp-electrico-capixyl-5/

**Microshop** (nuevo) · microshop.com.ar · mercado AR · verificado 2026-10-17
- Precio/oferta: ARS 45.780 (tachado ARS 60.000, '24% OFF'), envío gratis, 10% off por transferencia.
- Propuesta: Tienda de gadgets con marca propia registrada ('Micro Masajeador Capilar®').
- Mensajes: 'Revitaliza tu cabello', 'placentero masaje'.
- Formatos: No obtenido.
- Hecho observado: Envío gratis y descuento por transferencia, igual que la mayoría de las tiendas AR.
- No obtenible: Anuncios, ventas.
- Fuentes: https://www.microshop.com.ar/productos/micro-masajeador-capilar/

**AUREVIA (en Farmatodo)** (nuevo) · farmatodo.com.co · mercado CO · verificado 2026-10-17
- Precio/oferta: COP 37.425 (lista COP 49.900); despacho 4–5 días.
- Propuesta: Venta dentro de una cadena de farmacias (confianza del canal).
- Mensajes: 'Rejuvenecedor de folículos', 'ideal para frenar la caída'.
- Formatos: No obtenido.
- Hecho observado: Producto similar vendido en farmacia en Colombia.
- Inferencia: En CO el canal farmacia da confianza que una tienda nueva no tiene.
- No obtenible: Anuncios, ventas.
- Fuentes: https://www.farmatodo.com.co/producto/500031920-rejuvenecedor-de-foliculos-capilares-y-aplicador-de-tonico-aurevia-caja-x-1

**Anyra** (nuevo) · shopanyra.com · mercado US · verificado 2026-10-17
- Precio/oferta: USD 50,95 (tachado USD 158,95, 'SAVE 68%').
- Propuesta: DTC con prueba social masiva y estadísticas de 'clientes'.
- Mensajes: 'Rated 4.9 | 12,319 Customers', '93% saw healthier follicle stimulation… thicker hair growth'.
- Formatos: No obtenido.
- Hecho observado: Usa porcentajes de satisfacción y conteo de clientes en la página.
- No obtenible: Si las cifras de clientes y reseñas son verificables.
- No obtenible: Anuncios, ventas.
- Fuentes: https://shopanyra.com/products/electric-red-light-scalp-massager-comb-with-oil-applicator

**Hairrova RootGlow** (nuevo) · hairrova.com · mercado US · verificado 2026-10-17
- Precio/oferta: USD 89,99 (tachado USD 149,99), envío express gratis, 30 días de devolución, 1 año de garantía.
- Propuesta: Promesa de resultado con plazo.
- Mensajes: 'Clinically proven… visible hair growth in 56 days'.
- Formatos: No obtenido.
- Hecho observado: Garantía de devolución explícita y destacada.
- No obtenible: Respaldo del 'clinically proven'.
- No obtenible: Anuncios, ventas.
- Fuentes: https://hairrova.com/products/hairrova-scalp-hair-growth-therapy-brush

**Nordic Biolabs** (nuevo) · nordic-biolabs.com · mercado US · verificado 2026-10-17
- Precio/oferta: USD 79 (tachado USD 158, 'SAVE 50%'); garantía de devolución 120 días.
- Propuesta: Aparato como vehículo de un consumible propio (recompra).
- Mensajes: 'Hair regrowth', testimonios y cita profesional.
- Formatos: No obtenido.
- Hecho observado: Modelo aparato + consumible.
- No obtenible: Anuncios, ventas.
- Fuentes: https://nordic-biolabs.com/products/nordic-applicator-for-hair-serum

**Genéricos en Amazon (mriya, Satorix, UniiSuui, ABVOT)** (nuevo) · amazon.com · mercado US · verificado 2026-10-17
- Precio/oferta: USD 21,99 – 49,99.
- Propuesta: 'Zero mess', 'no more greasy hands', resistente al agua, temporizador 10 min.
- Mensajes: Varios usan el beneficio de aplicar el líquido en la raíz sin ensuciarse.
- Formatos: Listados de Amazon.
- Hecho observado: El mismo tipo de aparato se consigue desde USD 21,99 en EE. UU.
- Inferencia: En EE. UU. el precio de Flubberhome (USD 41,93 + envío) compite contra Amazon con envío rápido.
- No obtenible: Anuncios.
- Fuentes: https://www.amazon.com/mriya-Electric-Applicator-Massager-Treatment/dp/B0DLWC7WXC, https://www.amazon.com/Satorix-Electric-Scalp-Massager-Applicator/dp/B0GW9G41D4

- Patrón: HECHO: 7 de las 9 fichas del registro muestran precio tachado o '% OFF' (Gadnic y los genéricos de Amazon no); en Argentina además hay 10–20% de descuento por transferencia.
- Patrón: HECHO: la mayoría promete anticaída o crecimiento; solo Gadnic y los genéricos de Amazon se quedan en masaje y aplicación.
- Patrón: HECHO: los que más destacan confianza la apoyan en garantía (12 meses, 1 año, 120 días) o en el canal (farmacia, marca local).
- Patrón: HECHO: tres vendedores venden el aparato junto con un tónico o serum.
- Patrón: INFERENCIA: el beneficio funcional más repetido y verificable es 'aplicar el producto en la raíz sin ensuciarse las manos'.
- Patrón: NO OBTENIBLE: qué anuncios corren, desde cuándo y con qué formato (Biblioteca de anuncios bloqueada).

## G. Plan de mejora

| # | Acción | Impacto | Confianza | Urgencia | Costo | Dificultad | Aprobación |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Aprobar la corrección del costo duplicado en Escalafy (7–16/09) | medio (métricas correctas) | alta | alta | 0 | baja | sí |
| 2 | Hacer la compra de prueba EXP-001 y confirmar el evento Purchase | alto | alta | alta | ≈ USD 42 reembolsable | baja | sí |
| 3 | Quitar el precio tachado (compare-at) de las 3 variantes | medio (confianza, riesgo de rechazo) | media | media | 0 | baja | sí |
| 4 | Cargar en config los costos reales: envío por pedido, comisión de pago, impuestos, y un límite de gasto aprobado | medio (rentabilidad real y alertas P0) | alta | media | 0 | baja | no |
| 5 | Decidir la política de garantía y el bloque de uso (EXP-003) | medio | baja | media | 0 | media | sí |
| 6 | Recién después: EXP-002 (AR+CO, solo video, USD 60) con EXP-004 como segundo anuncio | alto | media | baja | USD 60 | media | sí |
| 7 | Habilitar acceso a facebook.com / graph.facebook.com o reconectar Adspirer para ver Pixel, facturación y Biblioteca de anuncios | medio (cobertura) | alta | media | 0 | baja | sí |

## H. Experimentos

**EXP-001 · Compra de prueba de punta a punta** (nuevo) — estado: pendiente de aprobación · prioridad P1
- Problema: 0 compras con 6 checkouts en 30 días; no sabemos si el checkout o el pago funcionan.
- Evidencia: Shopify: 6 sesiones llegaron al checkout, 0 completaron; 0 pedidos en 365 días.
- Hipótesis: Si el checkout o un medio de pago falla para compradores de AR/CO, ninguna mejora de anuncio va a vender.
- Variable: Ninguna (diagnóstico).
- Constantes: Tienda, precios y campañas pausadas.
- Métrica principal: Pedido creado en Shopify + evento Purchase recibido por Meta.
- Protección: Medios de pago ofrecidos en AR y CO; costo de envío mostrado para 1 unidad; moneda del checkout.
- Presupuesto máximo (sujeto a aprobación): 0 en anuncios; el costo de una compra real reembolsable (USD 41,93) o un pedido con la pasarela en modo prueba.
- Duración: Una sesión, desde un celular con datos de Argentina y otro de Colombia si es posible.
- Éxito: Pedido completo y Purchase en Meta.
- Fracaso: Error, medio de pago ausente o Purchase que no llega: corregir antes de gastar.
- Inconcluso: No aplica.
- Riesgos: Ninguno sobre la cuenta publicitaria. Lo hace el dueño: Claude no carga tarjetas.

**EXP-002 · Reactivación controlada solo AR + CO con los videos ganadores** (nuevo) — estado: propuesto · prioridad P2
- Problema: Cuando hubo gasto, 42% se fue a EE. UU. con USD 7,97 por visita.
- Evidencia: AR USD 0,19 y CO USD 0,15 por visita; videos V10/V02 los mejores.
- Hipótesis: Con el mismo presupuesto en AR+CO y solo video, conseguimos suficientes carritos e inicios de pago para saber si la tienda convierte.
- Variable: Mercados (solo AR y CO) y formato (solo video V10 y V02).
- Constantes: Objetivo Ventas/Compra, oferta, página de destino.
- Métrica principal: Inicios de pago (Shopify) por cada USD 10.
- Protección: Costo por visita ≤ USD 0,40; visitas/clic ≥ 70%; carritos ≥ 1,5% de las sesiones.
- Presupuesto máximo (sujeto a aprobación): 60 en total (aprox. USD 8,5 por día durante 7 días), sujeto a aprobación.
- Duración: 7 días seguidos sin pausar (las pausas reinician el aprendizaje).
- Éxito: ≥ 1 compra o ≥ 5 inicios de pago.
- Fracaso: ≥ 400 visitas con 0 inicios de pago: el problema es la tienda/oferta, parar.
- Inconcluso: Menos de 400 visitas.
- Riesgos: Gastar sin resolver EXP-001. Solo después de EXP-001.

**EXP-003 · Confianza en la página: garantía clara y uso real** (nuevo) — estado: propuesto · prioridad P2
- Problema: 786 sesiones → 10 carritos (1,3%).
- Evidencia: Competidores destacan garantía de 12 meses / 1 año / 120 días; Flubberhome ofrece cambios 30 días sin abrir.
- Hipótesis: Una política de prueba clara ('probalo 30 días') y un bloque de 'cómo se usa' con el video V02 suben el paso visita → carrito.
- Variable: Bloque de garantía y uso en la página de producto (un solo cambio).
- Constantes: Precio, anuncios, tráfico.
- Métrica principal: Sesiones con carrito / sesiones.
- Protección: Llegada al checkout; consultas por WhatsApp/Instagram.
- Presupuesto máximo (sujeto a aprobación): 0 extra (se mide con el tráfico de EXP-002).
- Duración: Comparación antes/después con ≥ 400 sesiones en cada tramo.
- Éxito: Carrito ≥ 2,5% de las sesiones.
- Fracaso: Sin cambio con ≥ 400 sesiones.
- Inconcluso: Menos sesiones.
- Riesgos: Comparación antes/después, no A/B: estacionalidad. La política la decide el dueño.

**EXP-004 · Ángulo creativo: 'tu tónico en la raíz, no en tus manos'** (nuevo) — estado: propuesto · prioridad P3
- Problema: Necesitamos un mensaje diferenciado sin claims médicos.
- Evidencia: Competidores prometen crecimiento; los genéricos de Amazon venden 'zero mess'. Nuestro producto tiene depósito real (bible/product).
- Hipótesis: Mostrar el problema cotidiano (aplicar el tónico con los dedos, se ensucia el pelo y las manos) genera clics con más intención que 'masaje relajante'.
- Variable: Gancho y guion (un video nuevo).
- Constantes: Mercado, presupuesto y destino iguales a EXP-002; control = V10.
- Métrica principal: Costo por inicio de pago vs control.
- Protección: Retención de video (ThruPlay / reproducción 3 s), CTR de enlace, costo por visita.
- Presupuesto máximo (sujeto a aprobación): 30, dentro de EXP-002 como segundo anuncio, sujeto a aprobación.
- Duración: Hasta 2.000 impresiones por anuncio.
- Éxito: ≥ 20% menos costo por visita con igual o mejor tasa de carrito.
- Fracaso: Peor que el control en costo por visita y carrito.
- Inconcluso: Menos de 2.000 impresiones.
- Riesgos: Usar el producto mal en el video (sin agua, sin espuma). Revisar con la skill creativa.
- Concepto creativo: Microdrama Edificio Flubber: Juli le explica a Rama, que se pone el tónico con los dedos frente al espejo, cómo cargar el depósito y aplicarlo con el pelo seco.
- Gancho: Primer plano: dedos pegoteados de tónico y Rama diciendo '¿otra vez el pelo grasoso?'. Texto: '¿Te ponés el tónico con los dedos?'
- Guion: 0–2 s dedos y frustración · 2–6 s Juli aparece con el ScalpCare · 6–14 s carga el depósito, intensidad suave, círculos lentos con pelo seco · 14–20 s Rama mira sus manos limpias · 20–25 s producto + 'Conocé ScalpCare Pro™'.
- Texto principal: Tu tónico va a la raíz, no a tus dedos. ScalpCare Pro™ tiene un depósito atrás: lo cargás, elegís una de sus 3 intensidades y lo pasás suave sobre el pelo seco. Recargable por USB-C.
- Titular: Aplicá tu tónico sin ensuciarte
- Llamada a la acción: Conocé ScalpCare Pro™
- Formato: Video vertical 9:16, 20–25 s, subtítulos, etiqueta de contenido con IA.

## I. Rentabilidad

| Producto | Precio | Costo unitario | Margen bruto | CPA máx. (costos conocidos) | CPA máx. (escenario) | ROAS de equilibrio (escenario) |
| --- | --- | --- | --- | --- | --- | --- |
| ScalpCare Pro 1 unidad | USD 41.93 | USD 18.91 | USD 23.02 | USD 23.02 | USD 18.83 | 2.23 |
| ScalpCare Pro Pack Dúo | USD 71.88 | USD 37.82 | USD 34.06 | USD 34.06 | USD 18.87 | 3.81 |
| ScalpCare Pro Pack Familiar | USD 89.85 | USD 56.73 | USD 33.12 | USD 33.12 | USD 16.13 | 5.57 |

- Escenario = ESTIMACIÓN: 10% de comisiones e impuestos sobre el precio y USD 8 de envío cuando el envío es gratis. No es un dato.
- Costos faltantes (no documentados): payment_fee_pct, shipping_cost_per_order_usd, tax_pct. Ninguna conclusión de rentabilidad es definitiva.
- Ventas verificadas Shopify en el período: 0 pedidos, USD 0.00. Ingresos atribuidos por Meta: USD 0.00.

## J. Alertas

- **[P1] USD 227.93 gastados en el período sin compras** · nueva · detectada 2026-10-17T14:21-03:00 · veces: 1 · confianza media · impacto: Gasto sin retorno verificable. · acción: Antes de reactivar gasto, probar el checkout de punta a punta y revisar la oferta (ver experimentos).
- **[P1] Escalafy cuenta dos veces el gasto de Meta del 7 al 16/09** · nueva · detectada 2026-10-17T14:21-03:00 · veces: 1 · confianza alta · impacto: ROAS, CPA y ganancia del panel combinado de Escalafy subestimados; comparaciones de período engañosas. · acción: Borrar en Escalafy los tramos del 7 al 16/09 del costo manual (dejar 3–5/09 si ese gasto no aparece sincronizado). Tenemos el permiso costs:write, pero es una modificación: requiere tu aprobación. · requiere aprobación
- **[P1] Tráfico sin ventas: 0 pedidos en 365 días** · nueva · detectada 2026-10-17T14:21-03:00 · veces: 1 · confianza alta (hecho) / media (causa) · impacto: Todo gasto en anuncios es improductivo hasta resolverlo. · acción: EXP-001 (compra de prueba) antes de cualquier gasto nuevo; después EXP-002 y EXP-003. · requiere aprobación
- **[P2] No hay campañas activas en la cuenta** · nueva · detectada 2026-10-17T14:21-03:00 · veces: 1 · confianza alta · impacto: Cero aprendizaje mientras siga así. · acción: Confirmar si la pausa es intencional. Reactivar solo con un experimento aprobado. · requiere aprobación
- **[P2] 'US - VID Demo (V02)': CPM 20× la mediana** · nueva · detectada 2026-10-17T14:21-03:00 · veces: 1 · confianza media · impacto: Cada visita cuesta mucho más. · acción: Comparar costo por visita de ese mercado antes de volver a asignarle presupuesto. · requiere aprobación
- **[P2] Entrega intermitente: el gasto se prende y se apaga** · nueva · detectada 2026-10-17T14:21-03:00 · veces: 1 · confianza media · impacto: Los resultados no son comparables entre días y Meta no sale de aprendizaje. · acción: Revisar el historial de actividad y Facturación en Ads Manager.
- **[P2] Precio tachado en 'ScalpCare Pro 1 unidad' sin precio anterior verificable** · nueva · detectada 2026-10-17T14:21-03:00 · veces: 1 · confianza alta · impacto: Riesgo de confianza y de rechazo de anuncios. · acción: Decidir si se quita el compare-at price en Shopify. · requiere aprobación
- **[P2] Precio tachado en 'ScalpCare Pro Pack Dúo' sin precio anterior verificable** · nueva · detectada 2026-10-17T14:21-03:00 · veces: 1 · confianza alta · impacto: Riesgo de confianza y de rechazo de anuncios. · acción: Decidir si se quita el compare-at price en Shopify. · requiere aprobación
- **[P2] Precio tachado en 'ScalpCare Pro Pack Familiar' sin precio anterior verificable** · nueva · detectada 2026-10-17T14:21-03:00 · veces: 1 · confianza alta · impacto: Riesgo de confianza y de rechazo de anuncios. · acción: Decidir si se quita el compare-at price en Shopify. · requiere aprobación
- **[P2] EE. UU. se lleva el 42% del gasto con el peor costo por visita** · nueva · detectada 2026-10-17T14:21-03:00 · veces: 1 · confianza media · impacto: Con el mismo dinero AR/CO habrían traído ~40 veces más visitas. · acción: No reactivar la campaña US hasta tener una venta en LatAm. Si se prueba, que sea un experimento aparte. · requiere aprobación
- **[P2] Garantía más débil que la de la competencia** · nueva · detectada 2026-10-17T14:21-03:00 · veces: 1 · confianza baja · impacto: Puede explicar parte de la fuga carrito → compra. · acción: Decisión del dueño sobre la política (ver EXP-003). No cambiar textos de la tienda sin aprobación. · requiere aprobación
- **[P3] Afirmación sin respaldo en el catálogo: 'Pack Dúo · Más elegido - ScalpCare Pro'** · nueva · detectada 2026-10-17T14:21-03:00 · veces: 1 · confianza alta · impacto: Riesgo de confianza si se publica. · acción: Renombrar antes de publicar ese producto. · requiere aprobación

## K. Decisiones pendientes (requieren aprobación expresa)

1. Corregir en Escalafy el costo manual 'Meta Ads · Ventajas - Septiembre': borrar los tramos del 7 al 16/09 (ARS 126.277,25 duplicados). ¿Lo hago?
2. EXP-001: hacer vos una compra de prueba (Claude no carga tarjetas) o activar la pasarela en modo prueba.
3. Quitar los precios 'antes' (59,90 / 119,80 / 179,70 USD) de ScalpCare Pro en Shopify.
4. Confirmar si la pausa de las 4 campañas es intencional (el monitor no reactiva nada).
5. Dar un límite de gasto diario y mensual aprobado, y los costos de envío, comisiones e impuestos.
6. Política de garantía/cambios (EXP-003).
7. Red del entorno: permitir facebook.com y graph.facebook.com, o reconectar Adspirer.

## L. Estado de la ejecución

- Inicio: 2026-10-17T14:21:25-03:00 · Fin del análisis: 2026-10-17T14:27:40-03:00
- Completado: Conexiones verificadas (Escalafy, Shopify, Exa)
- Completado: Estado de campañas, conjuntos y anuncios
- Completado: Métricas 30 días vs 30 días previos, por anuncio y diarias
- Completado: Embudo Shopify
- Completado: Costos de producto, envío, impuestos y costos adicionales en Escalafy
- Completado: Investigación pública: 9 fichas de competidores
- Completado: Backlog de experimentos
- Parcial: Competencia: sin anuncios (Biblioteca de anuncios bloqueada)
- Parcial: Rentabilidad: faltan costos de envío, comisiones e impuestos
- Falló: Meta directo (Ads Manager, Pixel, Facturación): bloqueado por la red del entorno
- Falló: Conector Adspirer: 403
- Próxima ejecución programada: 2026-10-17 15:46 (America/Argentina/Buenos_Aires) — tarea trig_01W98gbW1v5HysUuvdqXiFXe
- Snapshot: data/snapshots/2026-10-17T14-21-03-00.json
