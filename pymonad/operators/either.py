# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Adds operators to the Either monad. """
from typing import Any, TypeVar

import pymonad.either
import pymonad.monad
import pymonad.operators.operators

S = TypeVar('S') # pylint: disable=invalid-name
T = TypeVar('T') # pylint: disable=invalid-name

class Either(pymonad.operators.operators.MonadOperators, pymonad.either.Either[S, T]): # pylint: disable=abstract-method
    """ See pymonad.operators.operators and pymonad.either. """

def Left(value: S) -> Either[S, Any]: # pylint: disable=invalid-name
    """ Creates a value of the first possible type in the Either monad. """
    return Either(None, (value, False))

def Right(value: T) -> Either[Any, T]: # pylint: disable=invalid-name
    """ Creates a value of the second possible type in the Either monad. """
    return Either(value, (None, True))







class _Error(Either[S, T]): # pylint: disable=too-many-ancestors, abstract-method
    def __repr__(self):
        return f'Result: {self.value}' if self.is_right() else f'Error: {self.monoid[0]}' # pylint: disable=no-member

def Error(value: S) -> _Error[S, Any]: # pylint: disable=invalid-name
    """ Creates an error value as the result of a calculation. """
    return _Error(None, (value, False))

def Result(value: T) -> _Error[Any, T]: # pylint: disable=invalid-name
    """ Creates a value representing the successful result of a calculation. """
    return _Error(value, (None, True))

Error.insert = _Error.insert
