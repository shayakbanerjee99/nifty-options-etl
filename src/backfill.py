"""Backfill helper that runs the pipeline over a date range."""

from __future__ import annotations

from datetime import date, timedelta

from .pipeline import run_pipeline_for_date


def run_backfill(start_date: date, end_date: date, config: dict, session) -> int:
    loaded = 0
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:
            loaded += run_pipeline_for_date(current, config, session)
        current += timedelta(days=1)
    return loaded
