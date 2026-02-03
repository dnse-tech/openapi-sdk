'use strict';

const { DNSEClient } = require('../dnse');

async function main() {
  const client = new DNSEClient({
    apiKey: 'replace-with-api-key',
    apiSecret: 'replace-with-api-secret',
    baseUrl: 'https://openapi.dnse.com.vn',
  });

  const payload = {
    accountNo: '0001000115',
    symbol: 'HPG',
    side: 'BUY',
    orderType: 'LO',
    price: 25950,
    quantity: 100,
    loanPackageId: 2396,
  };

  const { status, body } = await client.postOrder('STOCK', payload, 'replace-with-trading-token', {
    dryRun: false,
  });
  console.log(status, body);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
