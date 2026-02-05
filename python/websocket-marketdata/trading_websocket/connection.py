import asyncio
import logging
import ssl
from typing import Optional, AsyncIterator
import websockets
from websockets.client import WebSocketClientProtocol
from .exceptions import ConnectionError, ConnectionClosed

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class WebSocketConnection:
    """
    WebSocket connection manager with automatic reconnection.

    Features:
    - Exponential backoff reconnection
    - Connection health monitoring
    - Graceful shutdown
    """

    def __init__(
            self,
            url: str,
            timeout: float = 60.0,
            heartbeat_interval: float = 25.0,
            auto_reconnect: bool = True,
            max_retries: int = 10,
    ):
        """
        Initialize connection manager.

        Args:
            url: WebSocket URL
            timeout: Connection timeout (seconds)
            heartbeat_interval: Heartbeat interval (seconds)
            auto_reconnect: Enable automatic reconnection
            max_retries: Maximum reconnection attempts
        """
        self.url = url
        self.timeout = timeout
        self.heartbeat_interval = heartbeat_interval
        self.auto_reconnect = auto_reconnect
        self.max_retries = max_retries

        self._ws: Optional[WebSocketClientProtocol] = None
        self._retry_count = 0
        self._is_connected = False

    async def connect(self) -> None:
        """
        Establish WebSocket connection.

        Raises:
            ConnectionError: Failed to connect after max retries
            asyncio.TimeoutError: Connection timeout
        """
        while self._retry_count < self.max_retries:
            try:
                logger.info(f"Connecting to {self.url} (attempt {self._retry_count + 1}/{self.max_retries})")
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                self._ws = await asyncio.wait_for(
                    websockets.connect(self.url,
                                       ssl=ssl_context,
                                       ping_interval=30,
                                       ping_timeout=30,
                                       close_timeout=10,
                                       max_queue=None), timeout=self.timeout)

                self._is_connected = True
                self._retry_count = 0
                logger.info("Connected successfully")
                return

            except (websockets.exceptions.WebSocketException, OSError) as e:
                self._retry_count += 1

                if self._retry_count >= self.max_retries:
                    raise ConnectionError(f"Failed to connect after {self.max_retries} attempts: {e}")

                # Exponential backoff: 1s, 2s, 4s, 8s, ... up to 60s
                delay = min(2 ** (self._retry_count - 1), 60)
                logger.warning(f"Connection failed: {e}. Retrying in {delay}s...")
                await asyncio.sleep(delay)

    async def send(self, message: bytes) -> None:
        if not self._ws or not self._is_connected:
            raise ConnectionError("Not connected")

        await self._ws.send(message)

    async def receive(self) -> bytes:
        if not self._ws or not self._is_connected:
            raise ConnectionError("Not connected")

        try:
            message = await self._ws.recv()
            return message if isinstance(message, bytes) else message.encode()
        except websockets.exceptions.ConnectionClosed as e:
            self._is_connected = False

            # Handle different close codes
            if e.code in (1000, 1001):  # Normal closure, going away
                logger.info(f"Connection closed normally: {e.code}")
                raise ConnectionClosed(f"Connection closed normally: {e}")
            elif e.code in (1006, 1011, 1012):  # Abnormal, server error, restart
                logger.warning(f"Connection closed abnormally: {e.code}")
                if self.auto_reconnect:
                    # Reconnection will be handled by caller
                    raise ConnectionClosed(f"Connection closed abnormally: {e}", recoverable=True)
                else:
                    raise ConnectionClosed(f"Connection closed abnormally: {e}")
            else:
                logger.error(f"Connection closed with unexpected code: {e.code}")
                raise ConnectionClosed(f"Connection closed: {e}")

    async def close(self) -> None:
        """Close connection gracefully"""
        if self._ws:
            await self._ws.close()

        self._is_connected = False
        logger.info("Connection closed")

    @property
    def is_connected(self) -> bool:
        """Check if connection is active"""
        return self._is_connected and self._ws is not None

    def __aiter__(self) -> AsyncIterator[bytes]:
        """Allow async iteration over messages"""
        return self

    async def __anext__(self) -> bytes:
        """Get next message"""
        try:
            return await self.receive()
        except ConnectionClosed:
            raise StopAsyncIteration
