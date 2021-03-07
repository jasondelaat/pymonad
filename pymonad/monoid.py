# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
"""Monoid Implementation.

A monoid is an algebraic structure consisting of a set of objects, S,
and an operation usually denoted as '+' which obeys the following
rules:

    1. Closure: If 'a' and 'b' are in S, then 'a + b' is also in S.
    2. Identity: There exists an element in S (denoted 0) such that
       a + 0 = a = 0 + a
    3. Associativity: (a + b) + c = a + (b + c)

The monoid module provides a generic zero/identity element called
IDENTITY.

Monoid addition with IDENTITY simply always returns the other element
regardless of type.

Example:
    IDENTITY == IDENTITY # True.
    IDENTITY + 10      # 10
    'hello' + IDENTITY # 'hello'

"""

from typing import Any, Generic, List, TypeVar, Union # pylint: disable=unused-import

T = TypeVar('T') # pylint: disable=invalid-name
MonoidT = Union['Monoid[T]', '_MonoidIdentity']

class Monoid(Generic[T]):
    """Base class for Monoid instances.

    To implement a monoid instance, create a sub-class of Monoid and
    override the identity_element and addition_operation methods
    ensuring that the closure, identity, and associativity laws hold.

    """

    def __init__(self, value: T) -> None:
        self.value = value

    def __add__(self: MonoidT, other: MonoidT) -> MonoidT:
        return self.addition_operation(other)

    def __eq__(
            self: Union['_MonoidIdentity', 'Monoid[T]'],
            other: Union['_MonoidIdentity', 'Monoid[T]']
    ) -> bool:
        return self.value == other.value

    def addition_operation(self: MonoidT, other: MonoidT) -> MonoidT:
        """Defines how monoid values are added together.

        addition_operation() method is automatically called by
        __add__() so monoid values are typically combined using the +
        operator and not addition_operation() directly.

        This method must be overridden in subclasses of Monoid.

        Args:
          other: a monoid value of the same type as self.

        Returns:
          Another monoid value of the same type as self and other.

        """
        raise NotImplementedError

    @staticmethod
    def identity_element() -> 'Monoid[Any]':
        """Returns the identity value for the monoid type.

        This method must be overridden in subclasses of Monoid.

        """
        raise NotImplementedError

class _MonoidIdentity:
    def __init__(self):
        self.value = None

    def __add__(self, other):
        return other

    def __radd__(self, other):
        return other

    def __repr__(self):
        return 'IDENTITY'

IDENTITY = _MonoidIdentity()

def mconcat(monoid_list: List[MonoidT]) -> MonoidT:
    """Takes a list of monoid values and reduces them to a single value
    by applying the '+' operation to all elements of the list.

    """
    result = monoid_list[0]
    for value in monoid_list:
        result += value
    return result
