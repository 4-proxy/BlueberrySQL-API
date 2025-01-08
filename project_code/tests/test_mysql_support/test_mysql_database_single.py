# -*- coding: utf-8 -*-

"""
Test cases for `MySQLDataBaseSingle` from the `mysql_database_single.py` file.

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.4.0"

import unittest
from unittest import mock as UnitMock

from tests.test_helper import *

from mysql_support import mysql_database_single as tested_module
from mysql_support.mysql_database_single import MySQLDataBaseSingle as tested_class

from abstract.database.sql_database import SQLDataBase
from abstract.database.connection_interface import SingleConnectionInterface
from abstract.api.sql_api_interface import SQLAPIInterface

from typing import Dict, Any, Tuple


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
            'port': 1234
        }
        cls._expected_fields: Tuple[str, ...] = (
            '_' + tested_class.__name__ + '__connection_with_database',
            'dbconfig',
        )

    # ------------------------------------------------------------------------------------------------------------------
    def _create_instance_of_tested_class(self) -> tested_class:
        _class = self._tested_class
        dbconfig: Dict[str, Any] = self._dbconfig

        instance = _class(**dbconfig)

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
    @UnitMock.patch.object(target=SQLDataBase, attribute='__init__',
                           autospec=True)
    def test_constructor_calls_SQLDataBase_init_with_kwargs_dbconfig(self,
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
    @UnitMock.patch.object(target=tested_module, attribute='MySQLConnection',
                           autospec=True)
    def test_method_create_new_connection_with_database_sets_MySQLConnection_to_field_connection_with_database(self,
                                                                                                               MockMySQLConnection: UnitMock.MagicMock) -> None:
        # Build
        _class = self._tested_class
        expected_field: str = '_' + _class.__name__ + '__connection_with_database'
        expected_value = 'OK!'

        MockMySQLConnection.return_value = expected_value

        # Operate
        instance: tested_class = self._create_instance_of_tested_class()

        actual_field_value: str = getattr(instance, expected_field)

        # Check
        self.assertEqual(
            first=actual_field_value,
            second=expected_value,
            msg=(
                f"Failure! Inspected field value: *{expected_field}* - is doesn't match the expected value!\n"
                f"So the value of the field: *{expected_field}* - is not an instance of expected class!"
            )
        )
