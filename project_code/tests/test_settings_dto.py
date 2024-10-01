# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.2.0"

import unittest

from settings_dto import PoolSettingsDTO

from typing import Dict, Any, Tuple


# _____________________________________________________________________________
class PositiveTestPoolSettingsDTO(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = PoolSettingsDTO

        cls._expected_pool_parameters: Dict[str, type] = {
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
        expected_field_names = self._expected_pool_parameters.keys()
        test_class = self._tested_class

        # Operate
        present_field_names: Dict[str, Any] = test_class.__dataclass_fields__

        # Check
        for expected_field in expected_field_names:
            with self.subTest():
                self.assertIn(
                    member=expected_field,
                    container=present_field_names,
                    msg=f"Failure! Expected field: {expected_field} - is not present!"
                )

    # -------------------------------------------------------------------------
    def test_field_types_match_expected(self) -> None:
        from dataclasses import Field

        # Build
        expected_parameters = self._expected_pool_parameters.items()
        test_class = self._tested_class

        # Operate
        present_fields: Dict[str, Field[Any]] = test_class.__dataclass_fields__

        # Check
        for expected_field, expected_type in expected_parameters:
            with self.subTest():
                present_field: Field[Any] = present_fields[expected_field]
                present_type: Any = present_field.type

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

        cls._valid_pool_parameters: Dict[str, Any] = {
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
        test_pool_params: Dict[str, Any] = self._valid_pool_parameters.copy()
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
        test_pool_params: Dict[str, Any] = self._valid_pool_parameters.copy()
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
