# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import common_tests
import pymonad
from pymonad.state import _State

class EqState(_State):
    def __eq__(self, other):
        try:
            return self.run(0) == other.run(0)
        except:
            return self.run(0) == other

class StateTests(unittest.TestCase):
    def test_insert(self):
        self.assertEqual(
            EqState.insert(2),
            (2, 0)
        )

class StateFunctor(common_tests.FunctorTests, unittest.TestCase):
    def setUp(self):
        self._class = EqState

class StateApplicative(common_tests.ApplicativeTests, unittest.TestCase):
    def setUp(self):
        self._class = EqState

class StateMonad(common_tests.MonadTests, unittest.TestCase):
    def setUp(self):
        self._class = EqState

class StateThen(common_tests.ThenTests, unittest.TestCase):
    def setUp(self):
        self._class = EqState
