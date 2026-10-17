"""Flubberhome Meta Ads monitor: turns one run's snapshot into findings, alerts and a report.

    python monitor.py validate data/snapshots/<run_id>.json
    python monitor.py run <snapshot.json> [--force]

The snapshot is written by the agent from what the connectors returned (Escalafy, Shopify,
public web). This script never calls an ad platform: it only reads files and writes under
data/. A metric that was not obtained is null and stays "no disponible"; it is never 0.
"""
import argparse
import hashlib
import json
import os
import shutil
import statistics
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "monitor.json"
# Tests point MONITOR_DATA at a scratch directory so they never touch the real history.
DATA = Path(os.environ.get("MONITOR_DATA", ROOT / "data"))
STATE = DATA / "state"
PRIORITIES = ["P0", "P1", "P2", "P3"]
CATEGORIES = ["fortaleza", "debilidad", "anomalia", "oportunidad"]
EXPERIMENT_STATES = ["propuesto", "pendiente de aprobación", "aprobado", "en ejecución", "completado", "descartado"]
REQUIRED = ["run_id", "started_at", "currency", "period", "sources", "objects", "ads", "totals", "store"]


# ---------- helpers ----------

def load_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.replace(p)


def div(a, b):
    if a is None or b is None or b == 0:
        return None
    return a / b


def fmt(v, kind="num"):
    if v is None:
        return "no disponible"
    if kind == "usd":
        return f"USD {v:,.2f}"
    if kind == "pct":
        return f"{v * 100:.2f}%"
    if kind == "int":
        return f"{int(round(v)):,}"
    return f"{v:,.2f}"


def change(cur, prev):
    if cur is None or prev is None:
        return None
    if prev == 0:
        return None if cur == 0 else float("inf")
    return (cur - prev) / prev


def fmt_change(c):
    if c is None:
        return "sin comparación"
    if c == float("inf"):
        return "nuevo (antes 0)"
    return f"{'+' if c >= 0 else ''}{c * 100:.0f}%"


def safe_id(text):
    return "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in text)


# ---------- validation ----------

def validate(snap):
    """Returns (errors, warnings). Errors stop the run; warnings go to the report."""
    errors, warnings = [], []
    for key in REQUIRED:
        if key not in snap:
            errors.append(f"falta el campo obligatorio '{key}'")
    if errors:
        return errors, warnings
    for name in ("current", "previous"):
        per = snap["period"].get(name)
        if not per or not per.get("start") or not per.get("end"):
            errors.append(f"period.{name} incompleto")
    if snap["currency"] != "USD":
        warnings.append(f"moneda del snapshot {snap['currency']}: los umbrales están en USD")
    for name, src in snap["sources"].items():
        if src.get("status") not in ("ok", "partial", "failed", "blocked", "not_configured"):
            errors.append(f"sources.{name}.status inválido: {src.get('status')}")
    for i, ad in enumerate(snap["ads"]):
        if "id" not in ad:
            errors.append(f"ads[{i}] sin id")
        for k, v in ad.get("metrics", {}).items():
            if v is not None and not isinstance(v, (int, float)):
                errors.append(f"ads[{i}].metrics.{k} no es numérico: {v!r}")
            elif isinstance(v, (int, float)) and v < 0:
                errors.append(f"ads[{i}].metrics.{k} negativo")
    for f in snap.get("findings", []):
        if f.get("priority") not in PRIORITIES:
            errors.append(f"hallazgo '{f.get('title')}' con prioridad inválida")
        if f.get("category") not in CATEGORIES:
            errors.append(f"hallazgo '{f.get('title')}' con categoría inválida")
    for e in snap.get("experiments", []):
        if e.get("estado", "propuesto") not in EXPERIMENT_STATES:
            errors.append(f"experimento {e.get('id')} con estado inválido")
    ids = [a["id"] for a in snap["ads"] if "id" in a]
    if len(ids) != len(set(ids)):
        errors.append("ads con ids duplicados")
    lag_end = snap["period"]["current"]["end"]
    warnings.append(f"los últimos días hasta {lag_end} todavía pueden cambiar (pedidos tardíos, reexpresión de Meta)")
    return errors, warnings


# ---------- analysis ----------

