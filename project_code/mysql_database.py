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
__version__ = "0.3.0"

from mysql.connector.pooling import MySQLConnectionPool

from settings_dto import PoolSettingsDTO

from typing import Any
from database_types.exceptions import *


# _____________________________________________________________________________
class MySQLDataBase:
    def __init__(self, pool_settings: PoolSettingsDTO, **dbconfig: Any) -> None:
        self.__is_instance_PoolSettingsDTO(inspected_obj=pool_settings)

        self._pool_settings: PoolSettingsDTO = pool_settings

    # =========================================================================
    def __is_instance_PoolSettingsDTO(self, inspected_obj: Any) -> None:
        if not isinstance(inspected_obj, PoolSettingsDTO):
            raise IsNotPoolSettingsDTO()

    # -------------------------------------------------------------------------
    def create_pool(self) -> MySQLConnectionPool:
        name: str = self._pool_settings.pool_name
        size: int = self._pool_settings.pool_size
        reset_session: bool = self._pool_settings.pool_reset_session

        pool = MySQLConnectionPool(pool_name=name,
                                   pool_size=size,
                                   pool_reset_session=reset_session
                                   )

        return pool
