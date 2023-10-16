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

from .util import get_content, mock_requests_get

DATAPATH = Path(__file__).parent / "data"
TIMESTAMP = datetime.datetime(1982, 1, 17, 0, 1, 2, 4)


def test_run(tmp_path):
    """Run Once."""
    filepath = tmp_path / "data.xlsx"
    copyfile(DATAPATH / "input.xlsx", filepath)

    data = {"sensor.mysensor": 84, "input_number.myinput": "55.2"}
    with mock.patch("requests.get", side_effect=mock_requests_get("myhost", 123, "mytoken", data)):
        homeassistant2xlsx.run(filepath, "myhost", "123", "mytoken", timestamp=TIMESTAMP)

    assert get_content(filepath) == {
        "Sheet1": (
            (
                "Date",
                "DateTime",
                "Time",
                "My Entity",
                None,
                "Calc 1",
                "Calc 2",
                None,
                "My-Default",
                "My-Int",
                "My-Float",
                "My-Unknown",
                "Unknown",
            ),
            (None, None, None, 21, None, "=D2/2", None, None, None, None, None, None, None),
            (
                datetime.datetime(2023, 10, 16, 0, 0),
                datetime.datetime(2023, 10, 16, 14, 40),
                datetime.time(12, 33),
                42,
                None,
                "=D3/2",
                "=D3-D2",
                None,
                None,
                None,
                None,
                None,
                None,
            ),
            (
                datetime.date(1982, 1, 17),
                datetime.datetime(1982, 1, 17, 0, 1, 2),
                datetime.time(0, 1, 2),
                84,
                None,
                "=D4/2",
                "=D4-D3",
                None,
                "55.2",
                "invalid literal for int() with base 10: '55.2'",
                55.2,
                "INVALID-TYPE",
                "unavailable",
            ),
        ),
        "empty": (),
        "no homeassistant": (("Header 1", "Header 2"), ("Cell 1", "Cell 2")),
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
                ("My Entity", None, "Calc 1", "Calc 2", None, "My-Default", "My-Int", "My-Float", "Unknown"),
                (21, None, "=A2/2", None, None, None, None, None, None),
                (42, None, "=A3/2", "=A3-A2", None, None, None, None, None),
                (
                    84,
                    None,
                    "=A4/2",
                    "=A4-A3",
                    None,
                    "55.2",
                    "invalid literal for int() with base 10: '55.2'",
                    55.2,
                    "unavailable",
                ),
            ),
            "empty": (),
            "no homeassistant": (("Header 1", "Header 2"), ("Cell 1", "Cell 2")),
        }

        args = ["--token", "mytoken", "--host", "myhost", "--port", "123", str(filepath), "--timeoffset", "-5"]
        homeassistant2xlsx.main(args=args)

        assert get_content(filepath) == {
            "Sheet1": (
                ("My Entity", None, "Calc 1", "Calc 2", None, "My-Default", "My-Int", "My-Float", "Unknown"),
                (21, None, "=A2/2", None, None, None, None, None, None),
                (42, None, "=A3/2", "=A3-A2", None, None, None, None, None),
                (
                    84,
                    None,
                    "=A4/2",
                    "=A4-A3",
                    None,
                    "55.2",
                    "invalid literal for int() with base 10: '55.2'",
                    55.2,
                    "unavailable",
                ),
                (
                    84,
                    None,
                    "=A5/2",
                    "=A5-A4",
                    None,
                    "55.2",
                    "invalid literal for int() with base 10: '55.2'",
                    55.2,
                    "unavailable",
                ),
            ),
            "empty": (),
            "no homeassistant": (("Header 1", "Header 2"), ("Cell 1", "Cell 2")),
        }
