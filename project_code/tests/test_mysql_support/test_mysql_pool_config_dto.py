# -*- coding: utf-8 -*-

"""
Test cases for `MySQLPoolConfigDTO` from the `mysql_pool_config_dto.py` file.

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.2.2"

import unittest

from mysql.connector.pooling import CNX_POOL_MAXSIZE, CNX_POOL_MAXNAMESIZE

from tests.test_helper import *

from mysql_support.mysql_pool_config_dto import MySQLPoolConfigDTO as tested_class
from abstract.config.pool_config_dto import PoolConfigDTO

from typing import Any, Dict, Tuple


# ______________________________________________________________________________________________________________________
class PositiveTestMySQLPoolConfigDTO(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = tested_class

    # ------------------------------------------------------------------------------------------------------------------
    def test_class_is_subclass_of_PoolConfigDTO(self) -> None:
        TestHelper.check_inspected_class_is_subclass_of_expected_base_class(
            _cls=self._tested_class, expected_base_class=PoolConfigDTO
        )

    # ------------------------------------------------------------------------------------------------------------------
    def test_class_implements_expected_abstractmethod(self) -> None:
        # Build
        _class = self._tested_class
        expected_abstractmethod = 'validate_fields_data'

        # Check
        with self.assertRaises(expected_exception=AssertionError,
                               msg=f"Failure! The expected abstractmethod: *{expected_abstractmethod}* - is not implements!"):
            # Operate
            AbstractTestHelper.check_inspected_method_is_abstractmethod(
                _cls=_class, method_name=expected_abstractmethod
            )


# ______________________________________________________________________________________________________________________
class NegativeTestMySQLPoolConfigDTO(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = tested_class

        cls._valid_pool_params: Dict[str, Any] = {
            'name': "TestPool",
            'size': 5,
            'reset_session': True,
        }

    # ------------------------------------------------------------------------------------------------------------------
    def _check_invalid_field_value_raise_expected_exception(self,
                                                            field_name: str,
                                                            invalid_value: Any,
                                                            expected_exception: type) -> None:
        # Build
        _class = self._tested_class
        pool_params: Dict[str, Any] = self._valid_pool_params.copy()

        # Change valid field value to invalid for test case
        pool_params[field_name] = invalid_value

        # Check
        with self.assertRaises(expected_exception=expected_exception,
                               msg=f"Failure! The invalid value of field: *{field_name}* - not raise *{expected_exception}*!"):
            # Operate
            _class(**pool_params)

    # ------------------------------------------------------------------------------------------------------------------
    def test_invalid_type_of_name_field_raise_TypeError(self) -> None:
        self._check_invalid_field_value_raise_expected_exception(
            field_name='name', invalid_value=1234, expected_exception=TypeError
        )

    # ------------------------------------------------------------------------------------------------------------------
    def test_invalid_type_of_size_field_raise_TypeError(self) -> None:
        self._check_invalid_field_value_raise_expected_exception(
            field_name='size', invalid_value="5", expected_exception=TypeError
        )

    # ------------------------------------------------------------------------------------------------------------------
    def test_invalid_type_of_reset_session_field_raise_TypeError(self) -> None:
        self._check_invalid_field_value_raise_expected_exception(
            field_name='reset_session', invalid_value="True", expected_exception=TypeError
        )

    # ------------------------------------------------------------------------------------------------------------------
    def test_invalid_value_of_name_field_raise_ValueError(self) -> None:
        # Build
        invalid_values: Tuple[str, ...] = "", " ", "      "

        # Check
        for invalid_value in invalid_values:
            with self.subTest(pattern=invalid_value):
                self._check_invalid_field_value_raise_expected_exception(
                    field_name='name', invalid_value=invalid_value, expected_exception=ValueError
                )

    # ------------------------------------------------------------------------------------------------------------------
    def test_invalid_value_of_size_field_raise_ValueError(self) -> None:
        # Build
        invalid_values: Tuple[int, ...] = 0, -1, -10

        # Check
        for invalid_value in invalid_values:
            with self.subTest(pattern=invalid_value):
                self._check_invalid_field_value_raise_expected_exception(
                    field_name='size', invalid_value=invalid_value, expected_exception=ValueError
                )

    # ------------------------------------------------------------------------------------------------------------------
    def test_mysql_pool_size_max_limit(self) -> None:
        from random import randint

        # Build
        limit_of_size = CNX_POOL_MAXSIZE

        invalid_values: Tuple[int, ...] = tuple(
            randint(a=limit_of_size + 1, b=limit_of_size + 10) for i in range(5)
        )

        # Check
        for invalid_value in invalid_values:
            with self.subTest(pattern=invalid_value):
                self._check_invalid_field_value_raise_expected_exception(
                    field_name='size', invalid_value=invalid_value, expected_exception=ValueError
                )

    # ------------------------------------------------------------------------------------------------------------------
    def test_mysql_pool_name_max_size_limit(self) -> None:
        from random import randint
        from string import ascii_lowercase

        # Build
        limit_of_size = CNX_POOL_MAXNAMESIZE

        invalid_values = tuple(
            (char * (limit_of_size + randint(1, 30))) for char in ascii_lowercase
        )

        # Check
        for invalid_value in invalid_values:
            with self.subTest(pattern=invalid_value):
                self._check_invalid_field_value_raise_expected_exception(
                    field_name='name', invalid_value=invalid_value, expected_exception=ValueError
                )
