# ⚡ Solana Ecosystem Pulse

> **Autonomous Live Dashboard, Statistical Anomaly Detector & Multi-Format Intelligence Reports**  
> **Target Bounty:** *Develop Solana Ecosystem Auto-Updating Report & Interactive Dashboard* ($1,000 USDG)  
> **Sponsor:** Superteam Canada  
> **Author:** `@techsp13` (`0x01E7862BEd361b72784c0819AD68548D85A9ad49`)  
> **Live Interactive Dashboard:** [**https://techsp13.github.io/solana-ecosystem-pulse/**](https://techsp13.github.io/solana-ecosystem-pulse/)

---

## 🌟 Executive Summary

**Solana Ecosystem Pulse** is a zero-dependency, automated telemetry and intelligence engine for the Solana blockchain. It queries public Solana Mainnet RPCs, DeFiLlama liquidity pools, and on-chain validator registries to continuously evaluate network health, consensus stability, and economic growth.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               SOLANA ECOSYSTEM PULSE ARCHITECTURE                      │
├─────────────────────────┬──────────────────────────────────────────────────────────────┤
│ 1. Telemetry Collector  │ Pure Python RPC client querying getSlot, getEpochInfo, etc.  │
│ 2. Anomaly Engine       │ Statistical evaluation of TPS drops, slow slots & delinquency│
│ 3. Multi-Format Outputs │ Interactive HTML Dashboard, Markdown Report, Structured JSON │
│ 4. Autonomous CI/CD     │ GitHub Actions cron workflow refreshing data every 6 hours   │
└─────────────────────────┴──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Features

1. **Direct On-Chain Telemetry (Zero API Keys Required):**
   - Directly executes JSON-RPC calls (`getSlot`, `getEpochInfo`, `getRecentPerformanceSamples`, `getVoteAccounts`, `getSupply`) against public Solana endpoints with automatic failover.
2. **Comprehensive Metrics Coverage:**
   - **Throughput & Speed:** Live TPS, sample moving averages, target slot time ($400\text{ms}$).
   - **Consensus & Validators:** Active vs. delinquent validator counts, total staked SOL, Nakamoto superminority coefficient ($19$).
   - **Ecosystem & Macroeconomics:** Real-time SOL price, 24h price delta, DeFi Total Value Locked (TVL), 24h DEX trading volume, median fee ($0.00064).
3. **Automated Statistical Anomaly Detection:**
   - Evaluates network telemetry against predefined performance thresholds:
     - `TPS Degradation`: Flags if throughput drops below $1,800\text{ TPS}$.
     - `Slow Slot Latency`: Flags if block execution exceeds $500\text{ms}$.
     - `Validator Delinquency Spike`: Flags if offline validator count exceeds $3.0\%$.
     - `Price Volatility`: Flags extreme macro fluctuations ($>10\%$).
4. **Multi-Format Intelligence Delivery:**
   - **Interactive HTML Dashboard:** Modern dark-theme UI with Chart.js line graphs, responsive status badges, and live metric cards.
   - **Markdown Report (`reports/latest.md`):** Formatted tables and executive summaries for humans.
   - **Structured JSON (`reports/latest.json`):** Machine-readable telemetry for automated ingestion.
5. **Autonomous Cron Refresh:**
   - Powered by GitHub Actions (`.github/workflows/update-report.yml`) updating telemetry every 6 hours automatically.

---

## 📊 Live Sample Outputs

* **Interactive Dashboard:** [`index.html`](./index.html) or [Live GitHub Pages](https://techsp13.github.io/solana-ecosystem-pulse/)
* **Human-Readable Report:** [`reports/latest.md`](./reports/latest.md)
* **Machine-Readable API:** [`reports/latest.json`](./reports/latest.json)

---

## 🧪 Running Unit Tests

Execute the comprehensive unit test suite:

```bash
python -m unittest test_pulse.py
```

Output:
```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.05s — OK (100% Passing)
```

---

## 🛠️ Local Quickstart

### Prerequisites
* Python 3.9+ (Standard Library only — zero external pip dependencies needed!)

### 1. Clone the repository
```bash
git clone https://github.com/techsp13/solana-ecosystem-pulse.git
cd solana-ecosystem-pulse
```

### 2. Run Telemetry Collector & Generate Reports
```bash
python main.py
```

### 3. View Interactive Dashboard
Open `index.html` in your favorite web browser or start a local server:
```bash
python -m http.server 8000
```
Visit `http://localhost:8000`.

---

## 📄 License
MIT License. Open-source contribution for Superteam Canada.
