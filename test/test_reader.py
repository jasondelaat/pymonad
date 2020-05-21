# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import common_tests
import pymonad
from pymonad.reader import _Reader, Compose

class EqReader(pymonad.monad.MonadAlias, _Reader):
    def __eq__(self, other):
        try:
            return self(0) == other(0)
        except:
            return self(0) == other

class ReaderTests(unittest.TestCase):
    def test_insert(self):
        self.assertEqual(
            EqReader.insert(1),
            EqReader(lambda r: 1, None)
        )

class ComposeTests(unittest.TestCase):
    def test_insert_disabled(self):
        with self.assertRaises(AttributeError):
            Compose.insert(1)

    def test_apply_disabled(self):
        with self.assertRaises(AttributeError):
            Compose.apply(lambda x: x)

    def test_composition(self):
        inc = lambda x: x + 1
        dec = lambda x: x - 1
        inc_twice = (Compose(inc)
                     .then(inc)
                     .then(inc)
                     .then(dec))
        self.assertEqual(inc_twice(0), 2)

class ReaderFunctor(common_tests.FunctorTests, unittest.TestCase):
    def setUp(self):
        self._class = EqReader

class ReaderApplicative(common_tests.ApplicativeTests, unittest.TestCase):
    def setUp(self):
        self._class = EqReader

class ReaderMonad(common_tests.MonadTests, unittest.TestCase):
    def setUp(self):
        self._class = EqReader
