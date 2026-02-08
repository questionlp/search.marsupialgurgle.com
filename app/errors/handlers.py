# Copyright (c) 2025-2026 Linh Pham
# search.marsupialgurgle.com is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Application Error Handlers."""

from typing import Literal

from flask import render_template


def not_found(error) -> tuple[str, Literal[404]]:
    """Handle resource not found conditions."""
    return render_template("errors/404.html", error=error), 404


def handle_exception(error) -> tuple[str, Literal[500]]:
    """Handle exceptions in a semi-graceful manner."""
    return render_template("errors/500.html", error=error), 500
