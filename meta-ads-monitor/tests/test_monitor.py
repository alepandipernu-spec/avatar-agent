import copy
import importlib
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def base_snapshot(run_id="2026-10-17T07:46-03:00"):
    m = lambda **k: {"spend": None, "impressions": None, "reach": None, "clicks": None, "link_clicks": None,
                     "landing_page_views": None, "adds_to_cart": None, "checkouts_initiated": None,
                     "purchases": None, "purchase_value": None, "video_plays": None, "thruplays": None} | k
    return {
        "run_id": run_id, "started_at": run_id, "currency": "USD",
        "period": {"current": {"start": "2026-09-18", "end": "2026-10-17"},
                   "previous": {"start": "2026-08-19", "end": "2026-09-17"}},
        "sources": {"escalafy": {"status": "ok"}, "meta_ad_library": {"status": "blocked"}},
        "objects": [{"level": "campaign", "id": "c1", "state": "paused"},
                    {"level": "ad", "id": "a1", "state": "paused"}, {"level": "ad", "id": "a2", "state": "paused"},
                    {"level": "ad", "id": "a3", "state": "paused"}],
        "ads": [
            {"id": "a1", "name": "AR video", "metrics": m(spend=20, impressions=4000, link_clicks=200, landing_page_views=160)},
            {"id": "a2", "name": "US video", "metrics": m(spend=60, impressions=400, link_clicks=40, landing_page_views=4)},
            {"id": "a3", "name": "CO img", "metrics": m(spend=10, impressions=3000, link_clicks=50, landing_page_views=40)},
        ],
        "totals": {"current": m(spend=90, impressions=7400, link_clicks=290, landing_page_views=204, purchases=0),
                   "previous": m(spend=80, impressions=7000, link_clicks=300, landing_page_views=0)},
        "store": {"current": {"sessions": 700, "sessions_with_cart": 10, "sessions_reached_checkout": 6,
                              "sessions_completed_checkout": 0, "orders": 0, "revenue": 0},
                  "previous": {"sessions": 900}},
        "daily": [{"date": f"2026-10-{d:02d}", "spend": (5 if d % 2 else 0)} for d in range(1, 16)],
        "economics": {"products": [{"name": "1 unidad", "price": 41.93, "unit_cost": 18.91, "compare_at": 59.9}]},
        "findings": [], "experiments": [], "competitors": [],
    }


class MonitorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["MONITOR_DATA"] = self.tmp.name
        sys.path.insert(0, str(SCRIPTS))
        import monitor
        self.m = importlib.reload(monitor)

    def tearDown(self):
        os.environ.pop("MONITOR_DATA", None)
        self.tmp.cleanup()

    def write(self, snap, name="snap.json"):
        p = Path(self.tmp.name) / name
        p.write_text(json.dumps(snap), encoding="utf-8")
        return p

    def run_quiet(self, path, force=False):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = self.m.run(path, force)
        return code, out.getvalue(), err.getvalue()

    def test_missing_metric_is_not_zero(self):
        self.assertIsNone(self.m.div(None, 10))
        self.assertIsNone(self.m.div(5, 0))
        self.assertEqual(self.m.fmt(None), "no disponible")

    def test_funnel_rates_use_previous_stage(self):
        rows, worst = self.m.funnel(base_snapshot())
        lpv = next(r for r in rows if r["stage"].startswith("Visitas"))
        self.assertAlmostEqual(lpv["rate_from_prev"], 204 / 290)
        self.assertTrue(worst["stage"].startswith("Compras"))  # 0/6 from checkout

    def test_rules_detect_known_problems(self):
        cfg = self.m.load_json(self.m.CONFIG)
        rules = {f["rule"]: f for f in self.m.rule_findings(base_snapshot(), cfg, None)}
        self.assertIn("spend_no_purchase", rules)
        self.assertIn("paused_intentionally", rules)  # config records the owner's decision
        self.assertEqual(rules["paused_intentionally"]["priority"], "P3")
        self.assertIn("low_lpv_ratio", rules)  # US: 40 clicks → 4 LPV
        self.assertIn("compare_at_price", rules)
        self.assertIn("intermittent_delivery", rules)

    def test_pause_rules(self):
        cfg = self.m.load_json(self.m.CONFIG)
        snap = base_snapshot()
        snap["daily"].append({"date": "2026-10-18", "spend": 4})
        rules = {f["rule"]: f for f in self.m.rule_findings(snap, cfg, None)}
        self.assertEqual(rules["spend_during_pause"]["priority"], "P1")
        self.assertNotIn("paused_intentionally", rules)
        cfg = copy.deepcopy(cfg)
        cfg.pop("campaigns_paused_intentionally")
        rules = {f["rule"]: f for f in self.m.rule_findings(base_snapshot(), cfg, None)}
        self.assertEqual(rules["no_active_campaigns"]["priority"], "P2")

    def test_run_writes_report_with_all_sections(self):
        code, out, err = self.run_quiet(self.write(base_snapshot()))
        self.assertEqual(code, 0, err)
        report = (Path(self.tmp.name) / "reports" / "LATEST.md").read_text(encoding="utf-8")
        for sec in "ABCDEFGHIJKL":
            self.assertIn(f"## {sec}.", report)
        self.assertIn("no disponible", report)

    def test_same_run_is_not_duplicated(self):
        p = self.write(base_snapshot())
        self.assertEqual(self.run_quiet(p)[0], 0)
        code, _, err = self.run_quiet(p)
        self.assertEqual(code, 3)
        self.assertIn("ya está registrada", err)
        self.assertEqual(self.run_quiet(p, force=True)[0], 0)
        runs = self.m.load_json(Path(self.tmp.name) / "state" / "runs.json")
        self.assertEqual(len(runs), 1)

    def test_repeated_alert_is_grouped_and_resolution_detected(self):
        self.run_quiet(self.write(base_snapshot()))
        second = base_snapshot("2026-10-17T15:46-03:00")
        second["economics"]["products"][0]["compare_at"] = None  # owner removed the strike-through price
        _, out, _ = self.run_quiet(self.write(second, "s2.json"))
        result = json.loads(out)
        self.assertEqual(result["notify"], [])  # nothing new
        self.assertTrue(any("Precio tachado" in t for t in result["resolved"]))
        alerts = self.m.load_json(Path(self.tmp.name) / "state" / "alerts.json")
        spend = next(a for a in alerts.values() if a["rule"] == "spend_no_purchase")
        self.assertEqual(spend["occurrences"], 2)

    def test_material_change_renotifies(self):
        self.run_quiet(self.write(base_snapshot()))
        second = base_snapshot("2026-10-17T15:46-03:00")
        second["totals"]["current"]["spend"] = 200
        _, out, _ = self.run_quiet(self.write(second, "s2.json"))
        self.assertTrue(any("cambio material" in t for t in json.loads(out)["notify"]))

    def test_experiment_history_is_kept(self):
        snap = base_snapshot()
        snap["experiments"] = [{"id": "EXP-001", "titulo": "Checkout", "estado": "propuesto"}]
        self.run_quiet(self.write(snap))
        second = base_snapshot("2026-10-17T15:46-03:00")
        second["experiments"] = [{"id": "EXP-001", "titulo": "Checkout", "estado": "aprobado"}]
        self.run_quiet(self.write(second, "s2.json"))
        exp = self.m.load_json(Path(self.tmp.name) / "state" / "experiments.json")["EXP-001"]
        self.assertEqual(exp["estado"], "aprobado")
        self.assertEqual(exp["history"][0]["before"], {"estado": "propuesto"})

    def test_analyst_finding_resolved_by_key(self):
        snap = base_snapshot()
        snap["findings"] = [{"key": "dup", "category": "anomalia", "priority": "P1", "title": "Duplicado",
                             "evidence": "e", "diagnosis": "d", "confidence": "alta", "impact": "i", "action": "a"}]
        self.run_quiet(self.write(snap))
        second = base_snapshot("2026-10-17T15:46-03:00")
        second["resolved_findings"] = ["dup"]
        _, out, _ = self.run_quiet(self.write(second, "s2.json"))
        self.assertIn("Duplicado", json.loads(out)["resolved"])

    def test_invalid_snapshot_writes_nothing(self):
        snap = base_snapshot()
        snap["ads"][0]["metrics"]["spend"] = "12"
        del snap["store"]
        code, _, err = self.run_quiet(self.write(snap))
        self.assertEqual(code, 2)
        self.assertFalse((Path(self.tmp.name) / "state" / "runs.json").exists())
        self.assertIn("store", err)

    def test_bad_metric_type_rejected(self):
        snap = base_snapshot()
        snap["ads"][0]["metrics"]["spend"] = "12"
        errors, _ = self.m.validate(snap)
        self.assertTrue(any("no es numérico" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
