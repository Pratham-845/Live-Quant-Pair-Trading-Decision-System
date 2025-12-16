# storage/database.py

import sqlite3
import pandas as pd
from pathlib import Path

# Absolute, stable DB path (CRITICAL on Windows + Streamlit)
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "ticks.db"


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ticks (
            symbol TEXT,
            ts INTEGER,
            price REAL,
            qty REAL
        )
        """
    )

    conn.commit()
    conn.close()


def insert_tick(symbol: str, ts: int, price: float, qty: float):
    """
    EXACT signature expected by websocket client.
    DO NOT change argument names.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO ticks VALUES (?, ?, ?, ?)",
        (symbol, ts, price, qty),
    )

    conn.commit()
    conn.close()


def load_ticks(symbol: str) -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame()

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT ts, price, qty FROM ticks WHERE symbol = ? ORDER BY ts",
        conn,
        params=(symbol,),
    )

    conn.close()

    if df.empty:
        return df

    df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    df = df.set_index("ts").sort_index()

    return df
