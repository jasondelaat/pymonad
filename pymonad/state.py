# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import pymonad

class _State(pymonad.monad.Monad):
    @classmethod
    def insert(cls, value):
        return State(lambda s: (value, s))

    def amap(self, monad_value):
        return State(lambda s:
                     (self.value(s)(monad_value.value(s)),
                      monad_value.monoid(s)))

    def bind(self, kleisli_function):
        return State(lambda s: kleisli_function(self.value(s)).run(self.monoid(s)))

    def map(self, function):
        return State(lambda s: (function(self.value(s)), self.monoid(s)))

    def run(self, input_state):
        return self.value(input_state), self.monoid(input_state)

def State(state_function): # pylint: disable=invalid-name
    return _State(lambda s: state_function(s)[0], lambda s: state_function(s)[1])

State.insert = _State.insert
State.apply = _State.apply