def funnel(snap):
    t = snap["totals"]["current"]
    s = snap["store"]["current"]
    stages = [
        ("Impresiones (Meta)", t.get("impressions")),
        ("Clics en enlace (Meta)", t.get("link_clicks")),
        ("Visitas a la página de destino (Meta)", t.get("landing_page_views")),
        ("Sesiones de la tienda (Shopify, todas las fuentes)", s.get("sessions")),
        ("Sesiones con agregado al carrito (Shopify)", s.get("sessions_with_cart")),
        ("Sesiones que llegaron al checkout (Shopify)", s.get("sessions_reached_checkout")),
        ("Compras (Shopify)", s.get("orders")),
    ]
    rows, worst = [], None
    for i, (name, val) in enumerate(stages):
        rate = div(val, stages[i - 1][1]) if i else None
        rows.append({"stage": name, "value": val, "rate_from_prev": rate})
        # Shopify sessions include organic traffic, so the LPV→sessions step is not a drop-off.
        if i >= 2 and rate is not None and i != 3 and (worst is None or rate < worst["rate_from_prev"]):
            worst = rows[-1] | {"from": stages[i - 1][0]}
    return rows, worst


def economics(snap, cfg):
    econ = cfg["economics"]
    out = []
    for p in snap.get("economics", {}).get("products", []):
        price, cost = p.get("price"), p.get("unit_cost")
        gross = None if price is None or cost is None else price - cost
        known = gross
        missing = [k for k in ("shipping_cost_per_order_usd", "payment_fee_pct", "tax_pct") if econ.get(k) is None]
        if known is not None:
            if econ.get("shipping_cost_per_order_usd") is not None and p.get("free_shipping"):
                known -= econ["shipping_cost_per_order_usd"]
            for k in ("payment_fee_pct", "tax_pct"):
                if econ.get(k) is not None:
                    known -= price * econ[k]
        # Scenario: 10% fees+taxes and USD 8 shipping when the store pays it. Labelled as estimate.
        est = None
        if gross is not None:
            est = gross - price * 0.10 - (8 if p.get("free_shipping") else 0)
        out.append({
            "name": p.get("name"), "price": price, "unit_cost": cost, "compare_at": p.get("compare_at"),
            "gross_margin": gross, "max_cpa_known_costs": known, "max_cpa_scenario": est,
            "breakeven_roas_scenario": div(price, est) if est and est > 0 else None,
            "missing_costs": missing,
        })
    return out


