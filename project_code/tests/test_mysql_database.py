# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = []

__author__ = "4-proxy"
__version__ = "0.1.0"


import unittest

from unittest.mock import MagicMock

from mysql_database import MySQLDataBase
from settings_dto import PoolSettingsDTO

from typing import Any, Dict


# _____________________________________________________________________________
class PositiveTestMySQLDataBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = MySQLDataBase

    # -------------------------------------------------------------------------
    def test_constructor_accepts_PoolSettingsDTO(self) -> None:
        # Build
        mock_pool_settings = MagicMock(spec=PoolSettingsDTO)

        # Check
        self._tested_class(mock_pool_settings)

    # -------------------------------------------------------------------------
    def test_pool_settings_field_is_instance_of_PoolSettingsDTO(self) -> None:
        # Build
        mock_pool_settings = MagicMock(spec=PoolSettingsDTO)
        expected_field_name = '_pool_settings'

        # Operate
        test_instance = self._tested_class(mock_pool_settings)

        # Check
        expected_field: Any = getattr(test_instance, expected_field_name)
        self.assertIsInstance(
            obj=expected_field,
            cls=PoolSettingsDTO,
            msg="Failure! The inspected field object is not instance of PoolSettingsDTO!"
        )


# _____________________________________________________________________________
class NegativeTestMySQLDataBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = MySQLDataBase

    # -------------------------------------------------------------------------
    def test_constructor_raise_IsNotPoolSettingDTO(self) -> None:
        from database_types.exceptions import IsNotPoolSettingsDTO

        # Build
        test_pool_settings: Dict[str, Any] = {
            "pool_name": "PoolSettings",
            "pool_size": 5,
            "pool_reset_session": True
        }

        # Check
        with self.assertRaises(expected_exception=IsNotPoolSettingsDTO):
            self._tested_class(test_pool_settings)  # type: ignore
