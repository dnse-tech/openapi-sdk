# DNSE OpenAPI Python SDK

Official Python SDK for integrating with DNSE OpenAPI.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Dry Run](#dry-run)
- [Examples](#examples)

### Overview

DNSE OpenAPI is an API-first trading platform that enables developers to integrate brokerage, trading, margin, and market data services
into their own applications.

The DNSE Python SDK provides a lightweight client for securely interacting with DNSE OpenAPI REST endpoints. It handles request
signing, authentication, and communication details, allowing developers to focus on building trading systems, automation strategies,
and investment applications.

### Installation

#### Requirements

- Python 3.8+

#### Install from PyPI

```console
pip install openapi-sdk 
```

Upgrade

### Usage

Create a `DNSEClient` instance with your API credentials:

```python
from dnse import DNSEClient

client = DNSEClient(
    api_key="your_api_key",
    api_secret="your_api_secret",
    base_url="https://openapi.dnse.com.vn",
    api_version="2026-05-07",
)

status, body = client.get_accounts(dry_run=False)
print(status, body)
```

The SDK sends the API version in the `version` header. If `api_version` is omitted, it defaults to `2026-01-01`; it can also be set with the `DNSE_API_VERSION` environment variable.

### Dry Run

Set `dry_run=True` to preview the request without sending it to DNSE servers. No network call will be executed.

```python
client.get_accounts(dry_run=True)
```

### Examples

Run any example from the `sdk/python/examples` directory:

```
python sdk/python/api/get_accounts.py
```

#### Trading API

| Function                  | Description                                                                                                           |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------|
| `get_accounts.py`         | Demonstrates how to retrieve all trading sub-accounts managed under the account corresponding to the API Key.         |
| `get_balances.py`         | Demonstrates how to retrieve asset balances of a trading sub-account.                                                 |
| `get_loan_packages.py`    | Demonstrates how to retrieve available loan package codes. It is necessary for placing an order.                      |
| `get_ppse.py`             | Demonstrates how to retrieve buying power and selling power before placing an order.                                  |
| `get_orders.py`           | Demonstrates how to retrieve intraday order book.                                                                     |
| `get_order_detail.py`     | Demonstrates how to retrieve detailed information of a specific order (by ID).                                        |
| `get_order_history.py`    | Demonstrates how to retrieve historical orders.                                                                       |
| `get_execution_detail.py` | Demonstrates how to retrieve detailed execution information of an order.                                              |
| `get_positions.py`        | Demonstrates how to retrieve current holding positions.                                                               |
| `get_positions_by_id.py`  | Demonstrates how to retrieve detailed information of a specific position (by ID).                                     |
| `close_position.py`       | Demonstrates how to close an existing position (by ID).                                                               |
| `send_email_otp.py`       | Demonstrates how to request an OTP sent to your registered email. The OTP is required for generating a trading token. |
| `create_trading_token.py` | Demonstrates how to generate a Trading Token required for order placement.                                            |
| `post_order.py`           | Demonstrates how to submit a new trading order.                                                                       |
| `cancel_order.py`         | Demonstrates how to cancel an existing order.                                                                         |
| `replace_order.py`        | Demonstrates how to modify an existing order.                                                                         |

#### Market Data API

| Function                     | Description                                                                                |
|------------------------------|--------------------------------------------------------------------------------------------|
| `get_security_definition.py` | Demonstrates how to retrieve security definition and instrument details.                   |
| `get_instruments.py`         | Demonstrates how to retrieve the list of available trading instruments and their metadata. |
| `get_trades.py`              | Demonstrates how to retrieve historical trade data for a specific instrument.              |
| `get_latest_trade.py`        | Demonstrates how to retrieve the most recent trade for a specific instrument.              |
| `get_ohlc.py`                | Demonstrates how to retrieve OHLC (Open, High, Low, Close) data for a given time range.    |
| `get_close_price.py`         | Demonstrates how to retrieve the latest closing price of a specific instrument.            |
| `get_working_dates.py`       | Demonstrates how to retrieve trading working dates.                                        |

### WebSocket Market Data

| Function              | Description                                                                          |
|-----------------------|--------------------------------------------------------------------------------------|
| `sec_def.py`          | Demonstrates how to receive real-time security definition updates.                   |
| `quote.py`            | Demonstrates how to receive real-time best bid and ask prices.                       |
| `trade.py`            | Demonstrates how to receive real-time trade (tick) data.                             |
| `trade_extra.py`      | Demonstrates how to receive real-time trade data with additional aggregated metrics. |
| `ohlc.py`             | Demonstrates how to receive real-time OHLC data.                                     |
| `ohlc_closed.py`      | Demonstrates how to receive completed OHLC candle data.                              |
| `expected_price.py`   | Demonstrates how to receive expected price data during ATO and ATC sessions.         |
| `foreign_investor.py` | Demonstrates how to receive foreign investor trading data.                           |
| `market_index.py`     | Demonstrates how to receive market index data.                                       |
