# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Implements the Reader monad.

The Reader monad creates a context in which functions have access to
an additional read-only input.
"""
from typing import Any, Callable, Generic, TypeVar, Union

import pymonad.monad
import pymonad.tools

R = TypeVar('R') # pylint: disable=invalid-name
S = TypeVar('S') # pylint: disable=invalid-name
T = TypeVar('T') # pylint: disable=invalid-name

@pymonad.tools.curry(3)
def _bind(function_f, function_g, read_only):
    return function_f(function_g(read_only))(read_only)

@pymonad.tools.curry(3)
def _bind_or_map(function_f, function_g, read_only):
    return_value = _map(function_f, function_g, read_only)
    try:
        return return_value(read_only)
    except (TypeError, AttributeError):
        return return_value

@pymonad.tools.curry(3)
def _map(function_f, function_g, read_only):
    return function_f(function_g(read_only))

class _Reader(pymonad.monad.Monad, Generic[R, T]):
    @classmethod
    def insert(cls, value):
        return cls(lambda r: value, None)

    def amap(self: '_Reader[R, Callable[[S], T]]', monad_value: '_Reader[R, S]') -> '_Reader[R, T]':
        return self.__class__(lambda r: self(r)(monad_value(r)), None)

    def bind(
            self: '_Reader[R, S]', kleisli_function: Callable[[S], '_Reader[R, T]']
    ) -> '_Reader[R, T]':
        return self.__class__(_bind(kleisli_function, self), None) # pylint: disable=no-value-for-parameter

    def map(self: '_Reader[R, S]', function: Callable[[S], T]) -> '_Reader[R, T]':
        return self.__class__(_map(function, self), None) # pylint: disable=no-value-for-parameter

    def then(
            self: '_Reader[R, S]', function: Union[Callable[[S], T], Callable[[S], '_Reader[R, T]']]
    ) -> '_Reader[R, T]':
        return self.__class__(_bind_or_map(function, self), None) # pylint: disable=no-value-for-parameter

    def __call__(self, arg: R) -> T:
        return self.value(arg)

def Reader(function: Callable[[R], T]) -> _Reader[R, T]: # pylint: disable=invalid-name
    """ Creates an instance of the Reader monad.

    Args:
      function: a function which takes the read-only data as input and
        returns any appropriate type.

    Result:
      An instance of the Reader monad.
    """
    return _Reader(function, None)

Reader.apply = _Reader.apply
Reader.insert = _Reader.insert





def Compose(function: Callable[[R], T]) -> _Reader[R, T]: # pylint: disable=invalid-name
    """ Creates an instance of the Compose monad.

    Compose is basically an alias for the Reader monad except with the
    insert and apply methods removed. It's purpose is simply to
    provide a semantically meaningful monad instance to be used
    specifically for the purpose of function composition.

      Example:
        def inc(x): return x + 1
        def dec(x): return x - 1

        convoluted_inc_twice = (Compose(inc)
                                .then(inc)
                                .then(inc)
                                .then(dec))

        convoluted_inc_twice(0) # Result: 2

    Technically, 'convoluted_inc_twice' is an instance of the Reader
    monad but since Reader defines the __call__ method, we can treat
    it just like a function for all intents and purposes. The Compose
    monad composes functions forward. In the example, the three 'inc'
    operations happen first and then the 'dec' and not vice-versa.
    """
    return _Reader(function, None)






class _Pipe(_Reader, Generic[R, T]):
    def flush(self):
        """ Calls the composed Pipe function returning  the embedded result.

        The 'flush' method calls the composed function with dummy
        input since all functions in a Pipe chain should ignore that
        input anyway, simply joining inputs to outputs.
        """
        return self(None)

    def __pos__(self):
        return self.flush()

def Pipe(value: T) -> _Pipe[Any, T]: # pylint: disable=invalid-name
    """ Creates an instance of the Pipe monad.

    Pipe is basically an alias for the Reader monad except with the
    insert and apply methods removed. It's purpose is simply to
    provide a semantically meaningful monad instance to be used
    specifically for the purpose of chaining function calls by taking
    the output of one function as the input to the next.

    Since Pipe is a subclass of Reader it's really building a function
    but, semantically, pipes start with some input and end with a
    result. For this reason, Pipe adds a 'flush' method which calls
    the composed function with dummy input (which will be ignored) and
    simply returns the embedded result. Optionally, you can instead
    use the unary '+' operator instead of 'flush' to do the same
    thing.

      Example:
        def inc(x): return x + 1

        pipe_with_flush = (Pipe(0)
                          .then(inc)
                          .then(inc)
                          .flush())

        pipe_with_plus = +(Pipe(0)
                           .then(inc)
                           .then(inc))

        pipe_with_flush == pipe_with_plus # True
    """
    return _Pipe.insert(value)
