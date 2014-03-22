=======
PyMonad
=======

PyMonad is a small library 
implementing monads and related data abstractions
-- functors, applicative functors --
for use in implementing functional style programs.
For those familiar with monads in Haskell,
PyMonad aims to implement many of the features you're used to
so you can use monads in python quickly and easily.
For those who have never used monads but are interested,
PyMonad is an easy way to learn about them in, perhaps, 
a slightly more forgiving environment
without needing to learn Haskell.

Features
========

* Easily define curried functions with the ``@curry`` decorator.
* Straight-forward partial application: just pass a curried function the number of arguments you want.
* Composition of curried functions using ``*``.
* Functor, Applicative Functor, and Monad operators: ``*``, ``&``, and ``>>``
* Four basic monad types (with more come)
	1. Maybe - for when a calculation might fail
	2. Either - similar to Maybe but with additional error reporting
	3. List - For non-deterministic calculations
	4. Reader - For sequencing calculations which all access the same data.

Getting Started
===============

More detailed documentation is in the works
and will be updated periodically,
time permitting.
For now this guide should get you started.
Comments and suggestions welcome at
jason.develops@gmail.com

Installation
------------

Using pip::

	pip install PyMonad

Or download the package and run::

	python setup.py install

from the project directory.
You may have to use ``python3`` rather than ``python``
if you have more than one verion of Python installed.
	
Imports
-------

Import the entire package::
	
	from pymonad import *

Or just a single monad type::

	from pymonad.Maybe import *

If you're not importing everything
but want to use curried functions::

	from pymonad.Reader import curry

Curried Functions and Partial Application
-----------------------------------------

To define a curried function
use the ``@curry`` decorator::

	@curry
	def add(x, y):
		return x + y

	@curry
	def func(x, y, z):
		# Do something with x, y and z.
		...

The above fuctions can be partially applied 
by passing them less than their full set of arguments::

	add(7, 8)			# Calling 'add' normally returns 15 as expected.
	add7 = add(7)		# Partial application: 'add7' is a function taking one argument.
	add7(8)				# Applying the final argument retruns 15...
	add7(400)			# ... or 407, or whatever.

	# 'func' can be applied in any of the following ways.
	func(1, 2, 3)		# Call func normally.
	func(1, 2)(3)		# Partially applying two, then applying the last argument.
	func(1)(2, 3)		# Partially applying one, then applying the last two arguments.
	func(1)(2)(3)		# Partially applying one, partially applying again, then applying the last argument.

Function Composition
--------------------

Curried functions can be composed with the ``*`` operator.
Functions are applied from right to left::
	
	# Returns the first element of a list.
	@curry
	def head(aList): 
		return aList[0]

	# Returns everything except the first element of the list.
	@curry 
	def tail(aList): 
		return aList[1:]

	second = head * tail		# 'tail' will be applied first, then its result passed to 'head'
	second([1, 2, 3, 4])		# returns 2

You can also compose partially applied functions::

	@curry
	def add(x, y): 
		return x + y

	@curry
	def mul(x, y): 
		return x * y

	comp = add(7) * mul(2)		# 'mul(2)' is evaluated first, and it's result passed to 'add(7)'
	comp(4)						# returns 15

	# Composition order matters!
	comp = mul(2) * add(7)
	comp(4)						# returns 22

Functors, Applicative Functors, and Monads
------------------------------------------

All Monads are also Applicative Functors,
and all Applicative Functors are also Functors,
though the same is not necessarily true in reverse.
All the types included with PyMonad
are defined as all three
but you can define new types however you want.

Functors
--------

All functors define the ``fmap`` method
which can be invoked via the fmap operator ``*``.
``fmap`` takes functions which operate on simple types
-- integers, strings, etc. --
and allows them to operate of functor types::
	
	from pymonad.Maybe import *
	from pymonad.List import *

	# 'neg' knows nothing about functor types...
	def neg(x):
		return -x

	# ... but that doesn't stop us from using it anyway.
	neg * Just(9)				# returns Just(-9)
	neg * Nothing				# returns Nothing
	neg * List(1, 2, 3, 4)		# returns List(-1, -2, -3, -4)

Notice that the function is on the left
and the functor type is on the right.
If you think of ``*`` as a sort of fancy opening paren,
then normal calls and ``fmap`` calls have basically the same structure::

	------------------------------------------------------------------
					function		open		argument		close
	Normal call		  neg			 (			   9			  )
	fmap call	 	  neg			 *			 Just(9)
	------------------------------------------------------------------


