# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

from pymonad.Monad import *

class State(Monad):
	def __init__(self, functionOrValue):
		if callable(functionOrValue):
			super(State, self).__init__(functionOrValue)
		else:
			super(State, self).__init__(lambda state: (functionOrValue, state))

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

if __name__ == "__main__":
	from pymonad.Reader import curry

	def neg(x): return -x

	@curry
	def mul(x, y): return x * y

	@curry
	def add(x, y):
		return State(lambda state: (x + y, state + 1))

	@curry
	def sub(y, x):
		return State(lambda state: (x - y, state + 1))
		
	x = unit(State, 2) >> add(3) >> add(4) >> add(5) >> sub(6)
	print(x(0))

	y = neg * unit(State, 2)
	print(y(0))

	y = neg * State(2)
	print(y(1))

	y = mul * State(2) & State(9)
	print(y(0))
