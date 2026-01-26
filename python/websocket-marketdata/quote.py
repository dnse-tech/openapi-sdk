"""
Demonstrates:
- Subscribing to quote (BBO) updates

This example shows how to receive real-time quote data for multiple symbols.
"""

import asyncio
from trading_websocket import TradingClient
from trading_websocket.models import Trade, Quote, Bar, ExpectedPrice, TradeExtra, SecurityDefinition


async def main():
    # Initialize client
    encoding = "msgpack"  # json or msgpack
    client = TradingClient(
        api_key="api_key",
        api_secret="api_secret",
        base_url="wss://ws-openapi.dnse.com.vn",
        encoding=encoding,
    )

    def handle_quote(quote: Quote):
        print(f"QUOTE: {quote}")

    # Connect to gateway
    print("Connecting to WebSocket gateway...")
    await client.connect()
    print(f"Connected! Session ID: {client._session_id}\n")

    print("Subscribing to quotes for SSI and 41I1G2000...")
    await client.subscribe_quotes(["SSI", "41I1G2000"], on_quote=handle_quote, encoding=encoding)

    print("\nReceiving market data (will run for 1 hour)...\n")

    # Run for 1H to collect data
    # In a real application, you might run indefinitely or until a specific condition
    await asyncio.sleep(60 * 60)

    # Disconnect gracefully
    print("\n\nDisconnecting...")
    await client.disconnect()
    print("Disconnected!")


if __name__ == "__main__":
    asyncio.run(main())
