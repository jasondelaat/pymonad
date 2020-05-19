# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import common_tests
from pymonad.either import Either, Left, Right


class EitherTests(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(str(Right(9)), 'Right 9')
        self.assertEqual(str(Left(9)), 'Left 9')

    def test_insert(self):
        self.assertEqual(Either.insert(1), Right(1))

class EitherFunctor(common_tests.FunctorTests, unittest.TestCase):
    def setUp(self):
        self._class = Either

class EitherMonad(common_tests.MonadTests, unittest.TestCase):
    def setUp(self):
        self._class = Either
