# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'MySQLPoolConfigDTO',
    'MySQLPoolConfigError',
]

__author__ = "4-proxy"
__version__ = "0.2.0"

from mysql.connector.pooling import CNX_POOL_MAXSIZE, CNX_POOL_MAXNAMESIZE

from abstract.config.pool_config_dto import PoolConfigDTO


# ______________________________________________________________________________________________________________________
class MySQLPoolConfigError(Exception):
    pass


# ______________________________________________________________________________________________________________________
class MySQLPoolConfigDTO(PoolConfigDTO):
    def validate_fields_data(self) -> None:
        if not (isinstance(self.name, str) and
                isinstance(self.size, int) and
                isinstance(self.reset_session, bool)):
            raise MySQLPoolConfigError(
                "The fields: *name*, *size*, and *reset_session* - must be `str`, `int`, `bool` respectively!"
            )

        if not self.name.strip():
            raise MySQLPoolConfigError(
                "The *name* field value cannot be an empty string!"
            )

        if not all(char.isalpha() for char in self.name):
            raise MySQLPoolConfigError(
                "The *name* field doesn't allow alphanumeric, punctuation, or special characters.”"
            )

        if self.size <= 0:
            raise MySQLPoolConfigError(
                "The *size* field value cannot be <= 0!"
            )

        elif self.size > CNX_POOL_MAXSIZE:
            raise MySQLPoolConfigError(
                f"MySQL limits! The *size* field value cannot be > {CNX_POOL_MAXSIZE}!"
            )

        if len(self.name) > CNX_POOL_MAXNAMESIZE:
            raise MySQLPoolConfigError(
                f"MySQL limits! The length of *name* field value cannot be > {CNX_POOL_MAXNAMESIZE}!"
            )
