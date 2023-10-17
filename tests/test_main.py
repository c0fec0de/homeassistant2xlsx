#
# MIT License
#
# Copyright (c) 2023 c0fec0de
#

"""Basic Testing."""

import datetime
from pathlib import Path
from shutil import copyfile
from unittest import mock

import homeassistant2xlsx

from .util import Cell, get_content, mock_requests_get

DATAPATH = Path(__file__).parent / "data"
TIMESTAMP = datetime.datetime(1982, 1, 17, 0, 1, 2, 4)


def test_run(tmp_path):
    """Run Once."""
    filepath = tmp_path / "data.xlsx"
    copyfile(DATAPATH / "input.xlsx", filepath)

    data = {"sensor.mysensor": 84, "input_number.myinput": "55.2"}
    with mock.patch("requests.get", side_effect=mock_requests_get("myhost", 123, "mytoken", data)):
        homeassistant2xlsx.run(filepath, "myhost", "123", "mytoken", timestamp=TIMESTAMP)
        homeassistant2xlsx.run(
            filepath, "myhost", "123", "mytoken", timestamp=TIMESTAMP + datetime.timedelta(minutes=17)
        )

    assert get_content(filepath) == {
        "Sheet1": (
            (
                Cell("Date", number_format="yyyy\\-mm\\-dd", comment="date"),
                Cell("DateTime", number_format="yyyy\\-mm\\-dd\\ hh:mm:ss", comment="datetime"),
                Cell("Time", number_format="hh:mm:ss", comment="time"),
                Cell(None, number_format="hh:mm:ss"),
                Cell("Formatted Date", number_format="yyyy\\-mm\\-dd\\ hh:mm:ss", comment="datetime"),
                Cell(None, number_format="hh:mm:ss"),
                Cell("My Entity", comment="sensor.mysensor\n"),
                Cell(None),
                Cell("Calc 1", number_format="0.00"),
                Cell("Calc 2", number_format="0.00"),
                Cell(None),
                Cell("My-Default", number_format="0.00", comment="input_number.myinput"),
                Cell("My-Int", number_format="0.00", comment="input_number.myinput|int"),
                Cell("My-Float", number_format="0.00", comment="input_number.myinput|float"),
                Cell(None),
                Cell(
                    "Euro", number_format="#,##0.00\\ [$€-407];[RED]\\-#,##0.00\\ [$€-407]", comment="sensor.mysensor\n"
                ),
                Cell(None),
                Cell("Unknown Type", number_format="0.00", comment="input_number.myinput|foo"),
                Cell("Unknown Entity", comment="bar"),
            ),
            (
                Cell(None),
                Cell(None),
                Cell(None),
                Cell(None),
                Cell(None),
                Cell(None),
                Cell(21),
                Cell(None),
                Cell("=G2/2", number_format="0.00"),
                Cell(None),
                Cell(None),
                Cell(None),
                Cell(None),
                Cell(None),
                Cell(None),
                Cell(1, number_format="#,##0.00\\ [$€-407];[RED]\\-#,##0.00\\ [$€-407]"),
                Cell(None),
                Cell(None),
                Cell(None),
            ),
            (
                Cell(datetime.datetime(2023, 10, 16, 0, 0), number_format="yyyy\\-mm\\-dd"),
                Cell(datetime.datetime(2023, 10, 16, 14, 40), number_format="yyyy\\-mm\\-dd\\ hh:mm:ss"),
                Cell(datetime.time(12, 33), number_format="hh:mm:ss"),
                Cell(None),
                Cell(datetime.datetime(2023, 10, 16, 14, 40), number_format="dd/mm/yyyy\\ hh:m"),
                Cell(None),
                Cell(42),
                Cell(None),
                Cell("=G3/2", number_format="0.00"),
                Cell("=G3-G2", number_format="0.00"),
                Cell(None),
                Cell(None),
                Cell(None),
                Cell(None),
                Cell(None),
                Cell(2, number_format="#,##0.00\\ [$€-407];[RED]\\-#,##0.00\\ [$€-407]"),
                Cell(None),
                Cell(None),
                Cell(None),
            ),
            (
                Cell(datetime.date(1982, 1, 17), number_format="yyyy\\-mm\\-dd"),
                Cell(datetime.datetime(1982, 1, 17, 0, 1, 2), number_format="yyyy\\-mm\\-dd\\ hh:mm:ss"),
                Cell(datetime.time(0, 1, 2), number_format="hh:mm:ss"),
                Cell(None),
                Cell(datetime.datetime(1982, 1, 17, 0, 1, 2), number_format="dd/mm/yyyy\\ hh:m"),
                Cell(None),
                Cell(84),
                Cell(None),
                Cell("=G4/2", number_format="0.00"),
                Cell("=G4-G3", number_format="0.00"),
                Cell(None),
                Cell("55.2"),
                Cell("invalid literal for int() with base 10: '55.2'"),
                Cell(55.2),
                Cell(None),
                Cell(84, number_format="#,##0.00\\ [$€-407];[RED]\\-#,##0.00\\ [$€-407]"),
                Cell(None),
                Cell("INVALID-TYPE"),
                Cell("unavailable"),
            ),
            (
                Cell(datetime.date(1982, 1, 17), number_format="yyyy\\-mm\\-dd"),
                Cell(datetime.datetime(1982, 1, 17, 0, 18, 2), number_format="yyyy\\-mm\\-dd\\ hh:mm:ss"),
                Cell(datetime.time(0, 18, 2), number_format="hh:mm:ss"),
                Cell(None),
                Cell(datetime.datetime(1982, 1, 17, 0, 18, 2), number_format="dd/mm/yyyy\\ hh:m"),
                Cell(None),
                Cell(84),
                Cell(None),
                Cell("=G5/2", number_format="0.00"),
                Cell("=G5-G4", number_format="0.00"),
                Cell(None),
                Cell("55.2"),
                Cell("invalid literal for int() with base 10: '55.2'"),
                Cell(55.2),
                Cell(None),
                Cell(84, number_format="#,##0.00\\ [$€-407];[RED]\\-#,##0.00\\ [$€-407]"),
                Cell(None),
                Cell("INVALID-TYPE"),
                Cell("unavailable"),
            ),
        ),
        "empty": (),
        "no homeassistant": ((Cell("Header 1"), Cell("Header 2")), (Cell("Cell 1"), Cell("Cell 2"))),
    }