def rule_findings(snap, cfg, prev_snap):
    """Deterministic checks. Each returns an alert with a stable fingerprint."""
    th = cfg["thresholds"]
    t = snap["totals"]["current"]
    found = []

    def add(key, obj, priority, category, title, evidence, diagnosis, confidence, impact, action, approval, value=None):
        found.append({
            "fingerprint": hashlib.sha1(f"{key}|{obj}".encode()).hexdigest()[:12],
            "rule": key, "object": obj, "priority": priority, "category": category, "title": title,
            "evidence": evidence, "diagnosis": diagnosis, "confidence": confidence, "impact": impact,
            "action": action, "needs_approval": approval, "value": value, "source": "regla",
        })

    spend, purchases, orders = t.get("spend"), t.get("purchases"), snap["store"]["current"].get("orders")
    if spend is not None and spend >= th["spend_without_purchase_usd"] and (orders == 0) and (purchases in (0, None)):
        add("spend_no_purchase", "account", "P1", "debilidad",
            f"{fmt(spend, 'usd')} gastados en el período sin compras",
            f"Gasto Meta {fmt(spend, 'usd')}; compras Shopify {orders}; compras atribuidas por Meta {fmt(purchases, 'int')}.",
            "El embudo no llega a compra. No alcanza para culpar al anuncio: también pueden fallar oferta, precio, confianza o checkout.",
            "media", "Gasto sin retorno verificable.",
            "Antes de reactivar gasto, probar el checkout de punta a punta y revisar la oferta (ver experimentos).",
            False, spend)

    objs = snap["objects"]
    campaigns = [o for o in objs if o.get("level") == "campaign"]
    if campaigns and not any(o.get("state") == "active" for o in campaigns):
        last = max((d["date"] for d in snap.get("daily", []) if (d.get("spend") or 0) > 0), default=None)
        add("no_active_campaigns", "account", "P2", "anomalia",
            "No hay campañas activas en la cuenta",
            f"{len(campaigns)} campañas, todas en estado pausado. Último día con gasto: {last or 'sin gasto en el período'}.",
            "Sin entrega no hay datos nuevos. Si la pausa fue intencional (decisión del dueño), no es un problema.",
            "alta", "Cero aprendizaje mientras siga así.",
            "Confirmar si la pausa es intencional. Reactivar solo con un experimento aprobado.", True, len(campaigns))

    known_ids = {o["id"] for o in objs}
    orphan_spend = sum((a["metrics"].get("spend") or 0) for a in snap["ads"] if a["id"] not in known_ids)
    if orphan_spend > 0:
        n = sum(1 for a in snap["ads"] if a["id"] not in known_ids)
        add("orphan_objects", "account", "P2", "anomalia",
            f"{n} anuncios con gasto que no figuran en el catálogo actual",
            f"Gasto en anuncios sin nombre ni estado: {fmt(orphan_spend, 'usd')}.",
            "Probablemente anuncios o campañas borrados, o de otra cuenta conectada. Sus datos no se pueden auditar a fondo.",
            "media", "Parte del historial no es interpretable.",
            "Identificar en Ads Manager las campañas con esos IDs (ver anexo).", False, round(orphan_spend, 2))

    for a in snap["ads"]:
        m = a["metrics"]
        lc, lpv = m.get("link_clicks"), m.get("landing_page_views")
        ratio = div(lpv, lc)
        if lc and lc >= th["min_link_clicks_for_ratio"] and ratio is not None and ratio < th["lpv_per_link_click_min"]:
            add("low_lpv_ratio", a["id"], "P1" if ratio == 0 else "P2", "anomalia",
                f"'{a.get('name', a['id'])}': clics que no llegan a la tienda",
                f"{fmt(lc, 'int')} clics en enlace → {fmt(lpv, 'int')} visitas a la página ({fmt(ratio, 'pct')}).",
                "Clics accidentales, destino que no carga, o el Pixel no dispara en esa página.",
                "media", "Se paga tráfico que no se puede medir o no existe.",
                "Revisar URL de destino y evento PageView de ese anuncio.", False, ratio)

    cpms = [(a, div(a["metrics"].get("spend"), a["metrics"].get("impressions"))) for a in snap["ads"]
            if (a["metrics"].get("impressions") or 0) >= th["min_impressions_for_cpm"]]
    cpms = [(a, c * 1000) for a, c in cpms if c is not None]
    if len(cpms) >= 3:
        med = statistics.median(c for _, c in cpms)
        for a, c in cpms:
            if c > med * th["cpm_outlier_multiplier"]:
                add("cpm_outlier", a["id"], "P2", "debilidad",
                    f"'{a.get('name', a['id'])}': CPM {c / med:.0f}× la mediana",
                    f"CPM {fmt(c, 'usd')} vs mediana {fmt(med, 'usd')}.",
                    "Audiencia o mercado caro (p. ej. US) o entrega con poca competencia por presupuesto bajo.",
                    "media", "Cada visita cuesta mucho más.",
                    "Comparar costo por visita de ese mercado antes de volver a asignarle presupuesto.", True, c)

    days = [d for d in snap.get("daily", []) if d.get("spend") is not None]
    active = [d for d in days if d["spend"] > 0]
    if len(days) >= 7 and active:
        gaps = sum(1 for i in range(1, len(days)) if (days[i]["spend"] > 0) != (days[i - 1]["spend"] > 0))
        if gaps >= 6:
            add("intermittent_delivery", "account", "P2", "anomalia",
                "Entrega intermitente: el gasto se prende y se apaga",
                f"{len(active)} de {len(days)} días con gasto; {gaps} cortes en el período.",
                "Pausas manuales frecuentes, límite de gasto alcanzado o pagos rechazados. Cada corte reinicia el aprendizaje.",
                "media", "Los resultados no son comparables entre días y Meta no sale de aprendizaje.",
                "Revisar el historial de actividad y Facturación en Ads Manager.", False, gaps)
        med_spend = statistics.median(d["spend"] for d in active)
        last = days[-1]
        if last["spend"] > med_spend * th["daily_spend_spike_multiplier"]:
            limit = cfg["approved_spend"]["daily_limit_usd"]
            prio = "P0" if limit is not None and last["spend"] > limit else "P1"
            add("daily_spend_spike", last["date"], prio, "anomalia",
                f"Gasto del {last['date']} muy por encima de lo habitual",
                f"{fmt(last['spend'], 'usd')} vs mediana {fmt(med_spend, 'usd')}.",
                "Cambio de presupuesto o campaña nueva.", "alta", "Gasto no previsto.",
                "Verificar cambios recientes en Ads Manager.", True, last["spend"])

    atc_meta, atc_shop = t.get("adds_to_cart"), snap["store"]["current"].get("sessions_with_cart")
    if atc_meta and atc_shop and atc_meta > atc_shop * th["pixel_vs_shopify_atc_ratio_max"]:
        add("atc_mismatch", "account", "P1", "anomalia", "Meta cuenta muchos más carritos que Shopify",
            f"ATC Meta {atc_meta} vs sesiones con carrito Shopify {atc_shop}.",
            "Posible doble Pixel o evento duplicado.", "media", "Optimización con señal inflada.",
            "Revisar Shopify → Configuración → Eventos del cliente.", True, atc_meta)

    for p in snap.get("economics", {}).get("products", []):
        if p.get("compare_at") and p.get("price") and p["compare_at"] > p["price"]:
            add("compare_at_price", p.get("name"), "P2", "debilidad",
                f"Precio tachado en '{p.get('name')}' sin precio anterior verificable",
                f"Precio {fmt(p['price'], 'usd')}, 'antes' {fmt(p['compare_at'], 'usd')}, con 0 ventas registradas.",
                "Un precio de referencia que nunca se cobró puede leerse como engañoso y contradice la regla de la marca (sin precio tachado).",
                "alta", "Riesgo de confianza y de rechazo de anuncios.",
                "Decidir si se quita el compare-at price en Shopify.", True, p["compare_at"])
    for p in snap.get("store", {}).get("risky_titles", []):
        add("risky_claim", p, "P3", "debilidad", f"Afirmación sin respaldo en el catálogo: '{p}'",
            "Título con \"Más elegido\" sin ventas registradas (producto en borrador).", "Afirmación no verificable.", "alta",
            "Riesgo de confianza si se publica.", "Renombrar antes de publicar ese producto.", True)

    if prev_snap:
        for key, label in (("spend", "gasto"), ("link_clicks", "clics en enlace"), ("landing_page_views", "visitas")):
            c = change(t.get(key), prev_snap["totals"]["current"].get(key))
            if c is not None and c != float("inf") and abs(c) >= 0.5 and (t.get(key) or 0) >= 10:
                add(f"swing_{key}", "account", "P2", "anomalia", f"Cambio fuerte de {label} desde la ejecución anterior",
                    f"{fmt(prev_snap['totals']['current'].get(key))} → {fmt(t.get(key))} ({fmt_change(c)}).",
                    "Puede ser solo el corrimiento de la ventana de fechas.", "baja", "A vigilar.",
                    "Confirmar con los datos diarios.", False, c)
    return found


