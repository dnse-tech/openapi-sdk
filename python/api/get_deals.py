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

    status, body = client.get_deals(
        account_no="0001000115",
        market_type="DERIVATIVE",
        dry_run=False,
    )
    print(status, body)


if __name__ == "__main__":
    main()
