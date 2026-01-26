"""
TradingClient - High-level async WebSocket client for real-time trading data.

This module provides the main TradingClient class that handles:
- WebSocket connection management with automatic reconnection
- HMAC authentication
- Channel subscriptions (market data and private channels)
- Event-driven message handling
- Heartbeat monitoring
- Graceful shutdown
"""

from typing import Optional, Callable, List, Dict, Any
import asyncio
import logging
import time
from .connection import WebSocketConnection
from .auth import AuthManager
from .encoding import MessageEncoder, MessageDecoder
from .models import Trade, Quote, Bar, Order, Position, AccountUpdate, ExpectedPrice, SecurityDefinition, TradeExtra
from .exceptions import (
    AuthenticationError,
    ConnectionError,
    SubscriptionError,
    ConnectionClosed,
)

logger = logging.getLogger(__name__)


class TradingClient:
    """
    Async WebSocket client for real-time trading data.

    Features:
    - Automatic reconnection with re-authentication and re-subscription
    - HMAC-SHA256 authentication
    - Support for JSON and MessagePack encoding
    - Event-driven architecture with callback handlers
    - Heartbeat monitoring with pong tracking
    - Context manager support (async with)
    - Async iterator support (async for)
    """

    def __init__(
            self,
            api_key: str,
            api_secret: str,
            base_url: str = "wss://ws-openapi-uat.dnse.com.vn",
            encoding: str = "json",  # or "json"
            auto_reconnect: bool = True,
            max_retries: int = 10,
            heartbeat_interval: float = 25.0,
            timeout: float = 60.0,
    ):
        """
        Initialize trading client.

        Args:
            api_key: API key for authentication
            api_secret: API secret for HMAC signature
            base_url: WebSocket gateway URL
            encoding: Message encoding ("json" or "msgpack")
            auto_reconnect: Enable automatic reconnection
            max_retries: Maximum reconnection attempts
            heartbeat_interval: Seconds between heartbeat pings
            timeout: Connection timeout in seconds
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.encoding = encoding
        self.auto_reconnect = auto_reconnect
        self.max_retries = max_retries
        self.heartbeat_interval = heartbeat_interval
        self.timeout = timeout

        # Internal state
        self._connection: Optional[WebSocketConnection] = None
        self._auth_manager = AuthManager(api_key, api_secret)
        self._encoder = MessageEncoder(encoding)
        self._decoder = MessageDecoder(encoding)
        self._event_handlers: Dict[str, List[Callable]] = {}
        self._subscriptions: Dict[str, Dict[str, Any]] = {}  # channel -> {symbols, kwargs}
        self._is_authenticated = False
        self._session_id: Optional[str] = None
        self._message_queue: asyncio.Queue = asyncio.Queue()
        self._is_running = False
        self._last_pong_time: float = 0.0
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._message_handler_task: Optional[asyncio.Task] = None

    async def connect(self) -> None:
        """
        Establish WebSocket connection and authenticate.

        Raises:
            ConnectionError: Failed to connect
            AuthenticationError: Authentication failed
            asyncio.TimeoutError: Connection timeout
        """
        url = f"{self.base_url}/v1/stream?encoding={self.encoding}"

        logger.info(f"Connecting to {url}")

        self._connection = WebSocketConnection(
            url=url,
            timeout=self.timeout,
            heartbeat_interval=self.heartbeat_interval,
            auto_reconnect=self.auto_reconnect,
            max_retries=self.max_retries,
        )

        await self._connection.connect()

        # Wait for welcome message
        welcome = await asyncio.wait_for(
            self._connection.receive(), timeout=self.timeout
        )

        welcome_data = self._decoder.decode(welcome)
        self._session_id = welcome_data.get("session_id") or welcome_data.get("sid")

        logger.info(f"Connected! Session ID: {self._session_id}")

        # Authenticate
        await self._authenticate()

        # Start background tasks
        self._is_running = True
        self._last_pong_time = time.time()

        # Start message handler
        self._message_handler_task = asyncio.create_task(self._message_handler())

        # Start heartbeat
        if self.heartbeat_interval > 0:
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

    async def _authenticate(self) -> None:
        """
        Perform HMAC authentication.

        Raises:
            AuthenticationError: Authentication failed
            asyncio.TimeoutError: Authentication timeout
        """
        auth_msg = self._auth_manager.create_auth_message()
        encoded = self._encoder.encode(auth_msg)

        await self._connection.send(encoded)

        # Wait for auth response
        response = await asyncio.wait_for(
            self._connection.receive(), timeout=self.timeout
        )

        data = self._decoder.decode(response)
        action = data.get("action") or data.get("a")

        if action == "auth_success":
            self._is_authenticated = True
            logger.info("Authentication successful")
        elif action in ("auth_error", "error"):
            error_msg = data.get("message") or data.get("msg", "Unknown error")
            raise AuthenticationError(f"Authentication failed: {error_msg}")
        else:
            raise AuthenticationError(f"Unexpected response: {action}")

    async def subscribe_trades(
            self, symbols: List[str], on_trade: Optional[Callable[[Trade], None]] = None, encoding="json"
    ) -> None:
        channel = "tick.G1.json"
        if encoding == "msgpack":
            channel = "tick.G1.msgpack"
        await self._subscribe_channel(channel, symbols)

        if on_trade:
            self.on("trade", on_trade)

    async def subscribe_trade_extra(
            self, symbols: List[str], on_trade_extra: Optional[Callable[[TradeExtra], None]] = None, encoding="json"
    ) -> None:
        channel = "tick_extra.G1.json"
        if encoding == "msgpack":
            channel = "tick_extra.G1.msgpack"
        await self._subscribe_channel(channel, symbols)

        if on_trade_extra:
            self.on("trade_extra", on_trade_extra)

    async def subscribe_expected_price(
            self, symbols: List[str], on_expected_price: Optional[Callable[[ExpectedPrice], None]] = None,
            encoding="json"
    ) -> None:
        channel = "expected_price.G1.json"
        if encoding == "msgpack":
            channel = "expected_price.G1.msgpack"
        await self._subscribe_channel(channel, symbols)

        if on_expected_price:
            self.on("expected_price", on_expected_price)

    async def subscribe_sec_def(
            self, symbols: List[str], on_sec_def: Optional[Callable[[SecurityDefinition], None]] = None, encoding="json"
    ) -> None:
        channel = "security_definition.G1.json"
        if encoding == "msgpack":
            channel = "security_definition.G1.msgpack"
        await self._subscribe_channel(channel, symbols)

        if on_sec_def:
            self.on("security_definition", on_sec_def)

    async def subscribe_quotes(
            self, symbols: List[str], on_quote: Optional[Callable[[Quote], None]] = None, encoding="json"
    ) -> None:
        channel = "top_price.G1.json"
        if encoding == "msgpack":
            channel = "top_price.G1.msgpack"
        await self._subscribe_channel(channel, symbols)

        if on_quote:
            self.on("quote", on_quote)

    async def subscribe_bars(
            self,
            symbols: List[str],
            resolution: str = "1m",
            on_bar: Optional[Callable[[Bar], None]] = None, encoding="json"
    ) -> None:
        channel = "ohlc." + resolution + ".json"
        if encoding == "msgpack":
            channel = "ohlc." + resolution + ".msgpack"
        await self._subscribe_channel(channel, symbols)

        if on_bar:
            self.on("bar", on_bar)

    async def subscribe_orders(
            self, on_order: Optional[Callable[[Order], None]] = None
    ) -> None:
        await self._subscribe_channel("orders", [])

        if on_order:
            self.on("order", on_order)

    async def subscribe_positions(
            self, on_position: Optional[Callable[[Position], None]] = None
    ) -> None:

        await self._subscribe_channel("positions", [])

        if on_position:
            self.on("position", on_position)

    async def subscribe_account(
            self, on_account: Optional[Callable[[AccountUpdate], None]] = None
    ) -> None:
        await self._subscribe_channel("account", [])

        if on_account:
            self.on("account", on_account)

    async def _subscribe_channel(
            self, channel: str, symbols: List[str], **kwargs
    ) -> None:
        if not self._is_authenticated:
            raise SubscriptionError("Must authenticate before subscribing")

        subscribe_msg = {
            "action": "subscribe",
            "channels": [{"name": channel, "symbols": symbols, **kwargs}],
        }

        encoded = self._encoder.encode(subscribe_msg)
        await self._connection.send(encoded)

        # Store subscription for reconnection
        self._subscriptions[channel] = {"symbols": symbols, "kwargs": kwargs}

        logger.info(f"Subscribed to {channel}: {symbols}")

    async def unsubscribe(self, channel: str, symbols: List[str]) -> None:
        unsubscribe_msg = {
            "action": "unsubscribe",
            "channels": [{"name": channel, "symbols": symbols}],
        }

        encoded = self._encoder.encode(unsubscribe_msg)
        await self._connection.send(encoded)

        # Update local state
        if channel in self._subscriptions:
            stored_symbols = self._subscriptions[channel].get("symbols", [])
            for symbol in symbols:
                if symbol in stored_symbols:
                    stored_symbols.remove(symbol)

            # Remove channel if no symbols left
            if not stored_symbols:
                del self._subscriptions[channel]

        logger.info(f"Unsubscribed from {channel}: {symbols}")

    def on(self, event: str, handler: Callable) -> None:
        if event not in self._event_handlers:
            self._event_handlers[event] = []
        self._event_handlers[event].append(handler)

    async def _message_handler(self) -> None:
        while self._is_running:
            try:
                async for message in self._connection:
                    data = self._decoder.decode(message)
                    await self._dispatch_message(data)
            except ConnectionClosed as e:
                logger.warning(f"Connection closed: {e}")

                # Handle reconnection if enabled and error is recoverable
                if self.auto_reconnect and e.recoverable:
                    logger.info("Attempting to reconnect...")
                    try:
                        await self._handle_reconnection()
                    except Exception as reconnect_error:
                        logger.error(f"Reconnection failed: {reconnect_error}")
                        self._emit("error", reconnect_error)
                        break
                else:
                    self._emit("error", e)
                    break
            except Exception as e:
                logger.error(f"Message handler error: {e}")
                self._emit("error", e)

                # Only retry if auto_reconnect is enabled
                if not self.auto_reconnect:
                    break

    async def _dispatch_message(self, data: Dict[str, Any]) -> None:
        """
        Route message to appropriate handler.

        Args:
            data: Decoded message data
        """
        action = data.get("action") or data.get("a")
        msg_type = data.get("T")  # MessagePack type field

        if action == "subscribed":
            logger.debug(f"Subscription confirmed: {data}")
        elif action == "pong":
            # Update pong timestamp for health monitoring
            self._last_pong_time = time.time()
            logger.debug("Received pong")
        elif action == "error":
            error_msg = data.get("message") or data.get("msg")
            logger.error(f"Server error: {error_msg}")
            self._emit("error", Exception(error_msg))
        elif msg_type == "t":  # Trade
            trade = Trade.from_dict(data)
            self._emit("trade", trade)
            await self._message_queue.put(trade)
        elif msg_type == "te":  # Trade Extra
            trade = TradeExtra.from_dict(data)
            self._emit("trade_extra", trade)
            await self._message_queue.put(trade)
        elif msg_type == "e":  # Expected Price
            expectedPrice = ExpectedPrice.from_dict(data)
            self._emit("expected_price", expectedPrice)
            await self._message_queue.put(expectedPrice)
        elif msg_type == "sd":  # Security Definition
            securityDefinition = SecurityDefinition.from_dict(data)
            self._emit("security_definition", securityDefinition)
            await self._message_queue.put(securityDefinition)
        elif msg_type == "q":  # Quote
            quote = Quote.from_dict(data)
            self._emit("quote", quote)
            await self._message_queue.put(quote)
        elif msg_type == "b":  # Bar
            bar = Bar.from_dict(data)
            self._emit("bar", bar)
            await self._message_queue.put(bar)
        elif msg_type == "o":  # Order
            order = Order.from_dict(data)
            self._emit("order", order)
            await self._message_queue.put(order)
        elif msg_type == "p":  # Position
            position = Position.from_dict(data)
            self._emit("position", position)
            await self._message_queue.put(position)
        elif msg_type == "a":  # Account
            account = AccountUpdate.from_dict(data)
            self._emit("account", account)
            await self._message_queue.put(account)

    def _emit(self, event: str, data: Any) -> None:
        """
        Call all registered handlers for event.

        Args:
            event: Event name
            data: Event data
        """
        if event in self._event_handlers:
            for handler in self._event_handlers[event]:
                try:
                    # Support both sync and async handlers
                    if asyncio.iscoroutinefunction(handler):
                        asyncio.create_task(handler(data))
                    else:
                        handler(data)
                except Exception as e:
                    logger.error(f"Handler error for {event}: {e}")

    async def _heartbeat_loop(self) -> None:
        while self._is_running and self._connection and self._connection.is_connected:
            try:
                ping_msg = self._encoder.encode({"action": "ping"})
                await self._connection.send(ping_msg)
                logger.debug("Sent heartbeat ping")
                await asyncio.sleep(self.heartbeat_interval)
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                break

    async def _handle_reconnection(self) -> None:
        """
        Handle reconnection after connection drop.

        Performs:
        1. Re-establish connection
        2. Re-authenticate
        3. Re-subscribe to all previous channels
        4. Emit reconnected event
        """
        logger.info("Starting reconnection process...")

        # Store subscriptions before reconnect
        previous_subscriptions = self._subscriptions.copy()

        # Reset authentication state
        self._is_authenticated = False

        # Reconnect
        await self._connection.connect()

        # Wait for welcome message
        welcome = await asyncio.wait_for(
            self._connection.receive(), timeout=self.timeout
        )

        welcome_data = self._decoder.decode(welcome)
        self._session_id = welcome_data.get("session_id") or welcome_data.get("sid")

        logger.info(f"Reconnected! New Session ID: {self._session_id}")

        # Re-authenticate
        await self._authenticate()

        # Re-subscribe to all previous channels
        for channel, sub_data in previous_subscriptions.items():
            symbols = sub_data.get("symbols", [])
            kwargs = sub_data.get("kwargs", {})
            await self._subscribe_channel(channel, symbols, **kwargs)
            logger.info(f"Re-subscribed to {channel}: {symbols}")

        # Update pong time
        self._last_pong_time = time.time()

        # Emit reconnected event
        self._emit("reconnected", {"session_id": self._session_id})
        logger.info("Reconnection complete")

    @property
    def is_healthy(self) -> bool:
        if not self._connection or not self._connection.is_connected:
            return False

        if not self._is_authenticated:
            return False

        # Check if we received a pong recently
        if self.heartbeat_interval > 0:
            time_since_pong = time.time() - self._last_pong_time
            max_pong_delay = self.heartbeat_interval * 2
            if time_since_pong > max_pong_delay:
                logger.warning(
                    f"No pong received for {time_since_pong:.1f}s (max: {max_pong_delay:.1f}s)"
                )
                return False

        return True

    async def disconnect(self) -> None:
        """
        Close connection gracefully.

        Stops all background tasks and closes the WebSocket connection.
        """
        logger.info("Disconnecting...")

        # Stop background tasks
        self._is_running = False

        # Cancel tasks
        if self._heartbeat_task and not self._heartbeat_task.done():
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass

        if self._message_handler_task and not self._message_handler_task.done():
            self._message_handler_task.cancel()
            try:
                await self._message_handler_task
            except asyncio.CancelledError:
                pass

        # Close connection
        if self._connection:
            await self._connection.close()

        self._is_authenticated = False
        logger.info("Disconnected")

    async def __aenter__(self):
        """Context manager support - connect on entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup - disconnect on exit."""
        await self.disconnect()

    def __aiter__(self):
        """Allow async iteration over messages."""
        return self

    async def __anext__(self):
        if not self._is_running:
            raise StopAsyncIteration

        try:
            # Wait for next message with timeout to allow checking _is_running
            message = await asyncio.wait_for(self._message_queue.get(), timeout=1.0)
            return message
        except asyncio.TimeoutError:
            # Check if still running
            if self._is_running:
                # Retry
                return await self.__anext__()
            else:
                raise StopAsyncIteration
