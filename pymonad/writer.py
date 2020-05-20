# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

import pymonad

class Writer(pymonad.monad.Monad):
    @classmethod
    def insert(cls, value):
        return Writer(value, '')

    def bind(self, kleisli_function):
        result = kleisli_function(self.value)
        return Writer(result.value, self.monoid + result.monoid)

    def map(self, function):
        return Writer(function(self.value), self.monoid)

    def __eq__(self, other):
        return self.value == other.value and self.monoid == other.monoid

    def __repr__(self):
        return f'({self.value}, {self.monoid})'
