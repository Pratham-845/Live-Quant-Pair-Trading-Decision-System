# stream/websocket_client.py

import asyncio
import json
import websockets
from storage.database import insert_tick

BINANCE_WS = "wss://fstream.binance.com/ws"


async def stream_symbol(symbol: str):
    url = f"{BINANCE_WS}/{symbol}@trade"

    while True:
        try:
            async with websockets.connect(
                url,
                ping_interval=15,
                ping_timeout=10,
            ) as ws:

                print(f"[WS] Connected: {symbol}")

                async for msg in ws:
                    data = json.loads(msg)

                    insert_tick(
                        symbol=symbol,
                        ts=data["T"],
                        price=float(data["p"]),
                        qty=float(data["q"]),
                    )

        except Exception as e:
            print(f"[WS] {symbol} disconnected: {e}")
            await asyncio.sleep(3)
