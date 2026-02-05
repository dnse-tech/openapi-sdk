"""
Market data subscription example.

Demonstrates:
- Subscribing to trade extra updates

This example shows how to receive real-time market data for multiple symbols.
"""

import asyncio
from trading_websocket import TradingClient
import trading_websocket.models


async def main():
    # Initialize client
    encoding = "msgpack"  # json or msgpack
    client = TradingClient(
        api_key="api-key",
        api_secret="api-secret",
        base_url="wss://ws-openapi.dnse.com.vn",
        encoding=encoding,
    )

    def handle_trade_extra(trade: trading_websocket.models.TradeExtra):
        print(f"TRADE EXTRA: {trade}")

    # Connect to gateway
    print("Connecting to WebSocket gateway...")
    await client.connect()
    print(f"Connected! Session ID: {client._session_id}\n")

    print("Subscribing to trade extra for SSI and 41I1G2000...")
    await client.subscribe_trade_extra(["SSI", "41I1G2000"], on_trade_extra=handle_trade_extra, encoding=encoding)

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
