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

    status, body = client.get_trades_volume_profile(
        symbol="GAS",
        board_id="G1",
        from_date=1773282637,
        to_date=1773289837,
        dry_run=False,
    )
    print(status, body)


if __name__ == "__main__":
    main()
