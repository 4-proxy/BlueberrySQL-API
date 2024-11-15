# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'SQLAPIInterface',
]

__author__ = "4-proxy"
__version__ = "0.1.1"

from abc import ABC, abstractmethod

from typing import Any, Iterable


# ______________________________________________________________________________________________________________________
class SQLAPIInterface(ABC):
    @abstractmethod
    def execute_query_no_returns(self, sql_query: str, *query_data) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def execute_query_returns_one(self, sql_query: str, *query_data) -> Any:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def execute_query_returns_all(self, sql_query: str, *query_data) -> Iterable[Any]:
        pass
