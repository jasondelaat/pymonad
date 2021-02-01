# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Implements the base Monoid type.

A monoid is an algebraic structure consisting of a set of objects, S,
such as integers; strings; etc., and an operation usually denoted as
'+' which obeys the following rules:
  1. Closure: If 'a' and 'b' are in S, then 'a + b' is also in S.
  2. Identity: There exists an element in S (denoted 0) such that
     a + 0 = 0 + a = a
  3. Associativity: (a + b) + c = a + (b + c)

For monoid types, the '+' operation is implemented by the method
'mplus' and the static method 'mzero' is defined to return the
identity element of the type.

For example, integers can be monoids in two ways:
  1. mzero = 0 and mplus = addition
  2. mzero = 1 and mplus = multiplication

String can also form a monoid where mzero is the empty string and
mplus is concatenation.
"""

from typing import Any, Generic, List, TypeVar, Union # pylint: disable=unused-import

T = TypeVar('T') # pylint: disable=invalid-name
MonoidT = Union['Monoid[T]', int, List, float, str]

class Monoid(Generic[T]):
    """ Abstract base class for Monoid instances.

    To implement a monoid instance, users should create a sub-class of
    Monoid and implement the mzero and mplus methods. Additionally, it
    is the implementers responsibility to ensure that the
    implementation adheres to the closure, identity and associativity
    laws for monoids.
    """

    def __init__(self, value: T) -> None:
        self.value = value

    def __add__(self: MonoidT, other: MonoidT) -> MonoidT:
        return self.addition_operation(other)

    def __eq__(self: Union['IDENTITY', 'Monoid[T]'], other: Union['IDENTITY', 'Monoid[T]']) -> bool:
        try:
            if self is IDENTITY and other is IDENTITY: # pylint: disable=no-else-return
                return True
            else:
                return self.value == other.value
        except AttributeError:
            return False

    def addition_operation(self: MonoidT, other: MonoidT) -> MonoidT:
        raise NotImplementedError

    @staticmethod
    def identity_element() -> 'Monoid[Any]':
        """
        A static method which simply returns the identity value for the monoid type.
        This method must be overridden in subclasses to create custom monoids.
        See also: the mzero function.

        """
        raise NotImplementedError

class _MonoidIdentityMeta(type, Monoid):
    @staticmethod
    def identity_element():
        raise AttributeError('Monoid IDENTITY has no identity_element.')

    def __add__(cls, other):
        return other

    def __radd__(cls, other):
        return other

    def __repr__(cls):
        return 'IDENTITY'

class IDENTITY(metaclass=_MonoidIdentityMeta): # pylint: disable=too-few-public-methods
    """ A generic zero/identity element for monoids.

    The IDENTITY class acts as a constant/singleton with monoid addition
    implemented on the class itself to always return the other
    element. It is not actually possible to create an instance of IDENTITY
    as calling the constructor simply returns the class itself.

    Example:
      IDENTITY == IDENTITY() # True.
      IDENTITY + 10      # 10
      'hello' + IDENTITY # 'hello'
    """
    def __new__(cls):
        return IDENTITY

def mconcat(monoid_list: List[MonoidT]) -> MonoidT:
    """
    Takes a list of monoid values and reduces them to a single value by applying the
    mplus operation to each all elements of the list.

    """
    result = monoid_list[0]
    for value in monoid_list:
        result += value
    return result
