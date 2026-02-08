# Copyright (c) 2025-2026 Linh Pham
# search.marsupialgurgle.com is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""pytest conftest.py File."""

import pytest
from flask import Flask

from app import create_app


@pytest.fixture
def client():
    """Pytest Client Fixture."""
    app: Flask = create_app()
    with app.test_client() as _client:
        yield _client
