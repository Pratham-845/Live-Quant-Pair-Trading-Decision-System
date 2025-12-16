# processing/resampler.py

import pandas as pd


def resample_ticks(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """
    Resample tick-level trade data into OHLC candles
    using EXCHANGE EVENT TIME as index.

    Parameters
    ----------
    df : DataFrame
        Must contain:
        - index: DatetimeIndex (UTC, exchange time)
        - column: 'price'
    timeframe : str
        Pandas resample rule ('1S', '1T', '5T', etc.)

    Returns
    -------
    DataFrame
        OHLC candles indexed by exchange time
    """

    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()

    # -------------------------------------------------
    # Ensure datetime index (EXCHANGE TIME)
    # -------------------------------------------------
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index, unit="ms", utc=True)

    # Always sort index (CRITICAL for live systems)
    df = df.sort_index()

    # -------------------------------------------------
    # Resample using exchange time ONLY
    # -------------------------------------------------
    ohlc = df["price"].resample(
        timeframe,
        label="right",
        closed="right"
    ).ohlc()

    # Drop incomplete candles
    ohlc = ohlc.dropna()

    return ohlc
