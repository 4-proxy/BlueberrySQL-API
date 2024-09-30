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
__version__ = "0.1.0"


from settings_dto import PoolSettingsDTO

from database_types.exceptions import *

from typing import NoReturn, Optional, Any


# _____________________________________________________________________________
class MySQLDataBase:
    def __init__(self, pool_settings: PoolSettingsDTO) -> None:
        self.__is_instance_PoolSettingsDTO(inspected_object=pool_settings)

        self._pool_settings: PoolSettingsDTO = pool_settings

    # =========================================================================
    def __is_instance_PoolSettingsDTO(self,
                                      inspected_object: Any) -> Optional[NoReturn]:
        if not isinstance(inspected_object,
                          PoolSettingsDTO):
            raise IsNotPoolSettingsDTO()
