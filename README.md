# nifty-options-etl

Extracting historical data from the NSE website and transforming it such that a user can load historical option chains.

## Project layout

```
nifty-options-etl/
├── config/
├── src/
│   ├── extract/
│   ├── transform/
│   ├── load/
│   ├── pipeline.py
│   └── backfill.py
├── tests/
├── scripts/
├── alembic/
└── pyproject.toml
```
