"""Data models for market data and private channel updates.

This module provides typed data models for all message types:
- Market data: Trade, Quote, Bar
- Private channels: Order, Position, AccountUpdate

All models support parsing from both abbreviated (MessagePack) and full (JSON) field names.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from decimal import Decimal


@dataclass
class PriceLevel:
    price: float
    quantity: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PriceLevel":
        return cls(
            price=data.get("p") or data.get("Price"),
            quantity=data.get("q") or data.get("Qtty")
        )


@dataclass
class Trade:
    marketId: int
    boardId: int
    isin: str
    symbol: str
    price: float
    quantity: int
    totalVolumeTraded: int
    grossTradeAmount: float
    highestPrice: float
    lowestPrice: float
    openPrice: float
    tradingSessionId: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Trade":
        return cls(
            marketId=data.get("market_id", 0) or data.get("mi", 0),
            boardId=data.get("board_id", 0) or data.get("bi", 0),
            isin=data.get("isin", 0) or data.get("is", 0),
            symbol=data.get("s") or data.get("symbol"),
            price=data.get("p", 0.0) or data.get("match_price", 0.0),
            quantity=data.get("q", 0) or data.get("match_qtty", 0),
            totalVolumeTraded=data.get("tvt", 0) or data.get("total_volume_traded", 0),
            grossTradeAmount=data.get("gta", 0) or data.get("gross_trade_amount", 0),
            highestPrice=data.get("hp", 0) or data.get("highest_price", 0),
            lowestPrice=data.get("lp", 0) or data.get("lowest_price", 0),
            openPrice=data.get("op", 0) or data.get("open_price", 0),
            tradingSessionId=data.get("tsi", 0) or data.get("trading_session_id", 0),
        )


@dataclass
class TradeExtra:
    marketId: int
    boardId: int
    isin: str
    symbol: str
    price: float
    quantity: int
    side: int
    avgPrice: float
    totalVolumeTraded: int
    grossTradeAmount: float
    highestPrice: float
    lowestPrice: float
    openPrice: float
    tradingSessionId: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TradeExtra":
        return cls(
            marketId=data.get("market_id", 0) or data.get("mi", 0),
            boardId=data.get("board_id", 0) or data.get("bi", 0),
            isin=data.get("isin", 0) or data.get("is", 0),
            symbol=data.get("s") or data.get("symbol"),
            price=data.get("p", 0.0) or data.get("match_price", 0.0),
            quantity=data.get("q", 0) or data.get("match_qtty", 0),
            side=data.get("si", 0) or data.get("side", 0),
            avgPrice=data.get("ap", 0) or data.get("avg_price", 0),
            totalVolumeTraded=data.get("tvt", 0) or data.get("total_volume_traded", 0),
            grossTradeAmount=data.get("gta", 0) or data.get("gross_trade_amount", 0),
            highestPrice=data.get("hp", 0) or data.get("highest_price", 0),
            lowestPrice=data.get("lp", 0) or data.get("lowest_price", 0),
            openPrice=data.get("op", 0) or data.get("open_price", 0),
            tradingSessionId=data.get("tsi", 0) or data.get("trading_session_id", 0),
        )


@dataclass
class ExpectedPrice:
    marketId: int
    boardId: int
    isin: str
    symbol: str
    closePrice: float
    expectedTradePrice: float
    expectedTradeQuantity: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExpectedPrice":
        return cls(
            marketId=data.get("market_id", 0) or data.get("mi", 0),
            boardId=data.get("board_id", 0) or data.get("bi", 0),
            isin=data.get("isin", 0) or data.get("is", 0),
            symbol=data.get("s") or data.get("symbol"),
            closePrice=data.get("close_price", 0.0) or data.get("cp", 0),
            expectedTradePrice=data.get("expected_trade_price", 0.0) or data.get("etp", 0.0),
            expectedTradeQuantity=data.get("expected_trade_quantity", 0) or data.get("etq", 0)
        )


@dataclass
class SecurityDefinition:
    marketId: int
    boardId: int
    symbol: str
    isin: str
    productId: str
    productGrpId: int
    securityGroupId: int
    basicPrice: float
    ceilingPrice: float
    floorPrice: float
    openInterestQuantity: int
    securityStatus: int
    symbolAdminStatusCode: int
    symbolTradingMethodStatusCode: int
    symbolTradingSanctionStatusCode: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SecurityDefinition":
        return cls(
            symbol=data.get("symbol") or data.get("s"),
            marketId=data.get("market_id", 0) or data.get("mi", 0),
            boardId=data.get("board_id", 0) or data.get("bi", 0),
            isin=data.get("isin", 0) or data.get("is", 0),
            productId=data.get("product_id") or data.get("pi"),
            productGrpId=data.get("product_grp_id", 0) or data.get("pgi", 0),
            securityGroupId=data.get("security_group_id", 0) or data.get("sgi", 0),
            basicPrice=data.get("basic_price", 0.0) or data.get("bp", 0.0),
            ceilingPrice=data.get("ceiling_price", 0.0) or data.get("cep", 0.0),
            floorPrice=data.get("floor_price", 0.0) or data.get("fp", 0.0),
            openInterestQuantity=data.get("open_interest_quantity", 0) or data.get("oiq", 0),
            securityStatus=data.get("security_status", 0) or data.get("ss", 0),
            symbolAdminStatusCode=data.get("symbol_admin_status_code", 0) or data.get("sasc", 0),
            symbolTradingMethodStatusCode=data.get("symbol_trading_method_status_code", 0) or data.get("stmsc", 0),
            symbolTradingSanctionStatusCode=data.get("symbol_trading_sanction_status_code", 0) or data.get("stssc", 0)
        )


@dataclass
class Quote:
    marketId: int
    boardId: int
    symbol: str
    isin: str
    bid: List[PriceLevel]
    offer: List[PriceLevel]
    totalOfferQtty: float
    totalBidQtty: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Quote":
        # Parse bids array
        bids_data = data.get("b") or data.get("bid") or []
        bids = [PriceLevel.from_dict(level) for level in bids_data]

        # Parse asks array
        offer_data = data.get("of") or data.get("offer") or []
        offers = [PriceLevel.from_dict(level) for level in offer_data]

        return cls(
            symbol=data.get("s") or data.get("symbol"),
            marketId=data.get("market_id", 0) or data.get("mi", 0),
            boardId=data.get("board_id", 0) or data.get("bi", 0),
            isin=data.get("isin", 0) or data.get("is", 0),
            bid=bids,
            offer=offers,
            totalOfferQtty=data.get("total_offer_qtty") or data.get("toq"),
            totalBidQtty=data.get("total_bid_qtty") or data.get("tbq")
        )

    @property
    def best_bid(self) -> Optional[Tuple[float, int]]:
        if not self.bid:
            return None
        return self.bid[0].price, self.bid[0].quantity

    @property
    def best_ask(self) -> Optional[Tuple[float, int]]:
        if not self.offer:
            return None
        return self.offer[0].price, self.offer[0].quantity

    @property
    def spread(self) -> Optional[float]:
        bid = self.best_bid
        offer = self.best_ask
        if bid and offer:
            return offer[0] - bid[0]
        return None


@dataclass
class Bar:
    symbol: str
    resolution: int
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    time: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Bar":
        return cls(
            symbol=data.get("s") or data.get("symbol"),
            resolution=data.get("r") or data.get("resolution"),
            open=data.get("o") or data.get("open"),
            high=data.get("h") or data.get("high"),
            low=data.get("l") or data.get("low"),
            close=data.get("c") or data.get("close"),
            volume=data.get("v") or data.get("volume"),
            time=data.get("t") or data.get("time"),
        )


@dataclass
class Order:
    order_id: str
    symbol: str
    side: str
    order_type: str
    status: str
    quantity: int
    filled_quantity: int
    price: Optional[Decimal]
    average_fill_price: Optional[Decimal]
    timestamp: datetime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Order":
        return cls(
            order_id=data.get("oid") or data.get("order_id"),
            symbol=data.get("S") or data.get("symbol"),
            side=data.get("sd") or data.get("side"),
            order_type=data.get("ot") or data.get("order_type"),
            status=data.get("st") or data.get("status"),
            quantity=data.get("q") or data.get("quantity"),
            filled_quantity=data.get("fq") or data.get("filled_quantity"),
            price=Decimal(str(data["p"])) if (data.get("p") or data.get("price")) else None,
            average_fill_price=Decimal(str(data["ap"])) if (data.get("ap") or data.get("average_fill_price")) else None,
            timestamp=datetime.fromtimestamp((data.get("t") or data.get("timestamp")) / 1000)
        )


@dataclass
class Position:
    symbol: str
    quantity: int
    average_price: Decimal
    market_value: Decimal
    cost_basis: Decimal
    unrealized_pl: Decimal
    unrealized_pl_percent: Decimal
    timestamp: datetime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Position":
        """Parse position from message data.

        Args:
            data: Raw message dict with either abbreviated or full field names

        Returns:
            Position instance

        Example:
            >>> Position.from_dict({"S": "AAPL", "q": 100, "ap": "150.00", ...})
        """
        return cls(
            symbol=data.get("S") or data.get("symbol"),
            quantity=data.get("q") or data.get("quantity"),
            average_price=Decimal(str(data.get("ap") or data.get("average_price"))),
            market_value=Decimal(str(data.get("mv") or data.get("market_value"))),
            cost_basis=Decimal(str(data.get("cb") or data.get("cost_basis"))),
            unrealized_pl=Decimal(str(data.get("upl") or data.get("unrealized_pl"))),
            unrealized_pl_percent=Decimal(str(data.get("uplp") or data.get("unrealized_pl_percent"))),
            timestamp=datetime.fromtimestamp((data.get("t") or data.get("timestamp")) / 1000)
        )


@dataclass
class AccountUpdate:
    cash: Decimal
    buying_power: Decimal
    portfolio_value: Decimal
    equity: Decimal
    timestamp: datetime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AccountUpdate":
        """Parse account update from message data.

        Args:
            data: Raw message dict with either abbreviated or full field names

        Returns:
            AccountUpdate instance

        Example:
            >>> AccountUpdate.from_dict({"c": "10000.00", "bp": "20000.00", ...})
        """
        return cls(
            cash=Decimal(str(data.get("c") or data.get("cash"))),
            buying_power=Decimal(str(data.get("bp") or data.get("buying_power"))),
            portfolio_value=Decimal(str(data.get("pv") or data.get("portfolio_value"))),
            equity=Decimal(str(data.get("eq") or data.get("equity"))),
            timestamp=datetime.fromtimestamp((data.get("t") or data.get("timestamp")) / 1000)
        )
