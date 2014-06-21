# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

import unittest
from pymonad.Maybe import Maybe, Just, First, Last, _Nothing, Nothing
from pymonad.Reader import curry
from MonadTester import *
from MonoidTester import *

class TestJustFunctor(unittest.TestCase, MonadTester):
	def __init__(self, x):
		super(TestJustFunctor, self).__init__(x)
		self.setClassUnderTest(Just)

	def testFunctorLaws(self):
		self.given(8)
		self.ensure_first_functor_law_holds()
		self.ensure_second_functor_law_holds()

class TestNothingFunctor(unittest.TestCase, MonadTester):
	def __init__(self, x):
		super(TestNothingFunctor, self).__init__(x)
		self.setClassUnderTest(_Nothing)

	def testFunctorLaws(self):
		self.given(None)
		self.ensure_first_functor_law_holds()
		self.ensure_second_functor_law_holds()

class TestJustApplicative(unittest.TestCase, MonadTester):
	def __init__(self, x):
		super(TestJustApplicative, self).__init__(x)
		self.setClassUnderTest(Just)

	def testApplicativeLaws(self):
		self.given(8)
		self.ensure_first_applicative_law_holds()
		self.ensure_second_applicative_law_holds()
		self.ensure_third_applicative_law_holds()
		self.ensure_fourth_applicative_law_holds()
		self.ensure_fifth_applicative_law_holds()

class TestNothingApplicative(unittest.TestCase, MonadTester):
	def __init__(self, x):
		super(TestNothingApplicative, self).__init__(x)
		self.setClassUnderTest(_Nothing)

	def testApplicativeLaws(self):
		self.given(None)
		self.ensure_first_applicative_law_holds()
		self.ensure_second_applicative_law_holds()
		self.ensure_third_applicative_law_holds()
		self.ensure_fourth_applicative_law_holds()
		self.ensure_fifth_applicative_law_holds()

class TestJustMonad(unittest.TestCase, MonadTester):
	def __init__(self, x):
		super(TestJustMonad, self).__init__(x)
		self.setClassUnderTest(Just)

	def monad_function_f(self, x):
		return Just(x + 10)

	def monad_function_g(self, x):
		return Just(x * 5)

	def testMonadLaws(self):
		self.given(8)
		self.ensure_first_monad_law_holds()
		self.ensure_second_monad_law_holds()
		self.ensure_third_monad_law_holds()

class TestNothingMonad(unittest.TestCase, MonadTester):
	def __init__(self, x):
		super(TestNothingMonad, self).__init__(x)
		self.setClassUnderTest(_Nothing)

	def monad_function_f(self, x):
		return Just(x + 10)

	def monad_function_g(self, x):
		return Just(x * 5)

	def testMonadLaws(self):
		self.given(None)
		self.ensure_first_monad_law_holds()
		self.ensure_second_monad_law_holds()
		self.ensure_third_monad_law_holds()

class TestMaybeEquality(unittest.TestCase, MonadTester):
	def testEqualityOfIdenticalTypes(self):
		self.givenMonads(Just(8), Just(8))
		self.ensureMonadsAreEqual()

	def testInequalityOfIdenticalTypes(self):
		self.givenMonads(Just(8), Just(9))
		self.ensureMonadsAreNotEqual()

	def testInequalityOfJustAndNothing(self):
		self.givenMonads(Just(8), Nothing)
		self.ensureMonadsAreNotEqual()

	def testMonadComparisonExceptionWithJust(self):
		self.givenMonads(Just(8), Reader(8))
		self.ensureComparisonRaisesException()

	def testMonadComparisonExceptionWithNothing(self):
		self.givenMonads(Nothing, Reader(8))
		self.ensureComparisonRaisesException()

class TestMaybeMonoid(unittest.TestCase, MonoidTester):
	def test_mzero(self):
		self.givenMonoid(Maybe)
		self.get_mzero()
		self.ensure_mzero_is(Nothing)

	def test_right_identity(self):
		self.givenMonoid(Just(9))
		self.ensure_monoid_plus_zero_equals(Just(9))

	def test_left_identity(self):
		self.givenMonoid(Just(9))
		self.ensure_zero_plus_monoid_equals(Just(9))

	def test_associativity(self):
		self.givenMonoids(Just(1), Just(2), Just(3))
		self.ensure_associativity()
	
	def test_mplus_with_two_just_values(self):
		self.givenMonoids(Just(1), Just(2))
		self.ensure_mconcat_equals(Just(3))

	def test_mplus_with_one_just_and_one_nothing(self):
		self.givenMonoids(Just(1), Nothing)
		self.ensure_mconcat_equals(Just(1))

class TestFirstMonoid(unittest.TestCase, MonoidTester):
	def test_mzero(self):
		self.givenMonoid(First)
		self.get_mzero()
		self.ensure_mzero_is(First(Nothing))

	def test_right_identity(self):
		self.givenMonoid(First(Just(9)))
		self.ensure_monoid_plus_zero_equals(First(Just(9)))

	def test_left_identity(self):
		self.givenMonoid(First(Just(9)))
		self.ensure_zero_plus_monoid_equals(First(Just(9)))

	def test_associativity(self):
		self.givenMonoids(First(Just(1)), First(Just(2)), First(Just(3)))
		self.ensure_associativity()
	
	def test_mplus_with_two_just_values(self):
		self.givenMonoids(First(Just(1)), First(Just(2)))
		self.ensure_mconcat_equals(First(Just(1)))

	def test_mplus_with_just_and_nothing(self):
		self.givenMonoids(First(Just(1)), Nothing)
		self.ensure_mconcat_equals(First(Just(1)))

	def test_mplus_with_nothing_and_just(self):
		self.givenMonoids(Nothing, First(Just(1)))
		self.ensure_mconcat_equals(First(Just(1)))

class TestLastMonoid(unittest.TestCase, MonoidTester):
	def test_mzero(self):
		self.givenMonoid(Last)
		self.get_mzero()
		self.ensure_mzero_is(Last(Nothing))

	def test_right_identity(self):
		self.givenMonoid(Last(Just(9)))
		self.ensure_monoid_plus_zero_equals(Last(Just(9)))

	def test_left_identity(self):
		self.givenMonoid(Last(Just(9)))
		self.ensure_zero_plus_monoid_equals(Last(Just(9)))

	def test_associativity(self):
		self.givenMonoids(Last(Just(1)), Last(Just(2)), Last(Just(3)))
		self.ensure_associativity()
	
	def test_mplus_with_two_just_values(self):
		self.givenMonoids(Last(Just(1)), Last(Just(2)))
		self.ensure_mconcat_equals(Last(Just(2)))

	def test_mplus_with_just_and_nothing(self):
		self.givenMonoids(Last(Just(1)), Nothing)
		self.ensure_mconcat_equals(Last(Just(1)))

	def test_mplus_with_nothing_and_just(self):
		self.givenMonoids(Nothing, Last(Just(1)))
		self.ensure_mconcat_equals(Last(Just(1)))

if __name__ == "__main__":
	unittest.main()
