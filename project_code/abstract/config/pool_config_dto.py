# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'PoolConfigDTO'
]

__author__ = "4-proxy"
__version__ = "0.1.0"

from dataclasses import dataclass
from abc import ABC, abstractmethod


# ______________________________________________________________________________________________________________________
@dataclass(frozen=True)
class PoolConfigDTO(ABC):
    name: str
    size: int
    reset_session: bool

    # ------------------------------------------------------------------------------------------------------------------
    def __post_init__(self) -> None:
        self.validate_fields_data()

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def validate_fields_data(self) -> None:
        pass
