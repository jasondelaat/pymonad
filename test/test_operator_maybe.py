# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

import unittest
import common_tests
from pymonad.operators.maybe import Maybe

class OperatorMaybeFunctor(common_tests.FunctorOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = Maybe

class OperatorMaybeApplicative(common_tests.FunctorOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = Maybe

class OperatorMaybeMonad(common_tests.FunctorOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = Maybe
