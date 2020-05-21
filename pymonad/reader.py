# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Implements the Reader monad.

The Reader monad creates a context in which functions have access to
an additional read-only input.
"""

import pymonad.monad
import pymonad.tools

@pymonad.tools.curry(3)
def _bind_or_map(function_f, function_g, read_only):
    try:
        return _bind(function_f, function_g, read_only)
    except TypeError:
        return _map(function_f, function_g, read_only)

@pymonad.tools.curry(3)
def _bind(function_f, function_g, read_only):
    return function_f(function_g(read_only))(read_only)

@pymonad.tools.curry(3)
def _map(function_f, function_g, read_only):
    return function_f(function_g(read_only))

class _Reader(pymonad.monad.Monad):
    @classmethod
    def insert(cls, value):
        return Reader(lambda r: value)

    def amap(self, monad_value):
        return Reader(lambda r: self(r)(monad_value(r)))

    def bind(self, kleisli_function):
        return Reader(_bind(kleisli_function, self)) # pylint: disable=no-value-for-parameter

    def map(self, function):
        return Reader(_map(function, self)) # pylint: disable=no-value-for-parameter

    def then(self, function):
        return Reader(_bind_or_map(function, self)) # pylint: disable=no-value-for-parameter

    def __call__(self, arg):
        return self.value(arg)

def Reader(function): # pylint: disable=invalid-name
    """ Creates an instance of the Reader monad.

    Args:
      function: a function which takes the read-only data as input and
        returns any appropriate type.

    Result:
      An instance of the Reader monad.
    """
    return _Reader(function, None)

Reader.insert = _Reader.insert
Reader.apply = _Reader.apply
