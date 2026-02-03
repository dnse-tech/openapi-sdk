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

    status, body = client.get_order_history(
        account_no="0001000115",
        market_type="STOCK",
        from_date="2025-12-01",
        to_date="2025-12-09",
        page_size=20,
        page_index=1,
        dry_run=False,
    )
    print(status, body)


if __name__ == "__main__":
    main()
