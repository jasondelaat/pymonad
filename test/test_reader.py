# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import common_tests
import pymonad
from pymonad.reader import _Reader

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

class ReaderFunctor(common_tests.FunctorTests, unittest.TestCase):
    def setUp(self):
        self._class = EqReader

class ReaderApplicative(common_tests.ApplicativeTests, unittest.TestCase):
    def setUp(self):
        self._class = EqReader

class ReaderMonad(common_tests.MonadTests, unittest.TestCase):
    def setUp(self):
        self._class = EqReader
