# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    "IsNotPoolConfigDTO",
]

__author__ = "4-proxy"
__version__ = "0.1.1"

from typing import Any


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class IsNotPoolConfigDTO(Exception):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        message = "The pool settings argument is not an instance of PoolConfigDTO!"
        super().__init__(message, *args, **kwargs)
