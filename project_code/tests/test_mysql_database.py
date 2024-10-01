# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = []

__author__ = "4-proxy"
__version__ = "0.2.0"


import unittest
import unittest.mock as UnitMock

from unittest.mock import MagicMock

import mysql_database as tested_module

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
    def _make_PoolSettingsDTO_mock(self) -> MagicMock:
        mock = MagicMock(spec=PoolSettingsDTO)

        return mock

    # -------------------------------------------------------------------------
    def test_constructor_accepts_PoolSettingsDTO(self) -> None:
        # Build
        mock_pool_settings: MagicMock = self._make_PoolSettingsDTO_mock()

        # Check
        self._tested_class(mock_pool_settings)

    # -------------------------------------------------------------------------
    def test_pool_settings_field_is_PoolSettingsDTO(self) -> None:
        # Build
        mock_pool_settings: MagicMock = self._make_PoolSettingsDTO_mock()
        expected_field_name = '_pool_settings'
        expected_type = PoolSettingsDTO
        test_class = self._tested_class

        # Operate
        test_instance = test_class(mock_pool_settings)

        expected_field: Any = getattr(test_instance, expected_field_name)

        # Check
        self.assertIsInstance(
            obj=expected_field,
            cls=expected_type,
            msg=f"Failure! Inspected field: {expected_field} is not instance of {expected_type}!"
        )

    # -------------------------------------------------------------------------
    def test_constructor_accepts_other_kwargs(self) -> None:
        # Build
        mock_pool_settings: MagicMock = self._make_PoolSettingsDTO_mock()
        test_kwargs: Dict[str, Any] = {
            "user": "4proxy",
            "fruit": "banana",
            "number": 9,
        }

        # Check
        self._tested_class(mock_pool_settings, **test_kwargs)

    # -------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_module,
                           attribute='MySQLConnectionPool', autospec=True)
    def test_create_connection_pool_returns_MySQLConnectionPool(self,
                                                                _) -> None:
        from mysql.connector.pooling import MySQLConnectionPool

        # Build
        mock_pool_settings: MagicMock = self._make_PoolSettingsDTO_mock()
        test_class = self._tested_class
        expected_type = MySQLConnectionPool

        # Operate
        db = test_class(mock_pool_settings)

        test_obj: MySQLConnectionPool = db.create_connection_pool()

        # Check
        self.assertIsInstance(
            obj=test_obj,
            cls=expected_type,
            msg=f"Failure! Inspected object: {test_obj} - is not instance of {expected_type}!"
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
