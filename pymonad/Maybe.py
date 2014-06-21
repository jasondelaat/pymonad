# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

from pymonad.Monad import *
from pymonad.Monoid import *

class Maybe(Monad, Monoid):
	""" 
	Represents a calculation which may fail. An alternative to using Exceptions. 
	'Maybe' is an abstract type and should not be instantiated directly. There are two types
	of 'Maybe' values: Just(something) and Nothing. 

	"""

	def __init__(self, value):
		"""
		Raises a NotImplementedError. 
		Do not create 'Maybe' values directly, use Just or Nothing instead.

		"""
		raise NotImplementedError("Can't create objects of type Maybe: use Just(something) or Nothing.")

	def __eq__(self, other):
		if not isinstance(other, Maybe): raise TypeError("Can't compare two different types.")

	@classmethod
	def unit(cls, value):
		return Just(value)

	@staticmethod
	def mzero():
		return Nothing

class Just(Maybe):
	""" The 'Maybe' type used to represent a calculation that has succeeded. """

	def __init__(self, value):
		"""
		Creates a Just value representing a successful calculation.
		'value' can be any type of value, including functions.

		"""
		super(Maybe, self).__init__(value)

	def __str__(self):
		return "Just " + str(self.getValue())

	def __eq__(self, other):
		super(Just, self).__eq__(other)
		if isinstance(other, _Nothing): return False
		elif (self.getValue() == other.getValue()): return True
		else: return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def fmap(self, function):
		""" Applies 'function' to the 'Just' value and returns a new 'Just' value. """
		return Just(function(self.getValue()))

	def amap(self, functorValue):
		""" 
		Applies the function stored in the functor to the value of 'functorValue',
		returning a new 'Just' value.

		"""
		return self.getValue() * functorValue

	def bind(self, function):
		""" Applies 'function' to a 'Just' value.
		'function' must accept a single argument and return a 'Maybe' type,
		either 'Just(something)' or 'Nothing'.

		"""
		return function(self.getValue())

	def mplus(self, other):
		if other == Nothing: return self
		else: return Just(self.value + other.value)

class _Nothing(Maybe):
	""" The 'Maybe' type used to represent a calculation that has failed. """
	def __init__(self, value=None):
		super(Maybe, self).__init__(value)

	def __str__(self):
		return "Nothing"

	def __eq__(self, other):
		super(_Nothing, self).__eq__(other)
		if isinstance(other, _Nothing): return True
		else: return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def fmap(self, _):
		""" Returns 'Nothing'. """
		return self

	def amap(self, _):
		""" Returns 'Nothing'. """
		return self

	def bind(self, _):
		""" Returns 'Nothing'. """
		return self

	def mplus(self, other):
		return other

Nothing = _Nothing()

class First(Monoid):
	def __init__(self, value):
		if not isinstance(value, Maybe): raise TypeError
		else: super(First, self).__init__(value)
	
	def __str__(self):
		return str(self.value)

	@staticmethod
	def mzero():
		return First(Nothing)

	def mplus(self, other):
		if isinstance(self.value, Just): return self
		else: return other

class Last(Monoid):
	def __init__(self, value):
		if not isinstance(value, Maybe): raise TypeError
		else: super(Last, self).__init__(value)
	
	def __str__(self):
		return str(self.value)

	@staticmethod
	def mzero():
		return First(Nothing)

	def mplus(self, other):
		if isinstance(other.value, Just): return other
		else: return self
