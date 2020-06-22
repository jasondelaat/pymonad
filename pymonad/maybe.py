# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Implements the Maybe monad and related functions.

The Maybe monad is used to represent calculations that may or may not
return a value. Alternately, if used as function inputs, Maybe values
can be used to indicate 'optional' inputs, explicitly passing
'Nothing' when no input is required.

When creating Maybe values directly use the 'Just' function or 'Nothing':

  Example:
    x = Just(19)
    y = Just('A string')
    z = Nothing

The 'insert' class method is a wrapper around the 'Just' function.

  Example:
    x = Maybe.insert(9) # Same as Just(9)
"""
from typing import Any, Callable, Generic, TypeVar

import pymonad.monad

S = TypeVar('S') # pylint: disable=invalid-name
T = TypeVar('T') # pylint: disable=invalid-name

class Maybe(pymonad.monad.Monad, Generic[T]):
    """ The Maybe monad class. """
    @classmethod
    def insert(cls, value: T) -> 'Maybe[T]':
        """ See Monad.insert """
        return cls(value, True)

    def amap(self: 'Maybe[Callable[[S], T]]', monad_value: 'Maybe[S]') -> 'Maybe[T]':
        """ See Monad.amap"""
        if self.is_nothing() or monad_value.is_nothing(): #pylint: disable=no-else-return
            return Nothing
        else:
            return monad_value.map(self.value)

    def bind(self: 'Maybe[S]', kleisli_function: 'Callable[[S], Maybe[T]]') -> 'Maybe[T]':
        """ See Monad.bind """
        if self.monoid is False: #pylint: disable=no-else-return
            return self
        else:
            try:
                return kleisli_function(self.value)
            except: # pylint: disable=bare-except
                return Nothing

    def is_just(self) -> bool:
        """ Returns True if the monad instance was created with the 'Just' function. """
        return self.monoid

    def is_nothing(self) -> bool:
        """ Returns True if the monad instance is the 'Nothing' value. """
        return not self.monoid

    def map(self: 'Maybe[S]', function: Callable[[S], T]) -> 'Maybe[T]':
        """ See Monad.map """
        if self.is_nothing(): #pylint: disable=no-else-return
            return self
        else:
            try:
                return self.__class__(function(self.value), True) # pytype: disable=not-callable
            except: # pylint: disable=bare-except
                return Nothing

    def __eq__(self, other):
        """ Checks equality of Maybe objects.

        Maybe objects are equal iff:
          1. They are both Nothing, or
          2. They are both Just and
            2a. They both contain the same value.
        """
        return self.value == other.value and self.monoid == other.monoid

    def __repr__(self):
        return f'Just {self.value}' if self.monoid else 'Nothing'

def Just(value: T) -> Maybe[T]: # pylint: disable=invalid-name
    """ A Maybe object representing the presence of an optional value. """
    return Maybe(value, True)

# A Maybe object representing the absence of an optional value.
Nothing: Maybe[Any] = Maybe(None, False) # pylint: disable=invalid-name







class Option(Maybe[T]): # MonadAlias must be the first parent class
    """ An alias for the Maybe monad class. """
    def __repr__(self):
        return f'Some {self.value}' if self.monoid else 'Nothing'

def Some(value: T) -> Option[T]: # pylint: disable=invalid-name
    """ An Option object representing the presence of an optional value. """
    return Option(value, True)
