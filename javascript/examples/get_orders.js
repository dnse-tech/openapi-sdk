'use strict';

const { DNSEClient } = require('../dnse');

async function main() {
  const client = new DNSEClient({
    apiKey: 'replace-with-api-key',
    apiSecret: 'replace-with-api-secret',
    baseUrl: 'https://openapi.dnse.com.vn',
  });

  const { status, body } = await client.getOrders('0001000115', 'STOCK', {
    dryRun: false,
  });
  console.log(status, body);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
