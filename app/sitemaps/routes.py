# Copyright (c) 2025 Linh Pham
# search.marsupialgurgle.com is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Sitemap Routes."""

from flask import Blueprint, Response, render_template

blueprint = Blueprint("sitemaps", __name__, template_folder="templates")


@blueprint.route("/sitemap.xml")
def primary() -> Response:
    """View: Primary Sitemap XML."""
    sitemap = render_template("sitemaps/sitemap.xml")
    return Response(sitemap, mimetype="text/xml")
