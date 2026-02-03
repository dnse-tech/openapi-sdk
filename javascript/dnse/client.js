'use strict';

const { randomUUID } = require('crypto');
const { buildSignature, formatDateHeader } = require('./common');

class DNSEClient {
  constructor({ apiKey, apiSecret, baseUrl = 'https://openapi.dnse.com.vn', algorithm = 'hmac-sha256', hmacNonceEnabled = true }) {
    this.apiKey = apiKey;
    this.apiSecret = apiSecret;
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.algorithm = algorithm;
    this.hmacNonceEnabled = hmacNonceEnabled;
  }

  getAccounts({ dryRun = false } = {}) {
    return this.#request('GET', '/accounts', { dryRun });
  }

  getBalances(accountNo, { dryRun = false } = {}) {
    return this.#request('GET', `/accounts/${accountNo}/balances`, { dryRun });
  }

  getLoanPackages(accountNo, marketType, { symbol, dryRun = false } = {}) {
    const query = { marketType };
    if (symbol) {
      query.symbol = symbol;
    }
    return this.#request('GET', `/accounts/${accountNo}/loan-packages`, { query, dryRun });
  }

  getDeals(accountNo, marketType, { dryRun = false } = {}) {
    return this.#request('GET', `/accounts/${accountNo}/deals`, {
      query: { marketType },
      dryRun,
    });
  }

  getOrders(accountNo, marketType, { dryRun = false } = {}) {
    return this.#request('GET', `/accounts/${accountNo}/orders`, {
      query: { marketType },
      dryRun,
    });
  }

  getOrderDetail(accountNo, orderId, marketType, { dryRun = false } = {}) {
    return this.#request('GET', `/accounts/${accountNo}/orders/${orderId}`, {
      query: { marketType },
      dryRun,
    });
  }

  getOrderHistory(
    accountNo,
    marketType,
    { from, to, pageSize, pageIndex, dryRun = false } = {},
  ) {
    const query = { marketType };
    if (from !== undefined) {
      query.from = from;
    }
    if (to !== undefined) {
      query.to = to;
    }
    if (pageSize !== undefined) {
      query.pageSize = pageSize;
    }
    if (pageIndex !== undefined) {
      query.pageIndex = pageIndex;
    }
    return this.#request('GET', `/accounts/${accountNo}/orders/history`, {
      query,
      dryRun,
    });
  }

  getPpse(accountNo, marketType, symbol, price, loanPackageId, { dryRun = false } = {}) {
    return this.#request('GET', `/accounts/${accountNo}/ppse`, {
      query: {
        marketType,
        symbol,
        price: String(price),
        loanPackageId: String(loanPackageId),
      },
      dryRun,
    });
  }

  getSecurityDefinition(symbol, { boardId, dryRun = false } = {}) {
    return this.#request('GET', `/price/secdef/${symbol}`, {
      query: { boardId },
      dryRun,
    });
  }

  postOrder(marketType, payload, tradingToken, { dryRun = false } = {}) {
    return this.#request('POST', '/accounts/orders', {
      query: { marketType },
      body: payload,
      headers: { 'trading-token': tradingToken },
      dryRun,
    });
  }

  putOrder(accountNo, orderId, marketType, payload, tradingToken, { dryRun = false } = {}) {
    return this.#request('PUT', `/accounts/${accountNo}/orders/${orderId}`, {
      query: { marketType },
      body: payload,
      headers: { 'trading-token': tradingToken },
      dryRun,
    });
  }

  cancelOrder(accountNo, orderId, marketType, tradingToken, { dryRun = false } = {}) {
    return this.#request('DELETE', `/accounts/${accountNo}/orders/${orderId}`, {
      query: { marketType },
      headers: { 'trading-token': tradingToken },
      dryRun,
    });
  }

  createTradingToken(otpType, passcode, { dryRun = false } = {}) {
    return this.#request('POST', '/registration/trading-token', {
      body: { otpType, passcode },
      dryRun,
    });
  }

  sendEmailOtp(email, { otpType = 'email_otp', dryRun = false } = {}) {
    return this.#request('POST', '/registration/send-email-otp', {
      body: { email, otpType },
      dryRun,
    });
  }

  async #request(method, path, { query, body, headers, dryRun } = {}) {
    const debug = String(process.env.DEBUG || '').toLowerCase() === 'true';
    const url = this.#buildUrl(path, query);
    const { dateValue, signatureHeaderValue } = this.#signatureHeaders(method, path);

    const requestHeaders = {
      Date: dateValue,
      'X-Signature': signatureHeaderValue,
      'x-api-key': this.apiKey,
    };

    if (body !== undefined) {
      requestHeaders['Content-Type'] = 'application/json';
    }

    if (headers) {
      Object.assign(requestHeaders, headers);
    }

    if (debug || dryRun) {
      const prefix = dryRun ? 'DRY RUN' : 'DEBUG';
      const queryParams = query || {};
      console.log(`${prefix} url:`, url);
      console.log(`${prefix} method:`, method);
      console.log(`${prefix} query_params:`, queryParams);
      console.log(`${prefix} headers:`, requestHeaders);
      console.log(`${prefix} body:`, body);
    }

    if (dryRun) {
      return { status: null, body: null };
    }

    const response = await fetch(url, {
      method,
      headers: requestHeaders,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });

    const responseBody = await response.text();
    return { status: response.status, body: responseBody };
  }

  #buildUrl(path, query) {
    const url = new URL(`${this.baseUrl}${path}`);
    if (query) {
      for (const [key, value] of Object.entries(query)) {
        if (value !== undefined && value !== null) {
          url.searchParams.set(key, String(value));
        }
      }
    }
    return url.toString();
  }

  #signatureHeaders(method, path) {
    const dateValue = formatDateHeader(new Date());
    const nonce = this.hmacNonceEnabled ? randomUUID().replace(/-/g, '') : null;
    const { headers, signature } = buildSignature(
      this.apiSecret,
      method,
      path,
      dateValue,
      this.algorithm,
      nonce,
    );

    let signatureHeaderValue = `Signature keyId="${this.apiKey}",algorithm="${this.algorithm}",headers="${headers}",signature="${signature}"`;
    if (nonce) {
      signatureHeaderValue += `,nonce="${nonce}"`;
    }

    return { dateValue, signatureHeaderValue };
  }
}

module.exports = {
  DNSEClient,
};
