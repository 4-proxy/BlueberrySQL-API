# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.4.0"


import unittest
import unittest.mock as UnitMock

from unittest.mock import MagicMock

import mysql_database as tested_module

from mysql_database import MySQLDataBase
from settings_dto import PoolConfigDTO

from typing import Any, Dict, Tuple, NewType


valid_params_PoolConfigDTO: Dict[str, Any] = {
    "pool_name": "TestPool",
    "pool_size": 5,
    "pool_reset_session": True
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MockPoolConfigDTO = NewType('MockPoolConfigDTO', MagicMock)


# _____________________________________________________________________________
class TestMySQLDataBasePositive(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = MySQLDataBase

    def setUp(self) -> None:
        super().setUp()
        self.mock_pool_config: MockPoolConfigDTO = self._create_mock_PoolConfigDTO()

    # -------------------------------------------------------------------------
    def _create_mock_PoolConfigDTO(self) -> MockPoolConfigDTO:
        mock = MagicMock(spec=PoolConfigDTO)

        mock.pool_name = valid_params_PoolConfigDTO["pool_name"]
        mock.pool_size = valid_params_PoolConfigDTO["pool_size"]
        mock.pool_reset_session = valid_params_PoolConfigDTO["pool_reset_session"]

        return mock

    # -------------------------------------------------------------------------
    def test_constructor_accepts_PoolConfigDTO(self) -> None:
        self._tested_class(self.mock_pool_config)

    # -------------------------------------------------------------------------
    def test_pool_config_field_is_instance_of_PoolConfigDTO(self) -> None:
        # Build
        expected_field_name = '_pool_config'
        expected_type = PoolConfigDTO
        test_class = self._tested_class

        # Operate
        test_instance = test_class(self.mock_pool_config)

        expected_field = getattr(test_instance, expected_field_name)

        # Check
        self.assertIsInstance(
            obj=expected_field,
            cls=expected_type,
            msg=f"Failure! Inspected field: {expected_field} is not instance of {expected_type}!"
        )

    # -------------------------------------------------------------------------
    def test_constructor_accepts_additional_kwargs(self) -> None:
        # Build
        test_kwargs: Dict[str, Any] = {
            "user": "4proxy",
            "fruit": "banana",
            "number": 9,
        }

        # Check
        self._tested_class(self.mock_pool_config, **test_kwargs)

    # -------------------------------------------------------------------------
    def test_additional_kwargs_stored_in_dbconfig_field(self) -> None:
        # Build
        expected_field_name = '_dbconfig'
        test_class = self._tested_class

        test_data: Dict[str, Any] = {
            "user": "4proxy",
            "database": "banana_base",
            "password": 1234,
        }

        # Operate
        test_instance = test_class(self.mock_pool_config, **test_data)

        expected_field_data = getattr(test_instance, expected_field_name)

        # Check
        self.assertDictEqual(
            d1=expected_field_data,
            d2=test_data,
            msg=f"Failure! The data of expected field: {expected_field_name} - do not match the test data!"
        )

    # -------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_module,
                           attribute='MySQLConnectionPool', autospec=True)
    def test_create_pool_returns_MySQLConnectionPool(self, _) -> None:
        from mysql.connector.pooling import MySQLConnectionPool

        # Build
        expected_type = MySQLConnectionPool
        test_class = self._tested_class

        # Operate
        test_instance = test_class(self.mock_pool_config)

        test_obj: MySQLConnectionPool = test_instance.create_pool()

        # Check
        self.assertIsInstance(
            obj=test_obj,
            cls=expected_type,
            msg=f"Failure! Inspected object: {test_obj} - is not instance of {expected_type}!"
        )

    # -------------------------------------------------------------------------
    def test_create_pool_returns_configured_MySQLConnectionPool_with_pool_config(
            self) -> None:
        from mysql.connector.pooling import MySQLConnectionPool

        # Build
        test_class = self._tested_class
        test_pool_config: MockPoolConfigDTO = self.mock_pool_config

        test_pool_params: Dict[str, Any] = {
            "pool_name": "TestPool",
            "pool_size": 3,
            "pool_reset_session": False,
        }

        # SetUp mock fields of PoolConfigDTO
        for attr, value in test_pool_params.items():
            setattr(test_pool_config, attr, value)

        # MySQLConnectionPool attribute names
        expected_attrs: Tuple[str, ...] = ("pool_name",
                                           "pool_size",
                                           "reset_session",
                                           )

        # Operate
        test_instance = test_class(test_pool_config)

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

    # -------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_module,
                           attribute='MySQLConnectionPool')
    def test_create_pool_returns_configured_MySQLConnectionPool_with_dbconfig(self,
                                                                              MockMySQLConnectionPool: MagicMock) -> None:
        from mysql.connector.pooling import MySQLConnectionPool

        # Build
        test_class = self._tested_class

        test_dbconfig: Dict[str, Any] = {
            "database": "TestDB",
            "user": "proxy4",
            "password": "1234qwerty",
        }

        # Operate
        test_instance = test_class(self.mock_pool_config, **test_dbconfig)

        test_obj: MySQLConnectionPool = test_instance.create_pool()

        call_args: Dict[str, Any] = MockMySQLConnectionPool.call_args[1]

        # Check
        call_arg_pairs = call_args.items()
        for expected_pair in test_dbconfig.items():
            self.assertIn(
                member=expected_pair,
                container=call_arg_pairs,
                msg=f"Failure! Expected kwarg: {expected_pair} - not found in call arguments!"
            )


# _____________________________________________________________________________
class TestMySQLDataBaseNegative(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = MySQLDataBase

    # -------------------------------------------------------------------------
    def test_constructor_raise_IsNotPoolSettingDTO(self) -> None:
        from database_types.exceptions import IsNotPoolConfigDTO

        # Build
        # Valid data, but not an instance of PoolConfigDTO
        test_obj: Dict[str, Any] = valid_params_PoolConfigDTO

        # Check
        with self.assertRaises(expected_exception=IsNotPoolConfigDTO):
            self._tested_class(test_obj)  # type: ignore
