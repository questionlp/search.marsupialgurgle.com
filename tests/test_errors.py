# Copyright (c) 2025-2026 Linh Pham
# search.marsupialgurgle.com is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Errors Module and Views."""

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_not_found(client: FlaskClient) -> None:
    """Testing errors.not_found."""
    response: TestResponse = client.get("/bad-url")
    assert response.status_code == 404
