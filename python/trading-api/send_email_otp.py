#!/usr/bin/env python3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dnse import DNSEClient


def main():
    client = DNSEClient(
        api_key="replace-with-api-key",
        api_secret="replace-with-api-secret",
        base_url="http://localhost:8080",
    )

    status, body = client.send_email_otp(dry_run=False)
    print(status, body)


if __name__ == "__main__":
    main()
