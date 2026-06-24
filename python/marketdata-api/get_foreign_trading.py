#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dnse import DNSEClient


def main():
    client = DNSEClient(
        api_key="replace-with-api-key",
        api_secret="replace-with-api-secret",
        base_url="https://openapi.dnse.com.vn",
    )

    status, body = client.get_foreign_trading(symbol="SSI", board_id="G1", from_date=1781037427, to_date=1781062643, limit = 100, order = "DESC", next_page_token=None, dry_run=False)
    print(status, body)


if __name__ == "__main__":
    main()
