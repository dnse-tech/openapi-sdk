"""
Market data subscription example.

Demonstrates:
- Subscribing to OHLCV bar updates

This example shows how to receive real-time market data for multiple symbols.
"""

import asyncio
from trading_websocket import TradingClient
from trading_websocket.models import Trade, Quote, Bar, ExpectedPrice, TradeExtra, SecurityDefinition


async def main():
    # Initialize client
    encoding = "msgpack"  # json or msgpack
    client = TradingClient(
        api_key="eyJvcmciOiJkbnNlIiwiaWQiOiIyYmRkMTRkYzAyZGI0NDhhOTMyNDE4MzI4YWU3ZGNiMiIsImgiOiJtdXJtdXIxMjgifQ==",
        api_secret="-xVyfXfkYQpXz29H-P3XD0bnzeyPHdyMIMT0VzwNxmCYI9clVJSq5uZooRD4v9Q0UwBIw8TA5XFvhP5vIamF-g",
        base_url="wss://ws-openapi-uat.dnse.com.vn",
        encoding=encoding,
    )

    def handle_bar(bar: Bar):
        print(f"BAR: {bar}")

    # Connect to gateway
    print("Connecting to WebSocket gateway...")
    await client.connect()
    print(f"Connected! Session ID: {client._session_id}\n")

    print("Subscribing to bar for SSI and 41I1G2000...")
    # internal 1 3 5 15 30 45 1H 4H 1D 1W
    await client.subscribe_bars(["SSI", "41I1G2000"], resolution="1", on_bar=handle_bar, encoding=encoding)

    # Subscribe to 1-minute OHLCV bars
    # Bars aggregate trade data into time intervals
    # print("Subscribing to 1-minute bars for TSLA...")
    # await client.subscribe_bars(["TSLA"], interval="1m", on_bar=handle_bar)

    print("\nReceiving market data (will run for 1 hour)...\n")

    # Run for 60 seconds to collect data
    # In a real application, you might run indefinitely or until a specific condition
    await asyncio.sleep(60 * 60)

    # Disconnect gracefully
    print("\n\nDisconnecting...")
    await client.disconnect()
    print("Disconnected!")


if __name__ == "__main__":
    asyncio.run(main())
