"""
Position event subscription example.

This example shows how to receive real-time position event for stock and derivative
"""

import asyncio
from datetime import datetime

from dnse import TradingClient
from dnse.websocket.models import Position


async def main():
    # Initialize client
    encoding = "json"  # json or msgpack
    client = TradingClient(
        api_key="api-key",
        api_secret="api-secret",
        base_url="wss://ws-openapi.dnse.com.vn",
        encoding=encoding,
        )

    def handle_position(data: Position):
        received_at = datetime.fromtimestamp(data.receivedAt).strftime("%H:%M:%S.%f")[:-3] if data.receivedAt else "N/A"
        print(f"[{received_at}] Position: {data}")

    # Connect to gateway
    print("Connecting to WebSocket gateway...")
    await client.connect()
    print(f"Connected! Session ID: {client._session_id}\n")

    print("Subscribing to position event")
    # market_type: DERIVATIVE | STOCK
    await client.subscribe_position_event(market_type="STOCK",
                                          on_position_event=handle_position, encoding=encoding)

    print("\nReceiving position event (will run for 1 hour)...\n")

    # Run for 8H to collect data
    # In a real application, you might run indefinitely or until a specific condition
    await asyncio.sleep(8 * 60 * 60)

    # Disconnect gracefully
    print("\n\nDisconnecting...")
    await client.disconnect()
    print("Disconnected!")


if __name__ == "__main__":
    asyncio.run(main())
