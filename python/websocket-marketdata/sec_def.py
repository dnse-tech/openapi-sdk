"""
Market data subscription example.

Demonstrates:
- Subscribing to security definition updates

This example shows how to receive real-time market data for multiple symbols.
"""

import asyncio
from trading_websocket import TradingClient
from trading_websocket.models import Trade, Quote, Bar, ExpectedPrice, TradeExtra, SecurityDefinition


async def main():
    # Initialize client
    encoding = "msgpack"  # json or msgpack
    client = TradingClient(
        api_key="api_key",
        api_secret="api_scret",
        base_url="wss://ws-openapi.dnse.com.vn",
        encoding=encoding,
    )

    def handle_security_definition(sec_def: SecurityDefinition):
        print(f"SECURITY DEFINITION: {sec_def}")

    # Connect to gateway
    print("Connecting to WebSocket gateway...")
    await client.connect()
    print(f"Connected! Session ID: {client._session_id}\n")

    print("Subscribing to security definition for SSI and 41I1G2000...")
    await client.subscribe_sec_def(["SSI", "41I1G2000"], on_sec_def=handle_security_definition, encoding=encoding)

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
