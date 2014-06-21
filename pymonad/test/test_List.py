# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

import unittest
from pymonad.Reader import curry
from pymonad.List import *
from MonoidTester import *

def neg(x): return -x
def head(x): return x[0]
def plusMinusSame(x):
	return List(x+1, x-1, x)

class ListTests(unittest.TestCase):
	def testListAsList(self):
		self.assertEqual(List(1, 2, 3)[0], 1)
		self.assertEqual(List(1, 2, 3)[1:], List(2, 3))
		self.assertEqual(List(1, 2, 3)[:2], List(1, 2))
		self.assertEqual(List([1, 2], [2, 3], [3, 4])[:1], List([1, 2]))
		a = List(1, 2, 3, 4)
		a[:2] = List(5, 6)
		self.assertEqual(a, List(5, 6, 3, 4))

	def testListEquality(self):
		self.assertTrue(List(1, 2) == List(1, 2))
		self.assertTrue(List(1, 2) != List([1, 2]))
		self.assertTrue(List(1, 2) != List(1))
		self.assertTrue(List(1, 2) != [1, 2])
		self.assertTrue([1, 2] != List(1, 2))

		self.assertFalse(List(1, 2) != List(1, 2))
		self.assertFalse(List(1, 2) == List([1, 2]))
		self.assertFalse(List(1, 2) == List(1))
		self.assertFalse(List(1, 2) == [1, 2])
		self.assertFalse([1, 2] == List(1, 2))

	def testListFunctor(self):
		self.assertEqual(neg * List(1, 2, 3), List(-1, -2, -3))
		self.assertEqual(head * List([1, 2], [2, 3], [3, 4]), List(1, 2, 3))
	
	def testListApplicative(self):
		@curry
		def add(x, y): return x + y

		self.assertEqual(add * List(1, 2, 3) & List(1, 2, 3), List(2, 3, 4, 3, 4, 5, 4, 5, 6))
		self.assertEqual(List(add(1), add(2), add(3)) & List(1, 2, 3), List(2, 3, 4, 3, 4, 5, 4, 5, 6))
		
	def testListMonad(self):
		self.assertEqual(List(1) >> plusMinusSame, List(2, 0, 1))
		self.assertEqual(List(1) >> plusMinusSame >> plusMinusSame, List(3, 1, 2, 1, -1, 0, 2, 0, 1))
		self.assertEqual(neg * (List(1) >> plusMinusSame), List(-2, 0, -1))
		self.assertEqual(neg * List(1) >> plusMinusSame, List(0, -2, -1))

class TestListUnit(unittest.TestCase):
	def testUnitOnList(self):
		self.assertEqual(List.unit(8), List(8))
		self.assertEqual(unit(List, 8), List(8))

class TestListMonoid(unittest.TestCase, MonoidTester):
	def test_mzero(self):
		self.givenMonoid(List)
		self.get_mzero()
		self.ensure_mzero_is(List())

	def test_right_identity(self):
		self.givenMonoid(List(1, 2, 3))
		self.ensure_monoid_plus_zero_equals(List(1, 2, 3))

	def test_left_identity(self):
		self.givenMonoid(List(1, 2, 3))
		self.ensure_zero_plus_monoid_equals(List(1, 2, 3))

	def test_associativity(self):
		self.givenMonoids(List(1, 2, 3), List(4, 5, 6), List(7, 8, 9))
		self.ensure_associativity()
	
	def test_mplus(self):
		self.givenMonoids(List(1, 2, 3), List(2, 3, 4))
		self.ensure_mconcat_equals(List(1, 2, 3, 2, 3, 4))

if __name__ == "__main__":
	unittest.main()
