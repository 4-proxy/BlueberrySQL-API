# -*- coding: utf-8 -*-

"""
Test cases for `MySQLDataBaseSingle` from the `mysql_database_single.py` file.

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.2.0"

import unittest
from unittest import mock as UnitMock

from tests.test_helper import *

from mysql_support.mysql_database_single import MySQLDataBaseSingle as tested_class

from abstract.database.sql_database import SQLDataBase
from abstract.database.connection_interface import SingleConnectionInterface
from abstract.api.sql_api_interface import SQLAPIInterface

from typing import Dict, Any


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

    # ------------------------------------------------------------------------------------------------------------------
    def _create_instance_of_tested_class(self) -> tested_class:
        _class = self._tested_class
        dbconfig: Dict[str, Any] = self._dbconfig

        instance = _class(**dbconfig)

        return instance

    # ------------------------------------------------------------------------------------------------------------------
    def test_is_subclass_of_SQLDataBase(self) -> None:
        TestHelper.check_inspected_class_is_subclass_of_expected_base_class(
            _class=self._tested_class, expected_base_class=SQLDataBase
        )

    # ------------------------------------------------------------------------------------------------------------------
    def test_overridden_abstractmethods_of_SQLDataBase(self) -> None:
        AbstractTestHelper.check_inspected_class_overridden_abstractmethods_of_expected_class(
            _class=self._tested_class, expected_class=SQLDataBase
        )

    # ------------------------------------------------------------------------------------------------------------------
    def test_implements_SingleConnectionInterface(self) -> None:
        AbstractTestHelper.check_inspected_class_implements_expected_interface(
            _class=self._tested_class, expected_interface=SingleConnectionInterface
        )

    # ------------------------------------------------------------------------------------------------------------------
    def test_implements_SQLAPIInterface(self) -> None:
        AbstractTestHelper.check_inspected_class_implements_expected_interface(
            _class=self._tested_class, expected_interface=SQLAPIInterface
        )

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=SQLDataBase, attribute='__init__')
    def test_calls_SQLDataBase_constructor_on_initialization_with_dbconfig_kwargs(self,
                                                                                  mock__init__: UnitMock.MagicMock) -> None:
        # Build
        dbconfig: Dict[str, Any] = self._dbconfig

        # Operate
        instance: tested_class = self._create_instance_of_tested_class()

        # Check
        # Note the direct transmission of the `self` parameter
        mock__init__.assert_called_once_with(self=instance, **dbconfig)
