# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

from pymonad.Monad import *
from pymonad.Monoid import *

class Writer(Monad): 
	"""
	Represents a context which stores the result of a calculation as well as a log
	of its activity. The log can be any monoid type, strings being a typical example.

	"""

	def __init__(self, value, logMessage=None):
		"""
		Constructs the Writer object. There are two ways to initialize a Writer object:
		Pass the value/logMessage pair as a two element tuple (or list), or
		pass the value and logMessage as two separate arguments. 

		"""
		if not logMessage:
			super(Writer, self).__init__(tuple(value))
		else:
			super(Writer, self).__init__((value, logMessage))

	def __str__(self):
		return str(self.value)

	def fmap(self, function):
		"""
		Applies a single argument normal function to a Writer value. A function applied in this
		way will preserve any existing log messages withing the Writer,
		but no additional log messages will be added.

		"""
		value, log = self.value
		newValue = function(value)
		return Writer((newValue, log))

	def amap(self, functorValue):
		"""
		Allows normal multi-argument functions to be called with Writer values as the arguments.
		As with 'fmap' a function applied with 'amap' will preserve any existing log messages 
		withing the Writer, but no additional log messages will be added.

		"""
		functorContent, log = functorValue.value
		newValue = self.value[0](functorContent)
		return Writer((newValue, log))

	def bind(self, function):
		"""
		Chains together functions which produce Writer instances.
		Any log messages produced by 'function' are appended to the existing
		log messages of the arguments.

		"""
		startValue, startLog = self.value
		newValue, newLog = function(startValue).value
		return Writer((newValue, startLog + newLog))

	@classmethod
	def unit(cls, value):
		"""
		Returns a Writer instance with 'value' paired with a log message equal
		to the 'mzero' (see Monoid.py for more information) of the log type.
		'unit' should not be called with the Writer class directly as it has no
		default log type. Instead use 'unit' with a subclass of Writer. For instance,
			StringWriter.unit(8)

		"""
		return Writer((value, mzero(cls.logType)))

	def getResult(self):
		"""
		Returns the result portion of the Writer instance. For example, given
			x = Writer(8, "initial value")
			
		x.getResult() will return 8.
		To get both the result and the log message use 'getValue()'.

		"""
		return self.value[0]

	def getLog(self):
		"""
		Returns the log message portion of the Writer instance. For example, given
			x = Writer(8, "initial value")

		x.getLog() will return "initial value".
		To get both the result and the log message use 'getValue()'.

		"""
		return self.value[1]

	def __eq__(self, other):
		if not isinstance(other, Writer): 
			raise TypeError("Can't compare two different types.")
		else:
			return super(Writer, self).__eq__(other)

class NumberWriter(Writer):
	""" A Writer monad type which uses numbers, either integers or floats, as the log type. """
	logType = int

class StringWriter(Writer):
	""" A Writer monad type which uses strings as the log type. """
	logType = str

class ListWriter(Writer):
	""" A Writer monad type which uses lists as the log type. """
	logType = list
