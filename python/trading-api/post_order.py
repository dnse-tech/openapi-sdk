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
        "accountNo": "0001000115",
        "symbol": "HPG",
        "side": "BUY",
        "orderType": "LO",
        "price": 25950,
        "quantity": 100,
        "loanPackageId": 2396,
    }

    status, body = client.post_order(
        market_type="STOCK",
        payload=payload,
        trading_token="replace-with-trading-token",
        order_category="NORMAL",
        dry_run=False,
    )
    print(status, body)


if __name__ == "__main__":
    main()
