# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Implements the Either monad and related functions.

The Either type represents values that can either type A or type B -
for any types A and B - but not both at the same time. As a function
input type, Either values can be used to define functions which can
sensibly deal with multiple types of input; of course in python we
don't need a special way to deal with multiple input types.

Perhaps more usefully, as an output type, Either values can be used to
signal that a function may cause an error: Either we get back a useful
result or we get back an error message.

When creating Either values directly use the 'Right' or 'Left'
functions:

  Example:
    x = Right(19)                     # Represents a result value
    y = Left('Something went wrong.') # Represents an error value

The 'insert' class method is a wrapper around the 'Right' function.

  Example:
    x = Either.insert(9) # Same as Right(9)
"""
from typing import Any, Callable, Generic, TypeVar

import pymonad.monad

M = TypeVar('M') # pylint: disable=invalid-name
S = TypeVar('S') # pylint: disable=invalid-name
T = TypeVar('T') # pylint: disable=invalid-name

class Either(pymonad.monad.Monad, Generic[M, T]):
    """ The Either monad class. """
    @classmethod
    def insert(cls, value: T) -> 'Either[Any, T]':
        """ See Monad.insert """
        return cls(value, (None, True))

    def amap(self: 'Either[M, Callable[[S], T]]', monad_value: 'Either[M, S]') -> 'Either[M, T]':
        if self.is_left(): # pylint: disable=no-else-return
            return self
        elif monad_value.is_left(): # pylint: disable=no-else-return
            return monad_value
        else:
            return self.__class__(self.value(monad_value.value), (None, True))

    def bind(
            self: 'Either[M, S]', kleisli_function: Callable[[S], 'Either[M, T]']
    ) -> 'Either[M, T]':
        """ See Monad.bind """
        if self.is_left(): # pylint: disable=no-else-return
            return self
        else:
            return kleisli_function(self.value)

    def either(
            self: 'Either[M, S]', left_function: Callable[[M], T], right_function: Callable[[S], T]
    ) -> T:
        """Extracts a bare value from an Either object.

        'either' takes two functions. If the Either object is a 'Left'
        then the first (left) function is called with the Left value
        as its argument.  Otherwise the second (right) function is
        called with the Right value as its argument.

        Example:
          e = (Either.insert(1)
               .then(add(7))
               .then(div(0))  # Returns a Left with a ZeroDivisionError
               .then(mul(5))
               .either(lambda e: 0, lambda x: x) # ignore the error and return 0
               ) # 'e' takes the value 0

        Args:
          left_function: a function from M to T where M is the type
            contained by Left values.
          right_function: a function from S to T where S is the type
            contained in by Right values.

        Result:
          A bare (non-monadic) value of type T.
        """
        if self.monoid[1]: # pylint: disable=no-else-return
            return right_function(self.value)
        else:
            return left_function(self.monoid[0])

    def is_left(self) -> bool:
        """ Returns True if this Either instance was created with the 'Left' function. """
        return not self.monoid[1]

    def is_right(self) -> bool:
        """ Returns True if this Either instance was created with the 'Right' function. """
        return self.monoid[1]

    def map(self: 'Either[M, S]', function: Callable[[S], T]) -> 'Either[M, T]':
        """ See Monad.map """
        if self.is_left(): # pylint: disable=no-else-return
            return self
        else:
            return self.__class__(function(self.value), (None, True))

    def __eq__(self, other):
        """ Checks equality of Maybe objects.

        Maybe objects are equal iff:
          1. They are both Nothing, or
          2. They are both Just and
            2a. They both contain the same value.
        """
        return self.value == other.value and self.monoid == other.monoid

    def __repr__(self):
        return f'Right {self.value}' if self.is_right() else f'Left {self.monoid[0]}'

def Left(value: M) -> Either[M, Any]: # pylint: disable=invalid-name
    """ Creates a value of the first possible type in the Either monad. """
    return Either(None, (value, False))

def Right(value: T) -> Either[Any, T]: # pylint: disable=invalid-name
    """ Creates a value of the second possible type in the Either monad. """
    return Either(value, (None, True))






class _Error(Either[M, T]):
    def __repr__(self):
        return f'Result: {self.value}' if self.is_right() else f'Error: {self.monoid[0]}'

def Error(value: M) -> _Error[M, Any]: # pylint: disable=invalid-name
    """ Creates an error value as the result of a calculation. """
    return _Error(None, (value, False))

def Result(value: T) -> _Error[Any, T]: # pylint: disable=invalid-name
    """ Creates a value representing the successful result of a calculation. """
    return _Error(value, (None, True))

Error.apply = _Error.apply
Error.insert = _Error.insert
