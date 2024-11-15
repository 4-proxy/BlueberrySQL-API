# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'PoolConnectionInterface',
]

__author__ = "4-proxy"
__version__ = "0.1.0"

from abc import ABC, abstractmethod


# ______________________________________________________________________________________________________________________
class PoolConnectionInterface[ConnectionPoolType, PooledConnectionType](ABC):
    @abstractmethod
    def create_connection_pool(self, **dbconfig) -> ConnectionPoolType:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def get_connection_from_pool(self) -> PooledConnectionType:
        pass
