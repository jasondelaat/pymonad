# -----------------------------------------------------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
#
# This file contains helper classes and functions to make monad tests more readable and maintainable.
# -----------------------------------------------------------------------------------------------------
from pymonad.Reader import *

def identity(value):
	return value

@curry
def neg(x):
	return -x

@curry
def plus10(x):
	return x + 10

@curry
def fmap(x, y):
	return x * y

@curry
def revCall(parameter, function):
	return function(parameter)


class FunctorTester(object):
	def setClassUnderTest(self, cl):
		self.classUnderTest = cl

	def given(self, *value):
		self.monad = self.classUnderTest(*value)

	def givenMonad(self, mon):
		self.monad = mon

	def givenMonads(self, first, second):
		self.monads = [first, second]

	def ensureMonadsAreEqual(self):
		self.assertEqual(self.monads[0], self.monads[1])

	def ensureMonadsAreNotEqual(self):
		self.assertNotEqual(self.monads[0], self.monads[1])

	def ensureComparisonRaisesException(self):
		self.assertRaises(TypeError, self.monads[0].__eq__, self.monads[1])

	def ensure_first_functor_law_holds(self): 
		fmap_ID = self.monad.fmap(identity)
		ID_functor = identity(self.monad)
		try: self.assertEqual(fmap_ID, ID_functor)
		except TypeError: self.assertEqual(fmap_ID(0), ID_functor(0))

	def ensure_second_functor_law_holds(self):
		fmap_of_composed = (neg * plus10) * self.monad
		composition_of_fmapped = neg * (plus10 * self.monad)
		try: self.assertEqual(fmap_of_composed, composition_of_fmapped)
		except TypeError: self.assertEqual(fmap_of_composed(0), composition_of_fmapped(0))

class ApplicativeTester(FunctorTester):
	def ensure_first_applicative_law_holds(self):
		x = unit(self.classUnderTest, neg) & self.monad
		y = neg * self.monad
		try: self.assertEqual(x, y)
		except TypeError: self.assertEqual(x(0), y(0))

	def ensure_second_applicative_law_holds(self):
		x = unit(self.classUnderTest, identity) & self.monad
		try: self.assertEqual(x, self.monad)
		except TypeError: self.assertEqual(x(0), self.monad(0))

	def ensure_third_applicative_law_holds(self):
		u = unit(self.classUnderTest, fmap)
		v = unit(self.classUnderTest, neg)
		w = unit(self.classUnderTest, plus10)
		lhs = u & v & w & self.monad
		rhs = v & (w & self.monad)
		try: self.assertEqual(lhs, rhs)
		except TypeError: self.assertEqual(lhs(0), rhs(0))

	def ensure_fourth_applicative_law_holds(self):
		x = unit(self.classUnderTest, neg)
		y = unit(self.classUnderTest, 8)
		z = unit(self.classUnderTest, neg(8))
		try: self.assertEqual(x & y, z)
		except TypeError: self.assertEqual((x & y)(0), z(0))

	def ensure_fifth_applicative_law_holds(self):
		u = unit(self.classUnderTest, neg)
		y = 8
		lhs = u & unit(self.classUnderTest, y)
		rhs = unit(self.classUnderTest, revCall(y)) & u
		try: self.assertEqual(lhs, rhs)
		except TypeError: self.assertEqual(lhs(0), rhs(0))

class MonadTester(ApplicativeTester):
	def ensure_first_monad_law_holds(self):
		lhs = unit(self.classUnderTest, 4) >> self.monad_function_f
		rhs = self.monad_function_f(4)
		try: self.assertEqual(lhs, rhs)
		except TypeError: self.assertEqual(lhs(0), rhs(0))

	def ensure_second_monad_law_holds(self):
		lhs = self.monad >> self.classUnderTest.unit
		rhs = self.monad
		try: self.assertEqual(lhs, rhs)
		except TypeError: self.assertEqual(lhs(0), rhs(0))

	def ensure_third_monad_law_holds(self):
		lhs = (self.monad >> self.monad_function_f) >> self.monad_function_g
		rhs = self.monad >> (lambda x: self.monad_function_f(x) >> self.monad_function_g)
		try: self.assertEqual(lhs, rhs)
		except TypeError: self.assertEqual(lhs(0), rhs(0))
