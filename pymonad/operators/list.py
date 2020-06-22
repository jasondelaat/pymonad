# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Adds operators to the List monad. """
from typing import List, TypeVar

import pymonad.list
import pymonad.monad
import pymonad.operators.operators

T = TypeVar('T') # pylint: disable=invalid-name

class _List(pymonad.operators.operators.MonadOperators, pymonad.list._List[T]): # pylint: disable=protected-access, too-many-ancestors, abstract-method
    """ See pymonad.operators.operators and pymonad.list. """

def ListMonad(*elements: List[T]) -> _List[T]: # pylint: disable=invalid-name
    """ Creates an instance of the List monad.

    Args:
      *elements: any number of elements to be inserted into the list

    Returns:
      An instance of the List monad.
    """

    return _List(list(elements), None)

ListMonad.apply = _List.apply
ListMonad.insert = _List.insert
