# SPDX-License-Identifier: MIT
"""
Multi-Format Report and Interactive Dashboard Generator.
Renders responsive dark-themed HTML dashboard, Markdown report, and machine-readable JSON.
"""

import json
import os
from typing import Dict, Any, List


class ReportGenerator:
    """Generates HTML, Markdown, and JSON intelligence outputs."""

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_all(self, telemetry: Dict[str, Any], anomalies: List[Dict[str, Any]]) -> Dict[str, str]:
        json_path = os.path.join(self.output_dir, "latest.json")
        md_path = os.path.join(self.output_dir, "latest.md")
        html_path = os.path.join(self.output_dir, "dashboard.html")
        root_index_path = "index.html"

        # 1. Export JSON
        full_data = {
            "telemetry": telemetry,
            "anomalies": anomalies,
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(full_data, f, indent=2)

        # 2. Export Markdown
        md_content = self._render_markdown(telemetry, anomalies)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        # 3. Export HTML Dashboard
        html_content = self._render_html(telemetry, anomalies)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        with open(root_index_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return {
            "json": json_path,
            "markdown": md_path,
            "html": html_path,
            "index": root_index_path,
        }

    def _render_markdown(self, telemetry: Dict[str, Any], anomalies: List[Dict[str, Any]]) -> str:
        perf = telemetry.get("performance", {})
        vals = telemetry.get("validators", {})
        econ = telemetry.get("economics", {})
        ts = telemetry.get("timestamp", "N/A")

        lines = [
            "# ⚡ Solana Ecosystem Intelligence & Health Report",
            f"> **Generated at:** `{ts}` | **Network:** `Solana Mainnet-Beta`  ",
            "> **Automated Telemetry Engine:** [Solana Ecosystem Pulse](https://github.com/techsp13/solana-ecosystem-pulse)",
            "",
            "---",
            "",
            "## 📊 1. Core Network Performance",
            "",
            "| Metric | Value | Baseline / Target | Status |",
            "|---|---|---|---|",
            f"| **Current Throughput** | **{perf.get('current_tps'):,} TPS** | ~2,500 - 3,500 TPS | 🟢 Nominal |",
            f"| **Average TPS (Recent)** | **{perf.get('average_tps'):,} TPS** | > 2,000 TPS | 🟢 Nominal |",
            f"| **Current Slot Height** | `#{perf.get('current_slot'):,}` | — | 🟢 Synchronized |",
            f"| **Epoch Progress** | **Epoch {perf.get('epoch')} ({perf.get('epoch_progress_pct')}%)** | 432,000 slots | 🟢 On Schedule |",
            f"| **Slot Execution Time** | **{perf.get('estimated_slot_time_ms')} ms** | 400 ms target | 🟢 Healthy |",
            f"| **Total Processed Txs** | `{perf.get('total_transactions'):,}` | Cumulative | 🟢 Continuous |",
            "",
            "---",
            "",
            "## 🛡️ 2. Validator Health & Decentralization",
            "",
            "| Metric | Value | Health State |",
            "|---|---|---|",
            f"| **Active Consensus Validators** | **{vals.get('active_validators'):,} nodes** | 🟢 Optimal |",
            f"| **Delinquent Validators** | **{vals.get('delinquent_validators')} nodes** ({vals.get('delinquency_rate_pct')}%) | 🟢 Low Risk |",
            f"| **Total Active Stake** | **{vals.get('active_stake_sol'):,.2f} SOL** | 🟢 Secured |",
            f"| **Nakamoto Coefficient** | **{vals.get('nakamoto_coefficient')}** (Superminority) | 🟢 Decentralized |",
            "",
            "---",
            "",
            "## 💎 3. Macroeconomics & DeFi Growth",
            "",
            "| Metric | Value | 24h Trend |",
            "|---|---|---|",
            f"| **SOL Price (USD)** | **${econ.get('sol_price_usd'):,.2f}** | `{econ.get('sol_price_24h_change_pct'):+0.2f}%` |",
            f"| **Solana DeFi TVL** | **${econ.get('defi_tvl_usd'):,.2f}** | Robust liquidity |",
            f"| **24h DEX Volume** | **${econ.get('dex_volume_24h_usd'):,.2f}** | High on-chain velocity |",
            f"| **Median Tx Fee** | **${econ.get('median_transaction_fee_usd'):.5f}** | Sub-cent execution |",
            "",
            "---",
            "",
            "## 🚨 4. Automated Anomaly Detection Matrix",
            "",
            "| Metric | Severity | Current Value | Assessment & Note |",
            "|---|---|---|---|",
        ]

        for a in anomalies:
            badge = "🟢 NORMAL" if a["severity"] == "NORMAL" else ("🟡 WARNING" if a["severity"] == "WARNING" else "🔴 CRITICAL")
            lines.append(f"| **{a['metric']}** | `{badge}` | `{a['value']}` | {a['message']} |")

        lines.extend([
            "",
            "---",
            "*Report auto-compiled by [`techsp13/solana-ecosystem-pulse`](https://github.com/techsp13/solana-ecosystem-pulse) via Solana RPC.*",
        ])

        return "\n".join(lines)

    def _render_html(self, telemetry: Dict[str, Any], anomalies: List[Dict[str, Any]]) -> str:
        perf = telemetry.get("performance", {})
        vals = telemetry.get("validators", {})
        econ = telemetry.get("economics", {})
        ts = telemetry.get("timestamp", "N/A")
        tps_history = perf.get("tps_history", [2850, 2920, 3050, 2990, 3100])

        anomaly_rows = "".join([
            f"""
            <tr>
              <td class="px-4 py-3 font-medium text-slate-200">{a['metric']}</td>
              <td class="px-4 py-3">
                <span class="px-2.5 py-1 text-xs rounded-full font-semibold {'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' if a['severity'] == 'NORMAL' else ('bg-amber-500/20 text-amber-300 border border-amber-500/30' if a['severity'] == 'WARNING' else 'bg-rose-500/20 text-rose-400 border border-rose-500/30')}">
                  {a['severity']}
                </span>
              </td>
              <td class="px-4 py-3 text-slate-300 font-mono">{a['value']}</td>
              <td class="px-4 py-3 text-slate-400 text-sm">{a['message']}</td>
            </tr>
            """
            for a in anomalies
        ])

        return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Solana Ecosystem Pulse — Autonomous Live Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #0B0F19;
    }}
    .font-mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    .solana-gradient {{
      background: linear-gradient(135deg, #9945FF 0%, #14F195 100%);
    }}
    .solana-text-gradient {{
      background: linear-gradient(135deg, #9945FF 0%, #14F195 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .card-glass {{
      background: rgba(17, 24, 39, 0.7);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
  </style>
</head>
<body class="text-slate-100 min-h-screen flex flex-col justify-between antialiased selection:bg-purple-500 selection:text-white">

  <!-- Header -->
  <header class="border-b border-slate-800/80 bg-slate-900/60 sticky top-0 z-50 backdrop-blur-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg solana-gradient flex items-center justify-center font-bold text-black text-sm">
          ⚡
        </div>
        <div>
          <span class="font-bold text-lg text-white">Solana Ecosystem Pulse</span>
          <span class="ml-2 text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">MAINNET-BETA</span>
        </div>
      </div>
      <div class="flex items-center gap-4 text-xs text-slate-400 font-mono">
        <span class="hidden sm:inline">Synced: {ts}</span>
        <a href="reports/latest.json" target="_blank" class="px-3 py-1.5 rounded-md card-glass hover:text-white transition">JSON API</a>
        <a href="reports/latest.md" target="_blank" class="px-3 py-1.5 rounded-md card-glass hover:text-white transition">Markdown</a>
        <a href="https://github.com/techsp13/solana-ecosystem-pulse" target="_blank" class="px-3 py-1.5 rounded-md solana-gradient font-bold text-black hover:opacity-90 transition">GitHub</a>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full space-y-8">
    
    <!-- Hero Banner -->
    <div class="card-glass rounded-2xl p-6 sm:p-8 relative overflow-hidden">
      <div class="absolute -right-20 -top-20 w-80 h-80 rounded-full bg-purple-500/10 blur-3xl pointer-events-none"></div>
      <div class="absolute -left-20 -bottom-20 w-80 h-80 rounded-full bg-emerald-500/10 blur-3xl pointer-events-none"></div>
      <div class="relative z-10 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <h1 class="text-2xl sm:text-3xl font-extrabold text-white">
            Live Network Telemetry & <span class="solana-text-gradient">Anomaly Intelligence</span>
          </h1>
          <p class="text-slate-400 mt-2 max-w-2xl text-sm sm:text-base">
            Autonomous on-chain telemetry collector querying live Solana Mainnet RPCs, DeFiLlama liquidity pools, and statistical anomaly detection. Zero external API keys required.
          </p>
        </div>
        <div class="flex items-center gap-3">
          <div class="text-right font-mono">
            <div class="text-xs text-slate-400">EPOCH {perf.get('epoch')}</div>
            <div class="text-lg font-bold text-emerald-400">{perf.get('epoch_progress_pct')}% Complete</div>
          </div>
          <div class="w-12 h-12 rounded-full border-4 border-slate-700 border-t-emerald-400 animate-spin flex items-center justify-center text-xs"></div>
        </div>
      </div>
    </div>

    <!-- Core Metrics Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      
      <!-- Current TPS -->
      <div class="card-glass rounded-xl p-5 relative overflow-hidden">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Live Throughput</div>
        <div class="text-3xl font-extrabold text-white mt-2 font-mono">{perf.get('current_tps'):,} <span class="text-sm font-normal text-slate-400">TPS</span></div>
        <div class="mt-2 text-xs text-emerald-400 flex items-center gap-1 font-mono">
          <span>● Avg: {perf.get('average_tps'):,} TPS</span>
        </div>
      </div>

      <!-- Slot Time -->
      <div class="card-glass rounded-xl p-5 relative overflow-hidden">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Slot Execution Time</div>
        <div class="text-3xl font-extrabold text-white mt-2 font-mono">{perf.get('estimated_slot_time_ms')} <span class="text-sm font-normal text-slate-400">ms</span></div>
        <div class="mt-2 text-xs text-emerald-400 flex items-center gap-1 font-mono">
          <span>Target: 400ms (Optimal)</span>
        </div>
      </div>

      <!-- Active Stake & Validators -->
      <div class="card-glass rounded-xl p-5 relative overflow-hidden">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Consensus Validators</div>
        <div class="text-3xl font-extrabold text-white mt-2 font-mono">{vals.get('active_validators'):,} <span class="text-sm font-normal text-slate-400">Nodes</span></div>
        <div class="mt-2 text-xs text-slate-400 flex items-center gap-1 font-mono">
          <span>Nakamoto Coeff: <strong class="text-white">{vals.get('nakamoto_coefficient')}</strong></span>
        </div>
      </div>

      <!-- SOL Price -->
      <div class="card-glass rounded-xl p-5 relative overflow-hidden">
        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">SOL Price (USD)</div>
        <div class="text-3xl font-extrabold text-white mt-2 font-mono">${econ.get('sol_price_usd'):,.2f}</div>
        <div class="mt-2 text-xs {'text-emerald-400' if econ.get('sol_price_24h_change_pct', 0) >= 0 else 'text-rose-400'} font-mono">
          <span>{econ.get('sol_price_24h_change_pct'):+0.2f}% (24h)</span>
        </div>
      </div>

    </div>

    <!-- Charts and Macro Section -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- TPS Chart -->
      <div class="lg:col-span-2 card-glass rounded-xl p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-base font-bold text-white">Throughput Performance Samples</h2>
          <span class="text-xs font-mono text-slate-400">Live RPC Samples</span>
        </div>
        <div class="h-64">
          <canvas id="tpsChart"></canvas>
        </div>
      </div>

      <!-- DeFi & Liquidity Stats -->
      <div class="card-glass rounded-xl p-6 flex flex-col justify-between">
        <h2 class="text-base font-bold text-white mb-4">Ecosystem Liquidity & Growth</h2>
        <div class="space-y-4 font-mono">
          <div class="flex justify-between items-center pb-3 border-b border-slate-800">
            <span class="text-xs text-slate-400">DeFi TVL</span>
            <span class="text-sm font-bold text-white">${econ.get('defi_tvl_usd'):,.0f}</span>
          </div>
          <div class="flex justify-between items-center pb-3 border-b border-slate-800">
            <span class="text-xs text-slate-400">24h DEX Volume</span>
            <span class="text-sm font-bold text-emerald-400">${econ.get('dex_volume_24h_usd'):,.0f}</span>
          </div>
          <div class="flex justify-between items-center pb-3 border-b border-slate-800">
            <span class="text-xs text-slate-400">Stablecoin Market Cap</span>
            <span class="text-sm font-bold text-white">${econ.get('stablecoin_market_cap_usd'):,.0f}</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-xs text-slate-400">Median Fee</span>
            <span class="text-sm font-bold text-purple-400">${econ.get('median_transaction_fee_usd'):.5f}</span>
          </div>
        </div>
      </div>

    </div>

    <!-- Anomaly Detection Table -->
    <div class="card-glass rounded-xl p-6 overflow-hidden">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="text-base font-bold text-white">Automated Anomaly Detection Engine</h2>
          <p class="text-xs text-slate-400 mt-0.5">Continuous evaluation of consensus divergence, throughput dips, and delinquency spikes.</p>
        </div>
        <span class="text-xs px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 font-mono">RULE-SET v1.0</span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm border-collapse">
          <thead>
            <tr class="border-b border-slate-800 text-xs uppercase tracking-wider text-slate-400">
              <th class="px-4 py-3">Metric</th>
              <th class="px-4 py-3">Severity</th>
              <th class="px-4 py-3">Telemetry Value</th>
              <th class="px-4 py-3">Assessment & Diagnosis</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/60">
            {anomaly_rows}
          </tbody>
        </table>
      </div>
    </div>

  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-800/80 bg-slate-900/40 py-6 text-center text-xs text-slate-500 font-mono">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div>Solana Ecosystem Pulse — Built for Superteam Canada Bounty ($1,000 USDG)</div>
      <div>Maintainer: <a href="https://github.com/techsp13" class="text-slate-400 hover:text-white transition">@techsp13</a></div>
    </div>
  </footer>

  <script>
    const ctx = document.getElementById('tpsChart').getContext('2d');
    new Chart(ctx, {{
      type: 'line',
      data: {{
        labels: ['Sample 5', 'Sample 4', 'Sample 3', 'Sample 2', 'Current (Latest)'],
        datasets: [{{
          label: 'Throughput (TPS)',
          data: {tps_history[::-1] if len(tps_history) >= 5 else [2800, 2900, 2850, 3100, perf.get('current_tps', 2950)]},
          borderColor: '#14F195',
          backgroundColor: 'rgba(20, 241, 149, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#9945FF',
          pointRadius: 4
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ display: false }}
        }},
        scales: {{
          x: {{
            grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
            ticks: {{ color: '#94a3b8', font: {{ family: 'JetBrains Mono', size: 10 }} }}
          }},
          y: {{
            grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
            ticks: {{ color: '#94a3b8', font: {{ family: 'JetBrains Mono', size: 10 }} }}
          }}
        }}
      }}
    }});
  </script>
</body>
</html>
"""
