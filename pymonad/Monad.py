# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

from pymonad.Applicative import *

class Monad(Applicative):
	"""
	Represents a "context" in which calculations can be executed.

	You won't create 'Monad' instances directly. Instead, sub-classes implement
	specific contexts. Monads allow you to bind together a series of calculations
	while maintaining the context of that specific monad.

	"""

	def __init__(self, value):
		""" Wraps 'value' in the Monad's context. """
		super(Monad, self).__init__(value)

	def bind(self, function):
		""" Applies 'function' to the result of a previous monadic calculation. """
		raise NotImplementedError

	def __rshift__(self, function):
		""" 
		The 'bind' operator. The following are equivalent:
			monadValue >> someFunction
			monadValue.bind(someFunction)

		"""
		if callable(function): 
			result = self.bind(function)
			if not isinstance(result, Monad): raise TypeError("Operator '>>' must return a Monad instance.")
			return result
		else:
			if not isinstance(function, Monad): raise TypeError("Operator '>>' must return a Monad instance.")
			return self.bind(lambda _: function)
