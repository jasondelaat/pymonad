# --------------------------------------------------------
# (c) Copyright 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Implements a monadic wrapper type for impure procedures. """

from typing import Any, Callable, Generic, Tuple, TypeVar, Union # pylint: disable=unused-import

import pymonad.monad

A = TypeVar('A') # pylint: disable=invalid-name
B = TypeVar('B') # pylint: disable=invalid-name

def _bind_or_map(monad_value, function):
    def _internal():
        result = function(monad_value.run())
        try:
            return result.run()
        except AttributeError:
            return result
    return _internal

class _IO(pymonad.monad.Monad, Generic[A]):
    @classmethod
    def insert(cls, value: A) -> '_IO[A]':
        """ See Monad.insert. """
        return cls(lambda: value, None)

    def amap(self: '_IO[Callable[[A], B]]', monad_value: '_IO[A]') -> '_IO[B]':
        """ See Monad.amap. """
        return self.__class__(lambda: self.run()(monad_value.run()), None)

    def bind(self: '_IO[A]', kleisli_function: Callable[[A], '_IO[B]']) -> '_IO[B]':
        """ See Monad.bind. """
        return self.__class__(lambda: kleisli_function(self.run()).run(), None)

    def map(self: '_IO[A]', function: Callable[[A], B]) -> '_IO[B]':
        """ See Monad.map. """
        return self.__class__(lambda: function(self.run()), None)

    def run(self: '_IO[A]') -> A:
        """ Executes the contained impure proceedure.

        Result:
          Can return any type.
        """
        return self.value()

    def then(
            self: '_IO[A]', function: Union[Callable[[A], B], Callable[[A], '_IO[B]']]
    ) -> '_IO[B]':
        """ See Monad.then. """
        return self.__class__(_bind_or_map(self, function), None)

def IO(function: Callable[[], A]) -> _IO[A]: # pylint: disable=invalid-name
    """ The IO Monad constructor function.

    Args:
      function - a arity-0 function which can perform any actions,
      including impure actions, and return any result or None.

    Result:
      An instance of the IO monad.
    """
    return _IO(function, None)

IO.apply = _IO.apply
IO.insert = _IO.insert
