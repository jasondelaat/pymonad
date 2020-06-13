# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Implements the State monad. """

from typing import Any, Callable, Generic, Tuple, TypeVar, Union # pylint: disable=unused-import

import pymonad.monad
import pymonad.tools

A = TypeVar('A') # pylint: disable=invalid-name
B = TypeVar('B') # pylint: disable=invalid-name
S = TypeVar('S') # pylint: disable=invalid-name

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

class _State(pymonad.monad.Monad, Generic[S, A]):
    @classmethod
    def insert(cls, value: A) -> '_State[Any, A]':
        """ See Monad.insert. """
        return State(lambda s: (value, s))

    def amap(self: '_State[S, Callable[[A], B]]', monad_value: '_State[S, A]') -> '_State[S, B]':
        """ See Monad.amap. """
        return State(lambda s:
                     (self.value(s)(monad_value.value(s)),
                      monad_value.monoid(s)))

    def bind(
            self: '_State[S, A]', kleisli_function: Callable[[A], '_State[S, B]']
    ) -> '_State[S, B]':
        """ See Monad.bind. """
        return State(_bind(self, kleisli_function)) # pylint: disable=no-value-for-parameter

    def map(self: '_State[S, A]', function: Callable[[A], B]) -> '_State[S, B]':
        """ See Monad.map. """
        return State(_map(self, function)) # pylint: disable=no-value-for-parameter

    def run(self: '_State[S, A]', input_state: S) -> Tuple[A, S]:
        """ Gives the state calculation an initial state and computes the result.

        Args:
          input_state: the initial state for the stateful calculation

        Result:
          A tuple containing the result of the stateful calculation
          and the final state.
        """
        return self.value(input_state), self.monoid(input_state)

    def then(
            self: '_State[S, A]', function: Union[Callable[[A], B], Callable[[A], '_State[S, B]']]
    ) -> '_State[S, B]':
        return State(_bind_or_map(self, function)) # pylint: disable=no-value-for-parameter

def State(state_function: Callable[[S], A]) -> _State[S, A]: # pylint: disable=invalid-name
    """ The State monad constructor function.

    Args:
      state_function: a function with type State -> (Any, State)

    Returns:
      An instance of the State monad.
    """
    return _State(lambda s: state_function(s)[0], lambda s: state_function(s)[1])

State.apply = _State.apply
State.insert = _State.insert
