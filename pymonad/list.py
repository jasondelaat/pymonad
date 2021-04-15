# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Implements the List monad.

The List monad is frequently used to represent calculations with
non-deterministic results, that is: functions which return more than
one (possible) result. For example, calculating how chess pieces might
move.

  Example:
    def knight_move(position):
        # calculates a list of every possible square a knight could move
        # to from it's current position
        return ListMonad(position_1, position_2, ..., position_N)

    # A list containing every square a knight could reach after 3 moves.
    three_moves = (List
                   .insert(initial_position) # However positions are defined.
                   .then(knight_move)
                   .then(knight_move)
                   .then(knight_move))
"""
from typing import Any, Callable, Generic, List, TypeVar, Union # pylint: disable=unused-import

import pymonad.monad
import pymonad.monoid

S = TypeVar('S') # pylint: disable=invalid-name
T = TypeVar('T') # pylint: disable=invalid-name

class _List(pymonad.monad.Monad, pymonad.monoid.Monoid, Generic[T]):
    @classmethod
    def insert(cls, value: T) -> '_List[T]':
        return cls([value], None)

    @staticmethod
    def identity_element() -> '_List[Any]':
        return ListMonad()

    def amap(self: '_List[Callable[[S], T]]', monad_value: '_List[S]') -> '_List[T]':
        result = []
        for function in self:
            for value in monad_value:
                result.append(function(value))
        return self.__class__(result, None)

    def bind(self: '_List[S]', kleisli_function: Callable[[S], '_List[T]']) -> '_List[T]':
        return self.map(kleisli_function).join()

    def join(self: '_List[_List[T]]') -> '_List[T]':
        """ Flattens a nested ListMonad instance one level. """
        return self.__class__( # pytype: disable=not-callable
            [element for lists in self for element in lists], None
        )

    def map(self: '_List[S]', function: Callable[[S], T]) -> '_List[T]':
        return self.__class__([function(x) for x in self], None)

    def then(
            self: '_List[S]', function: Union[Callable[[S], T], Callable[[S], '_List[T]']]
    ) -> '_List[T]':
        return_value = self.map(function)
        try:
            return return_value.join()
        except (TypeError, AttributeError):
            return return_value

    def addition_operation(self, other):
        if other is pymonad.monoid.IDENTITY: # pylint: disable=no-else-return
            return self
        else:
            return self.__class__((self.value + other.value), None)

    def __eq__(self, other):
        return self.value == other.value

    def __getitem__(self, index):
        result = self.value.__getitem__(index)
        try:
            if len(result) > 0:
                result_list = self.__class__(result, None)
            return result_list
        except TypeError:
            return result

    def __iter__(self):
        return iter(self.value)

    def __len__(self):
        return len(self.value)

    def __repr__(self):
        return str(self.value)

def ListMonad(*elements: List[T]) -> _List[T]: # pylint: disable=invalid-name
    """ Creates an instance of the List monad.

    Args:
      *elements: any number of elements to be inserted into the list

    Returns:
      An instance of the List monad.
    """

    return _List(list(elements), None)

ListMonad.insert = _List.insert
ListMonad.apply = _List.apply
ListMonad.identity_element = _List.identity_element
