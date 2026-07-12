from transform.schema import OptionRow


def test_option_row_from_raw_parses_expected_types() -> None:
    row = {
        "TIMESTAMP": "01-Jan-2024",
        "SYMBOL": "NIFTY",
        "INSTRUMENT": "OPTIDX",
        "EXPIRY_DT": "25-Jan-2024",
        "STRIKE_PR": "22000",
        "OPTION_TYP": "CE",
        "OPEN_INT": "1500",
    }

    parsed = OptionRow.from_raw(row)

    assert parsed.symbol == "NIFTY"
    assert parsed.strike_price == 22000.0
    assert parsed.open_interest == 1500
