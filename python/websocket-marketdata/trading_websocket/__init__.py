"""Trading WebSocket SDK for Python.

Async Python client for real-time trading data via WebSocket.
"""

from .client import TradingClient
from .models import Trade, Quote, Ohlc, Order, Position, AccountUpdate
from .exceptions import (
    TradingWebSocketError,
    ConnectionError,
    ConnectionClosed,
    AuthenticationError,
    SubscriptionError,
    EncodingError,
)

__version__ = "1.0.0"

__all__ = [
    "TradingClient",
    "Trade",
    "Quote",
    "Ohlc",
    "Order",
    "Position",
    "AccountUpdate",
    "TradingWebSocketError",
    "ConnectionError",
    "ConnectionClosed",
    "AuthenticationError",
    "SubscriptionError",
    "EncodingError",
]
