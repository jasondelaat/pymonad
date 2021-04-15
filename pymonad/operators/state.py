# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Adds operators to the State monad. """
from typing import TypeVar

import pymonad.monad
import pymonad.operators.operators
import pymonad.state

S = TypeVar('S') # pylint: disable=invalid-name
T = TypeVar('T') # pylint: disable=invalid-name

class State(pymonad.operators.operators.MonadOperators, pymonad.state.State[S, T]): # pylint: disable=protected-access, abstract-method
    """ See pymonad.operators.operators and pymonad.state. """
