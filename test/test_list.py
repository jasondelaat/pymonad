# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import common_tests
from pymonad.list import ListMonad

class ListTests(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(str(ListMonad(1, 2, 3)), '[1, 2, 3]')

    def test_insert(self):
        self.assertEqual(ListMonad.insert(1), ListMonad(1))

    def test_indexing(self):
        self.assertEqual(ListMonad(1, 2, 3)[0], 1)
        self.assertEqual(ListMonad(1, 2, 3)[1], 2)
        self.assertEqual(ListMonad(1, 2, 3)[2], 3)

    def test_slicing(self):
        self.assertEqual(ListMonad(1, 2, 3)[:], ListMonad(1, 2, 3))
        self.assertEqual(ListMonad(1, 2, 3)[1:], ListMonad(2, 3))
        self.assertEqual(ListMonad(1, 2, 3)[2:], ListMonad(3))

    def test_slicing_with_step(self):
        self.assertEqual(ListMonad(1, 2, 3, 4, 5)[::2], ListMonad(1, 3, 5))

    def test_len(self):
        self.assertEqual(len(ListMonad(1, 2, 3)), 3)

class ListFunctor(common_tests.FunctorTests, unittest.TestCase):
    def setUp(self):
        self._class = ListMonad

class ListApplicative(common_tests.ApplicativeTests, unittest.TestCase):
    def setUp(self):
        self._class = ListMonad
    def test_proper_output(self):
        self.assertEqual(
            ListMonad.apply(common_tests.add).to_arguments(ListMonad(1, 2, 3), ListMonad(4, 5, 6)),
            ListMonad(5, 6, 7, 6, 7, 8, 7, 8, 9)
        )

class ListMonadTests(common_tests.MonadTests, unittest.TestCase):
    def setUp(self):
        self._class = ListMonad

class ListThenTests(common_tests.ThenTests, unittest.TestCase):
    def setUp(self):
        self._class = ListMonad
