# -------------------------------------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
#
# These classes are helper classes to make the actual monoid test cases more readable.
# -------------------------------------------------------------------------------------

from pymonad.Monoid import *

class MonoidTester(object):
	def givenMonoid(self, m):
		self.monoid = m

	def givenMonoids(self, *ms):
		self.monoids = ms

	def get_mzero(self):
		self.mzero = mzero(self.monoid)

	def ensure_mzero_is(self, value):
		self.assertTrue(self.mzero == value)

	def ensure_monoid_plus_zero_equals(self, value):
		self.assertEqual(self.monoid + mzero(self.monoid), value)

	def ensure_zero_plus_monoid_equals(self, value):
		self.assertEqual(mzero(self.monoid) + self.monoid , value)

	def ensure_associativity(self):
		association1 = (self.monoids[0] + self.monoids[1]) + self.monoids[2]
		association2 = self.monoids[0] + (self.monoids[1] + self.monoids[2])
		association3 = self.monoids[0] + self.monoids[1] + self.monoids[2]
		self.assertEqual(association1, association2)
		self.assertEqual(association2, association3)
		self.assertEqual(association1, association3)

	def ensure_mconcat_equals(self, value):
		self.assertEqual(mconcat(self.monoids), value)

class Product(Monoid):
	@staticmethod
	def mzero():
		return Product(1)

	def mplus(self, other):
		return Product(self.value * other.value)
