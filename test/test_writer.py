# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import common_tests
from pymonad.writer import Writer

class WriterTests(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(
            str(Writer(1, 'one')),
            '(1, one)'
        )

    def test_insert(self):
        self.assertEqual(
            Writer.insert(1),
            Writer(1, '')
        )
        self.assertEqual(
            str(Writer.insert(1)),
            '(1, )'
        )

class WriterFunctor(common_tests.FunctorTests, unittest.TestCase):
    def setUp(self):
        self._class = Writer

class WriterApplicative(common_tests.ApplicativeTests, unittest.TestCase):
    def setUp(self):
        self._class = Writer

class WriterMonad(common_tests.MonadTests, unittest.TestCase):
    def setUp(self):
        self._class = Writer

class WriterThen(common_tests.ThenTests, unittest.TestCase):
    def setUp(self):
        self._class = Writer
