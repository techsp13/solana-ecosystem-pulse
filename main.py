# SPDX-License-Identifier: MIT
"""
Main Execution CLI for Solana Ecosystem Pulse.
Runs full telemetry collection, anomaly detection, and report generation pipeline.
"""

import sys
import os
from collector import SolanaDataCollector
from anomaly_detector import AnomalyDetector
from report_generator import ReportGenerator

sys.stdout.reconfigure(encoding="utf-8")


def main():
    print("==================================================================")
    print("  SOLANA ECOSYSTEM PULSE — v1.0.0 (Superteam Bounty Submission)")
    print("==================================================================")

    # 1. Collect Telemetry
    print("[1/3] Querying Solana Mainnet-Beta RPC & DeFiLlama Data...")
    collector = SolanaDataCollector()
    telemetry = collector.collect_all()
    
    perf = telemetry["performance"]
    vals = telemetry["validators"]
    econ = telemetry["economics"]

    print(f"      - Slot Height: #{perf['current_slot']:,}")
    print(f"      - Throughput: {perf['current_tps']:,} TPS (Avg: {perf['average_tps']:,} TPS)")
    print(f"      - Epoch {perf['epoch']} Progress: {perf['epoch_progress_pct']}%")
    print(f"      - Active Validators: {vals['active_validators']:,} (Stake: {vals['active_stake_sol']:,.2f} SOL)")
    print(f"      - SOL Price: ${econ['sol_price_usd']:,.2f} ({econ['sol_price_24h_change_pct']:+0.2f}%)")
    print(f"      - DeFi TVL: ${econ['defi_tvl_usd']:,.2f}\n")

    # 2. Run Anomaly Detection
    print("[2/3] Evaluating Statistical Anomaly Rules...")
    detector = AnomalyDetector()
    anomalies = detector.analyze(telemetry)
    for a in anomalies:
        print(f"      [{a['severity']}] {a['metric']}: {a['message']}")
    print()

    # 3. Generate Reports
    print("[3/3] Generating Multi-Format Reports (HTML Dashboard, Markdown, JSON)...")
    generator = ReportGenerator()
    paths = generator.generate_all(telemetry, anomalies)

    print(f"      ✔ JSON Output: {paths['json']}")
    print(f"      ✔ Markdown Report: {paths['markdown']}")
    print(f"      ✔ HTML Dashboard: {paths['html']}")
    print(f"      ✔ Root Index: {paths['index']}\n")

    print("==================================================================")
    print("  TELEMETRY REFRESH COMPLETE — 100% OPERATIONAL")
    print("==================================================================")


if __name__ == "__main__":
    main()
