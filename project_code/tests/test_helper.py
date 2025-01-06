# -*- coding: utf-8 -*-

"""
This module defines the `AbstractTestHelper` and `TestHelper` classes, which provide static methods
for various checks of classes and their methods for expected conformance.

The `AbstractTestHelper` class in particular serves as an auxiliary tool for testing, allowing you to test
abstract classes and methods against the requirements established in the
`Python` abstract class management system.

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    'AbstractTestHelper',
    'TestHelper'
]

__author__ = "4-proxy"
__version__ = "0.4.0"

import inspect

from inspect import Signature, Parameter
from abc import ABC
from os import name
from typing import Any, Callable, Iterable, Tuple, List, Type


# ______________________________________________________________________________________________________________________
class AbstractTestHelper:
    """AbstractTestHelper auxiliary class of checks for test cases.

    This class contains static methods that perform various checks
    on classes and their methods to ensure they conform to
    the expected abstract class structure and method signatures.
    """

    @staticmethod
    def check_inspected_class_is_abstract_of_ABC(_class: Type[ABC]) -> None:
        """check_inspected_class_is_abstract_of_ABC checks whether the class being checked is an abstract class.

        *`Python` allows you to create an instance of an abstract class if it has no methods.
        Hence the check via inheritance.

        Args:
            _class: The class to be checked.

        Raises:
            AssertionError: If the `_class` is not a subclass of `ABC`.
        """
        from abc import ABC

        # Check
        assert issubclass(_class, ABC), \
            f"Failure! Inspected class: *{_class}* - is not abstract of *{ABC}*!"

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_class_implements_expected_interface(_class, expected_interface: Type[ABC]) -> None:
        """check_inspected_class_implements_expected_interface checks if the `_class` implements the `expected_interface`.

        This method verifies that the `_class` is a subclass of the `expected_interface`
        and that it implements all abstractmethods defined in `expected_interface`.

        Args:
            _class: The class to be checked.
            expected_interface (Type[ABC]): The interface that is expected to be implemented by `_class`.

        Raises:
            AssertionError: If `_class` doesn't inherit from `expected_interface`
                            or does not implement all abstract methods defined in `expected_interface`.
        """
        # Check inheritance of abstract interface
        assert issubclass(_class, expected_interface), \
            f"Failure! Inspected class: *{_class}* - doesn't inherit the implementable interface *{expected_interface}*!"

        # Check implementation of abstract interface methods
        AbstractTestHelper.check_inspected_class_overridden_abstractmethods_of_expected_class(_class=_class,
                                                                                              expected_class=expected_interface)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_class_overridden_abstractmethods_of_expected_class(_class, expected_class: Type[ABC]) -> None:
        """check_inspected_class_overridden_abstractmethods_of_expected_class checks if the `_class` overridden abstractmethods of `expected_class`.

        This method verifies that all abstractmethods defined in the `expected_class`
        have been implemented in the `_class`.

        Args:
            _class: The class to be checked for overridden abstractmethods.
            expected_class: The class that defines the abstractmethods that should be overridden by `_class`.

        Raises:
            AssertionError: If any abstractmethod defined in `expected_class` is not overridden in `_class`.
        """
        # Build
        abstractmethods_of_expected_class: Tuple[str, ...] = tuple(expected_class.__abstractmethods__)

        # Operate
        for abstractmethod_name in abstractmethods_of_expected_class:
            # Build
            method: Callable = getattr(_class, abstractmethod_name)

            # Check
            assert hasattr(method, '__isabstractmethod__') is False, \
                f"Failure! Inspected class: *{_class}* - doesn't overridden abstractmethod *{abstractmethod_name}* of *{expected_class}*!"

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
        try:
            for expected_signature, actual_signature in zip(expected_signature_list,
                                                            actual_signature_list,
                                                            strict=True):
                if actual_signature != expected_signature:
                    raise ValueError

        except Exception:
            raise AssertionError(
                f"Failure! Signature list of the inspected method: *{method_name}* - not as expected!\n"
                f"Actual signature list: {actual_signature_list}\n"
                f"Expected signature list: {expected_signature_list}"
            )


# ______________________________________________________________________________________________________________________
class TestHelper:
    """TestHelper auxiliary class for validating classes and their methods.

    This class serves as a practical tool for unit testing and ensuring
    that classes adhere to defined structures.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_class_has_expected_method(_class, method_name: str) -> None:
        """check_inspected_class_has_expected_method checks if the expected method exists in the class.

        Args:
            _class: The class to be checked.
            method_name (str): The name of the method to be present in the `_class`.

        Raises:
            AssertionError: If the method is not present in the `_class`.
        """
        assert hasattr(_class, method_name), \
            f"Failure! Inspected class: *{_class}* - don't have expected method *{method_name}*!"

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_class_is_subclass_of_expected_base_class(_class, expected_base_class) -> None:
        """check_inspected_class_is_subclass_of_expected_base_class checks if the `_class` is subclass of `expected_base_class`.

        Args:
            _class: The class to be checked.
            expected_base_class: The base class that is expected to be inherited by `_class`.

        Raises:
            AssertionError: If `_class` is not a subclass of `expected_base_class`.
        """
        assert issubclass(_class, expected_base_class), \
            f"Failure! Inspected class: *{_class}* - is not a subclass of *{expected_base_class}*!"

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_object_has_expected_fields(_obj, expected_fields: Iterable[str]) -> None:
        """check_inspected_object_has_expected_fields checks if the `_obj` has expected fields.

        *This method is not suitable for checking class fields, as they do not support the use of `__repr__()`.

        Args:
            _obj: The object to be checked.
            expected_fields: Iterable sequence with the names of the expected fields of `_obj`.

        Raises:
            AssertionError: If `_obj` is not has one of `expected_fields`.
        """
        for expected_field in expected_fields:
            assert hasattr(_obj, expected_field), \
                f"Failure! Inspected object: *{_obj.__repr__()}* - not has expected field *{expected_field}*!"
