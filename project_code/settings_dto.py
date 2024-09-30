# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    "PoolSettingsDTO"
]

__author__ = "4-proxy"
__version__ = "0.1.0"


from dataclasses import dataclass


@dataclass(frozen=True)
class PoolSettingsDTO:
    pool_reset_session: bool
    pool_size: int
    pool_name: str
