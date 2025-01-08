# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'MySQLPoolConfigDTO'
]

__author__ = "4-proxy"
__version__ = "0.1.0"

from mysql.connector.pooling import CNX_POOL_MAXSIZE, CNX_POOL_MAXNAMESIZE

from abstract.config.pool_config_dto import PoolConfigDTO


# ______________________________________________________________________________________________________________________
class MySQLPoolConfigDTO(PoolConfigDTO):
    def validate_fields_data(self) -> None:
        if not isinstance(self.name, str):
            raise TypeError("The *name* field of pool config must be a string!")

        if not isinstance(self.size, int):
            raise TypeError("The *size* field of pool config must be an integer!")

        if not isinstance(self.reset_session, bool):
            raise TypeError("The *reset_session* field of pool config must be a bool!")

        if not self.name.strip():
            raise ValueError("The *name* field value cannot be an empty string!")

        if self.size <= 0:
            raise ValueError("The *size* field value cannot be <= 0!")

        elif self.size > CNX_POOL_MAXSIZE:
            raise ValueError(f"MySQL limits! The *size* field value cannot be > {CNX_POOL_MAXSIZE}!")

        if len(self.name) > CNX_POOL_MAXNAMESIZE:
            raise ValueError(f"MySQL limits! The length of *name* field value cannot be > {CNX_POOL_MAXNAMESIZE}!")
