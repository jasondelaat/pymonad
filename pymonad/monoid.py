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

from typing import (
    Any,
    Generic,
    List,
    TypeVar,
    Union,
    Iterable,
    Self,
)  # pylint: disable=unused-import

T = TypeVar("T")  # pylint: disable=invalid-name


class Monoid[T]:
    """Base class for Monoid instances.

    To implement a monoid instance, create a sub-class of Monoid and
    override the identity_element and addition_operation methods
    ensuring that the closure, identity, and associativity laws hold.

    """

    @classmethod
    def wrap(cls, value: T) -> Self:
        if value == None:
            return cls.identity_element()
        return cls(value)

    def __init__(self, value: T) -> None:
        if value == None:
            raise ValueError("None Objects not allowed in Monoids")
        self.value = value

    def __add__(self, other: Self | T) -> Self:
        if not isinstance(other, self.__class__):
            if isinstance(other, Monoid):
                raise ValueError("Incompatible Monoid")
            return self.addition_operation(self.__class__(other))
        return self.addition_operation(other)

    def __eq__(
        self: Union["_MonoidIdentity", "Monoid[T]"],
        other: Union["_MonoidIdentity", "Monoid[T]"],
    ) -> bool:
        return self.value == other.value

    def addition_operation(self: Self, other: Self) -> Self:
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

    @classmethod
    def identity_element[a: "Monoid"](cls: type[a]) -> a:
        """Returns the identity value for the monoid type.

        This method must be overridden in subclasses of Monoid

        """
        raise NotImplementedError


# class _MonoidIdentity[a : Monoid](a): #once Python Types has those features, this is what we want
class _MonoidIdentity[T](Monoid[T]):
    superclass = Monoid

    def __init__(self):
        found = False
        for i in type(self).__mro__:
            if (
                i != _MonoidIdentity
                and i != self.__class__
                and i != Monoid
                and i != Generic
                and i != object
            ):
                self.superclass = i
                found = True
                break
        if not found and self.__class__ != _MonoidIdentity:
            raise Exception("no superclass found")
        self.value = None

    def __add__(self: Self, other: Monoid[T] | T):
        if not isinstance(other, Monoid):
            return self.superclass(other)
        return other

    def __radd__(self, other: Self):
        if not isinstance(other, Monoid):
            return self.superclass(other)
        return other

    def __repr__(self):
        return "IDENTITY"


IDENTITY = _MonoidIdentity()


# mconcat([Monoida, Monoidb]) not throws an error :nice
def mconcat[a: Monoid](monoid_list: Iterable[a]) -> a:
    """Takes a list of monoid values and reduces them to a single value
    by applying the '+' operation to all elements of the list.
    Needs a non empty list, because Python doesn't allow calling on types
    """
    it = monoid_list.__iter__()

    # a.identity()
    result = it.__next__()
    for value in it:
        result = result + value
    return result
