# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

import unittest
from pymonad.Reader import curry
from pymonad.Either import *

def neg(x): return -x
def head(x): return x[0]

def m_neg(x):
	try: return Right(-x)
	except: return Left("error")

@curry
def add(x, y): return Right(x + y)

@curry
def div(y, x):
	if y == 0: return Left("division error")
	return Right(x/y)

class EitherTests(unittest.TestCase):
	def testEitherAbstract(self):
		self.assertRaises(NotImplementedError, Either, 7)
		self.assertRaises(NotImplementedError, Either, "string")
		self.assertRaises(NotImplementedError, Either, [])

	def testEitherEquality(self):
		self.assertTrue(Right(7) == Right(7))
		self.assertTrue(Left(7) == Left(7))
		self.assertTrue(Right(7) != Right(6))
		self.assertTrue(Right(7) != Right("blah"))
		self.assertTrue(Left(7) != Left("blah"))
		self.assertTrue(Left(7) != Left("blah"))
		self.assertTrue(Left(7) != Right(6))
		self.assertTrue(Left(7) != Right(7))

		self.assertFalse(Right(7) != Right(7))
		self.assertFalse(Left(7) != Left(7))
		self.assertFalse(Right(7) == Right(6))
		self.assertFalse(Right(7) == Right("blah"))
		self.assertFalse(Left(7) == Left("blah"))
		self.assertFalse(Left(7) == Left("blah"))
		self.assertFalse(Left(7) == Right(6))
		self.assertFalse(Left(7) == Right(7))

	def testEitherFunctor(self):
		self.assertEqual(neg * Right(7), Right(-7))
		self.assertEqual(neg * Left("error"), Left("error"))
		self.assertEqual(head * Right("hello"), Right("h"))
		self.assertEqual(head * Right([0, 1, 2]), Right(0))
		self.assertEqual(head * Left("hello"), Left("hello"))
		self.assertEqual(head * Left([0, 1, 2]), Left([0, 1, 2]))

	def testEitherApplicative(self):
		@curry
		def add(x, y): return x + y

		self.assertEqual(Right(add(7)) & Right(8), Right(15))
		self.assertEqual(add * Right(7) & Right(8), Right(15))
		self.assertEqual(add * Right(7) & Left("error"), Left("error"))
		self.assertEqual(add * Left("error") & Right(8), Left("error"))

	def testEitherMonad(self):
		self.assertEqual(Right(7) >> add(7) >> div(2), Right(7))
		self.assertEqual(Right(7) >> add(7) >> div(0), Left("division error"))
		self.assertEqual(Right(7) >> add(7) >> div(0) >> add(7), Left("division error"))
		self.assertEqual(Right(7) >> m_neg >> add(7), Right(0))
		self.assertEqual(Right("hello") >> m_neg, Left("error"))
		self.assertEqual(Left("Short-circuit") >> add(7) >> m_neg >> add(6) >> div(2) >> div(0), Left("Short-circuit"))
	
	def testBindReturnsMonad(self):
		self.assertRaises(TypeError, Right(7).__rshift__, lambda x: 9)
		self.assertRaises(TypeError, Right(7).__rshift__, 9)

class TestEitherUnit(unittest.TestCase):
	def testUnitOnEither(self):
		self.assertEqual(Either.unit(8), Right(8))
		self.assertEqual(unit(Either, 8), Right(8))

	def testUnitOnRight(self):
		self.assertEqual(Right.unit(8), Right(8))
		self.assertEqual(unit(Right, 8), Right(8))

	def testUnitOnLeft(self):
		self.assertEqual(unit(Left, 8), Right(8))

if __name__ == "__main__":
	unittest.main()
