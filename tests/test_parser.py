from pathlib import Path
from zipfile import ZipFile

from transform.parser import parse_udiff_zip


def test_parse_udiff_zip_filters_nifty_optidx(tmp_path: Path) -> None:
    csv_content = "\n".join(
        [
            "INSTRUMENT,SYMBOL,TIMESTAMP,EXPIRY_DT,STRIKE_PR,OPTION_TYP,OPEN_INT",
            "OPTIDX,NIFTY,01-Jan-2024,25-Jan-2024,22000,CE,100",
            "FUTIDX,NIFTY,01-Jan-2024,25-Jan-2024,22000,XX,100",
            "OPTIDX,BANKNIFTY,01-Jan-2024,25-Jan-2024,22000,PE,100",
        ]
    )

    zip_path = tmp_path / "sample.zip"
    with ZipFile(zip_path, "w") as archive:
        archive.writestr("fo01JAN2024bhav.csv", csv_content)

    rows = parse_udiff_zip(zip_path)

    assert len(rows) == 1
    assert rows[0]["SYMBOL"] == "NIFTY"
    assert rows[0]["INSTRUMENT"] == "OPTIDX"
