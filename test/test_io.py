# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import common_tests
import pymonad
from pymonad.io import _IO

class EqIO(_IO):
    def __eq__(self, other):
        try:
            return self.run() == other.run()
        except:
            return self.run() == other

class IOTests(unittest.TestCase):
    def test_insert(self):
        self.assertEqual(
            EqIO.insert(2),
            2
        )

class IOFunctor(common_tests.FunctorTests, unittest.TestCase):
    def setUp(self):
        self._class = EqIO

class IOApplicative(common_tests.ApplicativeTests, unittest.TestCase):
    def setUp(self):
        self._class = EqIO

class IOMonad(common_tests.MonadTests, unittest.TestCase):
    def setUp(self):
        self._class = EqIO

class IOThen(common_tests.ThenTests, unittest.TestCase):
    def setUp(self):
        self._class = EqIO
