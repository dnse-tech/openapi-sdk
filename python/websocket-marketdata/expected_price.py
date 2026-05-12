"""
Market data subscription example.

Demonstrates:
- Subscribing to expected price updates

This example shows how to receive real-time market data for multiple symbols.
"""

import asyncio
from datetime import datetime

from dnse import TradingClient
from dnse.websocket.models import ExpectedPrice


async def main():
    # Initialize client
    encoding = "msgpack"  # json or msgpack
    client = TradingClient(
        api_key="api-key",
        api_secret="api-secret",
        base_url="wss://ws-openapi.dnse.com.vn",
        encoding=encoding,
    )

    def handle_expected_price(expected_price: ExpectedPrice):
        received_at = datetime.fromtimestamp(expected_price.receivedAt).strftime("%H:%M:%S.%f")[:-3] if expected_price.receivedAt else "N/A"
        print(f"[{received_at}] EXPECTED PRICE: {expected_price}")

    # Connect to gateway
    print("Connecting to WebSocket gateway...")
    await client.connect()
    print(f"Connected! Session ID: {client._session_id}\n")

    print("Subscribing to expected price for SSI and 41I1G4000...")
    await client.subscribe_expected_price(["SSI", "41I1G4000"],
                                          on_expected_price=handle_expected_price, encoding=encoding, board_id="G1")

    print("\nReceiving market data (will run for 1 hour)...\n")

    # Run for 1H to collect data
    # In a real application, you might run indefinitely or until a specific condition
    await asyncio.sleep(60 * 60 * 8)

    # Disconnect gracefully
    print("\n\nDisconnecting...")
    await client.disconnect()
    print("Disconnected!")


if __name__ == "__main__":
    asyncio.run(main())
