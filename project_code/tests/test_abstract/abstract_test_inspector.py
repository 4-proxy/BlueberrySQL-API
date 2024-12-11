# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'AbstractTestInspector'
]

__author__ = "4-proxy"
__version__ = "0.1.1"

import inspect

from inspect import Signature, Parameter
from typing import Any, Callable, Tuple, List


# ______________________________________________________________________________________________________________________
class AbstractTestInspector:
    """Auxiliary class of checks for test cases

    This class contains static methods that perform various checks
    on classes and their methods to ensure they conform to
    the expected abstract class structure and method signatures.
    """
    @staticmethod
    def check_inspected_class_is_abstract_of_ABC(_class) -> None:
        """
        Python allows you to create an instance of an abstract class if it has no methods.
        Hence the check via inheritance.
        """
        from abc import ABC

        # Check
        assert issubclass(_class, ABC), \
            f"Failure! Inspected class: *{_class}* - is not abstract of *{ABC}*!"

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_class_has_expected_method(_class, method_name: str) -> None:
        assert hasattr(_class, method_name), \
            f"Failure! Inspected class: *{_class}* - don't have expected method *{method_name}*!"

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_method_is_abstractmethod(_class, method_name: str) -> None:
        """
        When working with the `@abstractmethod` decorator
        the method acquires the `__isabstractmethod__` field with the value `True`.
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
        """
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
