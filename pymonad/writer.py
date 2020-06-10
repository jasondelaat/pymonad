# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Implements the Writer monad.

The Writer monad is typically used to append information to a log. The
log type is often just strings but can be any type that behaves as a
monoid with a defined + (__add__) operator.

  Example:
    @curry(2)
    def add(x, y):
        return Writer(x + y, f"Called function 'add' with arguments {x} and {y}. Result: {x + y}")

    @curry(2)
    def mul(x, y):
        return Writer(x * y, f"Called function 'mul' with arguments {x} and {y}. Result: {x * y}")

    logged_arithmetic = (Writer
                         .insert(0)
                         .then(add(1))
                         .then(mul(2)))

    # logged_arithmetic = (2, "Called function 'add' with arguments 1 and 0. Result: 1
    #                     Called function 'mul' with arguments 2 and 1. Result: 2")
"""
from typing import Callable, Generic, List, TypeVar

import pymonad.monad
import pymonad.monoid

M = TypeVar('M', int, str, List, pymonad.monoid.Monoid, pymonad.monoid.ZERO) # pylint: disable=invalid-name
S = TypeVar('S') # pylint: disable=invalid-name
T = TypeVar('T') # pylint: disable=invalid-name

class Writer(pymonad.monad.Monad, Generic[M, T]):
    """ The Writer monad class. """
    @classmethod
    def insert(cls, value: T) -> 'Writer[M, T]':
        """ See Monad.insert. """
        return Writer(value, pymonad.monoid.ZERO)

    def bind(
            self: 'Writer[M, S]', kleisli_function: Callable[[S], 'Writer[M, T]']
    ) -> 'Writer[M, T]':
        """ See Monad.bind. """
        result = kleisli_function(self.value)
        return Writer(result.value, self.monoid + result.monoid)

    def map(self: 'Writer[M, S]', function: Callable[[S], T]) -> 'Writer[M, T]':
        """ See Monad.map. """
        return Writer(function(self.value), self.monoid)

    def __eq__(self, other):
        return self.value == other.value and self.monoid == other.monoid

    def __repr__(self):
        return f'({self.value}, {self.monoid})'