Notice that ``*`` is also the function composition operator.
In fact,
curried functions are instances of the ``Reader`` monad,
and ``fmap``ing a function over another function
is the same thing as function composition.

Applicative Functors
--------------------

Functors allow you to use normal functions of a single argument
-- like ``neg`` above --
with functor types.
Applicative Functors extend that capability
-- via ``amap`` and its operator ``&`` --
allowing you to use normal functions of multiple arguments
with functor types::

	# 'add' operates on simple types, not functors or applicatives...
	def add(x, y):
		return x + y

	# ... but we're going to use it on those types anyway.
	# Note that we're still using '*' but now in conjunction with '&'
	add * Just(7) & Just(8)					# returns Just(15)
	add * Nothing & Just(8)					# returns Nothing
	add * Just(7) & Nothing					# returns Nothing
	add * List(1, 2, 3) & List(4, 5, 6)		# returns List(5, 6, 7, 6, 7, 8, 7, 8, 9)

If ``*`` is a fancy paren,
``&`` is the fancy comma
used to separate arguments.

Monads
------

Monads allow you to sequence a series of calculations
within than monad
using the ``bind`` operator ``>>``.

The first argument to ``>>`` is a monad type.
The second argument is a function
which takes a single,
non-monad argument
and returns an instance of the same monad::

	from pymonad.List import *
	from pymonad.Reader import curry

	# Takes a simple number type and returns a 'List' containing that value and it's negative.
	def positive_and_negative(x):
		return List(x, -x)

	# You can call 'positive_and_negative' normally.
	positive_and_negative(9)		# returns List(9, -9)

	# Or you can create a List...
	x = List(9)

	# ... and then use '>>' to apply positive_and_negative'
	x >> positive_and_negative		# also returns List(9, -9)

	# But 'x' could also have more than one value...
	x = List(1, 2)
	x >> positive_and_negative		# returns List(1, -1, 2, -2)

	# And of course you can sequence partially applied functions.
	@curry
	def add_and_sub(x, y):
		return List(y + x, y - x)

	List(2) >> positive_and_negative >> add_and_sub(3)		# creates List(2)
															# applies positive_and_negative: List(2, -2)
															# then add_and_sub(3): List(5, -1, 1, -5)
															# final result: List(5, -1, 1, -5)

Variable assignment in monadic code
-----------------------------------

The second argument to ``>>`` is a function 
which takes a single, non-monad argument.
Because of that, 
you can use ``lambda`` to assign values to a variable
withing monadic code,
like this::
	
	from pymonad.Maybe import *

	Just(9) >> (lambda x: 				# Here, 'x' takes the value '9'
	Just(8) >> (lambda y:				# And 'y' takes the value '8'
	Just(x + y)))						# The final returned value is 'Just(9 + 8)', or 'Just(17)'

You can also simply ignore values if you wish::

	Just(9) >> Just(8)					# The '9' is thrown away and the result of this computation is 'Just(8)'

Implementing Monads
-------------------

Implementing other functors, applicatives, or monads is fairly straight-forward.
There are three classes, 
serving as interfaces::

	Monad --> Applicative --> Functor

To implement a new functor,
create a new class which derives from ``Functor``
and override the ``fmap`` method.

To implement a new applicative functor,
create a new class which derives from ``Applicative``
and override the ``amap`` and ``fmap`` methods.

To implement a new monad,
create a new class which derives from ``Monad``
and override at least the ``bind`` method, 
and preferably the ``amap`` and ``fmap`` methods as well.

The operators, ``*``, ``&``, and ``>>``
are pre-defined to call the above methods
so you shouldn't need to touch them directly.

Isn't there something missing?
------------------------------

If you're familiar with monads from Haskell,
you'll notice that the ``unit`` function
-- called ``return`` in Haskell --
isn't included.
In Haskell,
``return`` is polymorphic on the return type
but we can't implement polymorphism on return types in Python,
so there's no general way to write a ``unit`` function
as far as I know.
You can get around this in a few of ways:

1. Write a separate function which implements the ``unit`` functionality, or
2. Implement ``unit`` functionality directly in the class' ``__init__`` method, or
3. Define a static method on the class which implements ``unit`` functionality.
