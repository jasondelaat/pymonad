# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

import unittest
from pymonad.Reader import *

@curry
def neg(x): return -x

@curry
def sub(x, y): return x - y
@curry
def add(x, y): return x + y
@curry
def mul(x, y): return x * y


class ReaderTests(unittest.TestCase):
	def testCurry(self):
		@curry
		def add(x, y, z): return x + y + z
		@curry
		def sub(x, y, z): return x - y - z

		self.assertEqual(add(1, 2, 3), add(1)(2, 3))
		self.assertEqual(add(1, 2, 3), add(1, 2)(3))
		self.assertEqual(add(1, 2, 3), add(1)(2)(3))
		self.assertEqual(add(1, 2, 3), 6)

		self.assertEqual(sub(3, 2, 1), sub(3)(2, 1))
		self.assertEqual(sub(3, 2, 1), sub(3, 2)(1))
		self.assertEqual(sub(3, 2, 1), sub(3)(2)(1))
		self.assertEqual(sub(3, 2, 1), 0)
	
	def testReaderFunctor(self):
		comp1 = neg * sub(4)
		comp2 = sub(4) * neg
		comp3 = neg * sub(4) * neg
		self.assertEqual(comp1(3), -1)
		self.assertEqual(comp2(3), 7)
		self.assertEqual(comp3(3), -7)

	def testReaderApplicative(self):
		x = add * mul(5) & mul(6)
		self.assertEqual(x(5), 55)

	def testReaderMonad(self):
		x = (mul(2) >> (lambda a: 
			 add(10) >> (lambda b: 
			 Reader(a+b)))
			)
		self.assertEqual(x(3), 19)

class TestReaderUnit(unittest.TestCase):
	def testUnitOnReader(self):
		self.assertEqual(Reader.unit(8)("dummy value not used"), 8)
		self.assertEqual(unit(Reader, 8)("dummy value not used"), 8)

if __name__ == "__main__":
	unittest.main()
