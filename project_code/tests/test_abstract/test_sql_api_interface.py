# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.1.0"

import unittest

import inspect

from abstract.api.sql_api_interface import SQLAPIInterface as tested_class

from inspect import Signature, Parameter
from typing import Any, Callable, List, Tuple


# ______________________________________________________________________________________________________________________
class TestSQLAPIInterfacePositive(unittest.TestCase):
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
    def test_interface_has_expected_contracts(self) -> None:
        # Build
        interface = self._tested_class
        expected_contracts: List[str] = self._expected_contracts_of_interface

        # Check
        for expected_contract in expected_contracts:
            with self.subTest(msg=f"Inspected interface don't have expected contract: {expected_contract}!"):
                # Operate
                getattr(interface, expected_contract)

    # ------------------------------------------------------------------------------------------------------------------
    def test_everyone_expected_contract_is_abstractmethod(self) -> None:
        # Build
        interface = self._tested_class
        expected_contracts: List[str] = self._expected_contracts_of_interface

        # Check
        for expected_contract in expected_contracts:
            with self.subTest(msg=f"Expected contract: {expected_contract} of {interface} - is not abstractmethod!"):
                # Build
                method: Callable[..., Any] = getattr(interface, expected_contract)

                # Check
                self.assertTrue(expr=method.__isabstractmethod__)

    # ------------------------------------------------------------------------------------------------------------------
    def test_interface_contracts_signature_compliance(self) -> None:
        # Build
        interface = self._tested_class
        contracts: List[str] = self._expected_contracts_of_interface

        expected_params_signature: List[Tuple[str, Any]] = [
            ('sql_query', Parameter.POSITIONAL_OR_KEYWORD),
            ('query_data', Parameter.VAR_POSITIONAL),
        ]  # parameter name, parameter kind

        # Check
        for contract in contracts:
            with self.subTest(msg=f"Signature of inspected contract: {contract} - not as expected!"):
                # Build
                method: Callable[..., Any] = getattr(interface, contract)
                signature: Signature = inspect.signature(obj=method)
                params = list(signature.parameters.values())

                # Operate
                first_param: Parameter = params[1]
                second_param: Parameter = params[2]

                actual_params_signature: List[Tuple[str, Any]] = [
                    (first_param.name, first_param.kind),
                    (second_param.name, second_param.kind),
                ]  # parameter name, parameter kind

                # Check
                self.assertEqual(first=expected_params_signature,
                                 second=actual_params_signature)