def test_cli(tmp_path):
    """Run via CLI."""
    filepath = tmp_path / "data.xlsx"
    copyfile(DATAPATH / "notimestamp.xlsx", filepath)

    data = {"sensor.mysensor": 84, "input_number.myinput": "55.2"}
    with mock.patch("requests.get", side_effect=mock_requests_get("myhost", 123, "mytoken", data)):

        args = ["--token", "mytoken", "--host", "myhost", "--port", "123", str(filepath)]
        homeassistant2xlsx.main(args=args)

        assert get_content(filepath) == {
            "Sheet1": (
                (
                    Cell("My Entity", comment="sensor.mysensor\n"),
                    Cell(None),
                    Cell("Calc 1", number_format="0.00"),
                    Cell("Calc 2", number_format="0.00"),
                    Cell(None),
                    Cell("My-Default", number_format="0.00", comment="input_number.myinput"),
                    Cell("My-Int", number_format="0.00", comment="input_number.myinput|int"),
                    Cell("My-Float", number_format="0.00", comment="input_number.myinput|float"),
                    Cell("Unknown", comment="bar"),
                ),
                (
                    Cell(21),
                    Cell(None),
                    Cell("=A2/2", number_format="0.00"),
                    Cell(None),
                    Cell(None),
                    Cell(None),
                    Cell(None),
                    Cell(None),
                    Cell(None),
                ),
                (
                    Cell(42),
                    Cell(None),
                    Cell("=A3/2", number_format="0.00"),
                    Cell("=A3-A2", number_format="0.00"),
                    Cell(None),
                    Cell(None),
                    Cell(None),
                    Cell(None),
                    Cell(None),
                ),
                (
                    Cell(84),
                    Cell(None),
                    Cell("=A4/2", number_format="0.00"),
                    Cell("=A4-A3", number_format="0.00"),
                    Cell(None),
                    Cell("55.2"),
                    Cell("invalid literal for int() with base 10: '55.2'"),
                    Cell(55.2),
                    Cell("unavailable"),
                ),
            ),
            "empty": (),
            "no homeassistant": ((Cell("Header 1"), Cell("Header 2")), (Cell("Cell 1"), Cell("Cell 2"))),
        }

        args = ["--token", "mytoken", "--host", "myhost", "--port", "123", str(filepath), "--timeoffset", "-5"]
        homeassistant2xlsx.main(args=args)

        assert get_content(filepath) == {
            "Sheet1": (
                (
                    Cell("My Entity", comment="sensor.mysensor\n"),
                    Cell(None),
                    Cell("Calc 1", number_format="0.00"),
                    Cell("Calc 2", number_format="0.00"),
                    Cell(None),
                    Cell("My-Default", number_format="0.00", comment="input_number.myinput"),
                    Cell("My-Int", number_format="0.00", comment="input_number.myinput|int"),
                    Cell("My-Float", number_format="0.00", comment="input_number.myinput|float"),
                    Cell("Unknown", comment="bar"),
                ),
                (
                    Cell(21),
                    Cell(None),
                    Cell("=A2/2", number_format="0.00"),
                    Cell(None),
                    Cell(None),
                    Cell(None),
                    Cell(None),
                    Cell(None),
                    Cell(None),
                ),
                (
                    Cell(42),
                    Cell(None),
                    Cell("=A3/2", number_format="0.00"),
                    Cell("=A3-A2", number_format="0.00"),
                    Cell(None),
                    Cell(None),
                    Cell(None),
                    Cell(None),
                    Cell(None),
                ),
                (
                    Cell(84),
                    Cell(None),
                    Cell("=A4/2", number_format="0.00"),
                    Cell("=A4-A3", number_format="0.00"),
                    Cell(None),
                    Cell("55.2"),
                    Cell("invalid literal for int() with base 10: '55.2'"),
                    Cell(55.2),
                    Cell("unavailable"),
                ),
                (
                    Cell(84),
                    Cell(None),
                    Cell("=A5/2", number_format="0.00"),
                    Cell("=A5-A4", number_format="0.00"),
                    Cell(None),
                    Cell("55.2"),
                    Cell("invalid literal for int() with base 10: '55.2'"),
                    Cell(55.2),
                    Cell("unavailable"),
                ),
            ),
            "empty": (),
            "no homeassistant": ((Cell("Header 1"), Cell("Header 2")), (Cell("Cell 1"), Cell("Cell 2"))),
        }
