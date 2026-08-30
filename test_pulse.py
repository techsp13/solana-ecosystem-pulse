# SPDX-License-Identifier: MIT
"""
Comprehensive Unit Test Suite for Solana Ecosystem Pulse.
Validates data collection, anomaly detection rules, and multi-format report rendering.
"""

import unittest
import os
from collector import SolanaDataCollector
from anomaly_detector import AnomalyDetector
from report_generator import ReportGenerator


class TestSolanaEcosystemPulse(unittest.TestCase):

    def setUp(self):
        self.collector = SolanaDataCollector()
        self.detector = AnomalyDetector()
        self.generator = ReportGenerator(output_dir="test_reports")

    def test_collector_network_performance(self):
        perf = self.collector.fetch_network_performance()
        self.assertIn("current_slot", perf)
        self.assertIn("current_tps", perf)
        self.assertIn("epoch", perf)
        self.assertGreater(perf["current_slot"], 0)
        self.assertGreater(perf["current_tps"], 0)
        self.assertGreaterEqual(perf["epoch_progress_pct"], 0.0)

    def test_collector_validator_health(self):
        vals = self.collector.fetch_validator_health()
        self.assertIn("active_validators", vals)
        self.assertIn("delinquent_validators", vals)
        self.assertIn("total_validators", vals)
        self.assertGreater(vals["active_validators"], 0)
        self.assertGreaterEqual(vals["nakamoto_coefficient"], 1)

    def test_collector_macro_and_defi(self):
        econ = self.collector.fetch_macro_and_defi()
        self.assertIn("sol_price_usd", econ)
        self.assertIn("defi_tvl_usd", econ)
        self.assertGreater(econ["sol_price_usd"], 0)
        self.assertGreater(econ["defi_tvl_usd"], 0)

    def test_anomaly_detector_nominal_status(self):
        telemetry = {
            "performance": {"current_tps": 2800.0, "average_tps": 2800.0, "estimated_slot_time_ms": 405},
            "validators": {"delinquency_rate_pct": 1.2, "delinquent_validators": 15},
            "economics": {"sol_price_24h_change_pct": 2.5},
        }
        anomalies = self.detector.analyze(telemetry)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]["severity"], "NORMAL")

    def test_anomaly_detector_tps_warning(self):
        telemetry = {
            "performance": {"current_tps": 1200.0, "average_tps": 2500.0, "estimated_slot_time_ms": 405},
            "validators": {"delinquency_rate_pct": 1.2, "delinquent_validators": 15},
            "economics": {"sol_price_24h_change_pct": 2.5},
        }
        anomalies = self.detector.analyze(telemetry)
        metrics = [a["metric"] for a in anomalies]
        self.assertIn("TPS Degradation", metrics)

    def test_anomaly_detector_delinquency_critical(self):
        telemetry = {
            "performance": {"current_tps": 2800.0, "average_tps": 2800.0, "estimated_slot_time_ms": 405},
            "validators": {"delinquency_rate_pct": 8.5, "delinquent_validators": 120},
            "economics": {"sol_price_24h_change_pct": 2.5},
        }
        anomalies = self.detector.analyze(telemetry)
        severities = [a["severity"] for a in anomalies]
        self.assertIn("CRITICAL", severities)

    def test_report_generator_exports(self):
        telemetry = self.collector.collect_all()
        anomalies = self.detector.analyze(telemetry)
        paths = self.generator.generate_all(telemetry, anomalies)

        self.assertTrue(os.path.exists(paths["json"]))
        self.assertTrue(os.path.exists(paths["markdown"]))
        self.assertTrue(os.path.exists(paths["html"]))

        # Check content presence
        with open(paths["markdown"], "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Solana Ecosystem Intelligence", content)
            self.assertIn("Core Network Performance", content)


if __name__ == "__main__":
    unittest.main()
