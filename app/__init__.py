# Copyright (c) 2025 Linh Pham
# search.marsupialgurgle.com is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Application Initialization for Flask Application."""

from flask import Flask
from flask_sanitize_escape import SanitizeEscapeExtension

from app import config
from app.errors import handlers
from app.main.redirects import blueprint as redirects_bp
from app.main.routes import blueprint as main_bp
from app.sitemaps.routes import blueprint as sitemaps_bp
from app.utilities import current_year
from app.version import APP_VERSION


def create_app() -> Flask:
    """Create and initialize Flask application."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Override Jinja block-related options
    app.jinja_options = Flask.jinja_options.copy()
    app.jinja_options["trim_blocks"] = True
    app.jinja_options["lstrip_blocks"] = True
    app.create_jinja_environment()

    # Register error handlers
    app.register_error_handler(404, handlers.not_found)
    app.register_error_handler(500, handlers.handle_exception)

    # Load Application and Database Settings Files
    _app_settings = config.load_app_settings()
    _database_settings = config.load_database_settings()
    _database_settings["time_zone"] = _app_settings["time_zone"]

    app.config["app_settings"] = _app_settings
    app.config["database_settings"] = _database_settings

    # Add Jinja globals
    app.jinja_env.globals["app_version"] = APP_VERSION
    app.jinja_env.globals["block_ai_scrapers"] = bool(
        _app_settings.get("block_ai_scrapers", False)
    )
    app.jinja_env.globals["enable_query_expansion_mode"] = bool(
        _app_settings.get("enable_query_expansion_mode", False)
    )
    app.jinja_env.globals["current_year"] = current_year
    app.jinja_env.globals["git_repository"] = _app_settings.get("git_repository")
    app.jinja_env.globals["max_query_length"] = _app_settings["max_query_length"]
    app.jinja_env.globals["mg_audio_url_prefix"] = _app_settings.get(
        "mg_audio_url_prefix"
    )
    app.jinja_env.globals["results_per_page"] = _app_settings.get("results_per_age", 15)
    app.jinja_env.globals["site_url"] = _app_settings.get("site_url")
    app.jinja_env.globals["time_zone"] = _app_settings["app_time_zone"]
    app.jinja_env.globals["umami"] = _app_settings["umami"]
    app.jinja_env.globals["use_minified_css"] = bool(
        _app_settings.get("use_minified_css", False)
    )

    # Register Flask Sanitize Escape
    sanitize_extension = SanitizeEscapeExtension(app, sanitize_quotes=False)
    sanitize_extension.init_app(app)

    # Register Application Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(redirects_bp)
    app.register_blueprint(sitemaps_bp)

    return app
