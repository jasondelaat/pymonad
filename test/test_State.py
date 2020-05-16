# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

import unittest
from pymonad.State import *
from MonadTester import *

class TestStateFunctor(unittest.TestCase, MonadTester):
	def testFunctorLaws(self):
		self.givenMonad(unit(State, 8))
		self.ensure_first_functor_law_holds()
		self.ensure_second_functor_law_holds()

class TestStateApplicative(unittest.TestCase, MonadTester):
	def __init__(self, x):
		super(TestStateApplicative, self).__init__(x)
		self.setClassUnderTest(State)

	def testApplicativeLaws(self):
		self.givenMonad(unit(State, 8))
		self.ensure_first_applicative_law_holds()
		self.ensure_second_applicative_law_holds()
		self.ensure_third_applicative_law_holds()
		self.ensure_fourth_applicative_law_holds()
		self.ensure_fifth_applicative_law_holds()

class TestStateMonad(unittest.TestCase, MonadTester):
	def __init__(self, x):
		super(TestStateMonad, self).__init__(x)
		self.setClassUnderTest(State)

	def monad_function_f(self, x):
		return State(lambda st: (x + 10, st + 1))

	def monad_function_g(self, x):
		return State(lambda st: (x * 5, st + 2))

	def testMonadLaws(self):
		self.givenMonad(unit(State, 8))
		self.ensure_first_monad_law_holds()
		self.ensure_second_monad_law_holds()
		self.ensure_third_monad_law_holds()

class TestStateEquality(unittest.TestCase, MonadTester):
	def testMonadComparisonExceptionWithTwoIdenticalStates(self):
		self.givenMonads(unit(State, 8), unit(State, 8))
		self.ensureComparisonRaisesException()

	def testMonadComparisonExceptionWithTwoDifferentStates(self):
		self.givenMonads(unit(State, 8), unit(State, 9))
		self.ensureComparisonRaisesException()

	def testMonadComparisonExceptionWithDifferentTypes(self):
		self.givenMonads(unit(State, 8), Reader(8))
		self.ensureComparisonRaisesException()

if __name__ == "__main__":
	unittest.main()

