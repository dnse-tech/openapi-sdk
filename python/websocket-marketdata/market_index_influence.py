"""
Market Index influence subscription example.

Demonstrates:
- Subscribing to market index influence

This example shows how to receive real-time index influence
"""

import asyncio

from dnse import TradingClient
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

    def handle_market_index_influence(data):
        received_at = datetime.fromtimestamp(data.receivedAt).strftime("%H:%M:%S.%f")[:-3] if data.receivedAt else "N/A"
        print(f"[{received_at}] Market Index influence: {data}")

    # Connect to gateway
    print("Connecting to WebSocket gateway...")
    await client.connect()
    print(f"Connected! Session ID: {client._session_id}\n")

    print("Subscribing to market index influence...")
    await client.subscribe_market_index_influence(index_name='VN30', resolution=1, on_market_index_influence=handle_market_index_influence, encoding=encoding)

    print("\nReceiving market index influence (will run for 1 hour)...\n")

    # Run for 8H to collect data
    # In a real application, you might run indefinitely or until a specific condition
    await asyncio.sleep(8 * 60 * 60)

    # Disconnect gracefully
    print("\n\nDisconnecting...")
    await client.disconnect()
    print("Disconnected!")


if __name__ == "__main__":
    asyncio.run(main())
