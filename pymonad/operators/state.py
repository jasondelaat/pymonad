# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Adds operators to the State monad. """
from typing import Callable, Tuple, TypeVar

import pymonad.monad
import pymonad.operators.operators
import pymonad.state

S = TypeVar('S') # pylint: disable=invalid-name
T = TypeVar('T') # pylint: disable=invalid-name

class _State(pymonad.operators.operators.MonadOperators, pymonad.state._State[S, T]): # pylint: disable=protected-access, abstract-method
    """ See pymonad.operators.operators and pymonad.state. """

def State(state_function: Callable[[S], Tuple[T, S]]) -> _State[S, T]: # pylint: disable=invalid-name
    """ The State monad constructor function.

    Args:
      state_function: a function with type State -> (Any, State)

    Returns:
      An instance of the State monad.
    """
    return _State(lambda s: state_function(s)[0], lambda s: state_function(s)[1])

State.apply = _State.apply
State.insert = _State.insert
