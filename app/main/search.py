# Copyright (c) 2025-2026 Linh Pham
# search.marsupialgurgle.com is released under the terms of the MIT License
# SPDX-License-Identifier: MIT
#
# vim: set noai syntax=python ts=4 sw=4:
"""Clip Search Functions."""

from enum import Enum
from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from mysql.connector.errors import DatabaseError, ProgrammingError
from mysql.connector.pooling import PooledMySQLConnection
from slugify import slugify


class SearchMode(Enum):
    """Query search mode."""

    NATURAL = 1
    BOOLEAN = 2
    EXPANDED = 3


def search_clips(
    search_query: str,
    search_mode: SearchMode,
    results_per_page: int,
    offset: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, int | list[dict]]:
    """Search audio clips from the database.

    Returns dictionary with three keys: total_count, returned_count, and
    results. The results value includes a list of search results.
    """
    if not search_query or results_per_page is None or offset is None:
        return None

    if results_per_page <= 0 or offset is None or offset < 0:
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=True)
    try:
        match search_mode:
            case SearchMode.NATURAL:
                query = (
                    "SELECT COUNT(c.id) AS total_count "
                    "FROM clips c "
                    "JOIN tags t ON t.clip_id = c.id "
                    "WHERE MATCH (t.title, t.album, t.artist) "
                    "AGAINST (%s IN NATURAL LANGUAGE MODE)"
                )
            case SearchMode.BOOLEAN:
                query = (
                    "SELECT COUNT(c.id) AS total_count "
                    "FROM clips c "
                    "JOIN tags t ON t.clip_id = c.id "
                    "WHERE MATCH (t.title, t.album, t.artist) "
                    "AGAINST (%s IN BOOLEAN MODE)"
                )
            case SearchMode.EXPANDED:
                query = (
                    "SELECT COUNT(c.id) AS total_count "
                    "FROM clips c "
                    "JOIN tags t ON t.clip_id = c.id "
                    "WHERE MATCH (t.title, t.album, t.artist) "
                    "AGAINST (%s WITH QUERY EXPANSION)"
                )
        cursor.execute(query, (search_query,))
        result = cursor.fetchone()
    except ProgrammingError:
        return {"error": "ProgrammingError"}
    except DatabaseError:
        return {"error": "DatabaseError"}
    finally:
        cursor.close()

    if result is None:
        return {"total_count": 0, "returned_count": 0, "results": []}

    total_count: int = result["total_count"]
    if total_count == 0:
        return {"total_count": 0, "returned_count": 0, "results": []}

    cursor: MySQLCursor | Any = database_connection.cursor(dictionary=True)
    try:
        match search_mode:
            case SearchMode.NATURAL:
                query = (
                    "SELECT c.id, c.key, c.mp3, c.m4a, c.m4r, t.artist, t.album, "
                    "t.title, t.year "
                    "FROM clips c "
                    "JOIN tags t ON t.clip_id = c.id "
                    "WHERE MATCH (t.title, t.album, t.artist) "
                    "AGAINST (%s IN NATURAL LANGUAGE MODE) "
                    "LIMIT %s OFFSET %s"
                )
                cursor.execute(
                    query,
                    (
                        search_query,
                        results_per_page,
                        offset,
                    ),
                )
            case SearchMode.BOOLEAN:
                query = (
                    "SELECT c.id, c.key, c.mp3, c.m4a, c.m4r, t.artist, t.album, "
                    "t.title, t.year, MATCH (t.title, t.album, t.artist) "
                    "AGAINST (%s IN BOOLEAN MODE) AS score "
                    "FROM clips c "
                    "JOIN tags t ON t.clip_id = c.id "
                    "WHERE MATCH (t.title, t.album, t.artist) "
                    "AGAINST (%s IN BOOLEAN MODE) "
                    "ORDER BY score DESC "
                    "LIMIT %s OFFSET %s"
                )
                cursor.execute(
                    query,
                    (
                        search_query,
                        search_query,
                        results_per_page,
                        offset,
                    ),
                )
            case SearchMode.EXPANDED:
                query = (
                    "SELECT c.id, c.key, c.mp3, c.m4a, c.m4r, t.artist, t.album, "
                    "t.title, t.year "
                    "FROM clips c "
                    "JOIN tags t ON t.clip_id = c.id "
                    "WHERE MATCH (t.title, t.album, t.artist) "
                    "AGAINST (%s WITH QUERY EXPANSION) "
                    "LIMIT %s OFFSET %s"
                )
                cursor.execute(
                    query,
                    (
                        search_query,
                        results_per_page,
                        offset,
                    ),
                )

        results = cursor.fetchall()
    except ProgrammingError:
        return {"error": "ProgrammingError"}
    except DatabaseError:
        return {"error": "DatabaseError"}
    finally:
        cursor.close()

    if not results:
        return {"total_count": 0, "returned_count": 0, "results": []}

    clips: list[dict] = []
    for row in results:
        clips.append(
            {
                "id": row["id"],
                "key": row["key"],
                "key_slug": slugify(row["key"]),
                "mp3_path": f"{row['key']}.mp3" if bool(row["mp3"]) else None,
                "m4a_path": f"{row['key']}.m4a" if bool(row["m4a"]) else None,
                "m4r_path": f"{row['key']}.m4r" if bool(row["m4r"]) else None,
                "artist": row["artist"],
                "album": row["album"],
                "title": row["title"],
                "year": row["year"],
            }
        )

    return {"total_count": total_count, "returned_count": len(clips), "results": clips}
