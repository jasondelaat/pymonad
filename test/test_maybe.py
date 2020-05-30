# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import common_tests
import pymonad.tools
from pymonad.maybe import Maybe, Just, Nothing
from pymonad.maybe import Option, Some

class MaybeTests(unittest.TestCase):
    def test_repr_Just(self):
        self.assertEqual(str(Just(9)), 'Just 9')

    def test_repr_Nothing(self):
        self.assertEqual(str(Nothing), 'Nothing')

    def test_insert(self):
        self.assertEqual(Maybe.insert(9), Just(9))

class OptionTests(unittest.TestCase):
    def test_repr_Some(self):
        self.assertEqual(str(Some(9)), 'Some 9')

    def test_insert(self):
        self.assertEqual(Option.insert(9), Some(9))

    def test_insert_repr(self):
        self.assertEqual(str(Option.insert(9)), 'Some 9')

class MaybeFunctor(common_tests.FunctorTests, unittest.TestCase):
    def setUp(self):
        self._class = Maybe

    def test_mapping_over_nothing(self):
        self.assertEqual(
            Nothing.map(lambda x: x),
            Nothing
        )

class MaybeApplicative(common_tests.ApplicativeTests, unittest.TestCase):
    def setUp(self):
        self._class = Maybe

    def test_applying_with_nothing_in_first_arg(self):
        self.assertEqual(
            Maybe.apply(common_tests.add).to_arguments(Nothing, Just(1)),
            Nothing
        )

    def test_applying_with_nothing_in_second_arg(self):
        self.assertEqual(
            Maybe.apply(common_tests.add).to_arguments(Just(1), Nothing),
            Nothing
        )

class MaybeMonad(common_tests.MonadTests, unittest.TestCase):
    def setUp(self):
        self._class = Maybe

    def test_binding_with_nothing(self):
        self.assertEqual(
            Nothing.bind(Maybe.insert),
            Nothing
        )

class MaybeThen(common_tests.ThenTests, unittest.TestCase):
    def setUp(self):
        self._class = Maybe
