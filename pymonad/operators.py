# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Provides monad classes with operators.

The operators module overrides all base monad types and their aliases
with versions which support operators.

The defined operators are:
  &  - amap
  >> - bind
  *  - map

  Example:
    from pymonad.operators import Maybe, Just, Nothing
    from pymonad.tools import curry

    @curry(2)
    def add(x, y): return x + y

    @curry(2)
    def div(y, x):
        if y == 0:
            return Nothing
        else:
            return Just(x / y)

    # Equivalent to Maybe.apply(add).to_arguments(Just(1), Just(2))
    print(add * Just(1) & Just(2)) # Just 3

    # Equivalent to Maybe.insert(5).bind(div(2)).bind(div(0))
    print(Just(5) >> div(2) >> div(0)) # Nothing
"""
import pymonad.monad
import pymonad.maybe
import pymonad.either
import pymonad.reader
import pymonad.writer
import pymonad.state
import pymonad.list

class MonadOperators(pymonad.monad.MonadAlias):
    """ Defines the monad operators.

    The MonadOperators class allows users to create a monad alias for
    any monad class with the operators __and__, __rmul__, and
    __rshift__ defined.

      Example:
        class MaybeOp(MonadOperators, Maybe):
            pass

    Nothing extra needs to be implemented to get the correct behaviour
    unless the monad has multiple 'constructors' such as Just and
    Nothing. In this case, we need to override those constructors as well:

      Example:
        def Just(value):
            return MaybeOp(value, True)
        Nothing = MaybeOp(None, False)
    """
    def __and__(self, monad_value):
        return self.amap(monad_value)

    def __rmul__(self, function):
        return self.map(function)

    def __rshift__(self, kleisli_function):
        return self.bind(kleisli_function)

class Maybe(MonadOperators, pymonad.maybe.Maybe):
    """ The Maybe Monad with operators.

    See the MonadOperators class and pymonad.maybe.
    """

def Just(value): # pylint: disable=invalid-name
    """ A Maybe object representing the presence of an optional value. """
    return Maybe(value, True)

# A Maybe object representing the absence of an optional value.
Nothing = Maybe(None, False) # pylint: disable=invalid-name






class Either(MonadOperators, pymonad.either.Either):
    """ The Either Monad with operators.

    See the MonadOperators class and pymonad.either.
    """

def Right(value): # pylint: disable=invalid-name
    """ Creates a value of the second possible type in the Either monad. """
    return Either(value, (None, True))

def Left(value): # pylint: disable=invalid-name
    """ Creates a value of the first possible type in the Either monad. """
    return Either(None, (value, False))






class _Reader(MonadOperators, pymonad.reader._Reader): # pylint: disable=protected-access
    """ The Reader Monad with operators.

    See the MonadOperators class and pymonad.reader.
    """

def Reader(function): # pylint: disable=invalid-name
    """ Creates an instance of the Reader monad.

    Args:
      function: a function which takes the read-only data as input and
        returns any appropriate type.

    Result:
      An instance of the Reader monad.
    """
    return _Reader(function, None)

Reader.insert = _Reader.insert
Reader.apply = _Reader.apply






class Writer(MonadOperators, pymonad.writer.Writer):
    """ The Writer Monad with operators.

    See the MonadOperators class and pymonad.writer.
    """






class _State(MonadOperators, pymonad.state._State): # pylint: disable=protected-access
    """ The State Monad with operators.

    See the MonadOperators class and pymonad.state.
    """

def State(state_function): # pylint: disable=invalid-name
    """ The State monad constructor function.

    Args:
      state_function: a function with type State -> (Any, State)

    Returns:
      An instance of the State monad.
    """
    return _State(lambda s: state_function(s)[0], lambda s: state_function(s)[1])

State.insert = _State.insert
State.apply = _State.apply






class _List(MonadOperators, pymonad.list._List): # pylint: disable=protected-access
    """ The List Monad with operators.

    See the MonadOperators class and pymonad.list.
    """

def ListMonad(*elements): # pylint: disable=invalid-name, duplicate-code
    """ Creates an instance of the List monad.

    Args:
      *elements: any number of elements to be inserted into the list

    Returns:
      An instance of the List monad.
    """
    def _list_internal():
        yield from elements[1:]

    return _List(elements[0], _list_internal())

ListMonad.insert = _List.insert
ListMonad.apply = _List.apply
