# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

from pymonad.Functor import *

class Applicative(Functor):
	"""
	Represents a functor "context" which contains a function as a value rather than
	a type like integers, strings, etc.

	"""

	def __init__(self, function):
		""" Stores 'function' as the functors value. """
		super(Applicative, self).__init__(function)

	def amap(self, functorValue):
		""" 
		Applies the function stored in the functor to the value inside 'functorValue'
		returning a new functor value.

		"""
		raise NotImplementedError

	def __and__(self, functorValue):
		""" The 'amap' operator. """
		return self.amap(functorValue)
