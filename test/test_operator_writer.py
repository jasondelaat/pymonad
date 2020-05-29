# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

import unittest
import common_tests
from pymonad.operators.writer import Writer

class OperatorWriterFunctor(common_tests.FunctorOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = Writer

class OperatorWriterApplicative(common_tests.FunctorOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = Writer

class OperatorWriterMonad(common_tests.FunctorOperatorTests, unittest.TestCase):
    def setUp(self):
        self._class = Writer
