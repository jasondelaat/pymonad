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


async def inc(value):
    return await Promise(lambda resolve, reject: resolve(value + 1))

async def dec(value):
    return await Promise(lambda resolve, reject: resolve(value - 1))

async def dbl(value):
    return await Promise(lambda resolve, reject: resolve(2 * value))

def k_compose(f, g):
    async def _compose_internal(a):
        v = await f(a)
        return await g(v)
    return _compose_internal
    
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
            _run(k_compose(k_compose(inc, dec), dbl)(0)),
            _run(k_compose(inc, k_compose(dec, dbl))(0))
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
