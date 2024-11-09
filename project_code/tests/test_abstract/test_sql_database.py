# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.2.0"

import unittest

from abstract.database.sql_database import SQLDataBase as tested_class

from typing import Any, Callable, Dict, List


# ______________________________________________________________________________________________________________________
class ConcreteTestClass(tested_class):
    def __repr__(self) -> str:
        return "__repr__"

    def _get_info_about_connection(self) -> str:
        return "_get_info_about_connection"

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
        """
        Python allows you to create an instance of an abstract class if it has no methods.
        Hence the check via inheritance.
        """
        from abc import ABC

        # Build
        _class = self._tested_class

        # Check
        self.assertTrue(expr=issubclass(_class, ABC),
                        msg=f"Failure! Inspected class: {_class} - is not abstract of {ABC}!")

    # ------------------------------------------------------------------------------------------------------------------
    def test_repr_method_is_abstractmethod(self) -> None:
        # Build
        _class = self._tested_class

        # Operate
        method: Callable[..., Any] = getattr(_class, '__repr__')

        # Check
        self.assertTrue(expr=method.__isabstractmethod__,  # type: ignore
                        msg=f"Failure! __repr__ method is not abstractmethod!")

    # ------------------------------------------------------------------------------------------------------------------
    def test_get_info_methods_is_abstractmethods(self) -> None:
        # Build
        _class = self._tested_class

        method_names: List[str] = [
            '_get_info_about_server',
            '_get_info_about_connection',
        ]

        # Check
        for method_name in method_names:
            with self.subTest(msg=f"Inspected method: {method_name} - is not abstractmethod!"):
                # Build
                method: Callable[..., Any] = getattr(_class, method_name)

                # Check
                self.assertTrue(expr=method.__isabstractmethod__)  # type: ignore

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

        self.assertDictEqual(d1=expected_dbconfig,
                             d2=actual_dbconfig)
