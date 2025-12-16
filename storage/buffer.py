# storage/buffer.py

from collections import deque
import threading

# Keep last N ticks per symbol
MAX_TICKS = 2000

_buffers = {}
_lock = threading.Lock()


def add_tick(symbol: str, tick: dict):
    """
    Add a tick to the in-memory buffer.
    """
    with _lock:
        if symbol not in _buffers:
            _buffers[symbol] = deque(maxlen=MAX_TICKS)

        _buffers[symbol].append(tick)


def get_ticks(symbol: str):
    """
    Return buffered ticks for a symbol.
    """
    with _lock:
        if symbol not in _buffers:
            return []

        return list(_buffers[symbol])
