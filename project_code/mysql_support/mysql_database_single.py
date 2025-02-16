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
__version__ = "0.9.2"

from mysql.connector.connection import MySQLConnection

from abstract.database.sql_database import SQLDataBase
from abstract.api.sql_api_interface import SQLAPIInterface
from abstract.database.connection_interface import SingleConnectionInterface

from typing import Any, Dict, Iterable, Optional


# ______________________________________________________________________________________________________________________
class MySQLDataBaseSingle(SQLDataBase, SingleConnectionInterface[MySQLConnection], SQLAPIInterface):
    def __init__(self, **dbconfig: Any) -> None:
        SQLDataBase.__init__(self=self, **dbconfig)

        self.__connection_with_database: MySQLConnection = None  # type: ignore

        self.create_new_connection_with_database()

    # ------------------------------------------------------------------------------------------------------------------
    def create_new_connection_with_database(self) -> None:
        dbconfig: Dict[str, Any] = self.dbconfig
        connection = MySQLConnection(**dbconfig)

        self.__connection_with_database = connection

    # ------------------------------------------------------------------------------------------------------------------
    def get_connection_with_database(self) -> MySQLConnection:
        return self.__connection_with_database

    # ------------------------------------------------------------------------------------------------------------------
    def close_active_connection_with_database(self) -> None:
        active_connection: MySQLConnection = self.get_connection_with_database()

        if active_connection is not None:
            active_connection.close()

    # ------------------------------------------------------------------------------------------------------------------
    def execute_query_no_returns(self, sql_query: str, query_data: Optional[Iterable] = None) -> None:
        connection: MySQLConnection = self.get_connection_with_database()

        with connection.cursor() as cur:
            if query_data:
                cur.execute(operation=sql_query, params=query_data)
            else:
                cur.execute(operation=sql_query)

            connection.commit()

    # ------------------------------------------------------------------------------------------------------------------
    def execute_query_returns_one(self, sql_query: str, query_data: Optional[Iterable] = None) -> Any:
        connection: MySQLConnection = self.get_connection_with_database()

    # ------------------------------------------------------------------------------------------------------------------
    def execute_query_returns_all(self, sql_query: str, query_data: Optional[Iterable] = None) -> Iterable[Any]:
        connection: MySQLConnection = self.get_connection_with_database()

    # ------------------------------------------------------------------------------------------------------------------
    def __str__(self) -> str:
        return ""

    # ------------------------------------------------------------------------------------------------------------------
    def _get_info_about_server(self) -> str:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def _get_info_about_connection(self) -> str:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def __del__(self) -> None:
        self.close_active_connection_with_database()
