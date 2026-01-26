'use strict';

const { DNSEClient } = require('../dnse');

async function main() {
  const client = new DNSEClient({
    apiKey: 'replace-with-api-key',
    apiSecret: 'replace-with-api-secret',
    baseUrl: 'http://localhost:8080',
  });

  const { status, body } = await client.getAccounts({ dryRun: false });
  console.log(status, body);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
