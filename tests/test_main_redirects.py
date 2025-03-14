# Copyright (c) 2025 Linh Pham
# search.marsupialgurgle.com is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Main Redirect Module and Routes."""

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_favicon(client: FlaskClient) -> None:
    """Testing main.redirects.favicon."""
    response: TestResponse = client.get("/favicon.ico")
    assert response.status_code == 301
    assert response.location
