# Copyright (c) 2025-2026 Linh Pham
# search.marsupialgurgle.com is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Configuration Loading and Parsing."""

import json
from pathlib import Path

from app.utilities import time_zone_parser


def load_app_settings(
    app_settings_path: str = "app_settings.json",
    app_time_zone: str = "UTC",
    results_per_page: int = 15,
    max_query_string_length: int = 120,
) -> dict[str, dict | int | str | bool] | None:
    """Load application configuration settings."""
    _app_settings_path = Path(app_settings_path)
    if _app_settings_path.exists and _app_settings_path.is_file:
        with _app_settings_path.open(mode="r", encoding="utf-8") as app_settings_file:
            app_settings: dict[str, dict | int | str | bool] | None = json.load(
                app_settings_file
            )

        if not app_settings:
            return None

        # Process Maximum Search Query String Length (default: 120)
        max_query_length: int = int(
            app_settings.get("max_query_length", max_query_string_length)
        )
        max_query_length = max(max_query_length, 1)
        max_query_length = min(max_query_length, max_query_string_length)
        app_settings["max_query_length"] = max_query_length

        app_settings["enable_query_expansion_mode"] = bool(
            app_settings.get("enable_query_expansion_mode", False)
        )

        # Process time zone configuration settings
        time_zone = app_settings.get("time_zone", app_time_zone)
        time_zone_object, time_zone_string = time_zone_parser(time_zone)
        app_settings["app_time_zone"] = time_zone_object
        app_settings["time_zone"] = time_zone_string

        if "umami_analytics" in app_settings:
            umami = dict(app_settings.get("umami_analytics"))
            app_settings["umami"] = {
                "enabled": bool(umami.get("enabled", False)),
                "url": umami.get("url"),
                "website_id": umami.get("data_website_id"),
                "auto_track": bool(umami.get("data_auto_track", True)),
                "host_url": umami.get("data_host_url"),
                "domains": umami.get("data_domains"),
            }

            del app_settings["umami_analytics"]
        else:
            app_settings["umami"] = {"enabled": False}

        try:
            _results_per_page = int(
                app_settings.get("results_per_page", results_per_page)
            )
            app_settings["results_per_page"] = _results_per_page
        except ValueError:
            app_settings["results_per_page"] = results_per_page

        return app_settings

    return None


def load_database_settings(
    database_settings_path: str = "database_settings.json",
    connection_pool_size: int = 10,
    connection_pool_name: str = "mg_search",
) -> dict[str, dict | int | str | bool] | None:
    """Load database connection and configuration settings."""
    _database_settings_path = Path(database_settings_path)
    if _database_settings_path.exists and _database_settings_path.is_file:
        with _database_settings_path.open(
            mode="r", encoding="utf-8"
        ) as databaase_settings_file:
            database_settings: dict[str, dict | int | str | bool] | None = json.load(
                databaase_settings_file
            )

        if not database_settings:
            return None

        use_pool = bool(database_settings.get("use_pool", False))
        if use_pool:
            pool_name: str | None = database_settings.get(
                "pool_name", connection_pool_name
            )
            pool_size: int | None = database_settings.get(
                "pool_size", connection_pool_size
            )

            if pool_size < connection_pool_size:
                pool_size = connection_pool_size

            database_settings["pool_name"] = pool_name
            database_settings["pool_size"] = pool_size
            del database_settings["use_pool"]
        else:
            if "pool_name" in database_settings:
                del database_settings["pool_name"]

            if "pool_size" in database_settings:
                del database_settings["pool_size"]

            if "use_pool" in database_settings:
                del database_settings["use_pool"]

        return database_settings

    return None
