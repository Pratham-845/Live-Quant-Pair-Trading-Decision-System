# app.py

import time
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

from config import (
    SYMBOLS,
    TIMEFRAMES,
    UI_REFRESH_MS,
    DEFAULT_ROLLING_WINDOW,
    DEFAULT_Z_THRESHOLD,
)

from stream.stream_runner import start_background_stream
from storage.database import init_db, load_ticks
from storage.buffer import get_ticks
from processing.resampler import resample_ticks
from processing.analytics import (
    compute_hedge_ratio,
    compute_spread,
    compute_zscore,
    rolling_correlation,
    adf_pvalue,
)

# -------------------------------------------------
# Streamlit setup
# -------------------------------------------------
st.set_page_config(layout="wide")
st.title("📊 Live Quant Pair Analytics (Mean Reversion)")

# -------------------------------------------------
# Native auto refresh
# -------------------------------------------------
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh >= UI_REFRESH_MS / 1000:
    st.session_state.last_refresh = time.time()
    st.rerun()

# -------------------------------------------------
# Init DB & WebSocket (ONCE)
# -------------------------------------------------
if "initialized" not in st.session_state:
    init_db()
    start_background_stream(SYMBOLS)
    st.session_state.initialized = True

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.header("Controls")

symbol_a = st.sidebar.selectbox("Symbol A", SYMBOLS, index=0)
symbol_b = st.sidebar.selectbox("Symbol B", SYMBOLS, index=1)

timeframe = st.sidebar.selectbox(
    "Resample Timeframe",
    list(TIMEFRAMES.keys()),
    index=0
)

rolling_window = st.sidebar.slider(
    "Rolling Window",
    20, 200, DEFAULT_ROLLING_WINDOW
)

z_threshold = st.sidebar.slider(
    "Z-Score Threshold",
    1.0, 3.0, DEFAULT_Z_THRESHOLD, 0.1
)

# -------------------------------------------------
# Load live ticks
# -------------------------------------------------
df_a = load_ticks(symbol_a)
df_b = load_ticks(symbol_b)

if df_a.empty or df_b.empty:
    st.info("⏳ Waiting for live data from Binance WebSocket...")
    st.stop()

# -------------------------------------------------
# Resample
# -------------------------------------------------
candles_a = resample_ticks(df_a, timeframe)
candles_b = resample_ticks(df_b, timeframe)

if candles_a.empty or candles_b.empty:
    st.info("⏳ Building candles...")
    st.stop()

# -------------------------------------------------
# Align candles
# -------------------------------------------------
common = (
    candles_a
    .join(candles_b, lsuffix="_a", rsuffix="_b")
    .dropna()
    .sort_index()
)

if len(common) < rolling_window:
    st.warning(f"⚠️ Warming up: {len(common)}/{rolling_window} candles")
    st.stop()

# -------------------------------------------------
# Core analytics
# -------------------------------------------------
hedge_ratio = compute_hedge_ratio(common["close_a"], common["close_b"])
spread = compute_spread(common["close_a"], common["close_b"], hedge_ratio)

z_series = compute_zscore(spread, rolling_window)
corr_series = rolling_correlation(common["close_a"], common["close_b"], rolling_window)

adf_p = adf_pvalue(spread)
regime = "Mean-Reverting" if adf_p < 0.05 else "Trending"

latest_z = z_series.iloc[-1]

# -------------------------------------------------
# KPI BAR
# -------------------------------------------------
st.subheader("📌 Live Trading Metrics")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Hedge Ratio", f"{hedge_ratio:.3f}")
c2.metric("Spread", f"{spread.iloc[-1]:.2f}")
c3.metric("Z-Score", f"{latest_z:.2f}")
c4.metric("Correlation", f"{corr_series.iloc[-1]:.2f}")

c5, c6 = st.columns(2)
c5.metric("ADF p-value", f"{adf_p:.4f}")
c6.metric("Regime", regime)

# -------------------------------------------------
# Signal
# -------------------------------------------------
signal = (
    "🟥 OVERVALUED" if latest_z > z_threshold else
    "🟩 UNDERVALUED" if latest_z < -z_threshold else
    "🟨 NEUTRAL"
)

st.markdown(
    f"""
    <div style="padding:14px;border-radius:10px;
                background:#0f172a;text-align:center;
                font-size:18px;">
        <strong>Current Signal:</strong> {signal}
    </div>
    """,
    unsafe_allow_html=True
)

# =================================================
# UNIQUE ADDITIONS
# =================================================
st.divider()

# -------------------------------------------------
# Trade Readiness Checklist
# -------------------------------------------------
st.subheader("✅ Trade Readiness Checklist")

checks = {
    "Z-score near entry threshold": abs(latest_z) > 0.8 * z_threshold,
    "Spread is stationary (ADF)": adf_p < 0.05,
    "Correlation is stable (>0.5)": corr_series.iloc[-1] > 0.5,
}

