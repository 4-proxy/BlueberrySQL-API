# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'MySQLDataBaseSingle'
]

__author__ = "4-proxy"
__version__ = "0.1.0"

from typing import Any, Iterable
from abstract.database.sql_database import SQLDataBase
from abstract.api.sql_api_interface import SQLAPIInterface
from abstract.database.connection_interface import SingleConnectionInterface


# ______________________________________________________________________________________________________________________
class MySQLDataBaseSingle(SQLDataBase, SingleConnectionInterface, SQLAPIInterface):
    def create_connection_with_database(self, **dbconfig) -> Any:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def get_connection_with_database(self) -> Any:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def execute_query_no_returns(self, sql_query: str, *query_data) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def execute_query_returns_one(self, sql_query: str, *query_data) -> Any:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def execute_query_returns_all(self, sql_query: str, *query_data) -> Iterable[Any]:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def _get_info_about_server(self) -> str:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def _get_info_about_connection(self) -> str:
        pass
