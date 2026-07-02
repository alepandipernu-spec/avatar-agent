(function () {
  'use strict';

  document.documentElement.classList.remove('no-js');

  /* Money formatting (Shopify's standard money_format template) --------------- */
  function formatMoney(cents, format) {
    if (typeof cents === 'string') cents = cents.replace('.', '');
    var value = '';
    var placeholderRegex = /\{\{\s*(\w+)\s*\}\}/;
    var formatString = format || (window.themeMoneyFormat) || '${{amount}}';

    function defaultTo(v, fallback) {
      return v === null || v === undefined || v !== v ? fallback : v;
    }

    function formatWithDelimiters(number, precision, thousands, decimal) {
      precision = defaultTo(precision, 2);
      thousands = defaultTo(thousands, ',');
      decimal = defaultTo(decimal, '.');
      if (isNaN(number) || number === null) return 0;
      number = (number / 100.0).toFixed(precision);
      var parts = number.split('.');
      var dollarsPart = parts[0].replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1' + thousands);
      var centsPart = parts[1] ? decimal + parts[1] : '';
      return dollarsPart + centsPart;
    }

    var match = formatString.match(placeholderRegex);
    var kind = match ? match[1] : 'amount';

    switch (kind) {
      case 'amount_no_decimals':
        value = formatWithDelimiters(cents, 0);
        break;
      case 'amount_with_comma_separator':
        value = formatWithDelimiters(cents, 2, '.', ',');
        break;
      case 'amount_no_decimals_with_comma_separator':
        value = formatWithDelimiters(cents, 0, '.', ',');
        break;
      default:
        value = formatWithDelimiters(cents, 2);
    }
    return formatString.replace(placeholderRegex, value);
  }

  /* Scroll reveal ---------------------------------------------------------- */
  function initReveal() {
    var targets = document.querySelectorAll('[data-reveal]');
    if (!targets.length) return;

    if (!('IntersectionObserver' in window)) {
      targets.forEach(function (el) { el.classList.add('is-revealed'); });
      return;
    }

    var vh = window.innerHeight || 800;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });

    targets.forEach(function (el) {
      var rect = el.getBoundingClientRect();
      if (rect.top < vh * 0.9) {
        el.classList.add('is-revealed');
        return;
      }
      observer.observe(el);
    });
  }

  /* Header search (Shopify predictive search API) ----------------------------- */
  function initSearch() {
    var toggleBtns = document.querySelectorAll('[data-search-toggle]');
    var panel = document.querySelector('[data-search-panel]');
    var input = document.querySelector('[data-search-input]');
    if (!panel || !toggleBtns.length) return;

    toggleBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var isOpen = panel.classList.toggle('is-open');
        btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        if (isOpen && input) {
          window.requestAnimationFrame(function () { input.focus(); });
        }
      });
    });

    if (!input) return;
    var grid = document.querySelector('[data-search-results]');
    var emptyMsg = document.querySelector('[data-search-empty]');
    if (!grid) return;

    var controller = null;
    var debounceId = null;

    function renderResults(products) {
      grid.innerHTML = '';
      products.forEach(function (product) {
        var link = document.createElement('a');
        link.className = 'fh-search__result';
        link.href = product.url;

        var thumb = document.createElement('span');
        thumb.className = 'fh-search__thumb';
        if (product.image) {
          thumb.style.backgroundImage = "url('" + product.image + "')";
        }

        var info = document.createElement('span');
        info.style.display = 'flex';
        info.style.flexDirection = 'column';
        info.style.gap = '2px';

        var name = document.createElement('span');
        name.className = 'fh-search__result-name';
        name.textContent = product.title;

        var price = document.createElement('span');
        price.className = 'fh-search__result-price';
        price.textContent = product.price;

        info.appendChild(name);
        info.appendChild(price);
        link.appendChild(thumb);
        link.appendChild(info);
        grid.appendChild(link);
      });
    }

    function search(query) {
      if (controller) controller.abort();
      if (!query) {
        grid.innerHTML = '';
        if (emptyMsg) emptyMsg.hidden = true;
        return;
      }
      controller = ('AbortController' in window) ? new AbortController() : null;
      var url = window.Shopify && window.Shopify.routes && window.Shopify.routes.root
        ? window.Shopify.routes.root + 'search/suggest.json'
        : '/search/suggest.json';
      url += '?q=' + encodeURIComponent(query) + '&resources[type]=product&resources[limit]=6&resources[options][unavailable_products]=last';

      fetch(url, { signal: controller ? controller.signal : undefined })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          var products = (data.resources && data.resources.results && data.resources.results.products) || [];
          renderResults(products);
          if (emptyMsg) emptyMsg.hidden = products.length !== 0;
        })
        .catch(function (err) {
          if (err && err.name === 'AbortError') return;
        });
    }

    input.addEventListener('input', function () {
      var q = input.value.trim();
      window.clearTimeout(debounceId);
      debounceId = window.setTimeout(function () { search(q); }, 220);
    });
  }

  /* Add to cart (AJAX) + badge pop --------------------------------------------- */
  function shopifyRoot() {
    return (window.Shopify && window.Shopify.routes && window.Shopify.routes.root) || '/';
  }

  function pulseCartBadge(count) {
    var badge = document.querySelector('[data-cart-badge]');
    if (!badge) return;
    badge.textContent = count;
    badge.classList.toggle('visually-hidden', count === 0);
    badge.classList.remove('is-popping');
    void badge.offsetWidth;
    badge.classList.add('is-popping');
  }

  function initCartForms() {
    document.addEventListener('submit', function (e) {
      var form = e.target.closest('form[action*="/cart/add"]');
      if (!form) return;
      e.preventDefault();

      var submitBtn = form.querySelector('[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;

      var formData = new FormData(form);

      fetch(shopifyRoot() + 'cart/add.js', {
        method: 'POST',
        body: formData,
        headers: { Accept: 'application/json' }
      })
        .then(function (res) {
          if (!res.ok) return res.json().then(function (err) { throw err; });
          return res.json();
        })
        .then(function () {
          return fetch(shopifyRoot() + 'cart.js', { headers: { Accept: 'application/json' } });
        })
        .then(function (res) { return res.json(); })
        .then(function (cart) {
          pulseCartBadge(cart.item_count);
          if (document.querySelector('[data-cart-form]')) {
            window.location.reload();
          }
        })
        .catch(function () {
          form.submit();
        })
        .then(function () {
          if (submitBtn) submitBtn.disabled = false;
        });
    });
  }

  /* Quantity steppers (PDP + cart lines) --------------------------------------- */
  function initQtySteppers() {
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-qty-decrease], [data-qty-increase]');
      if (!btn) return;
      var wrap = btn.closest('[data-qty-wrapper]');
      if (!wrap) return;
      var input = wrap.querySelector('input[type="number"], [data-qty-value]');
      if (!input) return;

      var isInput = input.tagName === 'INPUT';
      var current = parseInt(isInput ? input.value : input.textContent, 10) || 1;
      var min = 1;
      if (isInput && input.min !== '' && input.min !== null && !isNaN(parseInt(input.min, 10))) {
        min = parseInt(input.min, 10);
      }
      var next = btn.hasAttribute('data-qty-decrease') ? current - 1 : current + 1;
      if (next < min) next = min;

      if (isInput) {
        input.value = next;
        if (wrap.hasAttribute('data-qty-auto-submit')) {
          input.dispatchEvent(new Event('change', { bubbles: true }));
        }
      } else {
        input.textContent = next;
      }
    });
  }

  /* PDP: variant swatches, thumbnails, live price ------------------------------ */
  function initProductGallery() {
    var jsonEl = document.querySelector('[data-product-json]');
    if (!jsonEl) return;

    var data = { variants: [], fallback_image: '' };
    try { data = JSON.parse(jsonEl.textContent); } catch (e) { return; }
    var variants = data.variants || [];

    var mainImg = document.querySelector('[data-gallery-main]');
    var idInput = document.querySelector('[data-product-variant-id]');
    var priceEl = document.querySelector('[data-product-price]');
    var comparePriceEl = document.querySelector('[data-product-compare-price]');
    var saveEl = document.querySelector('[data-product-save]');
    var lineEl = document.querySelector('[data-product-line-price]');
    var colorValueEl = document.querySelector('[data-product-color-value]');
    var addBtn = document.querySelector('[data-add-to-cart]');
    var qtyInput = document.querySelector('[data-qty-value]');

    function findVariant(id) {
      for (var i = 0; i < variants.length; i++) {
        if (String(variants[i].id) === String(id)) return variants[i];
      }
      return null;
    }

    function selectVariant(id) {
      var variant = findVariant(id);
      if (!variant) return;

      if (idInput) idInput.value = variant.id;

      var imgSrc = (variant.featured_image && variant.featured_image.src) || data.fallback_image;
      if (mainImg && imgSrc) mainImg.style.backgroundImage = "url('" + imgSrc + "')";

      if (priceEl) priceEl.textContent = formatMoney(variant.price);

      var qty = qtyInput ? (parseInt(qtyInput.value, 10) || 1) : 1;
      if (lineEl) lineEl.textContent = formatMoney(variant.price * qty);

      if (comparePriceEl) {
        if (variant.compare_at_price && variant.compare_at_price > variant.price) {
          comparePriceEl.textContent = formatMoney(variant.compare_at_price);
          comparePriceEl.style.display = '';
          if (saveEl) {
            var pct = Math.round(((variant.compare_at_price - variant.price) / variant.compare_at_price) * 100);
            saveEl.textContent = '-' + pct + '%';
            saveEl.style.display = '';
          }
        } else {
          comparePriceEl.style.display = 'none';
          if (saveEl) saveEl.style.display = 'none';
        }
      }

      if (colorValueEl) colorValueEl.textContent = variant.title;

      if (addBtn) {
        if (variant.available) {
          addBtn.removeAttribute('disabled');
        } else {
          addBtn.setAttribute('disabled', 'disabled');
        }
      }

      document.querySelectorAll('[data-variant-swatch]').forEach(function (el) {
        el.classList.toggle('is-active', String(el.getAttribute('data-variant-swatch')) === String(id));
      });
      document.querySelectorAll('[data-variant-thumb]').forEach(function (el) {
        el.classList.toggle('is-active', String(el.getAttribute('data-variant-thumb')) === String(id));
      });
    }

    document.addEventListener('click', function (e) {
      var control = e.target.closest('[data-variant-swatch], [data-variant-thumb]');
      if (control) {
        var id = control.getAttribute('data-variant-swatch') || control.getAttribute('data-variant-thumb');
        selectVariant(id);
        return;
      }
      var mediaThumb = e.target.closest('[data-media-thumb]');
      if (mediaThumb && mainImg) {
        mainImg.style.backgroundImage = mediaThumb.style.backgroundImage;
        document.querySelectorAll('[data-media-thumb]').forEach(function (el) { el.classList.remove('is-active'); });
        mediaThumb.classList.add('is-active');
      }
    });

    if (qtyInput && idInput) {
      qtyInput.addEventListener('input', function () { selectVariant(idInput.value); });
      qtyInput.addEventListener('change', function () { selectVariant(idInput.value); });
    }
  }

  /* Cart page: quantity updates, line removal, coupon deep-link ---------------- */
  function initCartPage() {
    var form = document.querySelector('[data-cart-form]');
    if (!form) return;

    form.addEventListener('change', function (e) {
      if (e.target.matches('[data-qty-value]')) {
        form.submit();
      }
    });

    document.addEventListener('click', function (e) {
      var removeBtn = e.target.closest('[data-cart-remove]');
      if (removeBtn) {
        var key = removeBtn.getAttribute('data-cart-remove');
        var input = form.querySelector('[data-cart-line-key="' + key + '"]');
        if (input) {
          input.value = 0;
          form.submit();
        }
        return;
      }

      var applyBtn = e.target.closest('[data-coupon-apply]');
      if (applyBtn) {
        var codeInput = document.querySelector('[data-coupon-input]');
        var code = codeInput ? codeInput.value.trim() : '';
        if (code) {
          window.location.href = '/discount/' + encodeURIComponent(code.toUpperCase()) + '?redirect=' + encodeURIComponent('/cart');
        }
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initReveal();
    initSearch();
    initCartForms();
    initQtySteppers();
    initProductGallery();
    initCartPage();
  });
})();
