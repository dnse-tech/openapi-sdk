"""
Market index subscription example.

Demonstrates:
- Subscribing to market index

This example shows how to receive real-time market index
"""

import asyncio

from dnse import TradingClient
from dnse.websocket.models import MarketIndex
from datetime import datetime


async def main():
    # Initialize client
    encoding = "msgpack"  # json or msgpack
    client = TradingClient(
        api_key="api-key",
        api_secret="api-secret",
        base_url="wss://ws-openapi.dnse.com.vn",
        encoding=encoding,
    )

    def handle_market_index(data: MarketIndex):
        received_at = datetime.fromtimestamp(data.receivedAt).strftime("%H:%M:%S.%f")[:-3] if data.receivedAt else "N/A"
        print(f"[{received_at}] Market index: {data}")

    # Connect to gateway
    print("Connecting to WebSocket gateway...")
    await client.connect()
    print(f"Connected! Session ID: {client._session_id}\n")

    print("Subscribing to market index...")
    await client.subscribe_market_index(market_index='HNX', on_market_index=handle_market_index, encoding=encoding)

    print("\nReceiving market index (will run for 1 hour)...\n")

    # Run for 1H to collect data
    # In a real application, you might run indefinitely or until a specific condition
    await asyncio.sleep(8 * 60 * 60)

    # Disconnect gracefully
    print("\n\nDisconnecting...")
    await client.disconnect()
    print("Disconnected!")


if __name__ == "__main__":
    asyncio.run(main())
