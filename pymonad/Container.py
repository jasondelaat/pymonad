class Container(object):
	""" Represents a wrapper around an arbitrary value and a method to access it. """

	def __init__(self, value):
		""" 
		Wraps the given value in the Container. 
		
		'value' is any arbitrary value of any type including functions.

		"""
		self.value = value
	
	def getValue(self):
		""" Returns the value held by the Container. """
		return self.value
