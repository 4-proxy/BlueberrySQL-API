# -*- coding: utf-8 -*-

"""
This module defines abstract interfaces for working with database connections.

This module contains two abstract classes `SingleConnectionInterface` and `PoolConnectionInterface`,
which define contracts for implementing database connections.

The `SingleConnectionInterface` is designed to handle single connection,
while the `PoolConnectionInterface` provides management of connection pool.

*Relationship with other modules:
    `sql_database`: The implementations of these interfaces are used by the `SQLDataBase`
                    to manage the connections to specific databases.
    `sql_api_interface`: The API interface uses these connections to perform database queries.

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'PoolConnectionInterface',
    'SingleConnectionInterface',
]

__author__ = "4-proxy"
__version__ = "0.4.0"

from abc import ABC, abstractmethod


# ______________________________________________________________________________________________________________________
class SingleConnectionInterface[ConnectionType](ABC):
    """SingleConnectionInterface abstract interface for handling a single database connection.

    This abstract interface defines basic methods for handling a single database connection.

    *Implementations are required to provide specific logic
    for connecting to a particular database type.

    Args:
        ABC: Class from the `abc` module, which allows the creation
             of abstract classes in Python.
    """

    @abstractmethod
    def create_new_connection_with_database(self) -> None:
        """create_new_connection_with_database establishes a connection to the database.

        This abstract method must be establishes connection to the database
        using the provided configuration and assign it to the intended field.
        That is, this method is a setter for a connection with database.

        *Implementations should also ensure that they check for an
        active connection before attempting to create a new one.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def get_connection_with_database(self) -> ConnectionType:
        """get_connection_with_database returns the current active connection with database.

        This abstract method must be implemented to return the current active connection.

        *If no active connection exists, it should attempt to create one.

        Returns:
            ConnectionType: An instance of the currently active connection with database.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def close_active_connection_with_database(self) -> None:
        """close_active_connection_with_database closes the current active connection with the database.

        This abstract method must be implemented to properly close the active connection
        to the database, ensuring that all resources are released and any necessary cleanup
        is performed.

        *Implementations should check if an active connection exists before attempting to close it,
        and handle any exceptions that may arise during the closing process.
        """
        pass


# ______________________________________________________________________________________________________________________
class PoolConnectionInterface[PooledConnectionType](ABC):
    """PoolConnectionInterface interface for handling connection pool of database.

    This abstract interface defines basic methods for handling a single database connection.

    *Implementations are required to provide specific logic
    for connecting to a particular database type.

    Args:
        ABC: Class from the `abc` module, which allows the creation
             of abstract classes in Python.
    """

    @abstractmethod
    def create_new_connection_pool(self) -> None:
        """create_new_connection_pool create a pool of database connections.

        This abstract method should create a database connection pool
        using the provided configuration and assign it to the intended field.
        That is, this method is a setter for a connection pool.

        *Implementations should also make sure that they check for an
        active connection pool before attempting to create a new one.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def get_connection_from_pool(self) -> PooledConnectionType:
        """get_connection_from_pool returns a connection from current pool.

        This abstract method must be return a pooled connection from current connection pool to database.

        *Provision should be provide a response to connection rejection when an exception is raised.
        For example, the pool is out of available connections.

        Returns:
            PooledConnectionType: An instance of the connection with database from current pool.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def close_active_pool(self) -> None:
        """close_active_pool closes the current connection pool.

        This abstract method should properly close all active connections
        within the connection pool and release any associated resources.

        *Implementations must ensure that all connections are safely terminated
        and that no further operations can be performed on the closed pool.
        """
        pass
