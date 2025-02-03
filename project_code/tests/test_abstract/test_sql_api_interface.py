# -*- coding: utf-8 -*-

"""
Test cases for `SQLAPIInterface` from the `sql_api_interface.py` file.

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.4.0"

import unittest

from tests.test_helper import *

from abstract.api.sql_api_interface import SQLAPIInterface as tested_class

from inspect import Parameter
from typing import Any, List, Tuple


# ______________________________________________________________________________________________________________________
class TestSQLAPIInterface(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = tested_class

        cls._expected_contracts_of_interface: List[str] = [
            'execute_query_no_returns',
            'execute_query_returns_one',
            'execute_query_returns_all',
        ]

    # ------------------------------------------------------------------------------------------------------------------
    def test_class_is_abstract_of_ABC(self) -> None:
        AbstractTestHelper.check_inspected_class_is_abstract_of_ABC(_cls=self._tested_class)

    # ------------------------------------------------------------------------------------------------------------------
    def test_interface_has_expected_contracts(self) -> None:
        # Build
        interface = self._tested_class
        expected_contracts: List[str] = self._expected_contracts_of_interface

        # Check
        for expected_contract in expected_contracts:
            with self.subTest(msg=f"Inspected interface don't have expected contract: *{expected_contract}*!"):
                TestHelper.check_inspected_class_has_expected_method(_cls=interface,
                                                                     method_name=expected_contract)

    # ------------------------------------------------------------------------------------------------------------------
    def test_everyone_expected_contract_is_abstractmethod(self) -> None:
        # Build
        interface = self._tested_class
        expected_contracts: List[str] = self._expected_contracts_of_interface

        # Check
        for expected_contract in expected_contracts:
            with self.subTest(msg=f"Expected contract: *{expected_contract}* of *{interface}* - is not abstractmethod!"):
                AbstractTestHelper.check_inspected_method_is_abstractmethod(_cls=interface,
                                                                            method_name=expected_contract)

    # ------------------------------------------------------------------------------------------------------------------
    def test_interface_contracts_signature_compliance(self) -> None:
        # Build
        interface = self._tested_class
        contracts: List[str] = self._expected_contracts_of_interface

        expected_parameter_default_to_None = 'query_data'
        expected_signature_list: List[Tuple[str, Any]] = [
            ('self', Parameter.POSITIONAL_OR_KEYWORD),
            ('sql_query', Parameter.POSITIONAL_OR_KEYWORD),
            ('query_data', Parameter.POSITIONAL_OR_KEYWORD),
        ]  # parameter name, parameter kind

        # Check
        for contract in contracts:
            with self.subTest(msg=f"Signature of inspected contract: *{contract}* - not as expected!"):
                AbstractTestHelper.check_inspected_method_signature_is_compliance(
                    _cls=interface,
                    method_name=contract,
                    expected_signature_list=expected_signature_list
                )
                AbstractTestHelper.check_inspected_method_parameter_defaults_to_none(
                    _cls=interface,
                    method_name=contract,
                    parameter_name=expected_parameter_default_to_None
                )
