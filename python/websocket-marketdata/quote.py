"""
Demonstrates:
- Subscribing to quote (BBO) updates

This example shows how to receive real-time quote data for multiple symbols.
"""

import asyncio
from datetime import datetime

from dnse import TradingClient
from dnse.websocket.models import Quote


async def main():
    # Initialize client
    encoding = "msgpack"  # json or msgpack
    client = TradingClient(
        api_key="api-key",
        api_secret="api-secret",
        base_url="wss://ws-openapi.dnse.com.vn",
        encoding=encoding,
    )

    def handle_quote(quote: Quote):
        received_at = datetime.fromtimestamp(quote.receivedAt).strftime("%H:%M:%S.%f")[:-3] if quote.receivedAt else "N/A"
        print(f"[{received_at}] QUOTE: {quote}")

    # Connect to gateway
    print("Connecting to WebSocket gateway...")
    await client.connect()
    print(f"Connected! Session ID: {client._session_id}\n")

    print("Subscribing to quotes for SSI and 41I1G4000...")
    await client.subscribe_quotes(["SSI", "41I1G4000"], on_quote=handle_quote, encoding=encoding, board_id="G1")

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
