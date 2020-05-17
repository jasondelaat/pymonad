# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import pymonad.tools
from pymonad.maybe import Maybe, Just, Nothing

curry = pymonad.tools.curry
compose = pymonad.tools.kleisli_compose

def add(x): return Just(x + 1)
def mul(x): return Just(x * 2)
def sub(x): return Just(x - 3)

@curry(2)
def div(y, x):
    return Nothing if y is 0 else Just(x / y)

class MonadLaws(unittest.TestCase):
    def setUp(self):
        self.input_value = 1

    def test_LeftIdentity_Just(self):
        result1 = add(self.input_value)
        result2 = compose(Maybe.insert, add)(self.input_value)
        self.assertEqual(result1, result2)

    def test_RightIdentity_Just(self):
        result1 = add(self.input_value)
        result2 = compose(add, Maybe.insert)(self.input_value)
        self.assertEqual(result1, result2)

    def test_Associativity_Just(self):
        result1 = compose(compose(add, mul), sub)(self.input_value)
        result2 = compose(add, compose(mul, sub))(self.input_value)
        self.assertEqual(result1, result2)

    def test_LeftIdentity_Nothing(self):
        result1 = div(0, self.input_value)
        result2 = compose(Maybe.insert, div(0))(self.input_value)
        self.assertEqual(result1, result2)

    def test_Rightdentity_Nothing(self):
        result1 = div(0, self.input_value)
        result2 = compose(div(0), Maybe.insert)(self.input_value)
        self.assertEqual(result1, result2)

    def test_Associativity_Nothing(self):
        result1 = compose(compose(add, div(0)), sub)(self.input_value)
        result2 = compose(add, compose(div(0), sub))(self.input_value)
        self.assertEqual(result1, result2)

