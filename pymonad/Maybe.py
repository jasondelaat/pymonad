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
		""" Injects 'value' into the Maybe monad.  """
		return Just(value)

	@staticmethod
	def mzero():
		""" Returns the identity element (Nothing) for the Maybe Monoid.  """
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
		"""
		Combines Maybe monoid values into a single monoid value.
		The Maybe monoid works when the values it contains are also monoids
		with a defined mzero and mplus. This allows you do things like:
			Just(1) + Just(9) == Just(10)
			Just("Hello ") + Just("World") == Just("Hello World")
			Just([1, 2, 3]) + Just([4, 5, 6]) == Just([1, 2, 3, 4, 5, 6])
		etc. 

		The identity value is 'Nothing' so:
			Just(1) + Nothing == Just(1)

		"""
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
		"""
		Combines Maybe monoid values into a single monoid value.
		The Maybe monoid works when the values it contains are also monoids
		with a defined mzero and mplus. This allows you do things like:
			Just(1) + Just(9) == Just(10)
			Just("Hello ") + Just("World") == Just("Hello World")
			Just([1, 2, 3]) + Just([4, 5, 6]) == Just([1, 2, 3, 4, 5, 6])
		etc. 

		The identity value is 'Nothing' so:
			Just(1) + Nothing == Just(1)

		"""
		return other

Nothing = _Nothing()

class First(Monoid):
	"""
	A wrapper around 'Maybe' values, 'First' is a monoid intended to make it easy to
	find the first non-failure value in a collection of values which may fail.

	"""
	def __init__(self, value):
		"""
		Only accepts instances of the 'Maybe' monad for value. Raises 'TypeError' if
		any other type of value is passed.

		"""
		if not isinstance(value, Maybe): raise TypeError
		else: super(First, self).__init__(value)
	
	def __str__(self):
		return str(self.value)

	@staticmethod
	def mzero():
		""" Returns the identity element (First(Nothing)) for the Maybe Monoid.  """
		return First(Nothing)

	def mplus(self, other):
		"""
		Returns the first encountered non-failure value if it exists. Returns 
		First(Nothing) otherwise.

		"""
		if isinstance(self.value, Just): return self
		else: return other

class Last(Monoid):
	"""
	A wrapper around 'Maybe' values, 'Last' is a monoid intended to make it easy to
	find the final non-failure value in a collection of values which may fail.

	"""
	def __init__(self, value):
		"""
		Only accepts instances of the 'Maybe' monad for value. Raises 'TypeError' if
		any other type of value is passed.

		"""
		if not isinstance(value, Maybe): raise TypeError
		else: super(Last, self).__init__(value)
	
	def __str__(self):
		return str(self.value)

	@staticmethod
	def mzero():
		""" Returns the identity element (Last(Nothing)) for the Maybe Monoid.  """
		return First(Nothing)

	def mplus(self, other):
		"""
		Returns the last non-failure value encountered if it exists. Returns 
		Last(Nothing) otherwise.

		"""
		if isinstance(other.value, Just): return other
		else: return self
