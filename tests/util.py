#
# MIT License
#
# Copyright (c) 2023 c0fec0de
#

"""Utilities."""

import urllib

import openpyxl


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
        data[sheet.title] = tuple(sheet.iter_rows(values_only=True))
    return data
