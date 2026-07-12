"""Row schema and validation for transformed option rows."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class OptionRow:
    trade_date: date
    symbol: str
    instrument: str
    expiry_date: date
    strike_price: float
    option_type: str
    open_interest: int

    @classmethod
    def from_raw(cls, row: dict[str, str]) -> "OptionRow":
        return cls(
            trade_date=datetime.strptime(row["TIMESTAMP"], "%d-%b-%Y").date(),
            symbol=row["SYMBOL"].strip(),
            instrument=row["INSTRUMENT"].strip(),
            expiry_date=datetime.strptime(row["EXPIRY_DT"], "%d-%b-%Y").date(),
            strike_price=float(row["STRIKE_PR"]),
            option_type=row["OPTION_TYP"].strip(),
            open_interest=int(row["OPEN_INT"]),
        )
