# --------------------------------------------------------
# (c) Copyright 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" The tools module contains useful functions that don't really belong anywhere else. """

from typing import Callable, List, Any

def _curry_helper(number_of_arguments: int,
                  function_to_curry: Callable,
                  accumulated_arguments: List[Any]) -> Callable:
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
