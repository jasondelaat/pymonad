# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

from pymonad.Monad import *
from pymonad.Monoid import *

class List(list, Monad, Monoid):
	"""
	Represents a non-deterministic calculation or a calculation with more than one possible result.
	Based on Python's built-in 'list' type, 'List' supports most basic list operations such as 
	indexing, slicing, etc.
	"""

	def __init__(self, *values):
		""" Takes any number of values (including none) and puts them in the List monad. """
		super(List, self).__init__(values)

	def __eq__(self, other):
		if not isinstance(other, List):
			raise TypeError("Can't compare List with non-List type.")
		return super(List, self).__eq__(other)

	def __ne__(self, other):
		if not isinstance(other, List):
			return True
		return super(List, self).__ne__(other)

	# For compatibility with python 2...though I thought this was depricated and not necessary.
	def __getslice__(self, start, end):
		return self.__getitem__(slice(start, end))

	def __getitem__(self, key):
		if isinstance(key, slice):
			return List(*super(List, self).__getitem__(key))
		return super(List, self).__getitem__(key)
		
	def __str__(self):
		display = "["
		for item in self:
			display += str(item) + ", "
		return display[:-2]+ "]"

	@classmethod
	def unit(cls, value):
		return List(value)

	def getValue(self): 
		""" 
		Returns the list.
		This method is mainly to maintain compatibility with other monads,
		it's not strictly necessary, you can simply operate on the 'List' like
		any other list in Python.

		"""
		return self

	def fmap(self, function):
		""" Applies 'function' to every element in a List, returning a new List. """
		return List(*list(map(function, self)))

	def amap(self, functorValue):
		""" Applies the function(s) stored in the functor to the contents of the 'functorValue' List. """
		result = []
		for func in self.getValue():
			result.extend(func * functorValue)
		return List(*result)

	def bind(self, function): 
		""" 
		Applies 'function' to the result of a previous List operation.
		'function' should accept a single non-List argument and return a new List.
		"""
		result = []
		for subList in (map(function, self)):
			result.extend(subList)
		return List(*result)

	def __rmul__(self, function): 
		return self.fmap(function)

	@staticmethod
	def mzero():
		""" Returns the identity element (an empty List) of the List monoid.  """
		return List()

	def mplus(self, other):
		"""
		Combines two List monoid values into a single List monoid by concatenating the
		two lists together.

		"""
		return List(*(super(List, self).__add__(other)))

	def __add__(self, other):
		""" Overrides Python's native list __add__ operator to call 'mplus'.  """
		return self.mplus(other)
