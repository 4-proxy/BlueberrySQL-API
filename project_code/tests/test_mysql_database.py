# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.3.0"


import unittest
import unittest.mock as UnitMock

from unittest.mock import MagicMock

import mysql_database as tested_module

from mysql_database import MySQLDataBase
from settings_dto import PoolSettingsDTO

from typing import Any, Dict, Tuple, NewType


valid_params_PoolSettingsDTO: Dict[str, Any] = {
    "pool_name": "TestPool",
    "pool_size": 5,
    "pool_reset_session": True
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MockPoolSettingsDTO = NewType('MockPoolSettingsDTO', MagicMock)


# _____________________________________________________________________________
class TestMySQLDataBasePositive(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = MySQLDataBase

    # -------------------------------------------------------------------------
    def _create_mock_PoolSettingsDTO(self) -> MockPoolSettingsDTO:
        mock = MagicMock(spec=PoolSettingsDTO(**valid_params_PoolSettingsDTO))

        return mock

    # -------------------------------------------------------------------------
    def test_constructor_accepts_PoolSettingsDTO(self) -> None:
        # Build
        mock_pool_settings: MockPoolSettingsDTO = self._create_mock_PoolSettingsDTO()

        # Check
        self._tested_class(mock_pool_settings)

    # -------------------------------------------------------------------------
    def test_pool_settings_field_is_instance_of_PoolSettingsDTO(self) -> None:
        # Build
        mock_pool_settings: MockPoolSettingsDTO = self._create_mock_PoolSettingsDTO()
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
    def test_constructor_accepts_additional_kwargs(self) -> None:
        # Build
        mock_pool_settings: MockPoolSettingsDTO = self._create_mock_PoolSettingsDTO()
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
    def test_create_pool_returns_MySQLConnectionPool(self, _) -> None:
        from mysql.connector.pooling import MySQLConnectionPool

        # Build
        mock_pool_settings: MockPoolSettingsDTO = self._create_mock_PoolSettingsDTO()
        expected_type = MySQLConnectionPool
        test_class = self._tested_class

        # Operate
        test_instance = test_class(mock_pool_settings)

        test_obj: MySQLConnectionPool = test_instance.create_pool()

        # Check
        self.assertIsInstance(
            obj=test_obj,
            cls=expected_type,
            msg=f"Failure! Inspected object: {test_obj} - is not instance of {expected_type}!"
        )

    # -------------------------------------------------------------------------
    def test_create_pool_returns_configured_MySQLConnectionPool(self) -> None:
        from mysql.connector.pooling import MySQLConnectionPool

        # Build
        mock_pool_settings: MockPoolSettingsDTO = self._create_mock_PoolSettingsDTO()
        test_class = self._tested_class

        # Must be different from default values of MySQLConnectionPool.__init__
        test_pool_params: Dict[str, Any] = {
            "pool_name": "TestPool",
            "pool_size": 3,
            "pool_reset_session": False,
        }

        # SetUp mock fields of PoolSettingsDTO
        for attr, value in test_pool_params.items():
            setattr(mock_pool_settings, attr, value)

        # MySQLConnectionPool attribute names
        expected_attrs: Tuple[str, ...] = ("pool_name",
                                           "pool_size",
                                           "reset_session",
                                           )

        # Operate
        test_instance = test_class(mock_pool_settings)

        test_obj: MySQLConnectionPool = test_instance.create_pool()

        # Check
        for expected_attr, expected_value in zip(expected_attrs,
                                                 test_pool_params.values()):
            with self.subTest(pattern=(expected_attr, expected_value)):
                # Build
                present_value: Any = getattr(test_obj, expected_attr)

                # Check
                self.assertEqual(
                    first=present_value,
                    second=expected_value,
                    msg=f"Failure! Inspected attr: {expected_attr} - has an invalid value!"
                )


# _____________________________________________________________________________
class TestMySQLDataBaseNegative(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = MySQLDataBase

    # -------------------------------------------------------------------------
    def test_constructor_raise_IsNotPoolSettingDTO(self) -> None:
        from database_types.exceptions import IsNotPoolSettingsDTO

        # Build
        # Valid data, but not an instance of PoolSettingsDTO
        test_obj: Dict[str, Any] = valid_params_PoolSettingsDTO

        # Check
        with self.assertRaises(expected_exception=IsNotPoolSettingsDTO):
            self._tested_class(test_obj)  # type: ignore
