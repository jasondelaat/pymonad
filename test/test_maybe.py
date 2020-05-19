# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import pymonad.tools
from pymonad.maybe import Maybe, Just, Nothing
from pymonad.maybe import Option, Some

curry = pymonad.tools.curry
k_compose = pymonad.tools.kleisli_compose

def compose(f, g):
    return lambda x: g(f(x))

def add(x): return Just(x + 1)
def mul(x): return Just(x * 2)
def sub(x): return Just(x - 3)
def identity(x): return x

def inc(x): return x + 1

@curry(2)
def div(y, x):
    return Nothing if y is 0 else Just(x / y)

@curry(2)
def plus(x, y):
    return x + y

@curry(2)
def minus(x, y):
    return x - y

def error(x):
    raise TypeError

class FunctorLaws(unittest.TestCase):
    def setUp(self):
        self.input_value = 1

    def test_LeftIdentity(self):
        result1 = compose(identity, Maybe.insert)(self.input_value)
        result2 = Maybe.insert(self.input_value)
        self.assertEqual(result1, result2)

    def test_RightIdentity(self):
        result1 = Maybe.insert(self.input_value)
        result2 = compose(Maybe.insert, identity)(self.input_value)
        self.assertEqual(result1, result2)

    def test_Mapping(self):
        result1 = Maybe.insert(self.input_value).map(str)
        result2 = Maybe.insert(str(self.input_value))
        self.assertEqual(result1, result2)

    def test_Composability(self):
        f_inc = lambda a: Maybe.insert(a).map(inc)
        f_str = lambda a: Maybe.insert(a).map(str)
        result1 = Maybe.insert(compose(inc, str)(self.input_value))
        result2 = k_compose(f_inc, f_str)(self.input_value)
        self.assertEqual(result1, result2)

class ApplicativeLaws(unittest.TestCase):
    def test_ApplyMap_MapApply(self):
        result1 = Maybe.insert(inc(1))
        result2 = Maybe.insert(inc).amap(Maybe.insert(1))
        self.assertEqual(result1, result2)

    def test_Associativity(self):
        result1 = Maybe.insert(plus).amap(Maybe.insert(1)).amap(Maybe.insert(2))
        result2 = (Maybe.insert(lambda args: plus(args[0], args[1]))
                   .amap(Maybe.insert(lambda b: (1, b))
                         .amap(Maybe.insert(2)))
                   )
        self.assertEqual(result1, result2)

    def test_Map_vs_Amap(self):
        result1 = Maybe.insert(inc).amap(Maybe.insert(1))
        result2 = Maybe.insert(1).map(inc)
        self.assertEqual(result1, result2)

    def test_AllPathsCommute(self):
        result1 = Maybe.insert(plus(1, 2))
        result2 = Maybe.insert(plus(1)).amap(Maybe.insert(2))
        result3 = Maybe.insert(plus).amap(Maybe.insert(1)).amap(Maybe.insert(2))
        self.assertEqual(result1, result2)
        self.assertEqual(result3, result2)
    
class MonadLaws(unittest.TestCase):
    def setUp(self):
        self.input_value = 1

    def test_LeftIdentity_Just(self):
        result1 = add(self.input_value)
        result2 = k_compose(Maybe.insert, add)(self.input_value)
        self.assertEqual(result1, result2)

    def test_RightIdentity_Just(self):
        result1 = add(self.input_value)
        result2 = k_compose(add, Maybe.insert)(self.input_value)
        self.assertEqual(result1, result2)

    def test_Associativity_Just(self):
        result1 = k_compose(k_compose(add, mul), sub)(self.input_value)
        result2 = k_compose(add, k_compose(mul, sub))(self.input_value)
        self.assertEqual(result1, result2)

    def test_LeftIdentity_Nothing(self):
        result1 = div(0, self.input_value)
        result2 = k_compose(Maybe.insert, div(0))(self.input_value)
        self.assertEqual(result1, result2)

    def test_Rightdentity_Nothing(self):
        result1 = div(0, self.input_value)
        result2 = k_compose(div(0), Maybe.insert)(self.input_value)
        self.assertEqual(result1, result2)

    def test_Associativity_Nothing(self):
        result1 = k_compose(k_compose(add, div(0)), sub)(self.input_value)
        result2 = k_compose(add, k_compose(div(0), sub))(self.input_value)
        self.assertEqual(result1, result2)

class MiscTests(unittest.TestCase):
    def test_repr_Just(self):
        self.assertEqual(str(Just(9)), 'Just 9')

    def test_repr_OptionAlias(self):
        self.assertEqual(str(Some(9)), 'Some 9')

    def test_OptionWithMaybeFunction_bind(self):
        result = Option.insert(1).then(add)
        self.assertEqual(result, Some(2))
        self.assertEqual(str(result), 'Some 2')

    def test_OptionWithMaybeFunction_map(self):
        result = Option.insert(1).then(plus(1))
        self.assertEqual(result, Some(2))
        self.assertEqual(str(result), 'Some 2')

    def test_OptionWithMaybeFunction_amap(self):
        result = Option.apply(plus).to_arguments(Some(1), Some(2))
        self.assertEqual(result, Some(3))
        self.assertEqual(str(result), 'Some 3')

    def test_repr_Nothing(self):
        self.assertEqual(str(Nothing), 'Nothing')

    def test_MappingFunctionThatRaisesErrors(self):
        self.assertEqual(Nothing, Just(0).map(error))

    def test_AmappingFunctionThatRaisesErrors(self):
        self.assertEqual(Nothing, Just(error).amap(Just(0)))

    def test_BindingFunctionThatRaisesErrors(self):
        self.assertEqual(Nothing, Just(0).bind(error))

    def test_CallingThenWithBareFunction(self):
        self.assertEqual(Just(1), Maybe.insert(0).then(inc))

    def test_CallingThenWithMonadFunction(self):
        self.assertEqual(Just(1), Maybe.insert(0).then(add))

    def test_CallingThenWithErrorFunction(self):
        self.assertEqual(Nothing, Just(0).then(error))

    def test_ApplySyntax(self):
        self.assertEqual(Just(9), Maybe.apply(plus).to_arguments(Just(4), Just(5)))

    def test_ApplyWithErrors(self):
        self.assertEqual(Nothing, Maybe.apply(error).to_arguments(Just(0)))

        
        
