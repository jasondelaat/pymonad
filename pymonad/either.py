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

import pymonad.monad

class Either(pymonad.monad.Monad):
    """ The Either monad class. """
    @classmethod
    def insert(cls, value):
        """ See Monad.insert """
        return Right(value)

    def amap(self, monad_value):
        if self.is_left(): # pylint: disable=no-else-return
            return self
        elif monad_value.is_left(): # pylint: disable=no-else-return
            return monad_value
        else:
            return Right(self.value(monad_value.value))

    def bind(self, kleisli_function):
        """ See Monad.bind """
        if self.is_left(): # pylint: disable=no-else-return
            return self
        else:
            try:
                return kleisli_function(self.value)
            except Exception as e: # pylint: disable=invalid-name, broad-except
                return Left(e)

    def is_left(self):
        """ Returns True if this Either instance was created with the 'Left' function. """
        return not self.monoid[1]

    def is_right(self):
        """ Returns True if this Either instance was created with the 'Right' function. """
        return self.monoid[1]

    def map(self, function):
        """ See Monad.map """
        if self.is_left(): # pylint: disable=no-else-return
            return self
        else:
            try:
                return Right(function(self.value))
            except Exception as e: # pylint: disable=invalid-name, broad-except
                return Left(e)

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

def Left(value): # pylint: disable=invalid-name
    """ Creates a value of the first possible type in the Either monad. """
    return Either(None, (value, False))

def Right(value): # pylint: disable=invalid-name
    """ Creates a value of the second possible type in the Either monad. """
    return Either(value, (None, True))






class _Error(pymonad.monad.MonadAlias, Either):
    def __repr__(self):
        return f'Result: {self.value}' if self.is_right() else f'Error: {self.monoid[0]}'

def Error(value): # pylint: disable=invalid-name
    """ Creates an error value as the result of a calculation. """
    return _Error(None, (value, False))

def Result(value): # pylint: disable=invalid-name
    """ Creates a value representing the successful result of a calculation. """
    return _Error(value, (None, True))

Error.insert = _Error.insert
