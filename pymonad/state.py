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
def _amap(monad_function, monad_value, state):
    function, new_state = monad_function.run(state)
    value, final_state = monad_value.run(new_state)
    return function(value), final_state

@pymonad.tools.curry(3)
def _bind(monad_value, kleisli_function, state):
    value, new_state = monad_value.run(state)
    return kleisli_function(value).run(new_state)

@pymonad.tools.curry(3)
def _bind_or_map(monad_value, function, state):
    value, new_state = monad_value.run(state)
    result = function(value)
    try:
        return result.run(new_state)
    except (TypeError, AttributeError):
        return result, new_state

@pymonad.tools.curry(3)
def _map(monad_value, function, state):
    value, new_state = monad_value.run(state)
    return function(value), new_state

class State(pymonad.monad.Monad, Generic[S, A]):
    """The State monad.

     Args:
       state_function: a function with type state -> (Any, state)
                       where 'state' can actually also be any type but
                       should remain consistent throughout a given
                       computation.

     Returns:
       An instance of the State monad.

    """
    def __init__(self, state_function, _=None):
        super().__init__(state_function, None)

    @classmethod
    def insert(cls, value: A) -> 'State[Any, A]':
        """ See Monad.insert. """
        return cls(lambda s: (value, s))

    def amap(self: 'State[S, Callable[[A], B]]', monad_value: 'State[S, A]') -> 'State[S, B]':
        """ See Monad.amap. """
        state_function = _amap(self, monad_value) # pylint: disable=no-value-for-parameter
        return self.__class__(state_function)

    def bind(
            self: 'State[S, A]', kleisli_function: Callable[[A], 'State[S, B]']
    ) -> 'State[S, B]':
        """ See Monad.bind. """
        state_function = _bind(self, kleisli_function) # pylint: disable=no-value-for-parameter
        return self.__class__(state_function)

    def map(self: 'State[S, A]', function: Callable[[A], B]) -> 'State[S, B]':
        """ See Monad.map. """
        state_function = _map(self, function) # pylint: disable=no-value-for-parameter
        return self.__class__(state_function) # pylint: disable=not-callable

    def run(self: 'State[S, A]', input_state: S) -> Tuple[A, S]:
        """ Gives the state calculation an initial state and computes the result.

        Args:
          input_state: the initial state for the stateful calculation

        Result:
          A tuple containing the result of the stateful calculation
          and the final state.
        """
        return self.value(input_state)

    def then(
            self: 'State[S, A]', function: Union[Callable[[A], B], Callable[[A], 'State[S, B]']]
    ) -> 'State[S, B]':
        return State(_bind_or_map(self, function)) # pylint: disable=no-value-for-parameter
