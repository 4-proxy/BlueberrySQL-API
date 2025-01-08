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
__version__ = "0.4.0"

from mysql.connector.connection import MySQLConnection

from abstract.database.sql_database import SQLDataBase
from abstract.api.sql_api_interface import SQLAPIInterface
from abstract.database.connection_interface import SingleConnectionInterface

from typing import Any, Iterable


# ______________________________________________________________________________________________________________________
class MySQLDataBaseSingle(SQLDataBase, SingleConnectionInterface[MySQLConnection], SQLAPIInterface):
    def __init__(self, **dbconfig) -> None:
        SQLDataBase.__init__(self=self, **dbconfig)

        self.__connection_with_database: MySQLConnection = None

        self.create_new_connection_with_database()

    # ------------------------------------------------------------------------------------------------------------------
    def create_new_connection_with_database(self) -> None:
        connection = MySQLConnection()

        self.__connection_with_database = connection

    # ------------------------------------------------------------------------------------------------------------------
    def get_connection_with_database(self) -> MySQLConnection:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def close_active_connection_with_database(self) -> None:
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
    def __str__(self) -> str:
        return ""

    # ------------------------------------------------------------------------------------------------------------------
    def _get_info_about_server(self) -> str:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def _get_info_about_connection(self) -> str:
        pass
