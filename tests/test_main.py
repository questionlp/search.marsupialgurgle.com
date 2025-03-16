# Copyright (c) 2025 Linh Pham
# search.marsupialgurgle.com is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Main Routes and Views."""

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing main.index."""
    response: TestResponse = client.get("/")
    assert response.status_code == 200
    assert "Hey Gurgle" in response.text
    assert "Marsupial Gurgle" in response.text
    assert "Search Audio Clips" in response.text


def test_about(client: FlaskClient) -> None:
    """Testing main.index."""
    response: TestResponse = client.get("/about")
    assert response.status_code == 200
    assert "Hey Gurgle" in response.text
    assert "The Hey Gurgle Name" in response.text
    assert "About" in response.text


def test_help_page(client: FlaskClient) -> None:
    """Testing main.help_page."""
    response: TestResponse = client.get("/help")
    assert response.status_code == 200
    assert "Hey Gurgle" in response.text
    assert "Marsupial Gurgle" in response.text
    assert "Help Page" in response.text


@pytest.mark.parametrize("query, mode", [("andrew", 1), ("luke", 2)])
def test_search(client: FlaskClient, query: str, mode: int) -> None:
    """Testing main.search with queries."""
    response: TestResponse = client.get(
        "/search", query_string={"query": query, "mode": mode}
    )
    assert response.status_code == 200
    assert "Hey Gurgle" in response.text
    assert "article" in response.text
    assert "<audio" in response.text
    assert "Clip Info" in response.text


def test_search_no_query(client: FlaskClient) -> None:
    """Testing main.search without a search query."""
    response: TestResponse = client.get("/search")
    assert response.status_code == 200
    assert "Hey Gurgle" in response.text
    assert "No search query was provided." in response.text


@pytest.mark.parametrize(
    "query, mode", [("THIS_WONT_RETURN_RESULTS", 1), ("THIS_WONT_RETURN_RESULTS", 2)]
)
def test_search_no_results(client: FlaskClient, query: str, mode: int) -> None:
    """Testing main.search without a query that yields no results."""
    response: TestResponse = client.get(
        "/search", query_string={"query": query, "mode": mode}
    )
    assert response.status_code == 200
    assert "Hey Gurgle" in response.text
    assert "No search results found for" in response.text


def test_robots_txt(client: FlaskClient) -> None:
    """Testing main.robots_txt."""
    response: TestResponse = client.get("/robots.txt")
    assert response.status_code == 200
    assert "Disallow: /search" in response.text
