# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    "MySQLDataBase",
]

__author__ = "4-proxy"
__version__ = "0.5.0"

from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection

from settings_dto import PoolConfigDTO

from typing import Any, Dict
from database_types.exceptions import *


# _____________________________________________________________________________
class MySQLDataBase:
    def __init__(self, pool_config: PoolConfigDTO, **dbconfig: Any) -> None:
        self.__is_instance_PoolConfigDTO(inspected_obj=pool_config)

        self._pool_config: PoolConfigDTO = pool_config
        self._dbconfig: Dict[str, Any] = dbconfig

        self._pool: MySQLConnectionPool = self.create_connection_pool()

    # =========================================================================
    def __is_instance_PoolConfigDTO(self, inspected_obj: Any) -> None:
        if not isinstance(inspected_obj, PoolConfigDTO):
            raise IsNotPoolConfigDTO()

    # -------------------------------------------------------------------------
    def create_connection_pool(self) -> MySQLConnectionPool:
        name: str = self._pool_config.pool_name
        size: int = self._pool_config.pool_size
        reset_session: bool = self._pool_config.pool_reset_session

        pool = MySQLConnectionPool(pool_name=name,
                                   pool_size=size,
                                   pool_reset_session=reset_session,
                                   **self._dbconfig)

        return pool

    # -------------------------------------------------------------------------
    def get_connection_from_pool(self) -> PooledMySQLConnection:
        pool: MySQLConnectionPool = self._pool

        connection: PooledMySQLConnection = pool.get_connection()

        return connection
