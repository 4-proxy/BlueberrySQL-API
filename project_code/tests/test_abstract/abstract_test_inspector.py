# -*- coding: utf-8 -*-

"""
This module defines the `AbstractTestInspector` class, which provides static methods
to test whether classes and their methods conform to expected structures.

This class serves as an auxiliary tool for testing, allowing you to check
abstract classes and methods against the requirements established in the
`Python` abstract class management system.

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'AbstractTestInspector'
]

__author__ = "4-proxy"
__version__ = "0.2.0"

import inspect

from inspect import Signature, Parameter
from typing import Any, Callable, Tuple, List


# ______________________________________________________________________________________________________________________
class AbstractTestInspector:
    """AbstractTestInspector auxiliary class of checks for test cases.

    This class contains static methods that perform various checks
    on classes and their methods to ensure they conform to
    the expected abstract class structure and method signatures.
    """

    @staticmethod
    def check_inspected_class_is_abstract_of_ABC(_class) -> None:
        """check_inspected_class_is_abstract_of_ABC checks whether the class being checked is an abstract class.

        *`Python` allows you to create an instance of an abstract class if it has no methods.
        Hence the check via inheritance.

        Args:
            _class: The class to be checked.

        Raises:
            AssertionError: If the class is not a subclass of ABC.
        """
        from abc import ABC

        # Check
        assert issubclass(_class, ABC), \
            f"Failure! Inspected class: *{_class}* - is not abstract of *{ABC}*!"

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_class_has_expected_method(_class, method_name: str) -> None:
        """check_inspected_class_has_expected_method checks if the expected method exists in the class.

        Args:
            _class: The class to be checked.
            method_name (str): The name of the method to be present in the class.

        Raises:
            AssertionError: If the method is not present in the class.
        """
        assert hasattr(_class, method_name), \
            f"Failure! Inspected class: *{_class}* - don't have expected method *{method_name}*!"

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_method_is_abstractmethod(_class, method_name: str) -> None:
        """check_inspected_method_is_abstractmethod checks whether the method is an abstract method.

        *When the `@abstractmethod` decorator is used, the method gets the `__isabstractmethod__` field
        with the value `True`.

        Args:
            _class: The class containing the method.
            method_name (str): The name of the method to be validated.

        Raises:
            AssertionError: If the method doesn't have a `__isabstractmethod__` field or it is not equal to `True`.
        """
        # Build
        expected_field = '__isabstractmethod__'

        # Operate
        inspected_method: Callable[..., Any] = getattr(_class, method_name)

        # Check
        assert hasattr(inspected_method, expected_field), \
            f"Failure! Inspected method: *{method_name}* - is exist, but don't have *{expected_field}* field!"

        assert getattr(inspected_method, expected_field) is True, \
            f"Failure! Inspected method: *{method_name}* - has *{expected_field}* field, but it's not *{True}*!"

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_method_signature_is_compliance(_class,
                                                       method_name: str,
                                                       expected_signature_list: List[Tuple[str, Any]]) -> None:
        """check_inspected_method_signature_is_compliance checks if the method signature matches the expected signature.

        *Parameters for testing are retrieved using the `inspect` module.

        Args:
            _class: The class containing the method.
            method_name (str): The name of the method to be checked.
            expected_signature_list (List[Tuple[str, Any]]): Expected list of method parameter signatures
                                                             in the format [(<parameter_name>, <parameter_type>), ...].

            *Note:
                `<parameter_name>` (str): The name of the method parameter.
                `<parameter_type>` (inspect.Parameter): The type of the parameter, defined with `inspect.Parameter`.

        Raises:
            AssertionError: If the actual method signature doesn't match the expected signature.

        Example of `expected_signature_list`:
            >>> expected_signature_list: List[Tuple[str, Any]] = [
            ...    ('self', Parameter.POSITIONAL_OR_KEYWORD),
            ...    ('dbconfig', Parameter.VAR_KEYWORD),
            ... ]
        """
        # Build
        method: Callable[..., Any] = getattr(_class, method_name)
        signature: Signature = inspect.signature(obj=method)
        params: List[Parameter] = list(signature.parameters.values())

        # Operate
        actual_signature_list: List[Tuple[str, Any]] = []
        for param in params:
            new_signature: Tuple[str, Any] = (param.name, param.kind)
            actual_signature_list.append(new_signature)

        # Check
        for expected_signature, actual_signature in zip(expected_signature_list, actual_signature_list):
            assert expected_signature == actual_signature, \
                f"Failure! Signature of the inspected parameter of method: *{method_name}* - not as expected!\n"\
                f"Actual signature: {actual_signature}\n"\
                f"Expected signature: {expected_signature}"
