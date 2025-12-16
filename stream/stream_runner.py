# stream/stream_runner.py

import threading
import asyncio
from stream.websocket_client import stream_symbol


def _run_stream(symbols):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    tasks = [stream_symbol(symbol) for symbol in symbols]
    loop.run_until_complete(asyncio.gather(*tasks))


def start_background_stream(symbols):
    thread = threading.Thread(
        target=_run_stream,
        args=(symbols,),
        daemon=True
    )
    thread.start()
