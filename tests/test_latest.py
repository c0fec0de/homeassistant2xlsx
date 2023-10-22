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


def test_latest(tmp_path):
    """Latest Marker."""
    filepath = tmp_path / "data.xlsx"
    copyfile(DATAPATH / "latest.xlsx", filepath)

    data = {"sensor.mysensor": "84"}
    with mock.patch("requests.get", side_effect=mock_requests_get("myhost", 123, "mytoken", data)):
        homeassistant2xlsx.run(filepath, "myhost", "123", "mytoken", timestamp=TIMESTAMP)

    assert get_content(filepath) == {
        "sheet1": (
            (Cell("Count"), Cell(None), Cell("Sensor", comment="sensor.mysensor|int"), Cell("Sensor Sum")),
            (Cell(1), Cell(None), Cell(5), Cell(None)),
            (Cell("=A2+1"), Cell(None), Cell(10), Cell("=C2+C3")),
            (Cell("=A3+1"), Cell(None), Cell(21), Cell("=C3+C4")),
            (Cell("=A4+1"), Cell(None), Cell(42), Cell("=C4+C5")),
            (Cell("=A5+1", comment="latest"), Cell(None), Cell(84), Cell("=C5+C6")),
            (Cell(None), Cell(None), Cell(None), Cell("Total")),
            (Cell(None), Cell(None), Cell(None), Cell("=D6")),
            (Cell(None), Cell(None), Cell(None), Cell(None)),
        ),
        "sheet2": (
            (Cell("Count"), Cell(None), Cell("Sensor", comment="sensor.mysensor|int")),
            (Cell(1), Cell(None), Cell(5)),
            (Cell("=A2+1"), Cell(None), Cell(10)),
            (Cell("=A3+1"), Cell(None), Cell(21)),
            (Cell("=A4+1"), Cell(None), Cell(42)),
            (Cell("=A5+1", comment="latest"), Cell(None), Cell(84)),
        ),
    }

    data = {"sensor.mysensor": "168"}
    with mock.patch("requests.get", side_effect=mock_requests_get("myhost", 123, "mytoken", data)):
        homeassistant2xlsx.run(filepath, "myhost", "123", "mytoken", timestamp=TIMESTAMP)
    assert get_content(filepath) == {
        "sheet1": (
            (Cell("Count"), Cell(None), Cell("Sensor", comment="sensor.mysensor|int"), Cell("Sensor Sum")),
            (Cell(1), Cell(None), Cell(5), Cell(None)),
            (Cell("=A2+1"), Cell(None), Cell(10), Cell("=C2+C3")),
            (Cell("=A3+1"), Cell(None), Cell(21), Cell("=C3+C4")),
            (Cell("=A4+1"), Cell(None), Cell(42), Cell("=C4+C5")),
            (Cell("=A5+1"), Cell(None), Cell(84), Cell("=C5+C6")),
            (Cell("=A6+1", comment="latest"), Cell(None), Cell(168), Cell("=C6+C7")),
            (Cell(None), Cell(None), Cell(None), Cell("Total")),
            (Cell(None), Cell(None), Cell(None), Cell("=D7")),
            (Cell(None), Cell(None), Cell(None), Cell(None)),
        ),
        "sheet2": (
            (Cell("Count"), Cell(None), Cell("Sensor", comment="sensor.mysensor|int")),
            (Cell(1), Cell(None), Cell(5)),
            (Cell("=A2+1"), Cell(None), Cell(10)),
            (Cell("=A3+1"), Cell(None), Cell(21)),
            (Cell("=A4+1"), Cell(None), Cell(42)),
            (Cell("=A5+1"), Cell(None), Cell(84)),
            (Cell("=A6+1", comment="latest"), Cell(None), Cell(168)),
        ),
    }
