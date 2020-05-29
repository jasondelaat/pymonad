# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Adds operators to the Either monad. """
import pymonad.monad
import pymonad.either
import pymonad.operators.operators

class Either(pymonad.operators.operators.MonadOperators, pymonad.either.Either):
    """ See pymonad.operators.operators and pymonad.either. """

def Right(value): # pylint: disable=invalid-name
    """ Creates a value of the second possible type in the Either monad. """
    return Either(value, (None, True))

def Left(value): # pylint: disable=invalid-name
    """ Creates a value of the first possible type in the Either monad. """
    return Either(None, (value, False))







class _Error(Either): # MonadAlias already in MRO from MonadOperators
    def __repr__(self):
        return f'Result: {self.value}' if self.is_right() else f'Error: {self.monoid[0]}'

def Result(value): # pylint: disable=invalid-name
    """ Creates a value representing the successful result of a calculation. """
    return _Error(value, (None, True))

def Error(value): # pylint: disable=invalid-name
    """ Creates an error value as the result of a calculation. """
    return _Error(None, (value, False))

Error.insert = _Error.insert
