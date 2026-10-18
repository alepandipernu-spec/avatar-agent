# Inteligencia competitiva — run 2026-10-18T03-55

**Foco:** Catálogo, tiendas y precios (franja 03:54).
**Modo:** solo lectura. **Repo:** público (GitHub `private: false`), así que no hay datos internos de Flubberhome (gasto, ventas, costos ni margen).
**Etiquetas:** [HECHO] = observado, con fuente · [ESTIMACIÓN] = calculado, con método · [HIPÓTESIS] = interpretación sin confirmar. Todas las consultas se hicieron el 18/10/2026, entre las 03:55 y las 04:30 (Buenos Aires).

---

## A. Resumen ejecutivo
- **Lo más importante es de Flubberhome.** Lo verificado en Shopify (solo lectura) y en la ficha pública:
  - Cobra en USD en los 4 países y las entregas a Latinoamérica tardan **10 a 20 días hábiles**.
  - Los competidores locales cobran en moneda local, con cuotas, descuento por transferencia o pago contra entrega, y entregan en 1 a 8 días.
  - [ESTIMACIÓN] En Argentina, 1 unidad + envío ≈ ARS 79.500. Es más caro que cualquier eléctrico local relevado.
- **Corrección de OPP-009.** El ángulo "en MX llega más rápido que los vendedores de China" **no sirve**: el plazo propio es igual o más lento.
- **Oportunidad nueva: OPP-012, costo total y plazo claros en LatAm (score 37, nº 2).**
- **Sin cambios de precio** en 7 competidores directos: Holy, Lena, Microshop, NIHLO, Anyra, Hairrova y Nordic.
  - Glokore suma el código **"BF26"** a su embudo. [HIPÓTESIS] Es una promo de Black Friday ya cargada.
- **Oportunidad nº 1 sin cambios:** OPP-001, la demo de aplicación sin goteo (score 80).

## B. Competidores analizados
| id | Mercado | Cat. | Qué se revisó |
|---|---|---|---|
| holy-cosmetics-co | CO | A | Ficha + políticas de envío y cambios (pendiente del run anterior) |
| lena-vegetal-ar, microshop-ar | AR | A | Precio y condiciones |
| nihlo-co | CO | A | Precio y garantía |
| anyra-us, hairrova-us, nordic-biolabs-us | US | A | Precio |
| glokore-us | US | A | Embudo checkout4 (sin comprar) |
| ml-electricos-ar | AR | A | Listado público (copia de Exa) |
| co-dtc-tiendas (Smartjoys) | CO | A | Garantía |
| **mount-lai-us** | US | C | **Nuevo, inspiracional:** kit de aparato + aceite en Ulta |

Las fuentes de cada uno están en `data/competitors.json`.

