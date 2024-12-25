# -*- coding: utf-8 -*-

"""
This module provides an abstract base class `SQLDataBase`
for creating specific SQL database implementations.

*Relationship with other modules:
    `connection_interface`: Uses connection interfaces to control the selected connection type.
    `sql_api_interface`: Provides an API for executing database queries.

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'SQLDataBase'
]

__author__ = "4-proxy"
__version__ = "0.4.0"

from abc import ABC, abstractmethod

from typing import Dict, Any


# ______________________________________________________________________________________________________________________
class SQLDataBase(ABC):
    """SQLDataBase abstract base class for SQL database.

    This class is used as a blueprint for creating specific database classes.

    *This class doesn't provide a direct interface for interacting with the database connection itself.
    Instead, it requires the implementation of a suitable interface for the type of connection
    (single connection or connection pool) to be used in conjunction.

    Args:
        ABC: Class from the `abc` module, which allows the creation
             of abstract classes in Python.
    """

    def __init__(self, **dbconfig) -> None:
        """__init__ initializes an instance of this class.

        This constructor accepts keyword arguments for database configuration,
        which can include parameters such as host, port, user, password, etc.

        *It is acceptable to establish a database connection when creating an instance
        to avoid calling the required methods outside the constructor.

        Args:
            dbconfig (dict): A dictionary containing database configuration parameters.
        """
        self.dbconfig = dbconfig

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def dbconfig(self) -> Dict[str, Any]:
        return self.__dbconfig

    # ------------------------------------------------------------------------------------------------------------------
    @dbconfig.setter
    def dbconfig(self, new_dbconfig: Dict[str, Any]) -> None:
        """dbconfig setter of the field.

        This setter allows updating the database configuration parameters.

        *It is important to make sure that the active connection method will be disconnected
        to allow `dbconfig` to be changed.

        Args:
            new_dbconfig (Dict[str, Any]): A dictionary containing new database configuration parameters.
        """
        self.__dbconfig: Dict[str, Any] = new_dbconfig

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def __repr__(self) -> str:
        """__repr__ presents an instance of SQLDataBase.

        This abstract method must be implemented in order to display
        complete details about the present object.

        *For example, since it is a database, it would be correct to display information
        about the DBMS/DB or the connection established and its parameters.

        Returns:
            str: A string representation of the instance.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _get_info_about_server(self) -> str:
        """_get_info_about_server retrieves information about the database server.

        This method must be implemented in derived classes to return
        relevant details about the database server, such as version,
        status, and other pertinent information.

        *If the DBMS is not a server-side DBMS (e.g., SQLite),
        the purpose of this method is to gather information about the
        database itself, such as the database file name and version.

        Returns:
            str: Information about the database server.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _get_info_about_connection(self) -> str:
        """_get_info_about_connection retrieves information about the current database connection.

        This method should be implemented in derived classes to provide details
        about the current connection, including connection status, parameters,
        and any other relevant information.

        *By `connection` is meant both a single connection and a connection pool.

        Returns:
            str: Information about the current database connection.
        """
        pass
