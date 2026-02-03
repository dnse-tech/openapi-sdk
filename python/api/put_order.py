#!/usr/bin/env python3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dnse import DNSEClient


def main():
    client = DNSEClient(
        api_key="replace-with-api-key",
        api_secret="replace-with-api-secret",
        base_url="https://openapi.dnse.com.vn",
    )

    payload = {
        "price": 12500,
        "quantity": 100,
    }

    status, body = client.put_order(
        account_no="0001000115",
        order_id="511",
        market_type="STOCK",
        payload=payload,
        trading_token="replace-with-trading-token",
        order_category="NORMAL",
        dry_run=False,
    )
    print(status, body)


if __name__ == "__main__":
    main()
