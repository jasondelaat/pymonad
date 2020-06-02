# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Adds operators to the State monad. """
import pymonad.monad
import pymonad.operators.operators
import pymonad.state

class _State(pymonad.operators.operators.MonadOperators, pymonad.state._State): # pylint: disable=protected-access
    """ See pymonad.operators.operators and pymonad.state. """

def State(state_function): # pylint: disable=invalid-name
    """ The State monad constructor function.

    Args:
      state_function: a function with type State -> (Any, State)

    Returns:
      An instance of the State monad.
    """
    return _State(lambda s: state_function(s)[0], lambda s: state_function(s)[1])

State.insert = _State.insert
State.apply = _State.apply
