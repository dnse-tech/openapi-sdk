'use strict';

const { DNSEClient } = require('../dnse');

async function main() {
  const client = new DNSEClient({
    apiKey: 'replace-with-api-key',
    apiSecret: 'replace-with-api-secret',
    baseUrl: 'https://openapi.dnse.com.vn',
  });

  const payload = {
    price: 12500,
    quantity: 100,
  };

  const { status, body } = await client.putOrder(
    '0001000115',
    '511',
    'STOCK',
    payload,
    'replace-with-trading-token',
    { dryRun: false },
  );
  console.log(status, body);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
