# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

import unittest
import common_tests
from pymonad.operators.either import Either

class OperatorEitherFunctor(common_tests.FunctorOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = Either

class OperatorEitherApplicative(common_tests.FunctorOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = Either

class OperatorEitherMonad(common_tests.FunctorOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = Either
