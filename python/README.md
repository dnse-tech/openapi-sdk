# DNSE Python SDK

This SDK provides a simple client for calling the DNSE APIs with HMAC signatures.

## Requirements

- Python 3.8+

## Usage

```python
from dnse import DNSEClient

client = DNSEClient(
    api_key="replace-with-api-key",
    api_secret="replace-with-api-secret",
    base_url="https://openapi.dnse.com.vn",
)

status, body = client.get_accounts(dry_run=False)
print(status, body)
```

## Dry run

Set `dry_run=True` on any API call to print the request and skip the network call.

## Examples

Run any example from the `sdk/python/examples` directory:

```bash
python sdk/python/api/get_accounts.py
```

Available examples:

- cancel_order.py
- create_trading_token.py
- get_accounts.py
- get_balances.py
- get_deals.py
- get_loan_packages.py
- get_order_detail.py
- get_order_history.py
- get_orders.py
- get_ppse.py
- get_security_definition.py
- post_order.py
- put_order.py
- send_email_otp.py
