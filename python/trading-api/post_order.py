#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dnse import DNSEClient


def main():
    client = DNSEClient(
        api_key="replace-with-api-key",
        api_secret="replace-with-api-secret",
        base_url="https://openapi.dnse.com.vn",
    )

    payload = {
        "symbol": "HPG",
        "side": "NB",
        "orderType": "LO",
        "price": 25950,
        "quantity": 100,
        "loanPackageId": 5757,
        "stopPrice": 28100,                                     # Giá kích hoạt (STOP/OCO)
        "conditionOperator": ">=",                              # Điều kiện kích hoạt (STOP)
        "stopOrderPrice": 28200,                                # Giá đặt lệnh cắt lỗ (OCO)
        "durationType": "GTD",                                  # Hiệu lực lệnh (STOP: GTD, OCO: DAY)
        "durationDateTime": "2026-08-07T07:30:00.000+07:00"     # Thời hạn lệnh (STOP)
    }

    status, body = client.post_order(
        account_no="0001000115",                                # Số tiểu khoản đặt lệnh
        market_type="STOCK",                                    # Thị trường giao dịch
        order_category="NORMAL",                                # Loại lệnh (NORMAL / STOP / OCO)
        trading_token="replace-with-trading-token",
        payload=payload,
        dry_run=False,
    )
    print(status, body)


if __name__ == "__main__":
    main()
