# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import pymonad.monoid as monoid

class MZero_Tests(unittest.TestCase):
    def test_left_identity(self):
        self.assertEqual(monoid.MONOID_ZERO + 10, 10)
        self.assertEqual(monoid.MONOID_ZERO * 10, 10)

    def test_right_identity(self):
        self.assertEqual(10 + monoid.MONOID_ZERO, 10)
        self.assertEqual(10 * monoid.MONOID_ZERO, 10)

    def test_repr(self):
        self.assertEqual(str(monoid.MONOID_ZERO), 'MZERO')
