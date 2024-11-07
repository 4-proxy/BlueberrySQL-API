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
__version__ = "0.1.0"

from abc import ABC, abstractmethod


# ______________________________________________________________________________________________________________________
class SQLDataBase(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def _get_info_about_server(self) -> None:
        pass

    @abstractmethod
    def _get_info_about_connection(self) -> None:
        pass
