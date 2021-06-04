# --------------------------------------------------------
# (c) Copyright 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest
import asyncio

import common_tests
import pymonad.monad
from pymonad.promise import Promise, _Promise

def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

class PromiseTests(unittest.TestCase):
    def test_insert(self):
        self.assertEqual(_run(Promise.insert(0)), 0)

    def test_catch(self):
        p = _run(Promise(lambda resolve, reject: reject(IndexError())).catch(lambda error: 0))
        self.assertEqual(p, 0)

class PromiseFunctorTests(unittest.TestCase):
    def setUp(self):
        self._class = _Promise

    def test_left_identity(self):
        self.assertEqual(
            _run(self._class.insert(common_tests.id(1))),
            _run(self._class.insert(1))
        )

    def test_rightidentity(self):
        self.assertEqual(
            _run(common_tests.id(self._class.insert(1))),
            _run(self._class.insert(1))
        )

    def test_apply_then_insert(self):
        self.assertEqual(
            _run(self._class.insert(1).map(common_tests.add(1))),
            _run(self._class.insert(common_tests.add(1, 1)))
        )

    def test_composition(self):
        self.assertEqual(
            _run(self._class.insert(1).map(lambda x: common_tests.sub(2, common_tests.add(1, x)))),
            _run(self._class.insert(1).map(common_tests.add(1)).map(common_tests.sub(2)))
        )

class PromiseApplicativeTests(unittest.TestCase):
    def setUp(self):
        self._class = _Promise

    def test_application_is_homomorphic(self):
        f = common_tests.add(1)
        self.assertEqual(
            _run(self._class.insert(f(2))),
            _run(self._class.apply(f).to_arguments(self._class.insert(2)))
        )

    def test_application_is_same_as_mapping(self):
        f = common_tests.add(1)
        self.assertEqual(
            _run(self._class.apply(f).to_arguments(self._class.insert(2))),
            _run(self._class.insert(2).map(f))
        )

    def test_application_is_associative(self):
        self.assertEqual(
            _run(self._class.apply(common_tests.add).to_arguments(
                self._class.insert(1),
                self._class.insert(2))),
            _run(self._class.apply(lambda args: common_tests.add(*args)).to_arguments(
                self._class.apply(lambda b: (1, b)).to_arguments(self._class.insert(2))
            ))
        )


def inc(value):
    return Promise(lambda resolve, reject: resolve(value + 1))

def dec(value):
    return Promise(lambda resolve, reject: resolve(value - 1))

def dbl(value):
    return Promise(lambda resolve, reject: resolve(2 * value))

k_compose = pymonad.tools.kleisli_compose
    
class PromiseMonadTests(unittest.TestCase):
    def setUp(self):
        self._class = _Promise

    def test_left_identity(self):
        self.assertEqual(
            _run(k_compose(self._class.insert, inc)(0)),
            _run(inc(0))
        )

    def test_right_identity(self):
        self.assertEqual(
            _run(k_compose(inc, self._class.insert)(0)),
            _run(inc(0))
        )
    def test_associativity(self):
        self.assertEqual(
            _run(k_compose(k_compose(dbl, inc), dec)(1)),
            _run(k_compose(dbl, k_compose(inc, dec))(1))
        )

class PromiseThenTests(unittest.TestCase):
    def setUp(self):
        self._class = _Promise

    def test_then_with_normal_function(self):
        self.assertEqual(
            _run(self._class.insert(0).then(common_tests.add(1))),
            _run(self._class.insert(1))
        )

    def test_then_with_kleisli_function(self):
        self.assertEqual(
            _run(self._class.insert(0).then(inc)),
            _run(inc(0))
        )

from pymonad.tools import async_func

def my_func(x: int, y: int = 1, z: int = 1):
    return (x + 2 * y) / z

async_my_func = async_func(my_func)

class PromiseAlgebraFunctions(unittest.TestCase):

    def setUp(self):
        self._class = _Promise

    @staticmethod
    async def add_one(x: int):
        await asyncio.sleep((x % 10)/100)
        return x + 1

    def test_compose_promises(self):
        self.assertEqual(
            _run(async_my_func(
                self._class.insert(1).map(self.add_one), z=self._class.insert(2)
            ).map(self.add_one)), my_func(x=2, z=2) + 1
        )