for k, v in checks.items():
    st.write(f"{'✔' if v else '✖'} {k}")

# -------------------------------------------------
# Trade Trigger Conditions
# -------------------------------------------------
st.subheader("🎯 Trade Trigger Conditions")

if latest_z >= 0:
    dist = z_threshold - latest_z
    st.write(f"🔴 SELL trigger when Z > {z_threshold}  (distance: {dist:.2f})")
else:
    dist = abs(-z_threshold - latest_z)
    st.write(f"🟢 BUY trigger when Z < {-z_threshold} (distance: {dist:.2f})")

# =================================================
# 🔥 DYNAMIC DECISION SNAPSHOT (FIXED)
# =================================================
st.subheader("📋 Decision Snapshot (LIVE + Recent)")

# -------- LIVE ROW (tick-based) --------
buffer_a = get_ticks(symbol_a)
buffer_b = get_ticks(symbol_b)

live_row = None

if buffer_a and buffer_b:
    pa = buffer_a[-1]["price"]
    pb = buffer_b[-1]["price"]

    mean = spread.rolling(rolling_window).mean().iloc[-1]
    std = spread.rolling(rolling_window).std().iloc[-1]

    if std > 0:
        live_spread = pa - hedge_ratio * pb
        live_z = (live_spread - mean) / std

        live_row = {
            "Time": "LIVE",
            "Spread": round(live_spread, 2),
            "Z-Score": round(live_z, 2),
            "Correlation": round(corr_series.iloc[-1], 2),
            "Signal": (
                "SELL" if live_z > z_threshold else
                "BUY" if live_z < -z_threshold else
                "HOLD"
            )
        }

# -------- Historical rows (confirmed candles) --------
hist_df = pd.DataFrame({
    "Time": z_series.index[-9:].astype(str),
    "Spread": spread[-9:].round(2),
    "Z-Score": z_series[-9:].round(2),
    "Correlation": corr_series[-9:].round(2),
})

hist_df["Signal"] = np.where(
    hist_df["Z-Score"] > z_threshold, "SELL",
    np.where(hist_df["Z-Score"] < -z_threshold, "BUY", "HOLD")
)

# Combine LIVE + history
if live_row:
    snap_df = pd.concat([pd.DataFrame([live_row]), hist_df], ignore_index=True)
else:
    snap_df = hist_df

st.dataframe(snap_df, use_container_width=True, hide_index=True)

# =================================================
# VISUAL INSIGHTS (UNCHANGED)
# =================================================
st.divider()

# Normalized Prices
st.subheader("📊 Normalized Price Comparison")

norm_df = common[["close_a", "close_b"]].copy()
norm_df["A"] = norm_df["close_a"] / norm_df["close_a"].iloc[0]
norm_df["B"] = norm_df["close_b"] / norm_df["close_b"].iloc[0]
norm_df = norm_df.reset_index()

st.altair_chart(
    alt.Chart(norm_df.melt("ts", value_vars=["A", "B"]))
    .mark_line(strokeWidth=2)
    .encode(x="ts:T", y="value:Q", color="variable:N")
    .properties(height=280),
    use_container_width=True
)

# Spread with Bands
st.subheader("📉 Spread with Statistical Bands")

band_df = pd.DataFrame({"time": spread.index, "spread": spread})
band_df["mean"] = spread.rolling(rolling_window).mean()
band_df["upper"] = band_df["mean"] + 2 * spread.rolling(rolling_window).std()
band_df["lower"] = band_df["mean"] - 2 * spread.rolling(rolling_window).std()
band_df = band_df.dropna().tail(300)

base = alt.Chart(band_df).encode(x="time:T")

st.altair_chart(
    base.mark_area(opacity=0.2, color="#38bdf8").encode(y="upper:Q", y2="lower:Q")
    + base.mark_line(color="orange").encode(y="spread:Q")
    + base.mark_line(strokeDash=[6, 4], color="white").encode(y="mean:Q"),
    use_container_width=True
)

# Z-score
st.subheader("🔥 Z-Score (Trade Trigger)")

z_df = pd.DataFrame({"time": z_series.index, "z": z_series}).dropna().tail(300)
z_base = alt.Chart(z_df).encode(x="time:T")

st.altair_chart(
    z_base.mark_line(color="red").encode(y="z:Q")
    + z_base.mark_rule(strokeDash=[4,4]).encode(y=alt.value(z_threshold))
    + z_base.mark_rule(strokeDash=[4,4]).encode(y=alt.value(-z_threshold))
    + z_base.mark_rule(color="gray").encode(y=alt.value(0)),
    use_container_width=True
)

# -------------------------------------------------
# Export
# -------------------------------------------------
export_df = pd.DataFrame({
    "spread": spread,
    "zscore": z_series,
    "correlation": corr_series
}).dropna()

st.download_button(
    "📥 Download Analytics CSV",
    export_df.to_csv().encode(),
    "analytics.csv",
    "text/csv"
)
