# Copyright (c) 2025 Linh Pham
# search.marsupialgurgle.com is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Application Bootstrap Script for Marsupial Gurgle Audio Search Site."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
