# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

import unittest
from MonoidTester import *
from pymonad.Monoid import *

class TestNaturalMonoid_Float(unittest.TestCase, MonoidTester):
	""" 
	The Float "Natural" Monoid just uses normal python numbers with: 
		mzero = 0, and 
		mplus = +
	It's not necessary to use a special class to use them.
	"""

	def testMonoidPlusZero(self): 
		self.givenMonoid(8.1)
		self.ensure_monoid_plus_zero_equals(self.monoid)

	def testZeroPlusMonoid(self): 
		self.givenMonoid(8.1)
		self.ensure_zero_plus_monoid_equals(self.monoid)

	def testMonoidAssociativity(self):
		self.givenMonoids(8.1, 2.4, 3.5)
		self.ensure_associativity()
	
class TestNaturalMonoid_Integer(unittest.TestCase, MonoidTester):
	""" 
	The Integer "Natural" Monoid just uses normal python numbers with: 
		mzero = 0, and 
		mplus = +
	It's not necessary to use a special class to use them.
	"""

	def testMonoidPlusZero(self): 
		self.givenMonoid(8)
		self.ensure_monoid_plus_zero_equals(self.monoid)

	def testZeroPlusMonoid(self): 
		self.givenMonoid(8)
		self.ensure_zero_plus_monoid_equals(self.monoid)

	def testMonoidAssociativity(self):
		self.givenMonoids(8, 2, 3)
		self.ensure_associativity()
	
class TestNaturalMonoid_String(unittest.TestCase, MonoidTester):
	""" 
	The String "Natural" Monoid just uses normal python strings with: 
		mzero = "", and 
		mplus = +
	It's not necessary to use a special class to use them.
	"""

	def testMonoidPlusZero(self): 
		self.givenMonoid("hello")
		self.ensure_monoid_plus_zero_equals(self.monoid)

	def testZeroPlusMonoid(self): 
		self.givenMonoid("hello")
		self.ensure_zero_plus_monoid_equals(self.monoid)

	def testMonoidAssociativity(self):
		self.givenMonoids("hello", "cruel", "world!")
		self.ensure_associativity()
	
class TestNaturalMonoid_List(unittest.TestCase, MonoidTester):
	""" 
	The List "Natural" Monoid just uses normal python lists with: 
		mzero = [], and 
		mplus = +
	It's not necessary to use a special class to use them.
	"""

	def testMonoidPlusZero(self): 
		self.givenMonoid([1, 2, 3])
		self.ensure_monoid_plus_zero_equals(self.monoid)

	def testZeroPlusMonoid(self): 
		self.givenMonoid([1, 2, 3])
		self.ensure_zero_plus_monoid_equals(self.monoid)

	def testMonoidAssociativity(self):
		self.givenMonoids([1, 2, 3], [4, 5, 6], [7, 8, 9])
		self.ensure_associativity()

class TestCustomMonoid(unittest.TestCase, MonoidTester):
	""" 
	User defined Monoids need to over-ride mzero and mplus.
	"""

	def testMonoidPlusZero(self): 
		self.givenMonoid(Product(3))
		self.ensure_monoid_plus_zero_equals(self.monoid)

	def testZeroPlusMonoid(self): 
		self.givenMonoid(Product(3))
		self.ensure_zero_plus_monoid_equals(self.monoid)

	def testMonoidAssociativity(self):
		self.givenMonoids(Product(3), Product(4), Product(5))
		self.ensure_associativity()

class TestNotAMonoid(unittest.TestCase):
	def testShouldRaiseTypeError(self):
		self.assertRaises(TypeError, mzero, {1: 1})

class Test_mconcat(unittest.TestCase, MonoidTester):
	def test_mconcat_on_natural_monoid(self):
		self.givenMonoids(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
		self.ensure_mconcat_equals(55)
	
	def test_mconcat_on_custom_monoid(self):
		self.givenMonoids(Product(2), Product(3), Product(4), Product(5))
		self.ensure_mconcat_equals(Product(120))

class Test_mzero(unittest.TestCase, MonoidTester):
	def test_mzero_with_integers(self):
		self.givenMonoid(8)
		self.get_mzero()
		self.ensure_mzero_is(0)

	def test_mzero_with_floats(self):
		self.givenMonoid(8.1)
		self.get_mzero()
		self.ensure_mzero_is(0)

	def test_mzero_with_strings(self):
		self.givenMonoid("hello")
		self.get_mzero()
		self.ensure_mzero_is("")

	def test_mzero_with_lists(self):
		self.givenMonoid([1, 2, 3])
		self.get_mzero()
		self.ensure_mzero_is([])

	def test_mzero_with_custom(self):
		self.givenMonoid(Product(3))
		self.get_mzero()
		self.ensure_mzero_is(Product(1))

	def test_mzero_with_class_int(self):
		self.givenMonoid(int)
		self.get_mzero()
		self.ensure_mzero_is(0)

	def test_mzero_with_class_float(self):
		self.givenMonoid(float)
		self.get_mzero()
		self.ensure_mzero_is(0)

	def test_mzero_with_class_str(self):
		self.givenMonoid(str)
		self.get_mzero()
		self.ensure_mzero_is("")

	def test_mzero_with_class_list(self):
		self.givenMonoid(list)
		self.get_mzero()
		self.ensure_mzero_is([])

	def test_mzero_with_custom_class(self):
		self.givenMonoid(Product)
		self.get_mzero()
		self.ensure_mzero_is(Product(1))
	
if __name__ == "__main__":
	unittest.main()
