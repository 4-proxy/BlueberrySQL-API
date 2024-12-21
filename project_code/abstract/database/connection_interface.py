# -*- coding: utf-8 -*-

"""
Module providing abstract interfaces for single and pool database connection implementations.

This module defines two abstract base classes: `SingleConnectionInterface` and `PoolConnectionInterface`.
These interfaces serve as contracts for creating specific implementations of APIs that handle single
database connections and connection pools, respectively.

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'PoolConnectionInterface',
    'SingleConnectionInterface',
]

__author__ = "4-proxy"
__version__ = "0.2.0"

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
    def create_connection_with_database(self, **dbconfig) -> ConnectionType:
        """create_connection_with_database establishes a connection to the database.

        This abstract method must be establishes connection to the database
        using the provided configuration in `dbconfig`.

        *Implementations should also ensure that they check for an
        active connection before attempting to create a new one.

        Args:
            dbconfig (dict): A dictionary containing database configuration parameters
                             for establishing a connection.

        Returns:
            ConnectionType: An instance representing the established database connection.
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


# ______________________________________________________________________________________________________________________
class PoolConnectionInterface[ConnectionPoolType, PooledConnectionType](ABC):
    """PoolConnectionInterface interface for handling connection pool of database.

    This abstract interface defines basic methods for handling a single database connection.

    *Implementations are required to provide specific logic
    for connecting to a particular database type.

    Args:
        ABC: Class from the `abc` module, which allows the creation
             of abstract classes in Python.
    """

    @abstractmethod
    def create_connection_pool(self, **dbconfig) -> ConnectionPoolType:
        """create_connection_pool create a pool of database connections.

        This abstract method must be creates a pool of database connections
        using the provided configuration in `dbconfig`.

        Args:
            dbconfig (dict): A dictionary containing database configuration parameters
                             for create pool connection.

        Returns:
            ConnectionPoolType: An instance representing the connection pool to database.
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
