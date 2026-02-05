"""
Market data subscription example.

Demonstrates:
- Subscribing to OHLCV updates

This example shows how to receive real-time market data for multiple symbols.
"""

import asyncio

from trading_websocket import TradingClient
from trading_websocket.models import Ohlc


async def main():
    # Initialize client
    encoding = "msgpack"  # json or msgpack
    client = TradingClient(
        api_key="api-key",
        api_secret="api-secret",
        base_url="wss://ws-openapi.dnse.com.vn",
        encoding=encoding,
    )

    def handle_ohlc(ohlc: Ohlc):
        print(f"OHLC: {ohlc}")

    # Connect to gateway
    print("Connecting to WebSocket gateway...")
    await client.connect()
    print(f"Connected! Session ID: {client._session_id}\n")

    print("Subscribing to ohlc for SSI and 41I1G2000 and VN30...")
    # internal 1 3 5 15 30 1H 1D 1W
    await client.subscribe_ohlc(["SSI", "VN30F1M", "VN30"], resolution="1", on_ohlc=handle_ohlc, encoding=encoding)

    # Subscribe to 1-minute OHLC

    print("\nReceiving market data (will run for 1 hour)...\n")

    # Run for 8H to collect data
    # In a real application, you might run indefinitely or until a specific condition
    await asyncio.sleep(8 * 60 * 60)

    # Disconnect gracefully
    print("\n\nDisconnecting...")
    await client.disconnect()
    print("Disconnected!")


if __name__ == "__main__":
    asyncio.run(main())
