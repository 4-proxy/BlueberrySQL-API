# -*- coding: utf-8 -*-

"""
Test cases for `PoolConfigDTO` from the `pool_config_dto.py` file.

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.3.1"

import unittest
from unittest import mock as UnitMock

from tests.test_helper import AbstractTestHelper

from abstract.config.pool_config_dto import PoolConfigDTO as tested_class

from _collections_abc import dict_items, dict_keys
from typing import Any, Dict


# ______________________________________________________________________________________________________________________
class ConcreteTestClass(tested_class):
    def validate_fields_data(self) -> None:
        pass


# ______________________________________________________________________________________________________________________
class TestPoolConfigDTO(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = tested_class

        cls._expected_dataclass_params: Dict[str, type] = {
            "name": str,
            "size": int,
            "reset_session": bool,
        }

    # ------------------------------------------------------------------------------------------------------------------
    def test_inspected_class_is_dataclass(self) -> None:
        from dataclasses import is_dataclass

        # Build
        _class = self._tested_class

        # Operate
        _is_dataclass: bool = is_dataclass(obj=_class)

        # Check
        self.assertTrue(expr=_is_dataclass,
                        msg=f"Failure! Inspected class: *{_class}* - is not a dataclass!")

    # ------------------------------------------------------------------------------------------------------------------
    def test_class_is_abstract_of_ABC(self) -> None:
        AbstractTestHelper.check_inspected_class_is_abstract_of_ABC(_cls=self._tested_class)

    # ------------------------------------------------------------------------------------------------------------------
    def test_inspected_dataclass_should_be_frozen(self) -> None:
        # Build
        _class = self._tested_class

        # Operate
        is_frozen: bool = _class.__dataclass_params__.frozen  # type: ignore

        # Check
        self.assertTrue(expr=is_frozen,
                        msg=f"Failure! Inspected class: *{_class}* - is dataclass, but it's not frozen!")

    # ------------------------------------------------------------------------------------------------------------------
    def test_all_expected_fields_are_present(self) -> None:
        # Build
        _class = self._tested_class
        expected_fields: dict_keys[str, type] = self._expected_dataclass_params.keys()

        # Operate
        present_fields: dict_keys[str, Any] = _class.__dataclass_fields__.keys()

        # Check
        for expected_field in expected_fields:
            with self.subTest():
                self.assertIn(
                    member=expected_field,
                    container=present_fields,
                    msg=f"Failure! Expected field: *{expected_field}* - is not present in *{_class}*!"
                )

    # ------------------------------------------------------------------------------------------------------------------
    def test_present_field_types_match_expected(self) -> None:
        from dataclasses import Field

        # Build
        _class = self._tested_class
        expected_params: dict_items[str, type] = self._expected_dataclass_params.items()

        # Operate
        present_params: Dict[str, Field[Any]] = _class.__dataclass_fields__

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
                    msg=f"Failure! Inspected field: *{expected_field}* - has type *{present_type}* not as expect *{expected_type}*!"
                )

    # ------------------------------------------------------------------------------------------------------------------
    def test_validate_fields_data_is_abstractmethod(self) -> None:
        AbstractTestHelper.check_inspected_method_is_abstractmethod(_cls=self._tested_class,
                                                                    method_name='validate_fields_data')

    # ------------------------------------------------------------------------------------------------------------------
    @UnitMock.patch.object(target=ConcreteTestClass, attribute='validate_fields_data')
    def test_post_constructor_calls_method_validate_fields_data(self,
                                                                mock_validate_fields_data: UnitMock.MagicMock) -> None:
        # Build
        _class = ConcreteTestClass

        # Operate
        instance = _class(name='test', size=1, reset_session=True)

        # Check
        mock_validate_fields_data.assert_called_once()
