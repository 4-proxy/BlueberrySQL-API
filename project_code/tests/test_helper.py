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
    'TestHelper',
    'TestHelperTool'
]

__author__ = "4-proxy"
__version__ = "0.7.1"

import inspect

from inspect import Signature, Parameter
from abc import ABC
from typing import Any, Callable, Iterable, NoReturn, Optional, Tuple, List, Type


# ______________________________________________________________________________________________________________________
class AbstractTestHelper:
    """
    AbstractTestHelper auxiliary class of checks for test cases.

    This class contains static methods that perform various checks
    on classes and their methods to ensure they conform to
    the expected abstract class structure and method signatures.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __new__(cls) -> NoReturn:
        raise TypeError(f"Sorry, but this class: *{cls.__qualname__}* - is not intended to be initialized!")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_class_is_abstract_of_ABC(_cls: Type[ABC]) -> None:
        """
        check_inspected_class_is_abstract_of_ABC checks whether the class being checked is an abstract class.

        *`Python` allows you to create an instance of an abstract class if it has no methods.
        Hence the check via inheritance.

        Args:
            _cls (Type[ABC]): The class to be checked.

        Raises:
            AssertionError: If the `_cls` is not a subclass of `ABC`.
        """
        from abc import ABC

        # Check
        if not issubclass(_cls, ABC):
            raise AssertionError(
                f"Failure! Inspected class: *{_cls}* - is not abstract of *{ABC}*!"
            )

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_class_implements_expected_interface(_cls: Type,
                                                            expected_interface: Type[ABC]) -> None:
        """
        check_inspected_class_implements_expected_interface checks if the `_cls` implements the `expected_interface`.

        This method verifies that the `_cls` is a subclass of the `expected_interface`
        and that it implements all abstractmethods defined in `expected_interface`.

        Args:
            _cls (Type): The class to be checked.
            expected_interface (Type[ABC]): The interface that is expected to be implemented by `_cls`.

        Raises:
            AssertionError: If `_cls` doesn't inherit from `expected_interface`
                            or does not implement all abstract methods defined in `expected_interface`.
        """
        # Check inheritance of abstract interface
        if not issubclass(_cls, expected_interface):
            raise AssertionError(
                f"Failure! Inspected class: *{_cls}* - doesn't inherit the implementable interface *{expected_interface}*!"
            )

        # Check implementation of abstract interface methods
        AbstractTestHelper.check_inspected_class_overridden_abstractmethods_of_expected_class(_cls=_cls,
                                                                                              expected_class=expected_interface)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_class_overridden_abstractmethods_of_expected_class(_cls: Type,
                                                                           expected_class: Type[ABC]) -> None:
        """
        check_inspected_class_overridden_abstractmethods_of_expected_class checks if the `_cls` overridden abstractmethods of `expected_class`.

        This method verifies that all abstractmethods defined in the `expected_class`
        have been implemented in the `_cls`.

        Args:
            _cls (Type): The class to be checked for overridden abstractmethods.
            expected_class: The class that defines the abstractmethods that should be overridden by `_cls`.

        Raises:
            AssertionError: If any abstractmethod defined in `expected_class` is not overridden in `_cls`.
        """
        # Build
        abstractmethods_of_expected_class: Tuple[str, ...] = tuple(expected_class.__abstractmethods__)

        # Operate
        for abstractmethod_name in abstractmethods_of_expected_class:
            # Build
            method: Callable = getattr(_cls, abstractmethod_name)

            # Check
            if hasattr(method, '__isabstractmethod__'):
                raise AssertionError(
                    f"Failure! Inspected class: *{_cls}* - doesn't overridden abstractmethod *{abstractmethod_name}* of *{expected_class}*!"
                )

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_method_is_abstractmethod(_cls: Type,
                                                 method_name: str) -> None:
        """
        check_inspected_method_is_abstractmethod checks whether the method is an abstract method.

        *When the `@abstractmethod` decorator is used, the method gets the `__isabstractmethod__` field
        with the value `True`.

        Args:
            _cls (Type): The class containing the method.
            method_name (str): The name of the method to be validated.

        Raises:
            AssertionError: If the method doesn't have a `__isabstractmethod__` field or it is not equal to `True`.
        """
        # Build
        expected_field = '__isabstractmethod__'

        # Operate
        try:
            inspected_method: Callable[..., Any] = getattr(_cls, method_name)
        except AttributeError:
            raise AssertionError(
                f"Failure! The passed class: *{_cls.__qualname__}* - doesn't have inspected method *{method_name}*!"
            )

        # Check
        if not hasattr(inspected_method, expected_field):
            raise AssertionError(
                f"Failure! Inspected method: *{method_name}* - is exist, but don't have *{expected_field}* field!\n"
                "So, maybe it's not an abstractmethod!"
            )

        if getattr(inspected_method, expected_field) is not True:
            raise AssertionError(
                f"Failure! Inspected method: *{method_name}* - has *{expected_field}* field, but it's not *{True}*!"
            )

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_method_signature_is_compliance(_cls: Type,
                                                       method_name: str,
                                                       expected_signature_list: List[Tuple[str, Any]]) -> None:
        """
        check_inspected_method_signature_is_compliance checks if the method signature matches the expected signature.

        *Parameters for testing are retrieved using the `inspect` module.

        Args:
            _cls (Type): The class containing the method.
            method_name (str): The name of the method to be checked.
            expected_signature_list (List[Tuple[str, Any]]): Expected list of method parameter signatures
                                                             in the format [(<parameter_name>, <parameter_Type>), ...].

            *Note:
                `<parameter_name>` (str): The name of the method parameter.
                `<parameter_Type>` (inspect.Parameter): The Type of the parameter, defined with `inspect.Parameter`.

        Raises:
            AssertionError: If the actual method signature doesn't match the expected signature.

        Example of `expected_signature_list`:
            >>> expected_signature_list: List[Tuple[str, Any]] = [
            ...    ('self', Parameter.POSITIONAL_OR_KEYWORD),
            ...    ('dbconfig', Parameter.VAR_KEYWORD),
            ... ]
        """
        # Build
        method: Callable[..., Any] = getattr(_cls, method_name)
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

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_method_parameter_defaults_to_none(_cls: Type,
                                                          method_name: str,
                                                          parameter_name: str) -> None:
        """
        check_inspected_method_parameter_defaults_to_none checks if the specified parameter defaults to `None`.

        Args:
            _cls (Type): The class containing the method.
            method_name (str): The name of the method to inspect.
            parameter_name (str): The name of the parameter to check.

        Raises:
            AssertionError: If the parameter does not default to `None`.
        """
        # Build
        method: Callable[..., Any] = getattr(_cls, method_name)
        signature: Signature = inspect.signature(obj=method)

        # Operate
        param: Optional[Parameter] = signature.parameters.get(parameter_name)

        # Check
        if param is None or param.default is not None:
            raise AssertionError(
                f"Failure! Inspected parameter: *{parameter_name}* in method *{method_name}* - does not default to *None*!"
            )


# ______________________________________________________________________________________________________________________
class TestHelper:
    """
    TestHelper auxiliary class for validating classes and their methods.

    This class serves as a practical tool for unit testing and ensuring
    that classes adhere to defined structures.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __new__(cls) -> NoReturn:
        raise TypeError(f"Sorry, but this class: *{cls.__qualname__}* - is not intended to be initialized!")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_class_has_expected_method(_cls: Type,
                                                  method_name: str) -> None:
        """
        check_inspected_class_has_expected_method checks if the expected method exists in the `_cls`.

        Args:
            _cls (Type): The class to be checked.
            method_name (str): The name of the method to be present in the `_cls`.

        Raises:
            AssertionError: If the method is not present in the `_cls`.
        """
        method = getattr(_cls, method_name, None)

        if method is None:
            raise AssertionError(
                f"Failure! Inspected class: *{_cls.__qualname__}* \
                    - doesn't have expected callable method *{method_name}*!"
            )

        if not callable(method):
            raise AssertionError(
                f"Failure! Inspected class: *{_cls.__qualname__}* \
                    - has attribute *{method_name}*, but it's not a callable!"
            )

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_class_is_subclass_of_expected_base_class(_cls: Type,
                                                                 expected_base_class: Type) -> None:
        """
        check_inspected_class_is_subclass_of_expected_base_class checks if the `_class` is subclass of `expected_base_class`.

        Args:
            _cls (Type): The class to be checked.
            expected_base_class (Type): The base class that is expected to be inherited by `_cls`.

        Raises:
            AssertionError: If `_cls` is not a subclass of `expected_base_class`.
        """
        if not issubclass(_cls, expected_base_class):
            raise AssertionError(
                f"Failure! Inspected class: *{_cls.__qualname__}* - is not a subclass of *{expected_base_class}*!"
            )

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_inspected_object_has_expected_fields(_obj: Any,
                                                   expected_fields: Iterable[str]) -> None:
        """
        check_inspected_object_has_expected_fields checks if the `_obj` has expected fields.

        *This method is not suitable for checking class fields, as they do not support the use of `__repr__()`.

        Args:
            _obj (Any): The object to be checked.
            expected_fields (Iterable[str]): Iterable sequence with the names of the expected fields of `_obj`.

        Raises:
            AssertionError: If `_obj` is not has one of `expected_fields`.
        """
        for expected_field in expected_fields:
            if not hasattr(_obj, expected_field):
                raise AssertionError(
                    f"Failure! Inspected object: *{_obj.__repr__()}* - not has expected field *{expected_field}*!"
                )


# ______________________________________________________________________________________________________________________
class TestHelperTool:
    """
    TestHelperTool provides helper methods for working with classes in a testing context.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __new__(cls) -> NoReturn:
        raise TypeError(f"Sorry, but this class: *{cls.__qualname__}* - is not intended to be initialized!")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_full_name_of_class_private_field(_cls: Type, private_field_name: str) -> str:
        """
        get_full_name_of_class_private_field gets the full name of the `_cls` private field.

        The method generates the full name of a private field by adding prefixes required to access it
        according to the naming conventions in `Python`.

        Args:
            _cls (Type): The class containing the private field.
            private_field_name (str): The name of the private field without prefixes.

        Returns:
            str: The full name of the private field in the format '_<class_name>__<field_name>'.

        Example usage:
            >>> full_name = TestHelperTool.get_full_name_of_class_private_field(MyClass, 'my_private_field')
            >>> print(full_name) # Output: '_MyClass__my_private_field'
        """
        field_name: str = private_field_name
        if not private_field_name.startswith('__'):
            field_name = '__' + private_field_name

        full_field_name: str = '_' + _cls.__name__ + field_name

        return full_field_name
