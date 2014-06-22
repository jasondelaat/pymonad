# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

from pymonad.Monad import *

class State(Monad):
	def fmap(self, function): 
		@State
		def newState(state):
			result, st = self(state)
			return (function(result), state)
		return newState

	def amap(self, functorValue):
		@State
		def newState(state):
			function = self.getResult(state)
			value = functorValue.getResult(state)
			return (function(value), state)
		return newState

	def bind(self, function): 
		@State
		def newState(state):
			result, st = self(state)
			return function(result)(st)
		return newState

	@classmethod
	def unit(cls, value): 
		return State(lambda state: (value, state))

	def getResult(self, state):
		return self.value(state)[0]

	def getState(self, state):
		return self.value(state)[1]

	def __call__(self, state): 
		return self.value(state)

	def __eq__(self, other):
		raise TypeError("State: Can't compare functions for equality.")
