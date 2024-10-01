# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.3.0"

import unittest

from mysql.connector.pooling import CNX_POOL_MAXSIZE, CNX_POOL_MAXNAMESIZE

from settings_dto import PoolSettingsDTO

from typing import Dict, Any, Tuple


MYSQL_POOL_SIZE_LIMIT: int = CNX_POOL_MAXSIZE
MYSQL_POOL_NAME_SIZE_LIMIT: int = CNX_POOL_MAXNAMESIZE


# _____________________________________________________________________________
class PositiveTestPoolSettingsDTO(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = PoolSettingsDTO

        cls._expected_pool_params: Dict[str, type] = {
            "pool_name": str,
            "pool_size": int,
            "pool_reset_session": bool,
        }

    # -------------------------------------------------------------------------
    def test_class_is_dataclass(self) -> None:
        from dataclasses import is_dataclass

        # Operate
        _is_dataclass: bool = is_dataclass(self._tested_class)

        # Check
        self.assertTrue(expr=_is_dataclass,
                        msg="Failure! The inspected class is not a dataclass!")

    # -------------------------------------------------------------------------
    def test_all_expected_fields_are_present(self) -> None:
        # Build
        expected_names = self._expected_pool_params.keys()
        test_class = self._tested_class

        # Operate
        present_names = test_class.__dataclass_fields__.keys()

        # Check
        for expected_name in expected_names:
            with self.subTest():
                self.assertIn(
                    member=expected_name,
                    container=present_names,
                    msg=f"Failure! Expected field: {expected_name} - is not present!"
                )

    # -------------------------------------------------------------------------
    def test_field_types_match_expected(self) -> None:
        from dataclasses import Field

        # Build
        expected_params = self._expected_pool_params.items()
        test_class = self._tested_class

        # Operate
        present_params: Dict[str, Field[Any]] = test_class.__dataclass_fields__

        # Check
        for expected_field, expected_type in expected_params:
            with self.subTest():
                # Build
                present_field: Field[Any] = present_params[expected_field]
                present_type: Any = present_field.type

                # Check
                self.assertIs(
                    expr1=present_type,
                    expr2=expected_type,
                    msg=f"Failure! Expected type of inspected field is not: {expected_field}!"
                )

    # -------------------------------------------------------------------------
    def test_dataclass_should_be_frozen(self) -> None:
        # Build
        test_class = self._tested_class

        # Operate
        is_frozen: bool = test_class.__dataclass_params__.frozen  # type: ignore

        # Check
        self.assertTrue(expr=is_frozen,
                        msg="Failure! The inspected dataclass is not frozen!")


# _____________________________________________________________________________
class NegativeTestPoolSettingsDTO(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = PoolSettingsDTO

        cls._valid_pool_params: Dict[str, Any] = {
            "pool_name": "TestPool",
            "pool_size": 5,
            "pool_reset_session": True,
        }

    # -------------------------------------------------------------------------
    def _check_invalid_field_value_type_raise_TypeError(self,
                                                        field_name: str,
                                                        invalid_value: Any) -> None:
        # Build
        test_class = self._tested_class
        test_pool_params: Dict[str, Any] = self._valid_pool_params.copy()
        test_pool_params[field_name] = invalid_value

        # Check
        with self.assertRaises(expected_exception=TypeError):
            # Operate
            test_class(**test_pool_params)

    # -------------------------------------------------------------------------
    def _check_invalid_field_value_raise_ValueError(self,
                                                    field_name: str,
                                                    invalid_value: Any) -> None:
        # Build
        test_class = self._tested_class
        test_pool_params: Dict[str, Any] = self._valid_pool_params.copy()
        test_pool_params[field_name] = invalid_value

        # Check
        with self.assertRaises(expected_exception=ValueError):
            # Operate
            test_class(**test_pool_params)

    # -------------------------------------------------------------------------
    def test_invalid_type_of_pool_name_raise_TypeError(self) -> None:
        self._check_invalid_field_value_type_raise_TypeError(field_name="pool_name",
                                                             invalid_value=1234)

    # -------------------------------------------------------------------------
    def test_invalid_type_of_pool_size_raise_TypeError(self) -> None:
        self._check_invalid_field_value_type_raise_TypeError(field_name="pool_size",
                                                             invalid_value="5")

    # -------------------------------------------------------------------------
    def test_invalid_type_of_pool_reset_session_raise_TypeError(self) -> None:
        self._check_invalid_field_value_type_raise_TypeError(field_name="pool_reset_session",
                                                             invalid_value="True")

    # -------------------------------------------------------------------------
    def test_invalid_value_of_pool_name_raise_ValueError(self) -> None:
        # Build
        invalid_values: Tuple[str, ...] = "", " ", "      "

        # Check
        for test_value in invalid_values:
            with self.subTest(pattern=test_value):
                self._check_invalid_field_value_raise_ValueError(field_name="pool_name",
                                                                 invalid_value=test_value)

    # -------------------------------------------------------------------------
    def test_invalid_value_of_pool_size_raise_ValueError(self) -> None:
        # Build
        invalid_values: Tuple[int, ...] = 0, -1, -10

        # Check
        for test_value in invalid_values:
            with self.subTest(pattern=test_value):
                self._check_invalid_field_value_raise_ValueError(field_name="pool_size",
                                                                 invalid_value=test_value)

    # -------------------------------------------------------------------------
    @unittest.skipIf(condition=(MYSQL_POOL_SIZE_LIMIT != 32),
                     reason="MySQL limits")
    def test_mysql_pool_size_max_limit_32(self) -> None:
        # Build
        invalid_values: Tuple[int, ...] = 33, 35, 100

        # Check
        for test_value in invalid_values:
            with self.subTest(pattern=test_value):
                self._check_invalid_field_value_raise_ValueError(field_name="pool_size",
                                                                 invalid_value=test_value)

    # -------------------------------------------------------------------------
    @unittest.skipIf(condition=(MYSQL_POOL_NAME_SIZE_LIMIT != 64),
                     reason="MySQL limits")
    def test_mysql_pool_name_max_size_64(self) -> None:
        # Build
        invalid_values: Tuple[str, ...] = ("a" * 65, "b" * 128, "c" * 256)

        # Check
        for test_value in invalid_values:
            with self.subTest(pattern=test_value):
                self._check_invalid_field_value_raise_ValueError(field_name="pool_name",
                                                                 invalid_value=test_value)
