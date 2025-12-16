🧠 Live Quant Pair Trading Decision System
📈 Real-Time Statistical Arbitrage Analytics using Binance Futures

This is not a charting application.

It is a real-time decision-support system for mean-reversion pair trading, built directly on live market microstructure data.

🎯 Problem Statement & Motivation

Most existing pair-trading dashboards suffer from fundamental design flaws:

❌ Dependence on static or pre-downloaded datasets

❌ Over-emphasis on visualization instead of decision logic

❌ Hidden assumptions buried inside aggregated indicators

This project is engineered to explicitly answer a trader’s core question:

“Is this pair tradable right now — and what statistical evidence supports that decision?”

Every architectural and analytical choice in this system exists to support that question.

⚙️ System Capabilities (High Level)

📡 Streams live trade-level data from Binance Futures

🧮 Converts raw ticks into statistically structured signals

🔁 Continuously evaluates mean-reversion validity

🧠 Explicitly separates live (in-progress) and confirmed (historical) state

🎯 Produces actionable trade context, not opaque indicators

No simulated data. No CSV ingestion. No delayed polling APIs.

🧩 Architecture Overview
Binance Futures WebSocket (Trades)
        ↓
In-Memory Tick Buffer        (Live State)
        ↓
SQLite Tick Store           (Persistence Layer)
        ↓
Timeframe Resampling        (Confirmed Candles)
        ↓
Statistical Analytics Engine
        ↓
Trader Decision Interface


Design Principle:

Ticks provide immediacy; candles provide statistical stability.

🛠️ Technology Stack
Layer	Technology	Rationale
📡 Data Feed	Binance WebSocket	True real-time trade data
🧮 Processing	Pandas, NumPy	Vectorized time-series analytics
📊 Statistics	Statsmodels	Econometric rigor
💾 Storage	SQLite	Lightweight & deterministic
🖥️ UI	Streamlit	Fast iteration with live refresh
📈 Visualization	Altair	Declarative, low-noise visuals
🚀 Setup & Execution
1️⃣ Clone Repository
git clone https://github.com/<your-username>/live-quant-pair-trading-dashboard.git
cd live-quant-pair-trading-dashboard

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Application
streamlit run app.py

📡 Live Data Ingestion Model

Subscribes to Binance Futures trade WebSocket streams

Each trade is:

🧠 Buffered in-memory for tick-level analytics

💾 Persisted to SQLite for candle construction

The UI refresh loop is decoupled from ingestion to prevent:

❌ UI thread blocking

❌ Artificial “live” charts

❌ Candle repainting & look-ahead bias

📐 Core Quantitative Methodology
🔹 1. Hedge Ratio — Position Neutralization

Estimated using Ordinary Least Squares (OLS):

𝑌
𝑡
=
𝛼
+
𝛽
𝑋
𝑡
Y
t
	​

=α+βX
t
	​


Where:

Yₜ → Price series of Symbol A

Xₜ → Price series of Symbol B

β → Hedge Ratio

Trader interpretation:
A hedge ratio of −0.38 implies:

Short 1 unit of A, Long 0.38 units of B for relative neutrality.

The hedge ratio is re-estimated continuously as new data arrives.

🔹 2. Spread Construction — The Tradable Object
𝑆
𝑝
𝑟
𝑒
𝑎
𝑑
𝑡
=
𝑌
𝑡
−
𝛽
𝑋
𝑡
Spread
t
	​

=Y
t
	​

−βX
t
	​


The spread represents relative mispricing, not price direction.

📉 Random walk → No statistical edge

🔁 Mean oscillation → Potential convergence trade

🔹 3. Z-Score — Normalized Deviation Metric
𝑍
𝑡
=
𝑆
𝑝
𝑟
𝑒
𝑎
𝑑
𝑡
−
𝜇
𝜎
Z
t
	​

=
σ
Spread
t
	​

−μ
	​


Uses rolling mean & volatility

Normalizes deviations across regimes

Primary entry / exit trigger

The system explicitly separates:

⚡ Live Z-Score (tick-based) → Anticipation

✅ Confirmed Z-Score (candle-based) → Validation

🔹 4. Stationarity Validation — ADF Test

The Augmented Dickey–Fuller (ADF) test is applied to the spread:

p < 0.05 → Mean-reverting

p ≥ 0.05 → Trending / unstable

Acts as a regime filter, preventing trades on illusory edges.

🔹 5. Rolling Correlation — Relationship Integrity

Rolling correlation monitors structural breakdowns.

High Z-Score + Weak Correlation = Trap, not opportunity
