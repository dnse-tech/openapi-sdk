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

    status, body = client.get_loans(
        account_no="0001000115",
        market_type="STOCK",
        disbursement_from="2026-06-01",
        disbursement_to="2026-07-31",
        due_date_from="2026-09-01",
        due_date_to="2026-12-31",
        position_id=None,
        page_index=0,
        page_size=25,
        dry_run=False,
    )
    print(status, body)


if __name__ == "__main__":
    main()
