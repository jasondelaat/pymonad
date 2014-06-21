# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

import unittest
from pymonad.Maybe import *
from pymonad.Reader import curry

@curry
def neg(x): return -x

@curry
def head(x): return x[0]

@curry
def add(x, y): return Just(x + y)

@curry
def div(y, x):
	if y == 0: return Nothing
	return Just(x/y)

@curry
def m_neg(x): return Just(-x)

class MaybeTests(unittest.TestCase):
	def testMaybeAbstract(self):
		self.assertRaises(NotImplementedError, Maybe, 7)
		self.assertRaises(NotImplementedError, Maybe, "string")
		self.assertRaises(NotImplementedError, Maybe, [])
		
	def testMaybeEquality(self):
		self.assertTrue(Nothing == Nothing)
		self.assertTrue(Just(6) == Just(6))
		self.assertTrue(Just(6) != Just(5))
		self.assertTrue(Just(6) != Nothing)
		self.assertTrue(Just(6) != Just("Six"))

		self.assertFalse(Nothing != Nothing)
		self.assertFalse(Just(6) != Just(6))
		self.assertFalse(Just(6) == Just(5))
		self.assertFalse(Just(6) == Nothing)
		self.assertFalse(Just(6) == Just("Six"))

		self.assertRaises(TypeError, Just(6).__eq__, neg)

	def testMaybeFunctor(self): 
		self.assertEqual(neg * Just(7), Just(-7))
		self.assertEqual(head * Just([0,1,2]), Just(0))
		self.assertEqual(head * Just("hello world!"), Just("h"))
		self.assertEqual(neg * Nothing, Nothing)
		self.assertEqual(head * Nothing, Nothing)

	def testMaybeApplicative(self):
		@curry
		def add(x, y): return x + y

		self.assertEqual(Just(add(7)) & Just(8), Just(15))
		self.assertEqual(add * Just(7) & Just(8), Just(15))
		self.assertEqual(Just(add(7)) & Nothing, Nothing)
		self.assertEqual(Nothing & Just(8), Nothing)

	def testMaybeMonad(self):
		self.assertEqual(Just(7) >> m_neg, Just(-7))
		self.assertEqual(Just(7) >> add(7) >> div(2), Just(7))
		self.assertEqual(Just(7) >> add(7) >> m_neg, Just(-14))
		self.assertEqual(Just(7) >> add(2) >> div(0), Nothing)
		self.assertEqual(Just(7) >> div(0) >> add(2), Nothing)
		self.assertEqual(Nothing >> add(7), Nothing)

	def testRecursionLimit(self):
		try: Just(7) >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg >> m_neg 
		except RuntimeError: self.fail()
		self.assertTrue(True)

	def testBindWithNoVariable(self):
		self.assertEqual(Just(7) >> Just(7), Just(7))
		self.assertEqual(Just(7) >> (lambda x: Just(x)), Just(7))

class TestMaybeUnit(unittest.TestCase):
	def testUnitOnMaybe(self):
		self.assertEqual(Maybe.unit(8), Just(8))
		self.assertEqual(unit(Maybe, 8), Just(8))

	def testUnitOnJust(self):
		self.assertEqual(Just.unit(8), Just(8))
		self.assertEqual(unit(Just, 8), Just(8))

	def testUnitOnNothing(self):
		self.assertEqual(Nothing.unit(8), Just(8))
		self.assertEqual(unit(Nothing, 8), Just(8))
class TestMaybeMonoid(unittest.TestCase, MonoidTester):
	def test_mzero(self):
		self.givenMonoid(Maybe)
		self.get_mzero()
		self.ensure_mzero_is(Nothing)

	def test_right_identity(self):
		self.givenMonoid(Just(9))
		self.ensure_monoid_plus_zero_equals(Just(9))

	def test_left_identity(self):
		self.givenMonoid(Just(9))
		self.ensure_zero_plus_monoid_equals(Just(9))

	def test_associativity(self):
		self.givenMonoids(Just(1), Just(2), Just(3))
		self.ensure_associativity()
	
	def test_mplus_with_two_just_values(self):
		self.givenMonoids(Just(1), Just(2))
		self.ensure_mconcat_equals(Just(3))

	def test_mplus_with_one_just_and_one_nothing(self):
		self.givenMonoids(Just(1), Nothing)
		self.ensure_mconcat_equals(Just(1))

class TestFirstMonoid(unittest.TestCase, MonoidTester):
	def test_mzero(self):
		self.givenMonoid(First)
		self.get_mzero()
		self.ensure_mzero_is(First(Nothing))

	def test_right_identity(self):
		self.givenMonoid(First(Just(9)))
		self.ensure_monoid_plus_zero_equals(First(Just(9)))

	def test_left_identity(self):
		self.givenMonoid(First(Just(9)))
		self.ensure_zero_plus_monoid_equals(First(Just(9)))

	def test_associativity(self):
		self.givenMonoids(First(Just(1)), First(Just(2)), First(Just(3)))
		self.ensure_associativity()
	
	def test_mplus_with_two_just_values(self):
		self.givenMonoids(First(Just(1)), First(Just(2)))
		self.ensure_mconcat_equals(First(Just(1)))

	def test_mplus_with_just_and_nothing(self):
		self.givenMonoids(First(Just(1)), Nothing)
		self.ensure_mconcat_equals(First(Just(1)))

	def test_mplus_with_nothing_and_just(self):
		self.givenMonoids(Nothing, First(Just(1)))
		self.ensure_mconcat_equals(First(Just(1)))

class TestLastMonoid(unittest.TestCase, MonoidTester):
	def test_mzero(self):
		self.givenMonoid(Last)
		self.get_mzero()
		self.ensure_mzero_is(Last(Nothing))

	def test_right_identity(self):
		self.givenMonoid(Last(Just(9)))
		self.ensure_monoid_plus_zero_equals(Last(Just(9)))

	def test_left_identity(self):
		self.givenMonoid(Last(Just(9)))
		self.ensure_zero_plus_monoid_equals(Last(Just(9)))

	def test_associativity(self):
		self.givenMonoids(Last(Just(1)), Last(Just(2)), Last(Just(3)))
		self.ensure_associativity()
	
	def test_mplus_with_two_just_values(self):
		self.givenMonoids(Last(Just(1)), Last(Just(2)))
		self.ensure_mconcat_equals(Last(Just(2)))

	def test_mplus_with_just_and_nothing(self):
		self.givenMonoids(Last(Just(1)), Nothing)
		self.ensure_mconcat_equals(Last(Just(1)))

	def test_mplus_with_nothing_and_just(self):
		self.givenMonoids(Nothing, Last(Just(1)))
		self.ensure_mconcat_equals(Last(Just(1)))

if __name__ == "__main__":
	unittest.main()
