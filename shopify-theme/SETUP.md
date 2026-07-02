# flubberhomme — tema de Shopify

Este directorio (`shopify-theme/`) es un **tema de Shopify completo (Online Store 2.0, Liquid)**
que recrea 1:1 el diseño del handoff `Diseño en Shopify.zip` (marca **flubberhomme**,
licuadoras portátiles LL-890): Home, PDP, Colección, Carrito, Ayuda, Nosotros y Contacto,
bilingüe ES/EN, con las mismas animaciones, tipografías y tokens de color del diseño original.

No es una copia literal del prototipo HTML (`Tienda.dc.html`) — como indica su propio README,
ese archivo es una *referencia de diseño* con una sintaxis de plantilla propia (`<x-dc>`, `sc-for`,
etc.) que no es código de producción. Este tema reimplementa el mismo look & feel usando
objetos **reales** de Shopify: `product`, `collection`, `cart`, checkout nativo, formulario de
contacto nativo, búsqueda predictiva nativa y localización nativa.

## 1. Subir el tema

Opciones:

- **Shopify CLI**: `shopify theme push` desde dentro de `shopify-theme/` (requiere estar
  logueado con `shopify login --store tu-tienda.myshopify.com`).
- **Admin → Tienda online → Temas → Subir tema**: comprimí el *contenido* de `shopify-theme/`
  (no la carpeta en sí) en un `.zip` y subilo ahí.

## 2. Crear los productos

El diseño original muestra 6 tarjetas en la colección: 4 colores de la misma licuadora + 2 packs.
Se mapean a **3 productos reales** de Shopify (la licuadora tiene una variante de Color con 4
valores, que el tema expande automáticamente en 4 tarjetas en la colección, igual que el diseño):

| Producto | Handle | Opción | Precio | Precio comparado |
|---|---|---|---|---|
| Licuadora Portátil (LL-890) | `licuadora-portatil-ll-890` | Color: Rosa / Blanco / Lavanda / Azul | $49.90 c/u | — |
| Pack Dúo — 2 Licuadoras | `pack-duo-2-licuadoras` | — | $89.90 | $99.80 (badge "Ahorrá $10") |
| Kit Smoothie + Recetario | `kit-smoothie-recetario` | — | $64.90 | — |

Se incluye `products_import.csv` listo para **Admin → Productos → Importar**. El CSV trae
títulos, precios, variantes y el tag `bestseller` en la licuadora (activa el badge "Más vendido"
en la variante Rosa, igual que el diseño). Las imágenes **no** viajan en el CSV (necesitan URLs
públicas) — subilas manualmente después de importar, usando los archivos de `assets/` como
referencia exacta de cada color:

- `assets/col-rosa.png` → imagen de la variante Rosa
- `assets/col-blanco.png` → imagen de la variante Blanco
- `assets/col-lavanda.png` → imagen de la variante Lavanda
- `assets/col-azul.png` → imagen de la variante Azul
- `assets/producto.png` → imagen principal/hero (útil como imagen del producto o para las
  secciones Home vía "Hero" → "Imagen del producto")
- `assets/box-rosa.png`, `assets/box-blanco.png` → sección "En la caja" del Home

> Importante: el tema **detecta automáticamente** cualquier producto con una única opción
> llamada "Color" (o "Colour") y lo expande en una tarjeta por variante en la colección y en
> los swatches del PDP — no hace falta tocar código para agregar un 5º color, solo agregar la
> variante en el Admin.

## 3. Colecciones y menú

1. Creá una colección (por ejemplo "Tienda", handle `all` o una manual) que incluya los 3
   productos de arriba.
2. En el editor de temas, configurá:
   - **Encabezado** → "Colección Tienda" y "Producto destacado" (para los links Tienda/Producto
     del nav).
   - **Hero** (sección del Home) → "Producto principal" (para el precio del CTA "Comprar ahora")
     y "Colección Ver la tienda".
   - **Franja más vendido** / **Banner CTA** → elegí el producto de la licuadora.
   - **Carrito** → colección para "Ir a la tienda" y colección para el cross-sell "Completá tu
     compra".

## 4. Páginas Ayuda / Nosotros / Contacto

Creá 3 páginas en **Admin → Tienda online → Páginas** (el contenido de cada una ya viene
resuelto por el tema vía traducciones, no hace falta escribir nada en el editor de la página):

| Página (título sugerido) | Template a asignar |
|---|---|
| Ayuda | `page.ayuda` |
| Nosotros | `page.nosotros` |
| Contacto | `page.contacto` |

Asigná el template desde el panel derecho de la página ("Plantilla de tema").
Después enlazalas desde **Pie de página** (sección del footer) en las settings
"Página de Ayuda / Nosotros / Contacto".

## 5. Idioma (ES/EN)

El selector ES/EN del header usa la **localización nativa de Shopify** (no un toggle simulado).
Para que aparezca:

1. **Configuración → Idiomas** → agregá "English" como idioma publicado.
2. El tema ya trae `locales/en.json` y `locales/es.default.json` con todos los textos fijos
   (nav, botones, carrito, FAQ, reseñas, etc.) en ambos idiomas, calcados del diseño original.
3. Los campos editables desde el Admin (títulos/descripciones de producto, páginas, colecciones)
   se traducen aparte con **Translate & Adapt** (gratis, Shopify App Store).

## 6. Cupón FLUBBER10

El carrito reemplaza el cupón simulado del prototipo por el mecanismo real de Shopify:
al tocar "Aplicar" redirige a `/discount/FLUBBER10?redirect=/cart`, que aplica el código a la
sesión de checkout. Para que funcione, creá en **Admin → Descuentos** un código:

- Código: `FLUBBER10`
- Tipo: Porcentaje, 10%
- Aplica a: todo el pedido (o a los 3 productos de arriba)

## 7. Colores de marca

**Configuración del tema → Marca** trae el color de acento (`#FF5C48` por defecto) y las 4
paletas alternativas del diseño original (azul, verde, violeta, naranja). El color "profundo"
de hover se calcula automáticamente oscureciendo el acento un 14%, igual que hacía el prototipo.

## Diferencias deliberadas frente al prototipo (y por qué)

El README del handoff pide explícitamente **no** copiar la sintaxis del prototipo y usar
"product/collection/cart objects reales" y "el carrito/checkout nativos de Shopify". Por eso:

- **Checkout**: se usa el checkout nativo y hosteado de Shopify (botón "Finalizar compra" del
  carrito) en vez de reconstruir un formulario de pago propio — construir un formulario de
  tarjeta propio sería además un riesgo de seguridad/PCI innecesario.
- **Búsqueda**: usa la Predictive Search API nativa (`/search/suggest.json`) en vez de filtrar
  una lista fija en memoria, así funciona con cualquier catálogo.
- **Cupón**: usa el deep-link nativo `/discount/CODE`, no un cálculo de -10% hecho a mano.
- **Envío**: la tarifa real solo la calcula Shopify en el checkout; el carrito muestra un aviso
  informativo ("Envío gratis en este pedido" según el umbral configurado, o "Envío calculado en
  el checkout") en vez de inventar un monto fijo de $5.90.
- **Newsletter / contacto**: usan los formularios nativos `customer` y `contact` de Shopify
  (entregan un email real al dueño de la tienda / suscriben al cliente), no un `alert()` de
  demostración.
