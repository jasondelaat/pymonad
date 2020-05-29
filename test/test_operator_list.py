# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

import unittest
import common_tests
from pymonad.operators.list import _List

class Operator_ListFunctor(common_tests.FunctorOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = _List

class Operator_ListApplicative(common_tests.FunctorOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = _List

class Operator_ListMonad(common_tests.FunctorOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = _List
