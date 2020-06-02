# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Implements the State monad. """

import pymonad.monad
import pymonad.tools

@pymonad.tools.curry(3)
def _bind(monad_value, kleisli_function, state):
    return kleisli_function(monad_value.value(state)).run(monad_value.monoid(state))

@pymonad.tools.curry(3)
def _bind_or_map(monad_value, function, state):
    try:
        return _bind(monad_value, function, state)
    except AttributeError:
        return _map(monad_value, function, state)

@pymonad.tools.curry(3)
def _map(monad_value, function, state):
    return (function(monad_value.value(state)), monad_value.monoid(state))

class _State(pymonad.monad.Monad):
    @classmethod
    def insert(cls, value):
        """ See Monad.insert. """
        return State(lambda s: (value, s))

    def amap(self, monad_value):
        """ See Monad.amap. """
        return State(lambda s:
                     (self.value(s)(monad_value.value(s)),
                      monad_value.monoid(s)))

    def bind(self, kleisli_function):
        """ See Monad.bind. """
        return State(_bind(self, kleisli_function)) # pylint: disable=no-value-for-parameter

    def map(self, function):
        """ See Monad.map. """
        return State(_map(self, function)) # pylint: disable=no-value-for-parameter

    def run(self, input_state):
        """ Gives the state calculation an initial state and computes the result.

        Args:
          input_state: the initial state for the stateful calculation

        Result:
          A tuple containing the result of the stateful calculation
          and the final state.
        """
        return self.value(input_state), self.monoid(input_state)

    def then(self, function):
        return State(_bind_or_map(self, function)) # pylint: disable=no-value-for-parameter

def State(state_function): # pylint: disable=invalid-name
    """ The State monad constructor function.

    Args:
      state_function: a function with type State -> (Any, State)

    Returns:
      An instance of the State monad.
    """
    return _State(lambda s: state_function(s)[0], lambda s: state_function(s)[1])

State.apply = _State.apply
State.insert = _State.insert
