# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.7.1"


import unittest
import unittest.mock as UnitMock

import mysql_database as tested_module
from mysql_database import MySQLDataBase as tested_class

from settings_dto import PoolConfigDTO
from tests.test_data.db_connection_config import connection_config as DB_CONNECTION_CONFIG

from unittest.mock import MagicMock
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from _collections_abc import dict_items, dict_values
from typing import Any, Dict, Tuple, TypeAlias

# Logical flags for tests
TEST_FLAG_MYSQL_SERVER_IS_ON = False

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
        _class = self._tested_class

        # Operate
        instance = _class(self.mock_pool_config)

        # Check
        instance_field: PoolConfigDTO = getattr(instance, expected_field_name)

        self.assertIsInstance(
            obj=instance_field,
            cls=expected_type,
            msg=(f"Failure! Inspected field: {expected_field_name} - is not instance of {expected_type}! "
                 f"It's: {type(instance_field)}")
        )

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_class,
                           attribute='create_connection_pool', autospec=True)
    def test_constructor_stores_additional_kwargs_in_dbconfig_field(self, _) -> None:
        # Build
        expected_field_name = '_dbconfig'
        _class = self._tested_class

        additional_kwargs: Dict[str, Any] = {
            "user": "4proxy",
            "database": "banana_base",
            "password": 1234,
        }

        # Operate
        instance = _class(self.mock_pool_config, **additional_kwargs)

        # Check
        instance_field: Dict[str, Any] = getattr(instance, expected_field_name)

        self.assertDictEqual(
            d1=instance_field,
            d2=additional_kwargs,
            msg=f"Failure! The data of expected field: {expected_field_name} - do not match the test data!"
        )

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_module,
                           attribute='MySQLConnectionPool', autospec=True)
    def test_create_connection_pool_returns_MySQLConnectionPool(self, _) -> None:
        # Build
        expected_type = MySQLConnectionPool
        _class = self._tested_class

        # Operate
        instance = _class(self.mock_pool_config)

        returned_obj: MySQLConnectionPool = instance.create_connection_pool()

        # Check
        self.assertIsInstance(
            obj=returned_obj,
            cls=expected_type,
            msg=f"Failure! Inspected object: {returned_obj} - is not instance of {expected_type}!"
        )

    # ------------------------------------------------------------------------------------------------------------------
    def test_create_connection_pool_returns_configured_MySQLConnectionPool_using_pool_config(self) -> None:
        # Build
        pool_config: MockPoolConfigDTO = self.mock_pool_config
        _class = self._tested_class

        # MySQLConnectionPool attribute names
        expected_attrs: Tuple[str, ...] = (
            "pool_name",
            "pool_size",
            "reset_session",
        )

        # The parameter values must be different from the default values of
        # MySQLConnectionPool.__init__
        pool_params: Dict[str, Any] = {
            "pool_name": "TestPoolWithConfig",
            "pool_size": 3,
            "pool_reset_session": False,
        }

        # SetUp mock fields of PoolConfigDTO
        for attr, value in pool_params.items():
            setattr(pool_config, attr, value)

        # Operate
        instance = _class(pool_config)

        returned_configured_obj: MySQLConnectionPool = instance.create_connection_pool()

        # Check
        expected_values: dict_values[str, Any] = pool_params.values()

        for expected_attr, expected_value in zip(expected_attrs, expected_values):
            with self.subTest(pattern=(expected_attr, expected_value)):
                # Build
                attr_value: Any = getattr(returned_configured_obj, expected_attr)

                # Check
                self.assertEqual(
                    first=attr_value,
                    second=expected_value,
                    msg=(f"Failure! Inspected attr: {expected_attr} - has an invalid value! "
                         f"It's: {attr_value}, when expected - {expected_value}")
                )

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_module,
                           attribute='MySQLConnectionPool', autospec=True)
    def test_create_connection_pool_returns_configured_MySQLConnectionPool_using_dbconfig(self,
                                                                                          MockMySQLConnectionPool: MagicMock) -> None:
        # Build
        _class = self._tested_class

        dbconfig: Dict[str, Any] = {
            "database": "TestDB",
            "user": "proxy4",
            "password": "1234qwerty",
        }

        # Operate
        instance = _class(self.mock_pool_config, **dbconfig)

        instance.create_connection_pool()

        call_args: Dict[str, Any] = MockMySQLConnectionPool.call_args[1]

        call_arg_pairs: dict_items[str, Any] = call_args.items()

        # Check
        for expected_pair in dbconfig.items():
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
    def test_constructor_initializes_pool_field_using_create_connection_pool(self,
                                                                             MockMySQLConnectionPool: MagicMock,
                                                                             mock_create_connection_pool: MagicMock) -> None:
        # Build
        expected_field_name = '_pool'
        expected_field_type = MySQLConnectionPool
        _class = self._tested_class

        mock_create_connection_pool.return_value = MockMySQLConnectionPool

        # Operate
        instance = _class(self.mock_pool_config)

        instance_field: MySQLConnectionPool = getattr(instance, expected_field_name)

        # Check
        mock_create_connection_pool.assert_called_once()

        self.assertIsInstance(
            obj=instance_field,
            cls=expected_field_type,
            msg=(f"Failure! Inspected field: {expected_field_name} - is not instance of {expected_field_type}! "
                 f"It's: {type(instance_field)}")
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
        _class = self._tested_class

        mock_get_connection.return_value = MockPooledMySQLConnection

        # Operate
        instance = _class(self.mock_pool_config)

        returned_obj: PooledMySQLConnection = instance.get_connection_from_pool()

        # Check
        self.assertIsInstance(
            obj=returned_obj,
            cls=expected_type,
            msg=(f"Failure! Inspected object: {returned_obj} - is not instance of {expected_type}! "
                 f"It's: {type(returned_obj)}")
        )

    # ------------------------------------------------------------------------------------------------------------------
    @unittest.skipUnless(condition=TEST_FLAG_MYSQL_SERVER_IS_ON, reason="MySQL server is off.")
    def test_get_connection_from_pool_returns_valid_connection_to_database(self) -> None:
        # Build
        _class = self._tested_class

        # Operate
        instance = _class(self.mock_pool_config, **DB_CONNECTION_CONFIG)

        returned_obj: PooledMySQLConnection = instance.get_connection_from_pool()

        # Check
        self.assertTrue(expr=returned_obj.is_connected(),
                        msg=f"Failure! The inspected connection: {returned_obj} - is not connected!")

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_module,
                           attribute='MySQLConnectionPool', autospec=True)
    @UnitMock.patch.object(target=tested_module.MySQLDataBase,
                           attribute='create_connection_pool', autospec=True)
    def test_change_dbconfig_for_connection_pool_using_MySQLConnectionPool_set_config(self,
                                                                                      mock_create_connection_pool: MagicMock,
                                                                                      MockMySQLConnectionPool: MagicMock) -> None:
        # Build
        _class = self._tested_class

        mock_create_connection_pool.return_value = MockMySQLConnectionPool

        dbconfig: Dict[str, Any] = {
            "database": "PickleDB",
            "user": "Rick",
            "password": "MortyWhereYou",
        }

        # Operate
        instance = _class(self.mock_pool_config)

        instance.change_dbconfig_for_connection_pool(new_dbconfig=dbconfig)

        # Check
        MockMySQLConnectionPool.set_config.assert_called_once_with(**dbconfig)


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
        expected_exception_msg: str = ("pool_config must be an instance of `PoolConfigDTO`! "
                                       "Obtained instance: <class 'dict'>")
        _class = self._tested_class

        pool_config_params: Dict[str, Any] = valid_params_PoolConfigDTO

        # Check
        with self.assertRaises(expected_exception=expected_exception) as ctx:
            # Operate
            _class(pool_config_params)  # type: ignore

        # Check
        exception_msg = str(ctx.exception)

        self.assertEqual(
            first=exception_msg,
            second=expected_exception_msg,
            msg="Failure! The exception message is not as expected!"
        )
