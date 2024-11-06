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

from abstract.database.single_connection_interface import SingleConnectionInterface as tested_class

from inspect import Parameter, Signature
from typing import List, Callable, Any, Tuple


# ______________________________________________________________________________________________________________________
class TestSingleConnectionInterface(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = tested_class

        cls._expected_contracts_of_interface: List[str] = [
            'create_connection_with_database',
            'get_connection_with_database',
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
                self.assertTrue(expr=method.__isabstractmethod__)  # type: ignore

    # ------------------------------------------------------------------------------------------------------------------
    def test_create_connection_with_database_signature_compliance(self) -> None:
        # Build
        interface = self._tested_class
        contract_name = 'create_connection_with_database'

        expected_signature: Tuple[str, Any] = ('dbconfig', Parameter.VAR_KEYWORD)

        # Operate
        method: Callable[..., Any] = getattr(interface, contract_name)
        signature: Signature = inspect.signature(obj=method)
        params = list(signature.parameters.values())

        # Check
        inspected_param: Parameter = params[1]
        actual_signature: Tuple[str, Any] = (inspected_param.name, inspected_param.kind)

        self.assertEqual(first=expected_signature,
                         second=actual_signature)
