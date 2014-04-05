from pymonad.Monad import *

class Maybe(Monad):
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

class _Nothing(Maybe):
	""" The 'Maybe' type used to represent a calculation that has failed. """
	def __init__(self):
		super(Maybe, self).__init__(None)

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

Nothing = _Nothing()
