# -*- coding: utf-8 -*-

"""
Test cases for `SQLDataBase` from the `sql_database.py` file.

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.5.1"

import unittest

from tests.test_helper import *

from abstract.database.sql_database import SQLDataBase as tested_class

from typing import Any, Dict, List


# ______________________________________________________________________________________________________________________
class ConcreteTestClass(tested_class):
    def __str__(self) -> str:
        return "__str__"

    def _get_info_about_server(self) -> str:
        return "_get_info_about_server"


# ______________________________________________________________________________________________________________________
class TestSQLDataBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = tested_class

    # ------------------------------------------------------------------------------------------------------------------
    def test_class_is_abstract_of_ABC(self) -> None:
        AbstractTestHelper.check_inspected_class_is_abstract_of_ABC(_cls=self._tested_class)

    # ------------------------------------------------------------------------------------------------------------------
    def test_str_method_is_abstractmethod(self) -> None:
        AbstractTestHelper.check_inspected_method_is_abstractmethod(_cls=self._tested_class,
                                                                    method_name='__str__')

    # ------------------------------------------------------------------------------------------------------------------
    def test_get_info_methods_is_abstractmethods(self) -> None:
        # Build
        _class = self._tested_class

        method_names: List[str] = [
            '_get_info_about_server',
        ]

        # Check
        for method_name in method_names:
            with self.subTest(msg=f"Inspected method: *{method_name}* of *{_class}* - is not abstractmethod!"):
                AbstractTestHelper.check_inspected_method_is_abstractmethod(_cls=_class,
                                                                            method_name=method_name)

    # ------------------------------------------------------------------------------------------------------------------
    def test_constructor_initializes_private_field_dbconfig(self) -> None:
        # Build
        _class = ConcreteTestClass

        expected_dbconfig: Dict[str, str] = {
            "host": "localhost",
            "user": "root",
            "password": "password",
        }

        # Operate
        instance = _class(**expected_dbconfig)

        # Check
        actual_dbconfig: Dict[str, Any] = instance.dbconfig

        self.assertDictEqual(d1=expected_dbconfig, d2=actual_dbconfig)
