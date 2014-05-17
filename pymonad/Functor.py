# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

from pymonad.Container import *

class Functor(Container):
	""" Represents a type of values which can be "mapped over." """

	def __init__(self, value):
		""" Stores 'value' as the contents of the Functor. """
		super(Functor, self).__init__(value)

	def fmap(self, function): 
		""" Applies 'function' to the contents of the functor and returns a new functor value. """
		raise NotImplementedError("'fmap' not defined.")
	
	def __rmul__(self, aFunction):
		""" 
		The 'fmap' operator.
		The following are equivalent:

			aFunctor.fmap(aFunction)
			aFunction * aFunctor

		"""
		
		return self.fmap(aFunction)

	@classmethod
	def unit(cls, value):
		""" Returns an instance of the Functor with 'value' in a minimum context.  """
		raise NotImplementedError

def unit(aClass, value):
	""" Calls the 'unit' method of 'aClass' with 'value'.  """
	return aClass.unit(value)
