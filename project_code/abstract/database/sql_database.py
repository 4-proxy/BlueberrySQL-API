# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'SQLDataBase'
]

__author__ = "4-proxy"
__version__ = "0.2.0"

from abc import ABC, abstractmethod

from typing import Dict, Any


# ______________________________________________________________________________________________________________________
class SQLDataBase(ABC):
    def __init__(self, **dbconfig) -> None:
        self.dbconfig = dbconfig

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def dbconfig(self) -> Dict[str, Any]:
        return self.__dbconfig

    # ------------------------------------------------------------------------------------------------------------------
    @dbconfig.setter
    def dbconfig(self, new_dbconfig: Dict[str, Any]) -> None:
        self.__dbconfig: Dict[str, Any] = new_dbconfig

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def __repr__(self) -> str:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _get_info_about_server(self) -> str:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _get_info_about_connection(self) -> str:
        pass