# ---------- state ----------

def update_alerts(found, run_id, th):
    """Groups repeated alerts by fingerprint. Marks what is new, escalated, changed or resolved."""
    path = STATE / "alerts.json"
    alerts = load_json(path, {})
    seen = set()
    notify = []
    for f in found:
        fp = f["fingerprint"]
        seen.add(fp)
        old = alerts.get(fp)
        if old is None or old["status"] == "resuelta":
            f.update(first_seen=run_id, occurrences=1, status="abierta", delta="nueva" if old is None else "reabierta")
            notify.append(f)
        else:
            f.update(first_seen=old["first_seen"], occurrences=old["occurrences"] + 1, status="abierta")
            if PRIORITIES.index(f["priority"]) < PRIORITIES.index(old["priority"]):
                f["delta"] = f"escalada {old['priority']}→{f['priority']}"
                notify.append(f)
            elif isinstance(f.get("value"), (int, float)) and isinstance(old.get("value"), (int, float)) and \
                    old["value"] and abs(f["value"] - old["value"]) / abs(old["value"]) >= th["material_change_pct"]:
                f["delta"] = "cambio material"
                notify.append(f)
            else:
                f["delta"] = "ya conocida"
        f["last_seen"] = run_id
        alerts[fp] = {k: v for k, v in f.items() if k != "delta"}
    resolved = []
    for fp, a in alerts.items():
        if fp not in seen and a["status"] == "abierta" and a.get("source") == "regla":
            a.update(status="resuelta", resolved_at=run_id)
            resolved.append(a)
    save_json(path, alerts)
    return notify, resolved


