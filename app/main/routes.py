# Copyright (c) 2025 Linh Pham
# search.marsupialgurgle.com is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Main Application Routes."""

import math
from pathlib import Path

from flask import (
    Blueprint,
    Response,
    current_app,
    g,
    render_template,
    send_file,
)
from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.main.clip import retrieve_clip_info
from app.main.search import SearchMode, search_clips
from app.utilities import pagination_list

blueprint = Blueprint("main", __name__)


@blueprint.route("/")
def index() -> str:
    """View: Landing Page."""
    return render_template("pages/index.html", exclude_footer_links=False)


@blueprint.route("/about")
def about() -> str:
    """View: About Page."""
    return render_template("pages/about.html")


@blueprint.route("/clip")
def clip_info() -> str:
    """View: Individual Clip Page."""
    request_data = g.sanitized_args
    _key: str | None = request_data.get("key")

    if not _key:
        return render_template("pages/clip.html")

    # Strip whitespaces from and enforce clip key ID length to 254
    _key = _key.strip()
    _key = _key[:254]

    database_connection: MySQLConnection | PooledMySQLConnection = connect(
        **current_app.config["database_settings"]
    )
    clip: dict[str, int | str | bool | None] | None = retrieve_clip_info(
        clip_key=_key, database_connection=database_connection
    )

    if clip and "error" in clip:
        return render_template("pages/clip.html", clip_key=_key, error=clip["error"])

    if clip:
        return render_template(
            "pages/clip.html", clip_key=_key, clip=clip, expand_info=True
        )

    return render_template("pages/clip.html", clip_key=_key)


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
    request_data = g.sanitized_args
    query: str | None = request_data.get("query")

    if not query:
        return render_template("pages/search.html")

    # Strip whitespaces from and enforce length limit on query string
    query = query.strip()
    query = query[: current_app.config["app_settings"]["max_query_length"]]

    try:
        page: int = int(request_data.get("page", 1))
        page = max(page, 1)
    except ValueError:
        page = 1

    try:
        search_mode: SearchMode = SearchMode(int(request_data.get("mode", 1)))

        # Only allow query expansion mode if the feature flag is enabled,
        # otherwise use the default natural language search mode instead
        if (
            not current_app.config["app_settings"]["enable_query_expansion_mode"]
            and search_mode == SearchMode.EXPANDED
        ):
            search_mode = SearchMode.NATURAL
            valid_search_mode: bool = False

        valid_search_mode: bool = True
    except ValueError:
        search_mode: SearchMode = SearchMode.NATURAL
        valid_search_mode: bool = False

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
            valid_search_mode=valid_search_mode,
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
