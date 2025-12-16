# config.py

# Symbols to stream (same as provided HTML)
SYMBOLS = ["btcusdt", "ethusdt"]

# Resampling timeframes (seconds)
TIMEFRAMES = {
    "1S": 1,
    "1T": 60,
    "5T": 300
}

# Frontend refresh interval (milliseconds)
UI_REFRESH_MS = 500

# Rolling window defaults
DEFAULT_ROLLING_WINDOW = 60

# Z-score alert threshold
DEFAULT_Z_THRESHOLD = 2.0

# SQLite database file
DB_PATH = "ticks.db"
