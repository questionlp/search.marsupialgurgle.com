# Copyright (c) 2025-2026 Linh Pham
# search.marsupialgurgle.com is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Redirection Routes."""

from flask import Blueprint, Response, url_for

from app.utilities import redirect_url

blueprint = Blueprint("main_redirects", __name__)


@blueprint.route("/favicon.ico")
def favicon() -> Response:
    """Redirect: /favicon.ico to /static/favicon.ico."""
    return redirect_url(url_for("static", filename="favicon.ico"), status_code=301)
