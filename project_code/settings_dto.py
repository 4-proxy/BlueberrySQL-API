# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    "PoolConfigDTO"
]

__author__ = "4-proxy"
__version__ = "0.3.0"


from dataclasses import dataclass


# _____________________________________________________________________________
@dataclass(frozen=True)
class PoolConfigDTO:
    pool_reset_session: bool
    pool_size: int
    pool_name: str

    def __post_init__(self) -> None:
        if not isinstance(self.pool_name, str):  # type: ignore
            raise TypeError("The pool_name field must be a string!")

        if not isinstance(self.pool_size, int):  # type: ignore
            raise TypeError("The pool_size field must be an integer!")

        if not isinstance(self.pool_reset_session, bool):  # type: ignore
            raise TypeError("The pool_reset_session field must be a bool!")

        if self.pool_name.isspace() or self.pool_name == "":
            raise ValueError("The pool_name value cannot be an empty string!")

        if self.pool_size <= 0:
            raise ValueError("The pool_size value cannot be <= 0!")

        elif self.pool_size > 32:
            raise ValueError(
                "MySQL limits! The pool_size value cannot be > 32!"
            )

        if len(self.pool_name) > 64:
            raise ValueError(
                "MySQL limits! The length of pool_name value cannot be > 64!"
            )
