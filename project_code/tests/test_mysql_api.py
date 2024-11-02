# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.1.0"

import unittest
import unittest.mock as UnitMock

import mysql_api as tested_module
from mysql_api import MySQLAPI as tested_class

from mysql_database import MySQLDataBase

from unittest.mock import MagicMock
from typing import Any, Callable, TypeAlias, Tuple


# Custom types
MockMySQLDataBase: TypeAlias = MagicMock


# ______________________________________________________________________________________________________________________
class TestMySQLAPIPositive(unittest.TestCase):
    execute_query_methods: Tuple[str, ...] = (
        'execute_query_no_returns',
        'execute_query_returns_one',
        'execute_query_returns_all',
    )

    @staticmethod
    def create_mock_MySQLDataBase() -> MockMySQLDataBase:
        mock = MagicMock(spec=MySQLDataBase)

        return mock

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = tested_class

    # ------------------------------------------------------------------------------------------------------------------
    def setUp(self) -> None:
        super().setUp()
        self.mock_mysql_database: MockMySQLDataBase = self.create_mock_MySQLDataBase()

    # ------------------------------------------------------------------------------------------------------------------
    def test_constructor_accepts_MySQLDataBase(self) -> None:
        self._tested_class(self.mock_mysql_database)

    # ------------------------------------------------------------------------------------------------------------------
    def test_db_field_is_instance_of_MySQLDataBase(self) -> None:
        # Build
        expected_field_name = '_db'
        expected_type = MySQLDataBase
        _class = self._tested_class

        # Operate
        instance = _class(self.mock_mysql_database)

        # Check
        instance_field: MySQLDataBase = getattr(instance, expected_field_name)

        self.assertIsInstance(
            obj=instance_field,
            cls=expected_type,
            msg=(f"Failure! Inspected field: {expected_field_name} - is not instance of {expected_type}! "
                 f"It's: {type(instance_field)}")
        )

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_module,
                           attribute='MySQLAPI', autospec=True)
    def test_has_these_methods(self, _) -> None:
        # Build
        expected_methods: Tuple[str, ...] = self.execute_query_methods
        _class = self._tested_class

        # Check
        for expected_method in expected_methods:
            with self.subTest(msg=f"Inspected class don't have expected method: {expected_method}!"):
                # Operate
                getattr(_class, expected_method)

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=tested_class,
                           attribute='execute_query_no_returns', autospec=True)
    @UnitMock.patch.object(target=tested_class,
                           attribute='execute_query_returns_one', autospec=True)
    @UnitMock.patch.object(target=tested_class,
                           attribute='execute_query_returns_all', autospec=True)
    def test_expected_methods_accepts_sql_string_and_additional_data(self, *_) -> None:
        # Build
        expected_methods: Tuple[str, ...] = self.execute_query_methods
        _class = self._tested_class

        sql_string: str = "IT'S SQL QUERY"
        additional_data: Tuple[str, ...] = ("One", "Two", "Three")

        # Operate
        instance = _class(self.mock_mysql_database)

        # Check
        for expected_method in expected_methods:
            with self.subTest(msg=f"Expected method: {expected_method} - didn't accept the specified arguments!"):
                # Build
                method: Callable[..., Any] = getattr(instance, expected_method)

                # Check
                method(sql_string, *additional_data)
