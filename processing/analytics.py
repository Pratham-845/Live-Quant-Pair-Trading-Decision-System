# processing/analytics.py

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller


def compute_hedge_ratio(y: pd.Series, x: pd.Series) -> float:
    """
    OLS hedge ratio: y = a + b*x
    Returns b or NaN if insufficient data.
    """
    y = y.dropna()
    x = x.dropna()

    # Warm-up check
    if len(y) < 5 or len(x) < 5:
        return np.nan

    x_const = sm.add_constant(x)
    model = sm.OLS(y, x_const, missing="drop").fit()

    # Sometimes only intercept exists
    if len(model.params) < 2:
        return np.nan

    return model.params.iloc[1]


def compute_spread(y: pd.Series, x: pd.Series, hedge_ratio: float) -> pd.Series:
    """
    Spread = y - hedge_ratio * x
    """
    return y - hedge_ratio * x


def compute_zscore(series: pd.Series, window: int) -> pd.Series:
    """
    Rolling z-score
    """
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    return (series - mean) / std


def rolling_correlation(y: pd.Series, x: pd.Series, window: int) -> pd.Series:
    """
    Rolling correlation
    """
    return y.rolling(window).corr(x)


def adf_pvalue(series: pd.Series) -> float:
    """
    Augmented Dickey-Fuller p-value
    """
    series = series.dropna()
    if len(series) < 20:
        return np.nan
    return adfuller(series)[1]
