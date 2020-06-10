# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import pymonad.monoid as monoid

class MZero_Tests(unittest.TestCase):
    def test_class_and_object_are_the_same(self):
        self.assertEqual(monoid.ZERO, monoid.ZERO())

    def test_left_identity(self):
        self.assertEqual(monoid.ZERO + 10, 10)

    def test_right_identity(self):
        self.assertEqual(10 + monoid.ZERO, 10)

    def test_repr(self):
        self.assertEqual(str(monoid.ZERO), 'MZERO')
