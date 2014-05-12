# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

from pymonad.Monad import *

class Either(Monad):
	""" 
	Represents a calculation that may either fail or succeed.
	An alternative to using exceptions. 'Either' is an abstract type and should not
	be instantiated directly. Instead use 'Right' (or its alias 'Result') and 
	'Left' (or its alias 'Error')
	"""

	def __init__(self, value):
		""" Raises a 'NotImplementedError'.  Use 'Right' or 'Left' instead. """
		raise NotImplementedError

	def __eq__(self, other):
		if not isinstance(other, Either): raise TypeError("Can't compare different types.")

	@classmethod
	def unit(cls, value):
		return Right(value)

class Left(Either):
	""" 
	Represents a calculation which has failed and contains an error code or message. 
	To help with readaility you may alternatively use the alias 'Error'.
	"""

	def __init__(self, errorMsg):
		""" 
		Creates a 'Left' "calculation failed" object.
		'errorMsg' can be anything which gives information about what when wrong.
		"""
		super(Either, self).__init__(errorMsg)

	def __eq__(self, other):
		super(Left, self).__eq__(other)
		if not isinstance(other, Left): return False
		elif (self.getValue() == other.getValue()): return True
		else: return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def __str__(self):
		return "Left: " + str(self.getValue())

	def fmap(self, _): 
		""" Returns the 'Left' instance that was used to call the method. """
		return self

	def amap(self, _):
		""" Returns the 'Left' instance that was used to call the method. """
		return self
		
	def bind(self, _):
		""" Returns the 'Left' instance that was used to call the method. """
		return self

class Right(Either):
	""" 
	Represents a calculation which has succeeded and contains the result of that calculation.
	To help with readaility you may alternatively use the alias 'Result'.
	"""

	def __init__(self, value):
		"""
		Creates a 'Right' "calculation succeeded" object.
		'value' is the actual calculated value of whatever operation was being performed
		and can be any type.
		"""
		super(Either, self).__init__(value)

	def __eq__(self, other):
		super(Right, self).__eq__(other)
		if not isinstance(other, Right): return False
		elif (self.getValue() == other.getValue()): return True
		else: return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def __str__(self):
		return "Right: " + str(self.getValue())

	def fmap(self, function):
		""" 
		Applies 'function' to the contents of the 'Right' instance and returns a 
		new 'Right' object containing the result. 
		'function' should accept a single "normal" (non-monad) argument and return
		a non-monad result.
		"""
		return Right(function(self.getValue()))

	def amap(self, functorValue):
		""" Applies the function stored in the functor to 'functorValue' returning a new Either value. """
		return self.getValue() * functorValue

	def bind(self, function):
		"""
		Applies 'function' to the result of a previous calculation.
		'function' should accept a single "normal" (non-monad) argument and return
		either a 'Left' or 'Right' type object.
		"""
		return function(self.getValue())

Error = Left
Result = Right
