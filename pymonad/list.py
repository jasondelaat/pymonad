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
import pymonad.monad

class _List(pymonad.monad.Monad):
    @classmethod
    def insert(cls, value):
        return ListMonad(value)

    def bind(self, kleisli_function):
        return self.map(kleisli_function).join()

    def map(self, function):
        return ListMonad(*[function(x) for x in self])

    def join(self):
        """ Flattens a nested ListMonad instance one level. """
        return ListMonad(*[element for lists in self for element in lists])

    def then(self, function):
        try:
            return self.bind(function)
        except TypeError:
            return self.map(function)

    def __eq__(self, other):
        return list(self) == list(other)

    def __iter__(self):
        yield self.value
        yield from self.monoid

    def __repr__(self):
        return str(list(self))

def ListMonad(*elements): # pylint: disable=invalid-name
    """ Creates an instance of the List monad.

    Args:
      *elements: any number of elements to be inserted into the list

    Returns:
      An instance of the List monad.
    """
    def _list_internal():
        yield from elements[1:]

    return _List(elements[0], _list_internal())

ListMonad.insert = _List.insert
ListMonad.apply = _List.apply
