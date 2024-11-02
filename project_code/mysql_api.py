# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    "MySQLAPI",
]

__author__ = "4-proxy"
__version__ = "0.1.0"

from mysql_database import MySQLDataBase


# ______________________________________________________________________________________________________________________
class MySQLAPI:
    def __init__(self, db: MySQLDataBase) -> None:
        self._db: MySQLDataBase = db

    # ------------------------------------------------------------------------------------------------------------------
    def execute_query_no_returns(self, sql_query: str, *query_data) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def execute_query_returns_one(self, sql_query: str, *query_data) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def execute_query_returns_all(self, sql_query: str, *query_data) -> None:
        pass
