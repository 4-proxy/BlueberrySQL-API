# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.2.2"

import unittest

from tests.test_abstract.abstract_test_inspector import AbstractTestInspector

from abstract.database.connection_interface import SingleConnectionInterface as tested_class

from inspect import Parameter
from typing import List, Any, Tuple


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
        AbstractTestInspector.check_inspected_class_is_abstract_of_ABC(_class=self._tested_class)

    # ------------------------------------------------------------------------------------------------------------------
    def test_interface_has_expected_contracts(self) -> None:
        # Build
        interface = self._tested_class
        expected_contracts: List[str] = self._expected_contracts_of_interface

        # Check
        for expected_contract in expected_contracts:
            with self.subTest(msg=f"Inspected interface don't have expected contract: *{expected_contract}*!"):
                AbstractTestInspector.check_inspected_class_has_expected_method(_class=interface,
                                                                                method_name=expected_contract)

    # ------------------------------------------------------------------------------------------------------------------
    def test_everyone_expected_contract_is_abstractmethod(self) -> None:
        # Build
        interface = self._tested_class
        expected_contracts: List[str] = self._expected_contracts_of_interface

        # Check
        for expected_contract in expected_contracts:
            with self.subTest(msg=f"Expected contract: *{expected_contract}* of *{interface}* - is not abstractmethod!"):
                AbstractTestInspector.check_inspected_method_is_abstractmethod(_class=interface,
                                                                               method_name=expected_contract)

    # ------------------------------------------------------------------------------------------------------------------
    def test_create_connection_with_database_signature_compliance(self) -> None:
        # Build
        interface = self._tested_class
        contract_name = 'create_connection_with_database'

        expected_signature_list: List[Tuple[str, Any]] = [
            ('self', Parameter.POSITIONAL_OR_KEYWORD),
            ('dbconfig', Parameter.VAR_KEYWORD),
        ]

        # Check
        AbstractTestInspector.check_inspected_method_signature_is_compliance(
            _class=interface,
            method_name=contract_name,
            expected_signature_list=expected_signature_list
        )
