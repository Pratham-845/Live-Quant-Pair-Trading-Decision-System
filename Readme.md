# **🧠 Live Quant Pair Trading Decision System**



Real-Time Statistical Arbitrage Analytics using Binance Futures



This is not a charting application.

It is a real-time decision-support system for mean-reversion trading, built on live market microstructure data.



#### **📌 Problem Statement \& Motivation**



Most existing pair-trading dashboards suffer from fundamental design issues:

* Dependence on static or pre-downloaded datasets
* Excessive focus on visualization over decision logic
* Implicit assumptions hidden behind aggregated metrics



This project is designed to explicitly answer a trader’s core question:

“Is this pair tradable right now — and what statistical evidence supports that decision?”

All system components are engineered to support this objective.



#### **⚙️ System Capabilities (High Level)**



* Streams live trade-level data from Binance Futures
* Transforms raw ticks into statistically structured signals
* Continuously evaluates mean-reversion validity
* Explicitly separates live (in-progress) and confirmed (historical) state
* Produces actionable trade context rather than opaque indicators.



No simulated data. No CSV ingestion. No delayed polling APIs.


**🧩 Architecture Overview**
---



Binance Futures WebSocket (Trades)

&nbsp;       ↓

In-Memory Tick Buffer        \[Live State]

&nbsp;       ↓

SQLite Tick Store           \[Persistence Layer]

&nbsp;       ↓

Timeframe Resampling        \[Confirmed Candles]

&nbsp;       ↓

Statistical Analytics Engine

&nbsp;       ↓

Trader Decision Interface





## **🛠️ Technology Stack**





| Layer         | Technology        | Rationale                              |

| ------------- | ----------------- | -------------------------------------- |

| Data Feed     | Binance WebSocket | True real-time trade data              |

| Processing    | Pandas, NumPy     | Vectorized time-series operations      |

| Statistics    | Statsmodels       | Econometric reliability                |

| Storage       | SQLite            | Lightweight, deterministic persistence |

| UI            | Streamlit         | Fast prototyping with live refresh     |

| Visualization | Altair            | Declarative, low-noise charts          |



#### 🚀 Setup \& Execution

1️⃣ Clone Repository

git clone https://github.com/<your-username>/live-quant-pair-trading-dashboard.git

cd live-quant-pair-trading-dashboard



2️⃣ Create Environment

python -m venv venv

venv\\Scripts\\activate



3️⃣ Install Dependencies

pip install -r requirements.txt



4️⃣ Run Application

streamlit run app.py


**📡 Live Data Ingestion Model**
---



Subscribes to Binance Futures trade streams



Each trade is:

* Buffered in memory for tick-level analytics
* Persisted to SQLite for time-based resampling



The UI refresh loop is decoupled from ingestion, preventing:



* UI thread blocking
* Artificial “live” updates
* Candle repainting or look-ahead bias



**📐 Core Quantitative Methodology**

1. Hedge Ratio — Position Neutralization
---

###### 

###### Estimated using Ordinary Least Squares (OLS): 

###### &nbsp;                 Yt​=α+βXt​



###### 2\. Spread Construction — Tradable Variable

###### &nbsp;                 Spreadt ​=Yt​−βXt​

The spread represents relative mispricing, independent of directional market moves.



Behavioral interpretation:

* Random walk → no statistical edge
* Mean oscillation → potential convergence trade



###### 3\. Z-Score — Normalized Deviation Metric

###### &nbsp;                Zt​= Spreadt​−μ​/σ

* Uses rolling mean \& volatility
* Normalizes deviations across regimes
* Primary entry / exit trigger

The system explicitly separates:

* ⚡ Live Z-Score (tick-based) → Anticipation
* ✅ Confirmed Z-Score (candle-based) → Validation





###### 4\. Stationarity Validation — ADF Test

###### 

The Augmented Dickey–Fuller (ADF) test is applied to the spread:

p < 0.05 → Mean-reverting

p ≥ 0.05 → Trending / unstable

Acts as a regime filter, preventing trades on illusory edges.

###### 

###### 5\. Rolling Correlation — Relationship Integrity



Rolling correlation monitors structural breakdowns.

High Z-Score + Weak Correlation = Trap, not opportunity

This system demonstrates how live market microstructure data can be transformed into statistically defensible trading decisions through disciplined engineering and quantitative design.

It prioritizes decision clarity, robustness, and real-world trading constraints over superficial visualization or predictive claims




