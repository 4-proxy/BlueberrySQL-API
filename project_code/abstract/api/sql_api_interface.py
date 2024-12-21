# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'SQLAPIInterface',
]

__author__ = "4-proxy"
__version__ = "0.2.2"

from abc import ABC, abstractmethod

from typing import Any, Iterable


# ______________________________________________________________________________________________________________________
class SQLAPIInterface(ABC):
    """SQLAPIInterface abstract interface representing basic interaction with SQL databases.

    This interface is used to be implemented by other classes,
    which are API wrapper for working with a specific SQL database type.

    *This interface is provided to extended by specific database implementations
    (e.g., MySQL, PostgreSQL, SQLite) to provide database-specific functionality.

    Args:
        ABC: Class from the `abc` module, which allows the creation
             of abstract classes in Python.
    """

    @abstractmethod
    def execute_query_no_returns(self, sql_query: str, *query_data) -> None:
        """execute_query_no_returns executes a SQL query that does not return any results.

        This abstract method must be implemented by subclasses to execute SQL commands
        that modify the database (e.g., INSERT, UPDATE, DELETE) and do not return any data.

        *Ensure that the SQL query is properly parameterized to prevent SQL injection.

        Args:
            sql_query (str): The SQL command to be executed.
            query_data (tuple): Optional parameters to be used in the SQL command.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def execute_query_returns_one(self, sql_query: str, *query_data) -> Any:
        """execute_query_returns_one executes a SQL query that is expected to return a single result.

        This abstract method must be implemented by subclasses to execute SQL queries
        that return a single row of data (e.g., SELECT).

        *If no results are found, this method should return `None`.

        Args:
            sql_query (str): The SQL command to be executed.
            query_data (tuple): Optional parameters to be used in the SQL command.

        Returns:
            Any: The single result row, or `None` if no results are found.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def execute_query_returns_all(self, sql_query: str, *query_data) -> Iterable[Any]:
        """execute_query_returns_all executes a SQL query that is expected to return multiple results.

        This abstract method must be implemented by subclasses to execute SQL queries
        that return multiple rows of data (e.g., SELECT statements).

        *The results should be returned as an iterable collection of Python (e.g., `list`, `tuple`).
        *If no results are found, this method should return `None`.

        Args:
            sql_query (str): The SQL command to be executed.
            query_data (tuple): Optional parameters to be used in the SQL command.

        Returns:
            Iterable[Any]: An iterable collection of result rows, or `None` if no results are found.
        """
        pass
