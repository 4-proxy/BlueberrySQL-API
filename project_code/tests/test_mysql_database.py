# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.7.0"


import unittest
import unittest.mock as UnitMock

import mysql_database as tested_module

from mysql_database import MySQLDataBase as tested_class
from settings_dto import PoolConfigDTO
from tests.test_data.db_connection_config import connection_config as DB_CONNECTION_CONFIG

from typing import Any, Dict, Tuple, TypeAlias
from unittest.mock import MagicMock
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from _collections_abc import dict_items

# Logical flags for tests
TEST_FLAG_MYSQL_SERVER_IS_ON = True

# Custom types
MockPoolConfigDTO: TypeAlias = MagicMock

# Auxiliary data
valid_params_PoolConfigDTO: Dict[str, Any] = {
    "pool_name": "Test-Pool",
    "pool_size": 5,
    "pool_reset_session": True,
}


# ______________________________________________________________________________________________________________________
class TestMySQLDataBasePositive(unittest.TestCase):
    @staticmethod
    def create_mock_PoolConfigDTO() -> MockPoolConfigDTO:
        mock = MagicMock(spec=PoolConfigDTO)

        mock.pool_name = valid_params_PoolConfigDTO["pool_name"]
        mock.pool_size = valid_params_PoolConfigDTO["pool_size"]
        mock.pool_reset_session = valid_params_PoolConfigDTO["pool_reset_session"]

        return mock

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = tested_class

    # ------------------------------------------------------------------------------------------------------------------
    def setUp(self) -> None:
        super().setUp()
        self.mock_pool_config: MockPoolConfigDTO = self.create_mock_PoolConfigDTO()

    # ------------------------------------------------------------------------------------------------------------------
    def test_constructor_accepts_PoolConfigDTO(self) -> None:
        self._tested_class(self.mock_pool_config)

    # ------------------------------------------------------------------------------------------------------------------
    def test_pool_config_field_is_instance_of_PoolConfigDTO(self) -> None:
        # Build
        expected_field_name = '_pool_config'
        expected_type = PoolConfigDTO
        test_class = self._tested_class

        # Operate
        test_instance = test_class(self.mock_pool_config)

        # Check
        present_field_data: PoolConfigDTO = getattr(test_instance, expected_field_name)

        self.assertIsInstance(
            obj=present_field_data,
            cls=expected_type,
            msg=f"Failure! Inspected field: {present_field_data} - is not instance of {expected_type}!"
        )

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_class,
                           attribute='create_connection_pool', autospec=True)
    def test_constructor_stores_additional_kwargs_in_dbconfig_field(self, _) -> None:
        # Build
        expected_field_name = '_dbconfig'
        test_class = self._tested_class

        test_data: Dict[str, Any] = {
            "user": "4proxy",
            "database": "banana_base",
            "password": 1234,
        }

        # Operate
        test_instance = test_class(self.mock_pool_config,
                                   **test_data)

        # Check
        present_field_data: Dict[str, Any] = getattr(test_instance, expected_field_name)

        self.assertDictEqual(
            d1=present_field_data,
            d2=test_data,
            msg=f"Failure! The data of expected field: {expected_field_name} - do not match the test data!"
        )

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_module,
                           attribute='MySQLConnectionPool', autospec=True)
    def test_create_connection_pool_returns_MySQLConnectionPool(self, _) -> None:
        # Build
        expected_type = MySQLConnectionPool
        test_class = self._tested_class

        # Operate
        test_instance = test_class(self.mock_pool_config)

        test_obj: MySQLConnectionPool = test_instance.create_connection_pool()

        # Check
        self.assertIsInstance(
            obj=test_obj,
            cls=expected_type,
            msg=f"Failure! Inspected object: {test_obj} - is not instance of {expected_type}!"
        )

    # ------------------------------------------------------------------------------------------------------------------
    def test_create_connection_pool_returns_configured_MySQLConnectionPool_with_pool_config(self) -> None:
        # Build
        test_pool_config: MockPoolConfigDTO = self.mock_pool_config
        test_class = self._tested_class

        # MySQLConnectionPool attribute names
        expected_attrs: Tuple[str, ...] = (
            "pool_name",
            "pool_size",
            "reset_session",
        )

        # The parameter values must be different from the default values of
        # MySQLConnectionPool.__init__
        test_pool_params: Dict[str, Any] = {
            "pool_name": "TestPoolWithConfig",
            "pool_size": 3,
            "pool_reset_session": False,
        }

        # SetUp mock fields of PoolConfigDTO
        for attr, value in test_pool_params.items():
            setattr(test_pool_config, attr, value)

        # Operate
        test_instance = test_class(test_pool_config)

        test_obj: MySQLConnectionPool = test_instance.create_connection_pool()

        # Check
        for expected_attr, expected_value in zip(expected_attrs, test_pool_params.values()):
            with self.subTest(pattern=(expected_attr, expected_value)):
                # Build
                present_value: Any = getattr(test_obj, expected_attr)

                # Check
                self.assertEqual(
                    first=present_value,
                    second=expected_value,
                    msg=f"Failure! Inspected attr: {expected_attr} - has an invalid value!"
                )

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_module,
                           attribute='MySQLConnectionPool', autospec=True)
    def test_create_connection_pool_returns_configured_MySQLConnectionPool_with_dbconfig(self,
                                                                                         MockMySQLConnectionPool: MagicMock) -> None:
        # Build
        test_class = self._tested_class

        test_dbconfig: Dict[str, Any] = {
            "database": "TestDB",
            "user": "proxy4",
            "password": "1234qwerty",
        }

        # Operate
        test_instance = test_class(self.mock_pool_config,
                                   **test_dbconfig)

        test_instance.create_connection_pool()

        call_args: Dict[str, Any] = MockMySQLConnectionPool.call_args[1]

        call_arg_pairs: dict_items[str, Any] = call_args.items()

        # Check
        for expected_pair in test_dbconfig.items():
            self.assertIn(
                member=expected_pair,
                container=call_arg_pairs,
                msg=f"Failure! Expected kwarg: {expected_pair} - not found in call arguments!"
            )

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_class,
                           attribute='create_connection_pool', autospec=True)
    @UnitMock.patch.object(target=tested_module,
                           attribute='MySQLConnectionPool', autospec=True)
    def test_constructor_initializes_pool_field_used_create_connection_pool(self,
                                                                            MockMySQLConnectionPool: MagicMock,
                                                                            mock_create_connection_pool: MagicMock) -> None:
        # Build
        expected_field_name = '_pool'
        expected_field_data_type = MySQLConnectionPool
        test_class = self._tested_class

        mock_create_connection_pool.return_value = MockMySQLConnectionPool

        # Operate
        test_instance = test_class(self.mock_pool_config)

        present_field_data: MySQLConnectionPool = getattr(test_instance, expected_field_name)

        # Check
        mock_create_connection_pool.assert_called_once()

        self.assertIsInstance(
            obj=present_field_data,
            cls=expected_field_data_type,
            msg=f"Failure! Inspected field: {expected_field_name} - data type does not match with {expected_field_data_type}!"
        )

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_module.MySQLConnectionPool,
                           attribute='get_connection', autospec=True)
    @UnitMock.patch.object(target=tested_module,
                           attribute='PooledMySQLConnection', autospec=True)
    def test_get_connection_from_pool_returns_PooledMySQLConnection(self,
                                                                    MockPooledMySQLConnection: MagicMock,
                                                                    mock_get_connection: MagicMock) -> None:
        # Build
        expected_type = PooledMySQLConnection
        test_class = self._tested_class

        mock_get_connection.return_value = MockPooledMySQLConnection

        # Operate
        test_instance = test_class(self.mock_pool_config)

        test_obj: PooledMySQLConnection = test_instance.get_connection_from_pool()

        # Check
        self.assertIsInstance(
            obj=test_obj,
            cls=expected_type,
            msg=f"Failure! Inspected object: {test_obj} - is not instance of {expected_type}!"
        )

    # ------------------------------------------------------------------------------------------------------------------
    @unittest.skipUnless(condition=TEST_FLAG_MYSQL_SERVER_IS_ON, reason="MySQL server is off.")
    def test_get_connection_from_pool_returns_valid_connection_to_database(self) -> None:
        # Build
        test_class = self._tested_class

        # Operate
        test_instance = test_class(self.mock_pool_config,
                                   **DB_CONNECTION_CONFIG)

        test_obj: PooledMySQLConnection = test_instance.get_connection_from_pool()

        # Check
        self.assertTrue(expr=test_obj.is_connected(),
                        msg=f"Failure! The inspected connection: {test_obj} - is not connected!")

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_module,
                           attribute='MySQLConnectionPool', autospec=True)
    @UnitMock.patch.object(target=tested_module.MySQLDataBase,
                           attribute='create_connection_pool', autospec=True)
    def test_change_dbconfig_for_connection_pool_uses_MySQLConnectionPool_set_config(self,
                                                                                     mock_create_connection_pool: MagicMock,
                                                                                     MockMySQLConnectionPool: MagicMock) -> None:
        # Build
        test_class = self._tested_class

        mock_create_connection_pool.return_value = MockMySQLConnectionPool

        test_dbconfig: Dict[str, Any] = {
            "database": "PickleDB",
            "user": "Rick",
            "password": "MortyWheareYou",
        }

        # Operate
        test_instance = test_class(self.mock_pool_config)

        test_instance.change_dbconfig_for_connection_pool(new_dbconfig=test_dbconfig)

        # Check
        MockMySQLConnectionPool.set_config.assert_called_once_with(**test_dbconfig)


# ______________________________________________________________________________________________________________________
class TestMySQLDataBaseNegative(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = tested_class

    # ------------------------------------------------------------------------------------------------------------------
    def test_set_pool_config_raises_AttributeError_when_not_PoolConfigDTO(self) -> None:
        # Build
        expected_exception = AttributeError
        expected_exception_msg: str = (
            "pool_config must be an instance of `PoolConfigDTO`! "
            f"Obtained instance: <class 'dict'>"
        )
        test_class = self._tested_class

        test_data: Dict[str, Any] = valid_params_PoolConfigDTO

        # Check
        with self.assertRaises(expected_exception=expected_exception) as ctx:
            # Operate
            test_class(test_data)  # type: ignore

        # Check
        present_exception_msg = str(ctx.exception)

        self.assertEqual(
            first=present_exception_msg,
            second=expected_exception_msg,
            msg="Failure! The exception message is not as expected!"
        )
