# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

import unittest
from pymonad.Writer import *
from MonadTester import *
from pymonad.Maybe import Just

class TestWriterFunctor(unittest.TestCase, MonadTester):
	def __init__(self, x):
		super(TestWriterFunctor, self).__init__(x)
		self.setClassUnderTest(NumberWriter)

	def testFunctorLaws(self):
		self.given((8, 5))
		self.ensure_first_functor_law_holds()
		self.ensure_second_functor_law_holds()

class TestWriterApplicative(unittest.TestCase, MonadTester):
	def __init__(self, x):
		super(TestWriterApplicative, self).__init__(x)
		self.setClassUnderTest(NumberWriter)

	def testApplicativeLaws(self):
		self.given((8, 5))
		self.ensure_first_applicative_law_holds()
		self.ensure_second_applicative_law_holds()
		self.ensure_third_applicative_law_holds()
		self.ensure_fourth_applicative_law_holds()
		self.ensure_fifth_applicative_law_holds()

class TestWriterMonad(unittest.TestCase, MonadTester):
	def __init__(self, x):
		super(TestWriterMonad, self).__init__(x)
		self.setClassUnderTest(StringWriter)

	def monad_function_f(self, x):
		return Writer((x / 10, "Division successful."))

	def monad_function_g(self, x):
		return Writer((x * 10, "Multiplication successful."))

	def testMonadLaws(self):
		self.given((8, "dummy"))
		self.ensure_first_monad_law_holds()
		self.ensure_second_monad_law_holds()
		self.ensure_third_monad_law_holds()

class TestWriterAlternateConstructorForm(unittest.TestCase, MonadTester):
	def testConstructors(self):
		firstConstructorForm = Writer(("value", "logMessage"))
		secondConstructorForm = Writer("value", "logMessage")
		self.assertEqual(firstConstructorForm, secondConstructorForm)

class TestWriterEquality(unittest.TestCase, MonadTester):
	def testEqualityOfIdenticalTypes(self):
		self.givenMonads(StringWriter(8, "log message"), StringWriter(8, "log message"))
		self.ensureMonadsAreEqual()

	def testEqualityWithBaseType(self):
		self.givenMonads(StringWriter(8, "log message"), Writer(8, "log message"))
		self.ensureMonadsAreEqual()

	def testInequalityOfIdenticalTypesWithDifferentLog(self):
		self.givenMonads(StringWriter(8, "log message"), StringWriter(8, "different message"))
		self.ensureMonadsAreNotEqual()

	def testInequalityOfIdenticalTypesWithDifferentResult(self):
		self.givenMonads(StringWriter(8, "log message"), StringWriter(9, "log message"))
		self.ensureMonadsAreNotEqual()

	def testInequalityOfDifferentTypes(self):
		self.givenMonads(StringWriter(8, "log message"), NumberWriter(8, 10))
		self.ensureMonadsAreNotEqual()

	def testMonadComparisonException(self):
		self.givenMonads(StringWriter(8, "log message"), Just(8))
		self.ensureComparisonRaisesException()

if __name__ == "__main__":
	unittest.main()
