# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

from pymonad.Monad import *
from pymonad.Monoid import *

class Writer(Monad): 
	def __init__(self, value, logMessage=None):
		if not logMessage:
			super(Writer, self).__init__(value)
		else:
			super(Writer, self).__init__((value, logMessage))

	def __str__(self):
		return str(self.value)

	def fmap(self, function):
		value, log = self.value
		newValue = function(value)
		return Writer((newValue, log))

	def amap(self, functorValue):
		functorContent, log = functorValue.value
		newValue = self.value[0](functorContent)
		return Writer((newValue, log))

	def bind(self, function):
		startValue, startLog = self.value
		newValue, newLog = function(startValue).value
		return Writer((newValue, startLog + newLog))

	@classmethod
	def unit(cls, value):
		return Writer((value, mzero(cls.logType)))

	def getValue(self):
		return self.value[0]

	def getLog(self):
		return self.value[1]

class NumberWriter(Writer):
	logType = int

class StringWriter(Writer):
	logType = str

class ListWriter(Writer):
	logType = list
