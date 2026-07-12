"""Idempotent insert/update logic for option rows."""

from __future__ import annotations

from sqlalchemy.dialects.sqlite import insert

from .models import OptionHistory


def upsert_option_rows(session, rows: list[dict[str, object]]) -> int:
    if not rows:
        return 0

    stmt = insert(OptionHistory).values(rows)
    stmt = stmt.on_conflict_do_update(
        index_elements=[
            OptionHistory.trade_date,
            OptionHistory.symbol,
            OptionHistory.expiry_date,
            OptionHistory.strike_price,
            OptionHistory.option_type,
        ],
        set_={
            "instrument": stmt.excluded.instrument,
            "open_interest": stmt.excluded.open_interest,
        },
    )
    result = session.execute(stmt)
    session.commit()
    return result.rowcount or 0
