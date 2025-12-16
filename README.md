🧠 Live Quant Pair Trading Decision System
========================================

Real-Time Statistical Arbitrage Analytics using Binance Futures

This is NOT a charting application.
It is a real-time decision-support system for statistical mean-reversion trading, built directly on live market microstructure data.

────────────────────────────────────────────────────────────────────
PROBLEM STATEMENT & MOTIVATION
────────────────────────────────────────────────────────────────────

Most existing pair-trading dashboards suffer from critical design flaws:

• Dependence on static or pre-downloaded datasets  
• Over-emphasis on visualization instead of decision logic  
• Hidden assumptions buried inside aggregated indicators  

This project is engineered to explicitly answer a trader’s core question:

“Is this pair tradable RIGHT NOW — and what statistical evidence supports that decision?”

Every architectural and analytical choice is made in service of this question.

────────────────────────────────────────────────────────────────────
SYSTEM CAPABILITIES (HIGH LEVEL)
────────────────────────────────────────────────────────────────────

• Streams LIVE trade-level data from Binance Futures  
• Converts raw ticks into statistically structured signals  
• Continuously validates mean-reversion viability  
• Explicitly separates live (in-progress) and confirmed (historical) state  
• Produces actionable trade context instead of opaque indicators  

No mock data. No CSV ingestion. No delayed polling APIs.

────────────────────────────────────────────────────────────────────
ARCHITECTURE OVERVIEW
────────────────────────────────────────────────────────────────────

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

────────────────────────────────────────────────────────────────────
TECHNOLOGY STACK
────────────────────────────────────────────────────────────────────

Layer            Technology        Rationale
------------------------------------------------------------
Data Feed        Binance WebSocket True real-time trade data
Processing       Pandas, NumPy     Vectorized analytics
Statistics       Statsmodels       Econometric rigor
Storage          SQLite            Lightweight & deterministic
UI               Streamlit         Live refresh, fast iteration
Visualization    Altair            Clean, declarative visuals

────────────────────────────────────────────────────────────────────
SETUP & EXECUTION
────────────────────────────────────────────────────────────────────

1. Clone Repository
   git clone https://github.com/<your-username>/live-quant-pair-trading-dashboard.git
   cd live-quant-pair-trading-dashboard

2. Create Environment
   python -m venv venv
   venv\Scripts\activate

3. Install Dependencies
   pip install -r requirements.txt

4. Run Application
   streamlit run app.py

────────────────────────────────────────────────────────────────────
LIVE DATA INGESTION MODEL
────────────────────────────────────────────────────────────────────

• Subscribes to Binance Futures trade WebSocket streams  
• Each trade is:
    - Buffered in-memory for tick-level analytics
    - Persisted to SQLite for candle construction

• UI refresh loop is DECOUPLED from ingestion to avoid:
    - UI thread blocking
    - Fake “live” charts
    - Candle repainting & look-ahead bias

────────────────────────────────────────────────────────────────────
CORE QUANTITATIVE METHODOLOGY
────────────────────────────────────────────────────────────────────

1. HEDGE RATIO (POSITION NEUTRALIZATION)
------------------------------------------------------------
Estimated using Ordinary Least Squares (OLS):

Y_t = α + βX_t

Where:
Y_t → Price of Symbol A  
X_t → Price of Symbol B  
β   → Hedge Ratio  

Trader Interpretation:
A hedge ratio of -0.38 implies:
Short 1 unit of A, Long 0.38 units of B for relative neutrality.

The hedge ratio is continuously re-estimated as new data arrives.

------------------------------------------------------------
2. SPREAD CONSTRUCTION (TRADABLE OBJECT)
------------------------------------------------------------
Spread_t = Y_t − βX_t

The spread represents RELATIVE MISPRICING, not price direction.

• Random walk → No statistical edge  
• Mean oscillation → Potential convergence trade  

------------------------------------------------------------
3. Z-SCORE (NORMALIZED DEVIATION)
------------------------------------------------------------
Z_t = (Spread_t − μ) / σ

• Computed using rolling mean & volatility  
• Normalizes deviations across regimes  
• Primary entry / exit signal  

The system explicitly separates:
• Live Z-Score (tick-based) → Anticipation
• Confirmed Z-Score (candle-based) → Validation

------------------------------------------------------------
4. STATIONARITY VALIDATION (ADF TEST)
------------------------------------------------------------
Augmented Dickey–Fuller test applied to spread:

• p < 0.05 → Mean-reverting  
• p ≥ 0.05 → Trending / unstable  

Acts as a regime filter to prevent trading false edges.

------------------------------------------------------------
5. ROLLING CORRELATION (RELATIONSHIP HEALTH)
------------------------------------------------------------
Rolling correlation monitors structural breakdowns.

High Z-score + Weak correlation = TRAP, not opportunity.

────────────────────────────────────────────────────────────────────
DASHBOARD DESIGN PHILOSOPHY
────────────────────────────────────────────────────────────────────

WHAT THIS SYSTEM INTENTIONALLY AVOIDS:
• Price prediction
• Curve-fitted backtests
• Indicator stacking

WHAT IT EXPLICITLY PROVIDES:
• Decision-critical statistical evidence
• Clear separation of live vs confirmed state
• Transparent reasoning for trade validity

────────────────────────────────────────────────────────────────────
KEY INTERFACE COMPONENTS
────────────────────────────────────────────────────────────────────

1. LIVE TRADING METRICS
------------------------------------------------------------
• Hedge Ratio
• Spread
• Z-Score
• Rolling Correlation
• Regime Classification

Designed for rapid situational awareness.

------------------------------------------------------------
2. TRADE READINESS CHECKLIST
------------------------------------------------------------
Binary trader filters:
• Is deviation meaningful?
• Is spread stationary?
• Is relationship stable?

Prevents low-quality trades.

------------------------------------------------------------
3. TRADE TRIGGER DISTANCE
------------------------------------------------------------
Shows distance to entry threshold.
Encourages anticipation over reaction.

------------------------------------------------------------
4. DECISION SNAPSHOT TABLE (DYNAMIC)
------------------------------------------------------------
LIVE row → Tick-based reality  
Historical rows → Confirmed candle analytics  

Avoids treating incomplete candles as facts.

------------------------------------------------------------
5. VISUAL ANALYTICS (CONFIRMATORY)
------------------------------------------------------------
Charts support decisions — they do not drive them.

• Normalized price behavior
• Spread with statistical bands
• Z-score vs thresholds

────────────────────────────────────────────────────────────────────
ENGINEERING DESIGN PRINCIPLES
────────────────────────────────────────────────────────────────────

• Explicit tick vs candle separation
• No forward-filled data
• Conservative warm-up enforcement
• Stateless UI refresh
• Minimal but robust indicator set

These reflect real trading constraints — not academic demos.
