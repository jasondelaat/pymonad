# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import common_tests
import pymonad
from pymonad.operators.state import _State

class EqState(_State):
    def __eq__(self, other):
        try:
            return self.run(0) == other.run(0)
        except:
            return self.run(0) == other

class StateOperatorFunctor(common_tests.FunctorOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = EqState

class StateOperatorApplicative(common_tests.ApplicativeOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = EqState

class StateOperatorMonad(common_tests.MonadOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = EqState
