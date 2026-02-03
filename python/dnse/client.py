#!/usr/bin/env python3
import json
import os
from urllib import parse, request

from .common import build_signature, get_date_header_name


class DNSEClient:
    def __init__(
        self,
        api_key,
        api_secret,
        base_url="https://openapi.dnse.com.vn",
        algorithm="hmac-sha256",
        hmac_nonce_enabled=True,
    ):
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url.rstrip("/")
        self._algorithm = algorithm
        self._hmac_nonce_enabled = hmac_nonce_enabled

    def get_accounts(self, dry_run=False):
        return self._request("GET", "/accounts", dry_run=dry_run)

    def get_balances(self, account_no, dry_run=False):
        return self._request("GET", f"/accounts/{account_no}/balances", dry_run=dry_run)

    def get_loan_packages(self, account_no, market_type, symbol=None, dry_run=False):
        query = {"marketType": market_type}
        if symbol:
            query["symbol"] = symbol
        return self._request(
            "GET",
            f"/accounts/{account_no}/loan-packages",
            query=query,
            dry_run=dry_run,
        )

    def get_deals(self, account_no, market_type, dry_run=False):
        return self._request(
            "GET",
            f"/accounts/{account_no}/deals",
            query={"marketType": market_type},
            dry_run=dry_run,
        )

    def get_orders(self, account_no, market_type, order_category=None, dry_run=False):
        query = {"marketType": market_type}
        if order_category:
            query["orderCategory"] = order_category
        return self._request(
            "GET",
            f"/accounts/{account_no}/orders",
            query=query,
            dry_run=dry_run,
        )

    def get_order_detail(self, account_no, order_id, market_type, order_category=None, dry_run=False):
        query = {"marketType": market_type}
        if order_category:
            query["orderCategory"] = order_category
        return self._request(
            "GET",
            f"/accounts/{account_no}/orders/{order_id}",
            query=query,
            dry_run=dry_run,
        )

    def get_order_history(
        self,
        account_no,
        market_type,
        from_date=None,
        to_date=None,
        page_size=None,
        page_index=None,
        dry_run=False,
    ):
        query = {"marketType": market_type}
        if from_date:
            query["from"] = from_date
        if to_date:
            query["to"] = to_date
        if page_size is not None:
            query["pageSize"] = page_size
        if page_index is not None:
            query["pageIndex"] = page_index
        return self._request(
            "GET",
            f"/accounts/{account_no}/orders/history",
            query=query,
            dry_run=dry_run,
        )

    def get_ppse(self, account_no, market_type, symbol, price, loan_package_id, dry_run=False):
        return self._request(
            "GET",
            f"/accounts/{account_no}/ppse",
            query={
                "marketType": market_type,
                "symbol": symbol,
                "price": str(price),
                "loanPackageId": str(loan_package_id),
            },
            dry_run=dry_run,
        )

    def get_security_definition(self, symbol, board_id=None, dry_run=False):
        query = {}
        if board_id:
            query["boardId"] = board_id
        return self._request(
            "GET",
            f"/price/secdef/{symbol}",
            query=query if query else None,
            dry_run=dry_run,
        )

    def post_order(self, market_type, payload, trading_token, order_category="NORMAL", dry_run=False):
        headers = {"trading-token": trading_token}
        query = {"marketType": market_type}
        if order_category:
            query["orderCategory"] = order_category
        return self._request(
            "POST",
            "/accounts/orders",
            query=query,
            body=payload,
            headers=headers,
            dry_run=dry_run,
        )

    def put_order(
        self,
        account_no,
        order_id,
        market_type,
        payload,
        trading_token,
        order_category=None,
        dry_run=False,
    ):
        headers = {"trading-token": trading_token}
        query = {"marketType": market_type}
        if order_category:
            query["orderCategory"] = order_category
        return self._request(
            "PUT",
            f"/accounts/{account_no}/orders/{order_id}",
            query=query,
            body=payload,
            headers=headers,
            dry_run=dry_run,
        )

    def cancel_order(
        self,
        account_no,
        order_id,
        market_type,
        trading_token,
        order_category=None,
        dry_run=False,
    ):
        headers = {"trading-token": trading_token}
        query = {"marketType": market_type}
        if order_category:
            query["orderCategory"] = order_category
        return self._request(
            "DELETE",
            f"/accounts/{account_no}/orders/{order_id}",
            query=query,
            headers=headers,
            dry_run=dry_run,
        )

    def create_trading_token(self, otp_type, passcode, dry_run=False):
        return self._request(
            "POST",
            "/registration/trading-token",
            body={"otpType": otp_type, "passcode": passcode},
            dry_run=dry_run,
        )

    def send_email_otp(self, dry_run=False):
        return self._request(
            "POST",
            "/registration/send-email-otp",
            dry_run=dry_run,
        )

    def _request(self, method, path, query=None, body=None, headers=None, dry_run=False):
        debug = os.getenv("DEBUG", "").lower() == "true"
        url = self._build_url(path, query)
        date_value, signature_header_value = self._signature_headers(method, path)
        date_header_name = get_date_header_name()

        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")

        req = request.Request(url, data=data, method=method)
        req.add_header(date_header_name, date_value)
        req.add_header("X-Signature", signature_header_value)
        req.add_header("x-api-key", self._api_key)

        if body is not None:
            req.add_header("Content-Type", "application/json")

        if headers:
            for key, value in headers.items():
                req.add_header(key, value)

        if debug or dry_run:
            prefix = "DRY RUN" if dry_run else "DEBUG"
            print(f"{prefix} url:", url)
            print(f"{prefix} method:", method)
            print(f"{prefix} query_params:", query or {})
            print(f"{prefix} headers:", dict(req.header_items()))
            print(f"{prefix} body:", body)

        if dry_run:
            return None, None

        try:
            with request.urlopen(req) as resp:
                body_text = resp.read().decode("utf-8")
                return resp.status, body_text
        except request.HTTPError as err:
            body_text = err.read().decode("utf-8") if err.fp else ""
            return err.code, body_text

    def _build_url(self, path, query):
        url = f"{self._base_url}{path}"
        if query:
            url = f"{url}?{parse.urlencode(query)}"
        return url

    def _signature_headers(self, method, path):
        date_value = self._date_header()
        nonce = None
        if self._hmac_nonce_enabled:
            import uuid

            nonce = uuid.uuid4().hex

        headers_list, signature = build_signature(
            self._api_secret,
            method,
            path,
            date_value,
            self._algorithm,
            nonce=nonce,
            header_name=get_date_header_name(),
        )
        signature_header_value = (
            f'Signature keyId="{self._api_key}",algorithm="{self._algorithm}",'
            f'headers="{headers_list}",signature="{signature}"'
        )
        if nonce:
            signature_header_value += f',nonce="{nonce}"'
        return date_value, signature_header_value

    def _date_header(self):
        from datetime import datetime, timezone

        return datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")
