"""CLI entry point for daily run."""

from __future__ import annotations

from datetime import date

import yaml

from src.backfill import run_backfill
from src.load.db import create_engine_and_session


def main() -> None:
    with open("config/config.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    _, SessionLocal = create_engine_and_session(config["database"]["url"])
    with SessionLocal() as session:
        run_backfill(date.today(), date.today(), config, session)


if __name__ == "__main__":
    main()
