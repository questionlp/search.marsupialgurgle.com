# Copyright (c) 2025-2026 Linh Pham
# search.marsupialgurgle.com is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Search Utility Functions."""

from datetime import datetime

import pytz
from flask import current_app

_utc_timezone = pytz.timezone("UTC")


def current_year(time_zone: pytz.timezone = _utc_timezone):
    """Return the current year."""
    now = datetime.now(time_zone)
    return now.strftime("%Y")


def pagination_list(current_page: int, total_pages: int) -> list[int | None] | None:
    """Generate a list of pagination entries."""
    if not current_page or not total_pages:
        return None

    if total_pages <= 7:
        return list(range(1, total_pages + 1))

    if current_page <= 3 or total_pages - current_page <= 2:
        return [1, 2, 3, None, total_pages - 2, total_pages - 1, total_pages]

    return [1, 2, None, current_page, None, total_pages - 1, total_pages]


def redirect_url(url: str, status_code: int = 302):
    """Returns a redirect response for a given URL."""
    # Use a custom response class to force set response headers
    # and handle the redirect to prevent browsers from caching redirect
    response = current_app.response_class(
        response=None, status=status_code, mimetype="text/plain"
    )

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = 0
    response.headers["Location"] = url
    return response


def time_zone_parser(time_zone: str) -> pytz.timezone:
    """Parses a time zone name into a pytz.timezone object.

    Returns pytz.timezone object and string if time_zone is valid.
    Otherwise, returns UTC if time zone is not a valid tz value.
    """
    try:
        time_zone_object = pytz.timezone(time_zone)
        time_zone_string = time_zone_object.zone
    except (pytz.UnknownTimeZoneError, AttributeError, ValueError):
        time_zone_object = pytz.timezone("UTC")
        time_zone_string = time_zone_object.zone

    return time_zone_object, time_zone_string
