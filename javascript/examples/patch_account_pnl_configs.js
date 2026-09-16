'use strict';

const { DNSEClient } = require('../dnse');

async function main() {
  const client = new DNSEClient({
    apiKey: 'replace-with-api-key',
    apiSecret: 'replace-with-api-secret',
    baseUrl: 'https://openapi.dnse.com.vn',
  });
  const payload = {
    takeProfit: {
      enabled: true, strategy: 'PNL_RATE', rate: 0.4, orderMethod: 'FASTEST', orderDeltaPrice: 2,
    },
    stopLoss: {
      enabled: true, strategy: 'DELTA_PRICE', rate: -0.1, orderMethod: 'DELTA_PRICE', orderDeltaPrice: 10.5, trailingEnabled: true,
    },
  };
  const { status, body } = await client.patchAccountPnlConfigs(
    '0001000115', 'DERIVATIVE', payload, 'replace-with-trading-token', { dryRun: false },
  );
  console.log(status, body);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
