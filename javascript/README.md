# DNSE JavaScript SDK

This SDK provides a simple client for calling the DNSE APIs with HMAC signatures.

## Requirements

- Node.js 18+

## Usage

```js
const { DNSEClient } = require('./dnse');

const client = new DNSEClient({
  apiKey: 'replace-with-api-key',
  apiSecret: 'replace-with-api-secret',
  baseUrl: 'https://openapi.dnse.com.vn',
});

client.getAccounts({ dryRun: false })
  .then(({ status, body }) => {
    console.log(status, body);
  })
  .catch((err) => {
    console.error(err);
  });
```

## Dry run

Set `dryRun: true` on any API call to print the request and skip the network call.

## Examples

Run any example from the `sdk/javascript/examples` directory:

```bash
node sdk/javascript/examples/get_accounts.js
```

Available examples:

- cancel_order.js
- create_trading_token.js
- get_accounts.js
- get_balances.js
- get_deals.js
- get_loan_packages.js
- get_order_detail.js
- get_order_history.js
- get_orders.js
- get_ppse.js
- get_security_definition.js
- post_order.js
- put_order.js
- send_email_otp.js