## C. Productos y ofertas
**Flubberhome** ([HECHO], Shopify en modo lectura y [ficha](https://flubberhomme.com/products/flubberhomme-scalp-topical-applicator-roller-electric-scalp-massage-comb)):
- Precios: 1 unidad USD 41,93 + USD 10 de envío; Pack Dúo USD 71,88; Pack Familiar USD 89,85. Sin precio tachado. Sin cambios.
- Mercados de Shopify: "Estados Unidos" y "Latinoamérica" (AR, MX y CO). El precio es USD 41,93 en los 4 países.
- El producto figura modificado el 18/10/2026 a las 02:45 (BA). No se identificó qué cambió: precios y variantes siguen iguales.

**Competidores** ([HECHO], 18/10/2026):

| Competidor | Precio | Envío | Garantía / cambios | Pago |
|---|---|---|---|---|
| Holy Cosmetics (CO) | COP 149.990 (tachado 199.990) | Servientrega 3–8 días hábiles; gratis solo desde COP 200.000 | Cambio en 5 días hábiles; reembolso solo por garantía legal | Contra entrega, PSE, Bancolombia, ADDI |
| Lena (AR) | ARS 25.600 (ARS 20.480 por transferencia) | Gratis desde ARS 60.000 | — | 3 cuotas sin interés |
| Microshop (AR) | ARS 45.780 | Gratis | — | 10% por transferencia |
| NIHLO (CO) | COP 89.900 | — | 1 año por defectos | — |
| Smartjoys (CO) | COP 64.900 | — | 2 meses por defectos | — |
| Glokore (US) | Packs no visibles | — | 60 días de devolución (menos envío) + plan de reemplazo pago | Código "BF26" |
| Mount Lai (Ulta) | Kit USD 148 ("valor USD 175") | Gratis desde USD 35 | — | — |

Notas de las fichas:
- **Lena:** sigue con "+70 vendidos" y "Sin stock / quedan 3" a la vez.
- **Holy:** mezcla IPX7 e IPX6, y uso en seco con uso durante el lavado.

Fuentes: [Holy](https://holycosmetics.com.co/products/masajeador-capilar-revitalizante-capilar) ([envíos](https://holycosmetics.com.co/policies/shipping-policy), [cambios](https://holycosmetics.com.co/policies/refund-policy)), [Lena](https://www.lenacosmetica.com.ar/productos/scalp-masajeador-capilar-tonico-capilar-control-caida/), [Microshop](https://www.microshop.com.ar/productos/micro-masajeador-capilar/), [NIHLO](https://www.nihlo.com.co/products/masajeador-capilar-nihlo), [Smartjoys](https://smartjoys.co/producto/cepillo-masajeador-de-terapia-capilar-portatil-electrico/), [Glokore](https://glokore.com/scalpmassager/checkout4), [Mount Lai](https://www.ulta.com/p/vitality-qi-scalp-revitalizing-duo-mkt77006485?sku=77010064).

**Precios de EE. UU. sin cambios:**
- Anyra: USD 50,95 ([ficha](https://shopanyra.com/products/electric-red-light-scalp-massager-comb-with-oil-applicator)).
- Hairrova: USD 89,99, sigue "Sold out" ([ficha](https://hairrova.com/products/hairrova-scalp-hair-growth-therapy-brush)).
- Nordic: USD 79 ([ficha](https://nordic-biolabs.com/products/nordic-applicator-for-hair-serum)).

**Formato kit (aparato + líquido), [HECHO]:**
- Mount Lai: USD 148 en Ulta.
- YENNYE: USD 35,99 con aceite de batana ([Amazon](https://www.amazon.com/YENNYE-Electric-Scalp-Oil-Applicator/dp/B0GHPCCR2P)).
- warmyard: GBP 26,99 con aceite de romero ([UK](https://www.warmyard.co.uk/products/3-in-1-scalp-massager-oil-bundle)).
- Lena: masajeador + tónico.

Son 4 mercados. Esto refuerza OPP-006, que de todos modos sigue con score bajo por costo y riesgo.

## D. Análisis publicitario
Sin revisión en esta ejecución (le toca a la de las 11:54). Último dato: 17/10/2026.

## E. Demanda y señales de ventas
| Señal | Valor | Tipo |
|---|---|---|
| ML AR, eléctrico líder | MegaCuper ARS 37.692, "+50 vendidos", sin cambios ([listado](https://listado.mercadolibre.com.ar/masajeador-cuero-cabelludo), copia de Exa) | HECHO: indicador de ML |
| ML AR, otros eléctricos | ARS 58.006–69.999 con "+5" a "+25 vendidos". Los envíos desde China van de ARS 28.709 a 58.037 | HECHO: indicador de ML |
| Kits aparato + líquido | Vistos en US, UK y AR | HECHO (oferta visible) |
| CyberMonday Argentina | 2, 3 y 4 de noviembre de 2026 ([Tiendanube](https://www.tiendanube.com/blog/cybermonday-argentina)) | HECHO |

**Qué no indican:** ventas mensuales ni rentabilidad de nadie.

## F. Experiencia de compra
Comparación de condiciones visibles, sin comprar ni iniciar ningún checkout:
- [HECHO] **Flubberhome** informa en la ficha:
  - Plazo de entrega y despacho.
  - Que el precio está en USD y que pueden aplicar impuestos de importación.
  - Reemplazo o reembolso si el producto falla (aviso dentro de 72 h).
  - Email y teléfono de contacto.
  - Esto ya es más transparente que la mayoría de los competidores. Lo que falta es tenerlo **junto al botón** y **en moneda local**.
- [HECHO] **Los locales** ponen la forma de pago al lado del precio:
  - Cuotas sin interés (Lena).
  - Descuento por transferencia (Lena y Microshop).
  - Contra entrega (Holy).
- [HECHO] **Glokore** ofrece un plan de reemplazo pago como agregado, después de los datos de envío.
  - [HIPÓTESIS] Monetiza el miedo a la falla de fábrica, que en reseñas aparece en 6 fuentes.
  - Para Flubberhome es más coherente publicar una garantía clara (OPP-003) que vender una.
- No se verificó si el checkout de ningún competidor funciona.

## G. Reseñas y debilidades competitivas
Sin revisión en esta ejecución. Último dato: 17/10/2026 (run 19-55).
- La garantía de Smartjoys es de solo 2 meses. Encaja con el patrón de fallas de fábrica.

## H. Estrategias adaptables
1. **Condiciones de pago y plazo junto al precio**, como hacen los locales, sin copiar sus precios. Ver OPP-012.
2. **"Valor del kit" en vez de precio tachado** (Mount Lai). Es una forma honesta de mostrar ahorro, coherente con OPP-007, si algún día existe un kit.

**No replicar:**
- Precios tachados inflados (Holy, Smartjoys, Anyra, Hairrova, Nordic).
- Planes de garantía pagos como reemplazo de una garantía básica.
- Especificaciones contradictorias.

## I. Oportunidades priorizadas
Fórmula: score = impacto × confianza × facilidad ÷ (costo × riesgo), +1 si la urgencia es 4 o más.

| # | id | Score | Estado | Acción concreta |
|---|---|---|---|---|
| 1 | OPP-001 demo de aplicación sin goteo | 80 | nueva | Probar el depósito con líquidos livianos y espesos; grabar la demo |
| 2 | **OPP-012 costo total y plazo claros en LatAm (nueva)** | **37** | nueva | Ver detalle abajo |
| 3 | OPP-002 salto desde el cepillo manual (AR) | 36 | nueva | — |
| 4 | OPP-007 precio honesto | 30 | nueva | — |
| 5 | OPP-009 precio y mensaje por mercado | **24 (antes 16)** | nueva | **Corregida:** se descarta "envío rápido" en MX |
| 6 | OPP-008 / OPP-011 | 24 / 24 | nueva | — |

**OPP-012, costo total y plazo claros en LatAm:**
- **Evidencia:**
  - Shopify cobra USD en los 4 países.
  - La ficha informa 10–20 días hábiles a LatAm y USD 10 de envío por 1 unidad.
  - Los locales entregan en 1–8 días, en moneda local y con pago local.
- **Estimación** (conversión simple, sin percepciones de tarjeta ni impuestos):
  - Argentina: 1 unidad + envío ≈ ARS 79.500, con el oficial del BNA de ARS 1.530 del 15/10/2026 ([fuente](https://eleconomista.com.ar/economia/dolar-hoy-cuanto-cotiza-viernes-16-octubre-n98903)). Los eléctricos locales relevados van de ARS 25.600 a 69.999.
  - Colombia: ≈ COP 164.600, con una TRM de 3.170,46. Holy cobra COP 149.990 + envío.
  - México: ≈ MXN 934, con 17,98 MXN/USD. Las tiendas locales cobran MXN 990–1.038.
- **Interpretación** [HIPÓTESIS]: la fricción en LatAm es la incertidumbre sobre el total final y el plazo, no el precio de lista.
- **Confianza:** media.
- **Acción:** poner junto al botón, por país, el precio aproximado en moneda local, una fecha estimada de llegada y los impuestos posibles. Presentar el Pack Dúo como la opción que absorbe el envío.
- **Para decidir el dueño:** stock local o precio en moneda local para AR. No se recomienda sin datos de costos.
- **Métrica:** tasa de checkout iniciado → compra por país, y consultas a soporte sobre plazo o impuestos.

## J. Próximas acciones
- **Run de las 11:54** (anuncios):
  - Intentar la Biblioteca de Meta.
  - Revisar perfiles públicos de Holy y de las tiendas de CO.
  - Ver si Glokore u otros ya muestran creatividades de Black Friday.
- **Run de las 19:54:** reseñas de Mercado Libre dentro de las publicaciones (pendiente).
- **Para el dueño** (no se contactó a nadie):
  - Confirmar los plazos reales por país.
  - Ver qué percepciones o impuestos paga un comprador argentino con tarjeta en USD.
  - Decidir si se participa del CyberMonday AR (2 al 4 de noviembre). Sin datos de margen no se recomienda ningún descuento.

## K. Nuevos hallazgos
- 1 competidor nuevo (Mount Lai, inspiracional).
- 1 producto nuevo.
- 2 señales de demanda nuevas.
- 1 oportunidad nueva (OPP-012) y 2 actualizadas (OPP-009 de 16 a 24, OPP-006 de 1,33 a 2).
- Políticas de Holy completadas.
- Sin cambios fuertes de precio en los competidores directos.

## L. Limitaciones
- **Biblioteca de Meta:** no se intentó (fuera de la franja de anuncios; bloqueada desde la nube).
- **Mercado Libre:** el listado directo pide login, así que se usó la copia de Exa, que puede estar desfasada.
- **Glokore:** los precios por pack no se ven porque la plantilla no se renderiza.
- **Conversiones de moneda:** aproximadas y sin impuestos. Los plazos de Flubberhome son los que publica la ficha, no tiempos medidos.
- **Shopify:** no se pudo identificar qué cambió en el producto a las 02:45.
- **Repo público:** sin datos internos. Conviene volverlo privado.
