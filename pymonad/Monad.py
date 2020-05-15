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
		self.is_monad_value = True

	def bind(self, function):
		""" Applies 'function' to the result of a previous monadic calculation. """
		raise NotImplementedError

	def then(self, function):
		""" Combines the functionality of bind and fmap.

		Instead of worrying about whether to use bind or fmap,
		users can just use the then method to chain function
		calls together. The then method uses attempts to use
		bind first and if that doesn't work, uses fmap
		instead.

		Args:
		function: A python function or lambda expression
		which returns either a build-in type (int, string,
		etc.) or an appropriate monad type (Maybe, Either,
		etc.)

		Returns:
		A monad value of the same type as 'self'
		"""

		result = self.bind(function)
		try:
			result.is_monad_value
			return result
		except AttributeError:
			return self.fmap(function)

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
