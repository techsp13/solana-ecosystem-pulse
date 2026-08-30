# SPDX-License-Identifier: MIT
"""
Automated Anomaly Detection Engine for Solana Network Health.
Evaluates network throughput, slot timing, consensus delinquency, and macro volatility.
"""

from typing import Dict, Any, List


class AnomalyDetector:
    """Evaluates telemetry snapshots and flags statistical anomalies."""

    def __init__(self):
        self.tps_min_threshold = 1800.0
        self.slot_time_max_ms = 500.0
        self.delinquency_max_pct = 3.0
        self.price_volatility_max_pct = 10.0

    def analyze(self, telemetry: Dict[str, Any]) -> List[Dict[str, Any]]:
        anomalies: List[Dict[str, Any]] = []

        perf = telemetry.get("performance", {})
        vals = telemetry.get("validators", {})
        econ = telemetry.get("economics", {})

        # 1. Throughput & TPS Health Check
        current_tps = perf.get("current_tps", 2500.0)
        avg_tps = perf.get("average_tps", 2500.0)
        
        if current_tps < self.tps_min_threshold:
            anomalies.append({
                "metric": "TPS Degradation",
                "severity": "WARNING",
                "value": f"{current_tps} TPS",
                "threshold": f"< {self.tps_min_threshold} TPS",
                "message": "Throughput below standard baseline. Possible block producer congestion or network slowdown.",
            })

        # 2. Slot Time Latency Check
        slot_time = perf.get("estimated_slot_time_ms", 408)
        if slot_time > self.slot_time_max_ms:
            anomalies.append({
                "metric": "Slow Slot Execution",
                "severity": "WARNING",
                "value": f"{slot_time} ms",
                "threshold": f"> {self.slot_time_max_ms} ms",
                "message": "Block generation time exceeds 500ms target threshold.",
            })

        # 3. Validator Delinquency & Consensus Risk
        delinquency_pct = vals.get("delinquency_rate_pct", 0.0)
        if delinquency_pct > self.delinquency_max_pct:
            anomalies.append({
                "metric": "Validator Delinquency Spike",
                "severity": "CRITICAL" if delinquency_pct > 6.0 else "WARNING",
                "value": f"{delinquency_pct}%",
                "threshold": f"> {self.delinquency_max_pct}%",
                "message": f"Elevated delinquent validator count ({vals.get('delinquent_validators')} offline nodes).",
            })

        # 4. Economic Volatility Check
        price_change = abs(econ.get("sol_price_24h_change_pct", 0.0))
        if price_change > self.price_volatility_max_pct:
            anomalies.append({
                "metric": "High SOL Volatility",
                "severity": "INFO",
                "value": f"{price_change}%",
                "threshold": f"> {self.price_volatility_max_pct}%",
                "message": "Significant price movement in the past 24 hours.",
            })

        if not anomalies:
            anomalies.append({
                "metric": "Network Status",
                "severity": "NORMAL",
                "value": "OPTIMAL",
                "threshold": "All green",
                "message": "All network health, throughput, and consensus metrics operating within nominal boundaries.",
            })

        return anomalies
