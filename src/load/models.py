"""SQLAlchemy table definitions for options history."""

from __future__ import annotations

from datetime import date

from sqlalchemy import Date, Float, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class OptionHistory(Base):
    __tablename__ = "option_history"
    __table_args__ = (
        UniqueConstraint(
            "trade_date",
            "symbol",
            "expiry_date",
            "strike_price",
            "option_type",
            name="uq_option_history_row",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trade_date: Mapped[date] = mapped_column(Date, nullable=False)
    symbol: Mapped[str] = mapped_column(String(16), nullable=False)
    instrument: Mapped[str] = mapped_column(String(16), nullable=False)
    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)
    strike_price: Mapped[float] = mapped_column(Float, nullable=False)
    option_type: Mapped[str] = mapped_column(String(2), nullable=False)
    open_interest: Mapped[int] = mapped_column(Integer, nullable=False)