def merge_registry(name, items, key, run_id):
    """Upserts by key without losing history: changed fields are appended to `history`."""
    path = STATE / f"{name}.json"
    reg = load_json(path, {})
    created, changed = [], []
    for it in items:
        k = it[key]
        old = reg.get(k)
        if old is None:
            reg[k] = it | {"created": run_id, "updated": run_id, "history": []}
            created.append(k)
            continue
        diff = {f: old.get(f) for f, v in it.items() if old.get(f) != v}
        if diff:
            old.setdefault("history", []).append({"run": run_id, "before": diff})
            old.update(it, updated=run_id)
            changed.append(k)
    save_json(path, reg)
    return reg, created, changed


# ---------- report ----------

def render(snap, cfg, ctx):
    t, p = snap["totals"]["current"], snap["totals"].get("previous", {})
    L = []
    w = L.append
    per = snap["period"]
    w(f"# Flubberhome · Meta Ads Monitor · {snap['run_id']}\n")
    w(f"Período: {per['current']['start']} → {per['current']['end']} · comparado con {per['previous']['start']} → {per['previous']['end']} · "
      f"moneda {snap['currency']} · zona {cfg['timezone']} · modo {cfg['mode']}\n")

    alerts = sorted(ctx["alerts"], key=lambda a: PRIORITIES.index(a["priority"]))
    w("## A. Resumen ejecutivo\n")
    for line in snap.get("summary", []):
        w(f"- {line}")
    top = [a for a in alerts if a["priority"] in ("P0", "P1")]
    w(f"- Alertas abiertas: {len(alerts)} ({len(top)} P0/P1). Nuevas o con cambio en esta ejecución: {len(ctx['notify'])}. Resueltas: {len(ctx['resolved'])}.")
    w("")

    w("## B. Estado técnico\n")
    w("| Fuente | Estado | Detalle |\n| --- | --- | --- |")
    for name, s in snap["sources"].items():
        w(f"| {name} | {s['status']} | {s.get('detail', '')} |")
    w("")
    for x in ctx["warnings"] + snap.get("data_quality", []):
        w(f"- {x}")
    if snap.get("unavailable_metrics"):
        w(f"- Métricas no disponibles en esta ejecución: {', '.join(snap['unavailable_metrics'])}.")
    w("")

    w("## C. Rendimiento publicitario\n")
    w("| Métrica | Actual | Anterior | Cambio |\n| --- | --- | --- | --- |")
    spend, imp, lc, lpv = t.get("spend"), t.get("impressions"), t.get("link_clicks"), t.get("landing_page_views")
    derived = {
        "CPM": (div(spend, imp) and div(spend, imp) * 1000, div(p.get("spend"), p.get("impressions")) and div(p.get("spend"), p.get("impressions")) * 1000, "usd"),
        "CTR de enlace": (div(lc, imp), div(p.get("link_clicks"), p.get("impressions")), "pct"),
        "CTR total (todos los clics)": (div(t.get("clicks"), imp), div(p.get("clicks"), p.get("impressions")), "pct"),
        "CPC de enlace": (div(spend, lc), div(p.get("spend"), p.get("link_clicks")), "usd"),
        "Costo por visita a la página": (div(spend, lpv), div(p.get("spend"), p.get("landing_page_views")), "usd"),
        "Frecuencia": (div(imp, t.get("reach")), div(p.get("impressions"), p.get("reach")), "num"),
        "CPA (compras Meta)": (div(spend, t.get("purchases")), div(p.get("spend"), p.get("purchases")), "usd"),
        "ROAS atribuido": (div(t.get("purchase_value"), spend), div(p.get("purchase_value"), p.get("spend")), "num"),
    }
    base = [("Gasto", "spend", "usd"), ("Impresiones", "impressions", "int"), ("Alcance (suma diaria)", "reach", "int"),
            ("Clics (todos)", "clicks", "int"), ("Clics en enlace", "link_clicks", "int"),
            ("Visitas a la página", "landing_page_views", "int"), ("Reproducciones 3 s", "video_plays", "int"),
            ("ThruPlays", "thruplays", "int"), ("Agregados al carrito (Meta)", "adds_to_cart", "int"),
            ("Inicios de pago (Meta)", "checkouts_initiated", "int"), ("Compras atribuidas (Meta)", "purchases", "int"),
            ("Valor de compras (Meta)", "purchase_value", "usd")]
    for label, k, kind in base:
        w(f"| {label} | {fmt(t.get(k), kind)} | {fmt(p.get(k), kind)} | {fmt_change(change(t.get(k), p.get(k)))} |")
    for label, (c, pv, kind) in derived.items():
        w(f"| {label} | {fmt(c, kind)} | {fmt(pv, kind)} | {fmt_change(change(c, pv))} |")
    w("\nPor anuncio (ordenado por gasto):\n")
    w("| Anuncio | Estado | Gasto | Impr. | CPM | CTR enlace | Clics enlace | LPV | LPV/clic | Costo/LPV |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for a in sorted(snap["ads"], key=lambda a: -(a["metrics"].get("spend") or 0)):
        m = a["metrics"]
        cpm = div(m.get("spend"), m.get("impressions"))
        w(f"| {a.get('name', a['id'])} | {a.get('state', '?')} | {fmt(m.get('spend'), 'usd')} | {fmt(m.get('impressions'), 'int')} | "
          f"{fmt(cpm and cpm * 1000, 'usd')} | {fmt(div(m.get('link_clicks'), m.get('impressions')), 'pct')} | {fmt(m.get('link_clicks'), 'int')} | "
          f"{fmt(m.get('landing_page_views'), 'int')} | {fmt(div(m.get('landing_page_views'), m.get('link_clicks')), 'pct')} | "
          f"{fmt(div(m.get('spend'), m.get('landing_page_views')), 'usd')} |")
    w("")

    w("## D. Análisis del embudo\n")
    w("| Etapa | Volumen | Tasa desde la etapa anterior |\n| --- | --- | --- |")
    for r in ctx["funnel"]:
        w(f"| {r['stage']} | {fmt(r['value'], 'int')} | {fmt(r['rate_from_prev'], 'pct')} |")
    if ctx["worst"]:
        wst = ctx["worst"]
        w(f"\nMayor punto de fuga medible: **{wst['from']} → {wst['stage']}** ({fmt(wst['rate_from_prev'], 'pct')}).")
    w("\nNota: las sesiones de Shopify incluyen tráfico orgánico y directo; el paso Meta → Shopify no es una tasa de conversión.")
    for line in snap.get("funnel_notes", []):
        w(f"- {line}")
    w("")

    w("## E. Fortalezas y debilidades\n")
    findings = snap.get("findings", []) + ctx["rule_findings"]
    for cat in CATEGORIES:
        items = [f for f in findings if f["category"] == cat]
        w(f"**{cat.upper()}**\n")
        if not items:
            w("- Sin hallazgos con evidencia suficiente en esta ejecución.")
        for f in sorted(items, key=lambda f: PRIORITIES.index(f["priority"])):
            w(f"- [{f['priority']}] {f['title']} — Evidencia: {f['evidence']} Diagnóstico: {f['diagnosis']} "
              f"Confianza: {f['confidence']}. Acción: {f['action']}{' (requiere aprobación)' if f.get('needs_approval') else ''}")
        w("")

    w("## F. Inteligencia competitiva\n")
    comps = snap.get("competitors", [])
    if not comps:
        w("- No se examinaron competidores en esta ejecución.")
    for c in comps:
        tag = " (nuevo)" if c["id"] in ctx["comp_created"] else (" (cambió)" if c["id"] in ctx["comp_changed"] else "")
        w(f"**{c['name']}**{tag} · {c.get('domain', '')} · mercado {c.get('market', '?')} · verificado {c.get('verified_at', '?')}")
        for k, label in (("price", "Precio/oferta"), ("value_prop", "Propuesta"), ("claims", "Mensajes"), ("formats", "Formatos")):
            if c.get(k):
                w(f"- {label}: {c[k]}")
        for k, label in (("facts", "Hecho observado"), ("inferences", "Inferencia"), ("hypotheses", "Hipótesis"), ("unknowns", "No obtenible")):
            for x in c.get(k, []):
                w(f"- {label}: {x}")
        w(f"- Fuentes: {', '.join(c.get('sources', []))}\n")
    for x in snap.get("competitive_patterns", []):
        w(f"- Patrón: {x}")
    w("")

    w("## G. Plan de mejora\n")
    w("| # | Acción | Impacto | Confianza | Urgencia | Costo | Dificultad | Aprobación |\n| --- | --- | --- | --- | --- | --- | --- | --- |")
    for i, a in enumerate(snap.get("plan", []), 1):
        w(f"| {i} | {a['action']} | {a['impact']} | {a['confidence']} | {a['urgency']} | {a['cost']} | {a['difficulty']} | {'sí' if a.get('needs_approval') else 'no'} |")
    w("")

    w("## H. Experimentos\n")
    exps = ctx["experiments"]
    for e in sorted(exps.values(), key=lambda e: e.get("prioridad", "P9")):
        tag = " (nuevo)" if e["id"] in ctx["exp_created"] else (" (actualizado)" if e["id"] in ctx["exp_changed"] else "")
        w(f"**{e['id']} · {e['titulo']}**{tag} — estado: {e.get('estado', 'propuesto')} · prioridad {e.get('prioridad', '?')}")
        for k, label in (("problema", "Problema"), ("evidencia", "Evidencia"), ("hipotesis", "Hipótesis"), ("variable", "Variable"),
                         ("constantes", "Constantes"), ("metrica_principal", "Métrica principal"), ("metricas_secundarias", "Protección"),
                         ("presupuesto_max_usd", "Presupuesto máximo (sujeto a aprobación)"), ("duracion", "Duración"),
                         ("exito", "Éxito"), ("fracaso", "Fracaso"), ("inconcluso", "Inconcluso"), ("riesgos", "Riesgos"),
                         ("concepto", "Concepto creativo"), ("gancho", "Gancho"), ("guion", "Guion"),
                         ("texto_principal", "Texto principal"), ("titular", "Titular"), ("cta", "Llamada a la acción"),
                         ("formato", "Formato")):
            if e.get(k) not in (None, "", []):
                w(f"- {label}: {e[k]}")
        w("")

    w("## I. Rentabilidad\n")
    w("| Producto | Precio | Costo unitario | Margen bruto | CPA máx. (costos conocidos) | CPA máx. (escenario) | ROAS de equilibrio (escenario) |\n| --- | --- | --- | --- | --- | --- | --- |")
    for e in ctx["econ"]:
        w(f"| {e['name']} | {fmt(e['price'], 'usd')} | {fmt(e['unit_cost'], 'usd')} | {fmt(e['gross_margin'], 'usd')} | "
          f"{fmt(e['max_cpa_known_costs'], 'usd')} | {fmt(e['max_cpa_scenario'], 'usd')} | {fmt(e['breakeven_roas_scenario'])} |")
    missing = sorted({m for e in ctx["econ"] for m in e["missing_costs"]})
    w(f"\n- Escenario = ESTIMACIÓN: 10% de comisiones e impuestos sobre el precio y USD 8 de envío cuando el envío es gratis. No es un dato.")
    if missing:
        w(f"- Costos faltantes (no documentados): {', '.join(missing)}. Ninguna conclusión de rentabilidad es definitiva.")
    w(f"- Ventas verificadas Shopify en el período: {fmt(snap['store']['current'].get('orders'), 'int')} pedidos, {fmt(snap['store']['current'].get('revenue'), 'usd')}. "
      f"Ingresos atribuidos por Meta: {fmt(t.get('purchase_value'), 'usd')}.")
    w("")

    w("## J. Alertas\n")
    if not alerts:
        w("- Sin alertas abiertas.")
    for a in alerts:
        w(f"- **[{a['priority']}] {a['title']}** · {a.get('delta', '')} · detectada {a['first_seen']} · veces: {a['occurrences']} · "
          f"confianza {a['confidence']} · impacto: {a['impact']} · acción: {a['action']}{' · requiere aprobación' if a.get('needs_approval') else ''}")
    for a in ctx["resolved"]:
        w(f"- RESUELTA: {a['title']} (abierta desde {a['first_seen']})")
    w("")

    w("## K. Decisiones pendientes (requieren aprobación expresa)\n")
    pend = snap.get("pending_decisions", [])
    for i, d in enumerate(pend, 1):
        w(f"{i}. {d}")
    if not pend:
        w("- Ninguna.")
    w("")

    w("## L. Estado de la ejecución\n")
    st = snap.get("execution", {})
    w(f"- Inicio: {snap['started_at']} · Fin del análisis: {ctx['finished_at']}")
    for k, label in (("completed", "Completado"), ("partial", "Parcial"), ("failed", "Falló")):
        for x in st.get(k, []):
            w(f"- {label}: {x}")
    w(f"- Próxima ejecución programada: {st.get('next_run', 'no verificada')}")
    w(f"- Snapshot: data/snapshots/{safe_id(snap['run_id'])}.json")
    return "\n".join(L) + "\n"


# ---------- commands ----------

def run(snapshot_path, force=False):
    cfg = load_json(CONFIG)
    snap = load_json(snapshot_path)
    if snap is None:
        print(f"ERROR: no existe {snapshot_path}", file=sys.stderr)
        return 2
    errors, warnings = validate(snap)
    if errors:
        print("ERROR: snapshot inválido, no se escribió nada:\n- " + "\n- ".join(errors), file=sys.stderr)
        return 2

    run_id = snap["run_id"]
    runs = load_json(STATE / "runs.json", [])
    if any(r["run_id"] == run_id for r in runs) and not force:
        print(f"ERROR: la ejecución {run_id} ya está registrada. Usá --force para reemplazarla (no se duplica).", file=sys.stderr)
        return 3
    runs = [r for r in runs if r["run_id"] != run_id]
    prev_run = runs[-1] if runs else None
    prev_snap = load_json(DATA / "snapshots" / f"{safe_id(prev_run['run_id'])}.json") if prev_run else None

    rule = rule_findings(snap, cfg, prev_snap)
    notify, resolved = update_alerts(rule + [f | {"fingerprint": hashlib.sha1(f"agent|{f.get('key', f['title'])}".encode()).hexdigest()[:12],
                                                 "source": "analista", "rule": "analista", "object": ""}
                                             for f in snap.get("findings", []) if f["priority"] in ("P0", "P1", "P2")],
                                     run_id, cfg["thresholds"])
    open_alerts = [a for a in load_json(STATE / "alerts.json", {}).values() if a["status"] == "abierta"]
    deltas = {a["fingerprint"]: a.get("delta") for a in notify}
    for a in open_alerts:
        a["delta"] = deltas.get(a["fingerprint"], "ya conocida")

    exps, exp_created, exp_changed = merge_registry("experiments", snap.get("experiments", []), "id", run_id)
    _, comp_created, comp_changed = merge_registry("competitors", snap.get("competitors", []), "id", run_id)
    fun, worst = funnel(snap)
    finished = datetime.now(ZoneInfo(cfg["timezone"])).isoformat(timespec="seconds")
    ctx = {"alerts": open_alerts, "notify": notify, "resolved": resolved, "rule_findings": rule, "warnings": warnings,
           "funnel": fun, "worst": worst, "econ": economics(snap, cfg), "experiments": exps,
           "exp_created": exp_created, "exp_changed": exp_changed, "comp_created": comp_created,
           "comp_changed": comp_changed, "finished_at": finished}
    report = render(snap, cfg, ctx)

    sid = safe_id(run_id)
    for d in ("snapshots", "reports"):
        (DATA / d).mkdir(parents=True, exist_ok=True)
    dest = DATA / "snapshots" / f"{sid}.json"
    if Path(snapshot_path).resolve() != dest.resolve():
        shutil.copyfile(snapshot_path, dest)
    rpath = DATA / "reports" / f"{sid}.md"
    rpath.write_text(report, encoding="utf-8")
    (DATA / "reports" / "LATEST.md").write_text(report, encoding="utf-8")
    runs.append({"run_id": run_id, "started_at": snap["started_at"], "finished_at": finished,
                 "report": rpath.name, "alerts_open": len(open_alerts),
                 "alerts_notify": [f"[{a['priority']}] {a['title']} ({a['delta']})" for a in notify],
                 "resolved": [a["title"] for a in resolved],
                 "sources": {k: v["status"] for k, v in snap["sources"].items()}})
    save_json(STATE / "runs.json", runs)

    # Verify what we wrote can be read back before claiming success.
    assert rpath.read_text(encoding="utf-8") == report
    assert load_json(STATE / "runs.json")[-1]["run_id"] == run_id
    print(json.dumps({"report": str(rpath), "alerts_open": len(open_alerts),
                      "notify": runs[-1]["alerts_notify"], "resolved": runs[-1]["resolved"]}, ensure_ascii=False, indent=2))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["validate", "run"])
    ap.add_argument("snapshot")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.command == "validate":
        snap = load_json(a.snapshot)
        if snap is None:
            print(f"ERROR: no existe {a.snapshot}", file=sys.stderr)
            sys.exit(2)
        errors, warnings = validate(snap)
        print(json.dumps({"errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
        sys.exit(2 if errors else 0)
    sys.exit(run(a.snapshot, a.force))


if __name__ == "__main__":
    main()
