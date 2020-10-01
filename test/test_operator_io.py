# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import common_tests
import pymonad
from pymonad.operators.io import _IO

class EqIO(_IO):
    def __eq__(self, other):
        try:
            return self.run() == other.run()
        except:
            return self.run() == other

class IOOperatorFunctor(common_tests.FunctorOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = EqIO

class IOOperatorApplicative(common_tests.ApplicativeOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = EqIO

class IOOperatorMonad(common_tests.MonadOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = EqIO
