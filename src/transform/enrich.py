"""Derived option row metrics."""

from __future__ import annotations

from dataclasses import asdict

from .schema import OptionRow


def expiry_bucket(days_to_expiry: int) -> str:
    if days_to_expiry <= 7:
        return "weekly"
    if days_to_expiry <= 31:
        return "near_month"
    return "far_month"


def enrich_row(row: OptionRow, spot_price: float | None = None) -> dict[str, object]:
    payload = asdict(row)
    days = (row.expiry_date - row.trade_date).days
    payload["days_to_expiry"] = days
    payload["expiry_bucket"] = expiry_bucket(days)
    if spot_price is not None:
        payload["moneyness"] = "ATM" if abs(row.strike_price - spot_price) < 1e-9 else (
            "ITM" if row.strike_price < spot_price else "OTM"
        )
    return payload
