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
    """PoolConfigDTO represents a frozen data transfer object (DTO) for pool configuration.

    This abstract class is used to hold configuration data for a pool.
    Being a frozen `dataclass`, instances of this class cannot be modified after creation,
    ensuring that the configuration remains immutable.
    Subclasses must implement the `validate_fields_data` method
    to provide specific validation logic for the configuration fields.

    Args:
        ABC: class from the `abc` module, which allows the creation
        of abstract classes in Python.

    Attributes:
        name (str): The name of the pool configuration.
        size (int): The size of the pool (how many connections are available).
        reset_session (bool): Whether to reset a data of connection after returning to the pool.
    """
    name: str
    size: int
    reset_session: bool

    # ------------------------------------------------------------------------------------------------------------------
    def __post_init__(self) -> None:
        """__post_init__ post-initialization to validate this class.

        This method calls the `validate_fields_data` method to verify that the
        provided field values meet the necessary criteria.

        *This method is called automatically after the instance is created.
        *The method can be extended by subclasses if the validation logic
        is not limited to the `validate_fields_data` method.
        """
        self.validate_fields_data()

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def validate_fields_data(self) -> None:
        """validate_fields_data validates the fields of the pool configuration.

        This abstract method must be implemented by subclasses to provide
        specific validation logic for the pool configuration fields.
        It should raise an appropriate exception if any field values are
        found to be invalid.

        *Specific/custom exception types are desirable.
        """
        pass
