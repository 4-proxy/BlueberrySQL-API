# -*- coding: utf-8 -*-

"""
Test cases for `MySQLDataBaseSingle` from the `mysql_database_single.py` file.

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.6.0"

import unittest
from unittest import mock as UnitMock

from tests.test_helper import AbstractTestHelper, TestHelper, TestHelperTool

from mysql_support import mysql_database_single as tested_module
from mysql_support.mysql_database_single import MySQLDataBaseSingle as tested_class

from abstract.database.sql_database import SQLDataBase
from abstract.database.connection_interface import SingleConnectionInterface
from abstract.api.sql_api_interface import SQLAPIInterface

from typing import Callable, Dict, Any, Tuple


# ______________________________________________________________________________________________________________________
class TestMySQLDataBaseSingle(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = tested_class

        cls._dbconfig: Dict[str, Any] = {
            'user': '4proxy',
            'database': 'banana_db',
            'password': 'passwordISme',
            'port': 1234,
        }
        cls._expected_fields: Tuple[str, ...] = (
            TestHelperTool.get_full_name_of_class_private_field(_cls=tested_class,
                                                                private_field_name='connection_with_database'),
            'dbconfig',
        )
        cls._execute_query_methods: Tuple[str, ...] = (
            'execute_query_no_returns',
            'execute_query_returns_one',
            'execute_query_returns_all',
        )

    # ------------------------------------------------------------------------------------------------------------------
    def setUp(self) -> None:
        self.mock_MySQLConnection_patch = UnitMock.patch.object(
            target=tested_module, attribute='MySQLConnection', autospec=True
        )
        self.mock_MySQLConnection_class: UnitMock.MagicMock = self.mock_MySQLConnection_patch.start()
        self.mock_MySQLConnection_instance = UnitMock.MagicMock()
        self.mock_MySQLConnection_class.return_value = self.mock_MySQLConnection_instance

    # ------------------------------------------------------------------------------------------------------------------
    def tearDown(self) -> None:
        self.mock_MySQLConnection_patch.stop()

    # ------------------------------------------------------------------------------------------------------------------
    def _create_instance_of_tested_class(self) -> tested_class:
        _cls = self._tested_class
        dbconfig: Dict[str, Any] = self._dbconfig

        instance = _cls(**dbconfig)

        return instance

    # ------------------------------------------------------------------------------------------------------------------
    def test_is_subclass_of_SQLDataBase(self) -> None:
        TestHelper.check_inspected_class_is_subclass_of_expected_base_class(
            _cls=self._tested_class, expected_base_class=SQLDataBase
        )

    # ------------------------------------------------------------------------------------------------------------------
    def test_overridden_abstractmethods_of_SQLDataBase(self) -> None:
        AbstractTestHelper.check_inspected_class_overridden_abstractmethods_of_expected_class(
            _cls=self._tested_class, expected_class=SQLDataBase
        )

    # ------------------------------------------------------------------------------------------------------------------
    def test_implements_SingleConnectionInterface(self) -> None:
        AbstractTestHelper.check_inspected_class_implements_expected_interface(
            _cls=self._tested_class, expected_interface=SingleConnectionInterface
        )

    # ------------------------------------------------------------------------------------------------------------------
    def test_implements_SQLAPIInterface(self) -> None:
        AbstractTestHelper.check_inspected_class_implements_expected_interface(
            _cls=self._tested_class, expected_interface=SQLAPIInterface
        )

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=SQLDataBase, attribute='__init__', autospec=True)
    @UnitMock.patch.object(target=tested_class, attribute='create_new_connection_with_database', autospec=True)
    def test_constructor_calls_SQLDataBase_init_with_kwargs_dbconfig(self, _,
                                                                     mock__init__: UnitMock.MagicMock) -> None:
        # Build
        dbconfig: Dict[str, Any] = self._dbconfig

        # Operate
        instance: tested_class = self._create_instance_of_tested_class()

        # Check
        # Note the direct transmission of the `self` parameter
        mock__init__.assert_called_once_with(self=instance, **dbconfig)

    # ------------------------------------------------------------------------------------------------------------------
    def test_instance_has_expected_fields(self) -> None:
        # Build
        instance: tested_class = self._create_instance_of_tested_class()

        # Check
        TestHelper.check_inspected_object_has_expected_fields(
            _obj=instance, expected_fields=self._expected_fields
        )

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_class, attribute='create_new_connection_with_database',
                           autospec=True)
    def test_constructor_calls_method_create_new_connection_with_database(self,
                                                                          mock_create_new_connection_with_database: UnitMock.MagicMock) -> None:
        # Operate
        instance: tested_class = self._create_instance_of_tested_class()

        # Check
        mock_create_new_connection_with_database.assert_called_once()

    # ------------------------------------------------------------------------------------------------------------------
    def test_method_create_new_connection_with_database_sets_configured_MySQLConnection_to_field_connection_with_database(
            self
    ) -> None:
        # Build
        _cls = self._tested_class
        expected_dbconfig: Dict[str, Any] = self._dbconfig
        expected_field: str = TestHelperTool.get_full_name_of_class_private_field(
            _cls=_cls, private_field_name='connection_with_database'
        )

        mock_MySQLConnection: UnitMock.MagicMock = self.mock_MySQLConnection_class
        mock_expected_connection: UnitMock.MagicMock = self.mock_MySQLConnection_instance

        # Operate
        instance: tested_class = self._create_instance_of_tested_class()

        actual_connection: str = getattr(instance, expected_field)

        # Check
        mock_MySQLConnection.assert_called_once_with(**expected_dbconfig)

        self.assertIs(
            expr1=actual_connection,
            expr2=mock_expected_connection,
            msg=(
                f"Failure! Inspected field value: *{expected_field}* - is doesn't match the expected value!\n"
                f"So the value of the field: *{expected_field}* - is not an expected instance!"
            )
        )

    # ------------------------------------------------------------------------------------------------------------------
    def test_method_get_connection_with_database_returns_valid_MySQLConnection(self) -> None:
        # Build
        mock_expected_connection: UnitMock.MagicMock = self.mock_MySQLConnection_instance

        # Operate
        instance: tested_class = self._create_instance_of_tested_class()

        actual_connection = instance.get_connection_with_database()

        # Check
        self.assertIs(
            expr1=actual_connection,
            expr2=mock_expected_connection,
            msg=(
                f"Failure! The inspected method returned a different value than expected!\n"
                f"The expected value was *{mock_expected_connection}* and the value returned was *{actual_connection}*!"
            )
        )

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_class, attribute='get_connection_with_database', autospec=True)
    def test_method_close_active_connection_with_database_uses_method_close_of_MySQLConnection(self,
                                                                                               mock_get_connection_with_database: UnitMock.MagicMock) -> None:
        # Build
        mock_connection: UnitMock.MagicMock = self.mock_MySQLConnection_instance

        mock_get_connection_with_database.return_value = mock_connection

        # Operate
        instance: tested_class = self._create_instance_of_tested_class()

        instance.close_active_connection_with_database()

        # Check
        mock_get_connection_with_database.assert_called_once()

        mock_connection.close.assert_called_once()

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_class, attribute='get_connection_with_database', autospec=True)
    def test_expected_execute_query_methods_uses_method_get_connection_with_database(self,
                                                                                     mock_get_connection_with_database: UnitMock.MagicMock) -> None:
        # Build
        expected_execute_query_methods: Tuple[str, ...] = self._execute_query_methods
        instance: tested_class = self._create_instance_of_tested_class()

        # Operate
        for execute_query_method_name in expected_execute_query_methods:
            mock_get_connection_with_database.reset_mock()
            with self.subTest(pattern=execute_query_method_name):
                method: Callable = getattr(instance, execute_query_method_name)
                method('sql_query')

                # Check
                mock_get_connection_with_database.assert_called_once()
