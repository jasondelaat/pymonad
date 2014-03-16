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
