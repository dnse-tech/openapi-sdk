'use strict';

const { DNSEClient } = require('../dnse');

async function main() {
  const client = new DNSEClient({
    apiKey: 'replace-with-api-key',
    apiSecret: 'replace-with-api-secret',
    baseUrl: 'https://openapi.dnse.com.vn',
  });

  const { status, body } = await client.getOrderHistory('0001000115', 'STOCK', {
    from: '2025-12-01',
    to: '2025-12-09',
    pageSize: 20,
    pageIndex: 1,
    dryRun: false,
  });
  console.log(status, body);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
