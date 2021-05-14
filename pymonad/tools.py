# --------------------------------------------------------
# (c) Copyright 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" The tools module contains useful functions that don't really belong anywhere else. """

from typing import Any, Callable, List, TypeVar

import pymonad.monad as monad

R = TypeVar('R') # pylint: disable=invalid-name
S = TypeVar('S') # pylint: disable=invalid-name
T = TypeVar('T') # pylint: disable=invalid-name

def _curry_helper(
        number_of_arguments: int, function_to_curry: Callable, accumulated_arguments: List[Any]
) -> Callable:
    """ Builds a curried version of the supplied function and returns it to the caller.

    Args:
      number_of_arguments: specifies how many arguments 'function_to_curry' takes as input.
      function_to_curry: a function or other callable object either built-in or user defined.
      accumulated_arguments: a list containing all the arguments so
        far supplied to 'function_to_curry'. For instance, if
        'function_to_curry' takes two arguments but has been called with
        only one so far, then accumulated_arguments will contain a
        single item.

    Returns:
      A new function which may be partially applied simply by passing
      the desired number of arguments.
    """
    def _curry_internal(*arguments: List[Any]):
        """ Handles the actual partial application of curried functions.

        Args:
          *arguments: a variable number of arguments to be
             (eventually) supplied to the wrapped function
             'function_to_curry'

        Returns:
          Either the result of calling the wrapped function_to_curry
          with the total accumulated arguments or the result of
          calling _curry_helper with the new, larger
          accumulated_arguments list.
        """
        all_arguments = accumulated_arguments[:]
        all_arguments.extend(arguments)
        if len(all_arguments) >= number_of_arguments: # pylint: disable=no-else-return
            return function_to_curry(*all_arguments)
        else:
            return _curry_helper(number_of_arguments, function_to_curry, all_arguments)
    return _curry_internal

# Use _curry_helper to define curry as itself being a curried function.
curry = _curry_helper(2, lambda n, f: _curry_helper(n, f, []), []) # pylint: disable=invalid-name
curry.__doc__ = """ Creates a curried function from a normal function of callable object.

The curry function is itself curried and can be partially
applied. It can be used either as a normal function call or as a
decorator. The required number_of_arguments parameter makes it
possible to curry functions which take a variable number of
arguments like the built-in 'map' function.

    Usage:

    curried_map = curry(2, map)

    @curry(2)
    def some_func(x, y, z):
        return x + y - z

Args:
    number_of_arguments: The number of arguments function_to_curry
    takes as input. If function_to_curry takes a variable number of
    arguments, then number of curried arguments desired in the
    result: function_to_curry will be called once this many
    arguments have been supplied.
    function_to_curry: The function that we wish to curry

Returns:
    A new function which may be partially applied simply by passing
    the desired number of arguments.
"""

def identity(value: T) -> T:
    """ Returns it's input value unchanged. """
    return value

def kleisli_compose(
        function_f: Callable[[R], monad.Monad[S]], function_g: Callable[[S], monad.Monad[T]]
) -> Callable[[R], monad.Monad[T]]:
    """ Composes two Kleisli functions.

    Kleisli functions are functions which take as input a 'bare' value
    and return an 'embellished' value. For instance, if we have a
    function f which maps a's to b's, it's type is:
      f :: a -> b

    Then the corresponding Kleisli function, f_kleisli has the type:
      f_kleisli :: a -> (b, m)

    The type (b, m) corresponds to the internal representation of the
    Monad class, so in terms of pymonad, a Kleisli function is one
    which maps values of type a to values of some sub-class of Monad.

      Example:
        def fail_if_zero(x):
            return Nothing if x is zero else Just(x)

        def add1(x):
            return Just(x + 1)

        new_function = kleisli_compose(add1, fail_if_zero)
        new_function(0) # returns Just(1)
        new_function(-1) # returns Nothing

    add1 and fail_if_zero are Kleisli functions and new_function is
    the function which results from first performing add1 followed by
    fail_if_zero.

    Args:
      function_f: a function with type: a -> (b, m)
      function_g: a function with type: b -> (c, m)

    Returns:
      A new Kleisli function with type: a -> (c, m)
    """
    return lambda a: function_f(a).bind(function_g)

@curry(3)
def monad_from_none_or_value(
        if_none: monad.Monad[T], if_value: Callable[[T], monad.Monad[T]], value: T
) -> monad.Monad[T]:
    """Creates a monad value from the given input.

    'monad_from_none_or_value' is a curried function which attempts to
    create a monad value from the given input and returns a default
    monad value if 'value' is None.

    Example:
      option_builder = monad_from_none_or_value(Nothing, Some)
      option_builder(None) # Nothing
      option_builder(2)    # Some(2)

    Args:
      if_none: a monad value. This is the default value that will be
               returned if 'value' is None
      if_value: any function which takes a value and returns an monad
                value. Typically a constructor like Just, Right, etc.
      value: The value with which to attempt creating the monad
             instance.

    Returns:
      An instance of one of the monad classes.

    """
    if value is None: #pylint: disable=no-else-return
        return if_none
    else:
        return if_value(value)
