"""
Market data subscription example.

Demonstrates:
- Subscribing to trade updates

This example shows how to receive real-time market data for multiple symbols.
"""

import asyncio
from trading_websocket import TradingClient
from trading_websocket.models import Trade, Quote, Bar, ExpectedPrice, TradeExtra, SecurityDefinition


async def main():
    # Initialize client
    encoding = "msgpack"  # json or msgpack
    client = TradingClient(
        api_key="eyJvcmciOiJkbnNlIiwiaWQiOiJiYWMwNWY3OThmOTU0OWQ5YmNiOTYyNzQ3YzY3NzRlYSIsImgiOiJtdXJtdXIxMjgifQ==",
        api_secret="D5KLFhyAV-qMffog5i6TRRHXxLv86Y8ozWUQkUeh6BCZ2WdN-OUoMk-kn5L-3ROZX0K4zdDQCYy5hrPGhjOl2w",
        base_url="wss://ws-openapi-uat.dnse.com.vn",
        encoding=encoding,
    )

    def handle_trade(trade: Trade):
        print(f"TRADE: {trade}")

    # Connect to gateway
    print("Connecting to WebSocket gateway...")
    await client.connect()
    print(f"Connected! Session ID: {client._session_id}\n")

    print("Subscribing to trades for SSI and 41I1G2000...")
    await client.subscribe_trades(["SSI", "41I1G2000"], on_trade=handle_trade, encoding=encoding)

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
