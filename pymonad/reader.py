# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import pymonad

class _Reader(pymonad.monad.Monad):
    @classmethod
    def insert(cls, value):
        return Reader(lambda r: value)

    def amap(self, monad_value):
        return Reader(lambda r: self(r)(monad_value(r)))

    def bind(self, kleisli_function):
        return Reader(lambda r: kleisli_function(self(r))(r)) #pylint: disable=unnecessary-lambda

    def map(self, function):
        return Reader(lambda r: function(self(r)))

    def __call__(self, arg):
        return self.value(arg)

def Reader(function): # pylint: disable=invalid-name
    return _Reader(function, None)

Reader.insert = _Reader.insert
Reader.apply = _Reader.apply
