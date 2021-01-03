# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Adds operators to the IO monad. """
from typing import Callable, TypeVar

import pymonad.monad
import pymonad.operators.operators
import pymonad.io

T = TypeVar('T') # pylint: disable=invalid-name

class _IO(pymonad.operators.operators.MonadOperators, pymonad.io._IO[T]): # pylint: disable=protected-access, abstract-method
    """ See pymonad.operators.operators and pymonad.io. """

def IO(io_function: Callable[[], T]) -> _IO[T]: # pylint: disable=invalid-name
    """ The IO monad constructor function.

    Returns:
      An instance of the IO monad.
    """
    return _IO(io_function, None)

IO.apply = _IO.apply
IO.insert = _IO.insert
