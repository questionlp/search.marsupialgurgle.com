# Copyright (c) 2025 Linh Pham
# search.marsupialgurgle.com is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Clip Information Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from mysql.connector.errors import DatabaseError, ProgrammingError
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify


def retrieve_clip_info(
    clip_key: str, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[str, int | str | bool | None] | None:
    """Retrieve clip information for a requested clip key ID.

    Returns a dictionary with clip information, including path,
    available file extensions and parsed audio tag metadata.
    """
    if not clip_key:
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    try:
        query = (
            "SELECT c.id, c.key, c.mp3, c.m4a, c.m4r, t.artist, t.album, "
            "t.title, t.year "
            "FROM clips c "
            "JOIN tags t ON t.clip_id = c.id "
            "WHERE c.key = %s "
            "LIMIT 1"
        )
        cursor: MySQLCursor = database_connection.cursor(dictionary=True)
        cursor.execute(query, (clip_key,))
        result = cursor.fetchone()
    except ProgrammingError:
        return {"error": "ProgrammingError"}
    except DatabaseError:
        return {"error": "DatabaseError"}
    finally:
        cursor.close()

    if not result:
        return None

    return {
        "id": result["id"],
        "key": result["key"],
        "key_slug": slugify(result["key"]),
        "mp3_path": f"{result['key']}.mp3" if bool(result["mp3"]) else None,
        "m4a_path": f"{result['key']}.m4a" if bool(result["m4a"]) else None,
        "m4r_path": f"{result['key']}.m4r" if bool(result["m4r"]) else None,
        "artist": result["artist"],
        "album": result["album"],
        "title": result["title"],
        "year": result["year"],
    }
