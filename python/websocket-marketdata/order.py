"""
Order event subscription example.

This example shows how to receive real-time order event for stock and derivative orders
"""

import asyncio
from datetime import datetime

from trading_websocket import TradingClient
from trading_websocket.models import Order


async def main():
    # Initialize client
    encoding = "json"  # json or msgpack
    client = TradingClient(
        api_key="api-key",
        api_secret="api-secret",
        base_url="wss://ws-openapi.dnse.com.vn",
        encoding=encoding,
    )

    def handle_order(data: Order):
        received_at = datetime.fromtimestamp(data.receivedAt).strftime("%H:%M:%S.%f")[:-3] if data.receivedAt else "N/A"
        print(f"[{received_at}] Order: {data}")

    # Connect to gateway
    print("Connecting to WebSocket gateway...")
    await client.connect()
    print(f"Connected! Session ID: {client._session_id}\n")

    print("Subscribing to order event")
    # market_type: DERIVATIVE | STOCK
    await client.subscribe_order_event(market_type="STOCK",
                                       on_order_event=handle_order, encoding=encoding)

    print("\nReceiving order event (will run for 1 hour)...\n")

    # Run for 8H to collect data
    # In a real application, you might run indefinitely or until a specific condition
    await asyncio.sleep(8 * 60 * 60)

    # Disconnect gracefully
    print("\n\nDisconnecting...")
    await client.disconnect()
    print("Disconnected!")


if __name__ == "__main__":
    asyncio.run(main())
