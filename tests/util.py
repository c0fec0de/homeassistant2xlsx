#
# MIT License
#
# Copyright (c) 2023 c0fec0de
#

"""Utilities."""

import urllib

import openpyxl


class Cell:

    """Simplified Cell for Testing."""

    def __init__(self, value, number_format="General", comment=None):
        self.value = value
        self.number_format = number_format
        self.comment = comment

    def __repr__(self):
        args = [repr(self.value)]
        if self.number_format != "General":
            args.append(f"number_format={self.number_format!r}")
        if self.comment:
            args.append(f"comment={self.comment!r}")
        argstr = ", ".join(args)
        return f"{self.__class__.__name__}({argstr})"

    @staticmethod
    def from_openpyxl_cell(cell):
        """Create Cell form Openpyxl"""
        return Cell(value=cell.value, number_format=cell.number_format, comment=cell.comment and cell.comment.text)

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.__dict__ == other.__dict__
        return NotImplemented


def mock_requests_get(host, port, token, data):
    """Immitate Home Assistant Response."""

    def mocked_get(url, headers=None, timeout=None):
        class MockResponse:
            """Immitate requests Response."""

            # pylint: disable=too-few-public-methods

            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                """JSON response."""
                return self.json_data

        urlp = urllib.parse.urlparse(url)

        assert headers == {"Authorization": f"Bearer {token}", "content-type": "application/json"}
        assert timeout == 60
        assert urlp.scheme == "http"
        assert urlp.hostname == host
        assert urlp.port == port
        assert urlp.path.startswith("/api/states/")
        entity = urlp.path[len("/api/states/") :]
        json_data = {"state": data.get(entity, "unavailable")}
        return MockResponse(json_data, 200)

    return mocked_get


def get_content(filepath):
    """Get Spreadsheet Content."""
    data = {}
    book = openpyxl.load_workbook(filepath)
    for sheet in book:
        data[sheet.title] = tuple(tuple(Cell.from_openpyxl_cell(cell) for cell in row) for row in sheet.iter_rows())
    return data
