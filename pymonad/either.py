# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Implements the Either monad and related functions.


When creating Either values directly use the 'Right' or 'Left'
functions:

  Example:
    x = Right(19)
    y = Left('A string')

The 'insert' class method is a wrapper around the 'Right' function.

  Example:
    x = Either.insert(9) # Same as Right(9)
"""

import pymonad.monad

class Either(pymonad.monad.Monad):
    @classmethod
    def insert(cls, value):
        return Right(value)

    def amap(self, monad_value):
        return monad_value.map(self.value)

    def bind(self, kleisli_function):
        if self.is_left():
            return self
        else:
            try:
                return kleisli_function(self.value)
            except Exception as e:
                return Left(e)

    def map(self, function):
        if self.is_left():
            return self
        else:
            try:
                return Right(function(self.value))
            except Exception as e:
                return Left(e)
    
    def is_right(self):
        return self.monoid[1]

    def is_left(self):
        return not self.monoid[1]


    def __eq__(self, other):
        return self.value == other.value and self.monoid == other.monoid

    def __repr__(self):
        return f'Right {self.value}' if self.is_right() else f'Left {self.monoid[0]}'

def Right(value): # pylint: disable=invalid-name
    return Either(value, (None, True))

def Left(value): # pylint: disable=invalid-name
    return Either(None, (value, False))
