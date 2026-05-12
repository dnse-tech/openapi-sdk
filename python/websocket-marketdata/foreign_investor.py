"""
Demonstrates:
- Subscribing to foreigner trading

This example shows how to receive real-time foreigner trading data
"""

import asyncio
from datetime import datetime

from dnse import TradingClient
from dnse.websocket.models import ForeignInvestor


async def main():
    # Initialize client
    encoding = "json"  # json or msgpack
    client = TradingClient(
        api_key="api-key",
        api_secret="api-secret",
        base_url="wss://ws-openapi.dnse.com.vn",
        encoding=encoding,
    )

    def handle_foreign_trading(data: ForeignInvestor):
        received_at = datetime.fromtimestamp(data.receivedAt).strftime("%H:%M:%S.%f")[:-3] if data.receivedAt else "N/A"
        print(f"[{received_at}] Foreign trading: {data}")

    # Connect to gateway
    print("Connecting to WebSocket gateway...")
    await client.connect()
    print(f"Connected! Session ID: {client._session_id}\n")

    print("Subscribing to foreigner trading...")
    await client.subscribe_foreign_trading(["HPG", "FPT"], board_id="G1", on_trade=handle_foreign_trading,
                                           encoding=encoding)

    print("\nReceiving foreigner trading data (will run for 8 hour)...\n")

    # Run for 8H to collect data
    # In a real application, you might run indefinitely or until a specific condition
    await asyncio.sleep(60 * 60 * 8)

    # Disconnect gracefully
    print("\n\nDisconnecting...")
    await client.disconnect()
    print("Disconnected!")


if __name__ == "__main__":
    asyncio.run(main())
