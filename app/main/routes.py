# Copyright (c) 2025 Linh Pham
# search.marsupialgurgle.com is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Main Application Routes."""

import math
from pathlib import Path

from flask import Blueprint, Response, current_app, render_template, request, send_file
from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.main.search import SearchMode, search_clips
from app.utilities import pagination_list

blueprint = Blueprint("main", __name__)


@blueprint.route("/")
def index() -> str:
    """View: Landing Page."""
    return render_template("pages/index.html", exclude_footer_links=True)


@blueprint.route("/help")
def help_page() -> str:
    """View: Help Page."""
    return render_template("pages/help.html")


@blueprint.route("/robots.txt")
def robots_txt() -> Response:
    """View: robots.txt File."""
    static_robots_txt: Path = Path.cwd() / "app" / "static" / "robots.txt"

    if not static_robots_txt.exists() or not static_robots_txt.is_file():
        _robots_txt: str = render_template("robots.txt")
        return Response(_robots_txt, mimetype="text/plain")

    return send_file(static_robots_txt, mimetype="text/plain")


@blueprint.route("/search")
def search() -> str:
    """View: Search Results."""
    query: str | None = request.args.get("query")

    if not query:
        return render_template(
            "pages/search.html",
        )

    query = query.strip()
    page: int = max(request.args.get("page", type=int, default=1), 1)
    try:
        search_mode: SearchMode = SearchMode(
            request.args.get("mode", type=int, default=1)
        )
    except ValueError:
        search_mode: SearchMode = SearchMode.NATURAL

    results_per_page: int = current_app.config["app_settings"]["results_per_page"]
    offset: int = (page - 1) * results_per_page

    database_connection: MySQLConnection | PooledMySQLConnection = connect(
        **current_app.config["database_settings"]
    )
    results_info: dict[str, int | list[dict]] = search_clips(
        search_query=query,
        search_mode=search_mode,
        results_per_page=results_per_page,
        offset=offset,
        database_connection=database_connection,
    )
    database_connection.close()

    if "error" in results_info:
        return render_template(
            "pages/search.html",
            search_query=query,
            search_mode=search_mode.value,
            error=results_info["error"],
        )

    total_count: int = results_info["total_count"]
    total_pages: int = math.ceil(total_count / results_per_page)
    returned_count: int = results_info["returned_count"]
    results: list[dict | None] = results_info["results"]
    _pagination_list: list[int | None] | None = pagination_list(
        current_page=page, total_pages=total_pages
    )

    if results:
        return render_template(
            "pages/search.html",
            search_query=query,
            search_mode=search_mode.value,
            current_page=page,
            total_count=total_count,
            total_pages=total_pages,
            pagination_list=_pagination_list,
            returned_count=returned_count,
            search_results=results,
        )

    return render_template(
        "pages/search.html", search_query=query, search_mode=search_mode.value
    )
