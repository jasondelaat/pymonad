# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

from pymonad.Monad import *

class State(Monad):
	""" Represents a calculation which produces a stateful side-effect.  """

	def fmap(self, function): 
		"""
		Applies 'function' to the result contained within the monad and passes the state
		along unchanged.

		"""
		@State
		def newState(state):
			result, st = self(state)
			return (function(result), state)
		return newState

	def amap(self, functorValue):
		"""
		Applies the function contained within the monad to the result of 'functorValue'
		and passes along the state unchanged.

		"""
		@State
		def newState(state):
			function = self.getResult(state)
			value = functorValue.getResult(state)
			return (function(value), state)
		return newState

	def bind(self, function): 
		"""
		Chains together a series of stateful computations. 'function' accepts a single value
		and produces a new 'State' value which may or may not alter the state when it is
		executed.

		"""
		@State
		def newState(state):
			result, st = self(state)
			return function(result)(st)
		return newState

	@classmethod
	def unit(cls, value): 
		"""
		Produces a new stateful calculation which produces 'value' and leaves the passed in 
		state untouched.

		"""
		return State(lambda state: (value, state))

	def getResult(self, state):
		""" Returns only the result of a stateful calculation, discarding the state. """
		return self.value(state)[0]

	def getState(self, state):
		""" Returns only the final state of a stateful calculation, discarding the result.  """
		return self.value(state)[1]

	def __call__(self, state): 
		"""
		Executes the stateful calculation contained within the monad with an initial 'state'.
		Returns the result and the final state as a 2-tuple.

		"""
		return self.value(state)

	def __eq__(self, other):
		"""
		Always raises a TypeError.
		The State monad contains functions which can not be directly compared for equality,
		so attempting to compare instances of State with anything will always fail.

		"""
		raise TypeError("State: Can't compare functions for equality.")
