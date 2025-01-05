# -*- coding: utf-8 -*-

"""
Test cases for `PoolConnectionInterface` from the `connection_interface.py` file.

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__author__ = "4-proxy"
__version__ = "0.4.0"

import unittest

from tests.test_helper import *

from abstract.database.connection_interface import PoolConnectionInterface as tested_class

from typing import List


# ______________________________________________________________________________________________________________________
class TestPoolConnectionInterface(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tested_class = tested_class

        cls._expected_contracts_of_interface: List[str] = [
            'create_new_connection_pool',
            'get_connection_from_pool',
            'close_active_pool'
        ]

    # ------------------------------------------------------------------------------------------------------------------
    def test_class_is_abstract_of_ABC(self) -> None:
        AbstractTestHelper.check_inspected_class_is_abstract_of_ABC(_class=self._tested_class)

    # ------------------------------------------------------------------------------------------------------------------
    def test_interface_has_expected_contracts(self) -> None:
        # Build
        interface = self._tested_class
        expected_contracts: List[str] = self._expected_contracts_of_interface

        # Check
        for expected_contract in expected_contracts:
            with self.subTest(msg=f"Inspected interface don't have expected contract: *{expected_contract}*!"):
                TestHelper.check_inspected_class_has_expected_method(_class=interface,
                                                                     method_name=expected_contract)

    # ------------------------------------------------------------------------------------------------------------------
    def test_everyone_expected_contract_is_abstractmethod(self) -> None:
        # Build
        interface = self._tested_class
        expected_contracts: List[str] = self._expected_contracts_of_interface

        # Check
        for expected_contract in expected_contracts:
            with self.subTest(msg=f"Expected contract: *{expected_contract}* of *{interface}* - is not abstractmethod!"):
                AbstractTestHelper.check_inspected_method_is_abstractmethod(_class=interface,
                                                                            method_name=expected_contract)
