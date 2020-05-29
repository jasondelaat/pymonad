# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import common_tests
import pymonad
from pymonad.operators.reader import _Reader

class EqReader(_Reader):
    def __eq__(self, other):
        try:
            return self(0) == other(0)
        except:
            return self(0) == other

class ReaderOperatorFunctor(common_tests.FunctorOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = EqReader

class ReaderOperatorApplicative(common_tests.ApplicativeOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = EqReader

class ReaderOperatorMonad(common_tests.MonadOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = EqReader
