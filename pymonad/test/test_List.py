# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

import unittest
from pymonad.Reader import curry
from pymonad.List import *
from MonadTester import *
from MonoidTester import *

class TestListFunctor(unittest.TestCase, MonadTester):
	def __init__(self, x):
		super(TestListFunctor, self).__init__(x)
		self.setClassUnderTest(List)

	def testFunctorLaws(self):
		self.given(1, 2, 3)
		self.ensure_first_functor_law_holds()
		self.ensure_second_functor_law_holds()

class TestListApplicative(unittest.TestCase, MonadTester):
	def __init__(self, x):
		super(TestListApplicative, self).__init__(x)
		self.setClassUnderTest(List)

	def testApplicativeLaws(self):
		self.given(1, 2, 3)
		self.ensure_first_applicative_law_holds()
		self.ensure_second_applicative_law_holds()
		self.ensure_third_applicative_law_holds()
		self.ensure_fourth_applicative_law_holds()
		self.ensure_fifth_applicative_law_holds()

class TestListMonad(unittest.TestCase, MonadTester):
	def __init__(self, x):
		super(TestListMonad, self).__init__(x)
		self.setClassUnderTest(List)

	def monad_function_f(self, x):
		return List(-x, x)

	def monad_function_g(self, x):
		return List(x * 5, x / 2)

	def testMonadLaws(self):
		self.given(1, 2, 3)
		self.ensure_first_monad_law_holds()
		self.ensure_second_monad_law_holds()
		self.ensure_third_monad_law_holds()

class TestListEquality(unittest.TestCase, MonadTester):
	def testEqualityOfIdenticalTypes(self):
		self.givenMonads(List(1, 2, 3), List(1, 2, 3))
		self.ensureMonadsAreEqual()

	def testInequalityOfIdenticalTypes(self):
		self.givenMonads(List(1, 2, 3), List(4, 5, 6))
		self.ensureMonadsAreNotEqual()

	def testMonadComparisonExceptionWithNothing(self):
		self.givenMonads(List(1, 2, 3), Reader(7))
		self.ensureComparisonRaisesException()

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
