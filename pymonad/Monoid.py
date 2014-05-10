# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
from pymonad.Container import *

class Monoid(Container):
	def __init__(self, value):
		super(Monoid, self).__init__(value)
	
	def __add__(self, other):
		return self.mplus(other)

	@staticmethod
	def mzero():
		raise NotImplementedError

	def mplus(self, other):
		raise NotImplementedError
	
def mzero(monoid_value):
	try:
		return monoid_value.mzero()
	except AttributeError:
		if isinstance(monoid_value, int) or isinstance(monoid_value, float) or monoid_value == int or monoid_value == float:
			return 0
		elif isinstance(monoid_value, str) or monoid_value == str:
			return ""
		elif isinstance(monoid_value, list) or monoid_value == list:
			return []
		else:
			raise TypeError(str(monoid_value) + " is not a Monoid.")

def mconcat(monoid_list):
	result = mzero(monoid_list[0])
	for value in monoid_list:
		result += value
	return result
