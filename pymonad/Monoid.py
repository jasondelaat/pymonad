# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
from pymonad.Container import *
from pymonad.Reader import curry

class Monoid(Container):
	"""
	Represents a data type which conforms to the following conditions:
	   1. Has an operation (called 'mplus') which combines two values of this type.
	   2. Has a value (called 'mzero') such that mplus(mzero, value) == mplus(value, mzero) = value.
	      In other words, mzero acts as an identity element under the mplus operation.
	   3. mplus is associative: mplus(a, mplus(b, c)) == mplus(mplus(a, b), c)

	   For instance, integers can be monoids in two ways: With mzero = 0 and mplus = + (addition)
	   or with mzero = 1 and mplus = * (multiplication).
	   In the case of strings, mzero = "" (the empty string) and mplus = + (concatenation).

	"""

	def __init__(self, value):
		""" Initializes the monoid element to 'value'.  """
		super(Monoid, self).__init__(value)
	
	def __add__(self, other):
		""" The 'mplus' operator.  """
		return self.mplus(other)

	@staticmethod
	def mzero():
		"""
		A static method which simply returns the identity value for the monoid type.
		This method must be overridden in subclasses to create custom monoids.
		See also: the mzero function.

		"""
		raise NotImplementedError

	def mplus(self, other):
		"""
		The defining operation of the monoid. This method must be overridden in subclasses
		and should meet the following conditions.
		   1. x + 0 == 0 + x == x
		   2. (x + y) + z == x + (y + z) == x + y + z
		Where 'x', 'y', and 'z' are monoid values, '0' is the mzero (the identity value) and '+' 
		is mplus.

		"""
		raise NotImplementedError

@curry
def mzero(monoid_type):
	"""
	Returns the identity value for monoid_type. Raises TypeError if monoid_type is not a valid monoid.

	There are a number of builtin types that can operate as monoids and they can be used as such
	as is. These "natural" monoids are: int, float, str, and list.
	While thee mzero method will work on monoids derived from the Monoid class,
	this mzero function will work for *all* monoid types, including the "natural" monoids.
	For this reason it is preferable to call this function rather than calling the mzero method directly
	unless you know for sure what type of monoid you're dealing with.

	"""
	try:
		return monoid_type.mzero()
	except AttributeError:
		if isinstance(monoid_type, int) or isinstance(monoid_type, float) or monoid_type == int or monoid_type == float:
			return 0
		elif isinstance(monoid_type, str) or monoid_type == str:
			return ""
		elif isinstance(monoid_type, list) or monoid_type == list:
			return []
		else:
			raise TypeError(str(monoid_type) + " is not a Monoid.")

@curry
def mconcat(monoid_list):
	"""
	Takes a list of monoid values and reduces them to a single value by applying the
	mplus operation to each all elements of the list.

	"""
	result = mzero(monoid_list[0])
	for value in monoid_list:
		result += value
	return result
