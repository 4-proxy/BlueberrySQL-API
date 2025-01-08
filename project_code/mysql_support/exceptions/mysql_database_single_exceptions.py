"""
Custom Exceptions for `MySQLDataBaseSingle` from `mysql_database_single.py` file.

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'MySQLDataBaseSingleConnectionError',
    'MySQLDataBaseSingleQueryError',
    'MySQLDataBaseSingleInitializationError',
]

__author__ = "4-proxy"
__version__ = "0.1.0"


# ______________________________________________________________________________________________________________________
class MySQLDataBaseSingleError(Exception):
    """
    Base exception for errors related to the `MySQLDataBaseSingle` class.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


# ______________________________________________________________________________________________________________________
class MySQLDataBaseSingleConnectionError(MySQLDataBaseSingleError):
    """
    Raised when a connection-related failure occurs in `MySQLDataBaseSingle`.
    """
    pass


# ______________________________________________________________________________________________________________________
class MySQLDataBaseSingleQueryError(MySQLDataBaseSingleError):
    """
    Raised when a query-related error occurs in `MySQLDataBaseSingle`.
    """
    pass


# ______________________________________________________________________________________________________________________
class MySQLDataBaseSingleInitializationError(MySQLDataBaseSingleError):
    """
    Raised when initialization of `MySQLDataBaseSingle` fails or is misconfigured.
    """
    pass
